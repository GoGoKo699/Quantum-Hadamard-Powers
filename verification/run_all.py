"""Finite checks of extraction, spectral filtering and source access comparisons."""

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


def two_heavy_probabilities(scale, tail_size):
    heavy = (1 + sqrt(tail_size * (tail_size + 2 - scale) / (2 * scale))) / (
        tail_size + 2
    )
    tail = (1 - 2 * heavy) / tail_size
    np.testing.assert_allclose(2 * heavy + tail_size * tail, 1, rtol=ATOL)
    np.testing.assert_allclose(2 * heavy**2 + tail_size * tail**2, 1 / scale, rtol=ATOL)
    return heavy, tail


def check_matched_profiles(scale, copy_budget):
    dimension = scale**2
    diffuse_tail_size = dimension - 2
    broad_tail_size = 2 * scale
    heavy, diffuse = two_heavy_probabilities(scale, diffuse_tail_size)
    _, broad = two_heavy_probabilities(scale, broad_tail_size)
    assert scale * diffuse_tail_size * diffuse**2 < 1 / 8
    assert scale * broad_tail_size * broad**2 > 1 / 4

    cap = 1 / (2 * scale)
    capped_count = copy_budget - 3
    middle = (heavy + (copy_budget - 2) * diffuse - capped_count * cap) / 2
    assert heavy > middle > cap > diffuse > 0
    remaining_mass = 1 - heavy - 2 * middle - capped_count * cap
    remaining_square = 1 / scale - heavy**2 - 2 * middle**2 - capped_count * cap**2
    tail_size = 8 * scale
    assert copy_budget + tail_size <= dimension

    uniform = np.full(tail_size, remaining_mass / tail_size)
    packed = np.zeros(tail_size)
    packed_count = int(remaining_mass / cap)
    packed[:packed_count] = cap
    packed[packed_count] = remaining_mass - packed_count * cap
    uniform_square = uniform @ uniform
    packed_square = packed @ packed
    assert uniform_square < remaining_square < packed_square
    # The displacement from uniform sums to zero, so the squared mass varies
    # quadratically along the segment from the uniform tail to the packed tail.
    fraction = sqrt((remaining_square - uniform_square) / (packed_square - uniform_square))
    tail = uniform + fraction * (packed - uniform)
    assert np.all((0 <= tail) & (tail <= cap))
    slow = np.concatenate(([heavy, middle, middle], np.full(capped_count, cap), tail))
    np.testing.assert_allclose(slow.sum(), 1, rtol=ATOL)
    np.testing.assert_allclose(slow @ slow, 1 / scale, rtol=ATOL)
    np.testing.assert_allclose(slow.max(), heavy, rtol=ATOL)
    largest = np.partition(slow, -copy_budget)[-copy_budget:]
    np.testing.assert_allclose(largest.sum(), 2 * heavy + (copy_budget - 2) * diffuse, rtol=ATOL)
    assert scale * (slow[3:] @ slow[3:]) > 1 / 8


def check_forward_hard_pair(dimension, power):
    bulk = dimension - 2
    odds = bulk ** (-(power - 1) / power)
    spike_probability = odds / (1 + odds)
    phase = np.pi / (2 * power)
    sources = np.full((2, dimension), sqrt((1 - spike_probability) / bulk), dtype=complex)
    sources[:, 0] = 0
    sources[:, 1] = sqrt(spike_probability) * np.exp(1j * np.array([phase, -phase]))
    np.testing.assert_allclose(np.abs(sources[0]), np.abs(sources[1]), atol=ATOL)
    powered = sources**power
    moment = np.linalg.norm(powered, axis=1, keepdims=True) ** 2
    np.testing.assert_allclose(moment, 2 * spike_probability**power, rtol=ATOL)
    targets = powered / np.sqrt(moment)
    np.testing.assert_allclose(targets @ targets.conj().T, np.eye(2), atol=ATOL)
    overlap = abs(np.vdot(*sources)) ** 2
    expected = 1 - 4 * spike_probability * (1 - spike_probability) * np.sin(phase) ** 2
    np.testing.assert_allclose(overlap, expected, atol=ATOL)


def check_purified_schur(alphabet, environment_size, power, batch_size):
    source = make_state(alphabet * environment_size).reshape(alphabet, environment_size)
    density = source @ source.conj().T
    rank_count = rank_size(power)
    routed = {}
    for sample in product(range(alphabet), repeat=batch_size):
        for selected in valid_subsets(sample, power):
            unused = residual(sample, selected)
            value = sample[selected[0]]
            key = (selected, unused)
            if key not in routed:
                routed[key] = np.zeros((alphabet, environment_size**batch_size), dtype=complex)
            slot_order = (value,) * power + unused
            routed[key][value] = kron([source[label] for label in slot_order]) / sqrt(rank_count)

    reduced = sum(block @ block.conj().T for block in routed.values())
    moment = np.trace(density**power).real
    success = np.trace(reduced).real
    diagonal = density.diagonal().real
    no_collision = sum(
        prod(diagonal[label] for label in unused)
        for unused in product(range(alphabet), repeat=batch_size - power)
        if has_no_collision(unused, power)
    )
    np.testing.assert_allclose(
        success, comb(batch_size, power) * moment * no_collision / rank_count, atol=ATOL
    )
    np.testing.assert_allclose(reduced / success, density**power / moment, atol=ATOL)


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
    profile_cases = ((256, 6), (1024, 10), (4096, 16))
    for scale, copy_budget in profile_cases:
        check_matched_profiles(scale, copy_budget)
    forward_cases = ((7, 2), (31, 3), (257, 5))
    for dimension, power in forward_cases:
        check_forward_hard_pair(dimension, power)
    purification_cases = ((3, 3, 2, 4), (3, 2, 3, 4))
    for case in purification_cases:
        check_purified_schur(*case)
    print(
        f"Passed {extraction_tests} extraction, {spectral_tests} spectral, "
        f"2 evaluator, {len(profile_cases)} profile, {len(forward_cases)} forward-pair, "
        f"and {len(purification_cases)} purification checks."
    )


if __name__ == "__main__":
    main()
