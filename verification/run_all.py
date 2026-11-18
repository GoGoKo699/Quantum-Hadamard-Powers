"""Finite checks of the coherent extraction and filtered source-query algorithm."""

from collections import Counter
from itertools import combinations, product
from math import comb, prod, sqrt

import numpy as np


ATOL = 2e-11
RNG = np.random.default_rng(181126)


def make_state(size):
    vector = RNG.normal(size=size) + 1j * RNG.normal(size=size)
    return vector / np.linalg.norm(vector)


def rank_size(power):
    return 1 << (comb(2 * power - 1, power) - 1).bit_length()


def residual(tuple_labels, selected):
    slots = set(selected)
    return tuple(value for i, value in enumerate(tuple_labels) if i not in slots)


def has_no_collision(labels, power):
    return max(Counter(labels).values(), default=0) < power


def valid_subsets(labels, power):
    for selected in combinations(range(len(labels)), power):
        if len({labels[i] for i in selected}) == 1 and has_no_collision(
            residual(labels, selected), power
        ):
            yield selected


def restore_tuple(batch_size, selected, unused, value):
    selected_set = set(selected)
    remaining = iter(unused)
    return tuple(value if i in selected_set else next(remaining) for i in range(batch_size))


def check_extraction(alpha, power, batch_size):
    labels = range(len(alpha))
    rank_count = rank_size(power)
    routed = {}
    for sample in product(labels, repeat=batch_size):
        matches = tuple(valid_subsets(sample, power))
        assert len(matches) <= rank_count
        for rank, selected in enumerate(matches):
            unused = residual(sample, selected)
            value = sample[selected[0]]
            key = (selected, unused, value)
            assert key not in routed, "Routing erased information"
            recovered = restore_tuple(batch_size, *key)
            assert recovered == sample
            assert tuple(valid_subsets(recovered, power)).index(selected) == rank
            routed[key] = prod(alpha[z] for z in sample) / sqrt(rank_count)

    residual_weights = {
        unused: prod(alpha[z] for z in unused)
        for unused in product(labels, repeat=batch_size - power)
        if has_no_collision(unused, power)
    }
    ideal = {
        (selected, unused, value): weight * alpha[value] ** power / sqrt(rank_count)
        for selected in combinations(range(batch_size), power)
        for unused, weight in residual_weights.items()
        for value in labels
    }
    assert routed.keys() == ideal.keys(), "Marked basis did not factor"
    np.testing.assert_allclose(list(routed.values()), [ideal[k] for k in routed], atol=ATOL)
    moment = np.sum(np.abs(alpha) ** (2 * power))
    no_collision = sum(abs(weight) ** 2 for weight in residual_weights.values())
    mass = sum(abs(value) ** 2 for value in routed.values())
    np.testing.assert_allclose(
        mass, comb(batch_size, power) * moment * no_collision / rank_count, atol=ATOL
    )


def kron(factors):
    tensor = np.ones(1, dtype=complex)
    for factor in factors:
        tensor = np.kron(tensor, factor)
    return tensor


def mark_basis(alphabet, power, batch_size):
    """Mark the valid ranks using the tuple-major tensor-product basis."""
    rank_count = rank_size(power)
    return np.array(
        [
            rank < len(subsets)
            for sample in product(range(alphabet), repeat=batch_size)
            for subsets in [tuple(valid_subsets(sample, power))]
            for rank in range(rank_count)
        ]
    )


def householder_to_uniform(size):
    first = np.eye(size)[0]
    uniform = np.ones(size) / sqrt(size)
    difference = first - uniform
    return np.eye(size) - 2 * np.outer(difference, difference) / (difference @ difference)


class TiltedDilation:
    """Simulate the flag, index coin, and test qubit without a dense walk matrix."""

    def __init__(self, projectors, tilt):
        self.projectors = projectors
        self.complements = [np.eye(len(tilt)) - projector for projector in projectors]
        self.tilt = tilt
        self.sine = np.sqrt(1 - tilt**2)
        self.coin = householder_to_uniform(len(projectors))
        self.shape = (2, len(projectors), 2, len(tilt))

    def embed(self, vector):
        signal = np.zeros(self.shape, dtype=complex)
        signal[0, 0, 0] = vector
        return signal

    def rotate_flag(self, state, direction):
        zero, one = state
        return np.stack(
            (self.tilt * zero - direction * self.sine * one,
             direction * self.sine * zero + self.tilt * one)
        )

    def apply(self, state):
        state = self.rotate_flag(state, +1)
        state = np.einsum("jk,fksx->fjsx", self.coin, state)
        for index, (projector, complement) in enumerate(
            zip(self.projectors, self.complements)
        ):
            zero, one = state[0, index]
            state[0, index] = (
                projector @ zero + complement @ one,
                complement @ zero + projector @ one,
            )
        state = np.einsum("jk,fksx->fjsx", self.coin, state)
        return self.rotate_flag(state, -1)

    def step(self, state):
        walked = -self.apply(state)
        walked[0, 0, 0] *= -1
        return walked

    def filter(self, vector, clock_size):
        state = self.embed(vector)
        total = state[0, 0, 0].copy()
        for _ in range(1, clock_size):
            state = self.step(state)
            total += state[0, 0, 0]
        return total / clock_size


def check_spectral(alpha, power, batch_size):
    rank_count = rank_size(power)
    rank_state = np.ones(rank_count) / sqrt(rank_count)
    vectors = [alpha] * batch_size + [rank_state]
    phi = kron(vectors)
    projectors = [
        kron([
            np.outer(vec, vec.conj()) if i == selected else np.eye(len(vec))
            for i, vec in enumerate(vectors)
        ])
        for selected in range(len(vectors))
    ]
    hamiltonian = np.eye(len(phi)) - sum(projectors) / len(projectors)
    mark = mark_basis(len(alpha), power, batch_size)
    c = 1 / batch_size
    tilt = np.where(mark, sqrt(c), 1.0)
    operator = np.eye(len(phi)) - tilt[:, None] * hamiltonian * tilt[None, :]
    eigenvalues, eigenvectors = np.linalg.eigh(operator)
    assert eigenvalues[0] >= -ATOL
    assert abs(eigenvalues[-1] - 1) < ATOL
    assert eigenvalues[-2] <= 1 - c / (batch_size + 1) + ATOL
    ground = phi / tilt
    ground /= np.linalg.norm(ground)
    np.testing.assert_allclose(operator @ ground, ground, atol=ATOL)

    dilation = TiltedDilation(projectors, tilt)
    signal = dilation.embed(phi)
    rng_bulk = make_state(signal.size).reshape(signal.shape)
    np.testing.assert_allclose(dilation.apply(dilation.apply(rng_bulk)), rng_bulk, atol=ATOL)
    np.testing.assert_allclose(dilation.apply(signal)[0, 0, 0], operator @ phi, atol=ATOL)

    clock_size = int(np.ceil(2 * sqrt(2 * (batch_size + 1) / c)))
    angles = np.arccos(eigenvalues.clip(-1, 1))
    factors = np.mean(np.cos(np.arange(clock_size)[:, None] * angles), axis=0)
    assert np.max(np.abs(factors[:-1])) <= 0.5 + ATOL
    state = phi
    rounds = 3
    for _ in range(rounds):
        state = dilation.filter(state, clock_size)
    expected = eigenvectors @ (factors**rounds * (eigenvectors.conj().T @ phi))
    np.testing.assert_allclose(state, expected, atol=ATOL)

    mu = float(np.linalg.norm(phi[mark]) ** 2)
    ideal_projected = np.vdot(ground, phi) * ground
    if mu < ATOL:
        assert np.linalg.norm(state[mark]) < sqrt(ATOL)
        return
    excited = np.linalg.norm(phi - ideal_projected)
    signal_norm = np.linalg.norm(ideal_projected[mark])
    assert excited / signal_norm <= sqrt(1 + mu / c) + ATOL
    actual_marked_error = np.linalg.norm((state - ideal_projected)[mark])
    assert actual_marked_error <= excited * 0.5**rounds + ATOL


def check_evaluator(function, expected_tag_probability):
    size = len(function)
    distribution = Counter(
        (tag, index if tag == 0 else function[index])
        for tag, index in product(range(2), range(size))
    )
    mass = sum(count**2 for count in distribution.values())
    tag_mass = sum(count**2 for (tag, _), count in distribution.items() if tag == 0)
    np.testing.assert_allclose(tag_mass / mass, expected_tag_probability, atol=ATOL)
    alpha = np.array([sqrt(count / (2 * size)) for count in distribution.values()])
    check_extraction(alpha, power=2, batch_size=3)


def main():
    extraction_tests = 0
    for size, power in product((2, 3, 4), (2, 3)):
        for batch_size in range(power, min(power + 4, 7)):
            for _ in range(3):
                check_extraction(make_state(size), power, batch_size)
                extraction_tests += 1
    check_extraction(np.array([0, 1j, 0]), power=2, batch_size=4)
    extraction_tests += 1

    spectral_tests = 0
    for power, batch_sizes in ((2, (2, 3, 4)), (3, (3, 4))):
        for batch_size in batch_sizes:
            check_spectral(make_state(2), power, batch_size)
            spectral_tests += 1
    check_spectral(np.array([0.0, 1j]), power=2, batch_size=4)
    check_spectral(np.array([sqrt(1 - 1e-7), 1j * sqrt(1e-7)]), power=2, batch_size=4)
    spectral_tests += 2

    check_evaluator((2, 3, 1, 0), 1 / 2)
    check_evaluator((0, 0, 2, 2), 1 / 3)
    print(f"Passed {extraction_tests} extraction, {spectral_tests} spectral, and 2 evaluator checks.")


if __name__ == "__main__":
    main()
