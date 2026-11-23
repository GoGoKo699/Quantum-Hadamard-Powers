# Learning Hadamard powers with de Wolf’s lecture notes

The project uses collisions to prepare a quantum state with powered amplitudes. A label measurement gives the new probabilities. The state itself also carries the new relative phases. This bridge identifies the tools needed to extract that state and price the source access.

The shared educational anchor is **Ronald de Wolf, _Quantum Computing: Lecture Notes_**, [arXiv:1907.09415v6](https://arxiv.org/abs/1907.09415v6), revised August 27, 2026. The section numbers follow that version.

## Targeted reading

| Read in de Wolf | Use in the project | Milestones |
|---|---|---|
| §§1.2.1–1.2.3, states, measurement and unitary evolution | Track basis amplitudes and project onto an agreement flag while leaving the selected label coherent. | [M01](MILESTONES.md#m01-computational-basis-amplitudes), [M04](MILESTONES.md#m04-a-flag-without-reading-the-label) |
| §4.6, phase estimation | A clock converts an eigenphase into an observable signal. The filter accepts zero phase exactly and attenuates phases separated from zero. | [M08](MILESTONES.md#m08-eigenvalues-become-eigenphases), [M09](MILESTONES.md#m09-a-finite-zero-phase-test), [M21](MILESTONES.md#m21-filtering-the-tilted-ground-state) |
| §7.3, amplitude amplification | Track the marked and unmarked components of a state. This gives the two-label filter for an input whose powered state is concentrated on its head. | [M12](MILESTONES.md#m12-the-operational-question), [M30](MILESTONES.md#m30-the-complete-algorithm-and-its-scope) |
| §§8.2–8.3 and 9.3–9.4, walks, selected unitaries and block encodings | Separate the cost of setup, one query step and checking. Select across local projectors coherently and identify the operator seen when the signal ancillas are zero. | [M10](MILESTONES.md#m10-setup-update-and-checking), [M20](MILESTONES.md#m20-one-selected-test-per-query-step), [M28](MILESTONES.md#m28-pricing-the-circuit) |
| §11.1, quantum query lower bounds | Identify the input oracle and the operations permitted between calls. The forward-only proof uses a separate state-discrimination simulation. | [M11](MILESTONES.md#m11-fair-query-comparisons), [M26](MILESTONES.md#m26-the-haar-square-lower-bound) |
| §§15.1 and 18.3, mixed states, measurements and reductions | Retain the selected auxiliary states through extraction, then compute the reduced mixed output on the label. | [M29](MILESTONES.md#m29-garbage-and-the-measured-law) |

The [spectral proof](../science/spectral.md) gives the specific tilt, the gap bound and the conditioned error. The [extraction proof](../science/extraction.md) identifies the directions the filter acts on.

## Translate the notation

| Tool | This project | Role |
|---|---|---|
| Prepared input state | Product of the source slots and a uniform rank register | Holds the unknown label amplitudes and phases. |
| Projective test | Collision mark $`G`$ on tuple–rank pairs | Selects a subspace in which a coherent powered label can be isolated. |
| Good-component probability | $`\mu=\lVert G\lvert\Phi\rangle\rVert^2`$ | Initial norm squared of the marked part before spectral filtering. |
| Clean-ancilla block | $`A=I-THT`$ | The spectrum of this block determines the eigenphases of its qubiterate. |
| Zero-phase clock outcome | Clean signal and zero-phase flags | Suppresses spectral components orthogonal to the tilted vector. |
| Reduced density operator | Label state after tracing the selected auxiliary registers | Keeps the normalized entrywise power of the source’s mixed label state. |

The input moment is $`S_r=\sum_y\lvert\alpha_y\rvert^{2r}`$. The mark weight $`\mu`$ additionally depends on the batch length and the rank condition. The output-error tolerance is $`\varepsilon`$.

## Follow a three-copy example

Take two labels and prepare

```math
\lvert\psi\rangle=\frac{\sqrt 3}{2}\lvert 0\rangle+\frac{i}{2}\lvert 1\rangle .
```

The computational-basis probabilities are $`(3/4,1/4)`$, and the probability of a collision between two independent samples is $`S_2=5/8`$. The normalized Hadamard square is

```math
\lvert\psi^{[2]}\rangle=\frac{3\lvert 0\rangle-\lvert 1\rangle}{\sqrt{10}} .
```

The minus sign comes from $`i^2=-1`$. Measuring the target in the computational basis gives $`(9/10,1/10)`$, which cannot reveal that relative sign.

Use $`t=3`$ source copies and a rank register with four equiprobable values. In the tuple $`001`$, one position pair is valid. In $`000`$, three pairs are valid. The rule accepts one rank for the first tuple and three for the second. In both tuples, every valid rank identifies a distinct pair with equal labels.

After a successful rank, route the selected pair to the first two registers, clear the duplicate label and retain the position pair and the unselected label. In the reindexed state, each position pair and each residual label has a contribution from both candidate output labels. Their respective factors are $`(\sqrt 3/2)^2=3/4`$ and $`(i/2)^2=-1/4`$. The residual amplitude multiplies each by the same factor. Therefore the residual system and the pair index factor from the output, so discarding them leaves the pure state above.

The initial weight of the marked component is $`\binom{3}{2}S_2/4=15/32`$. The residual has just one register, so it satisfies the requirement that it have no equal pair. With longer tuples that residual condition affects the success probability. Its dependence on the residual alone is what preserves the output factorization.

## Connect the phase filter to the output

The unfiltered starting vector is a product state. For each coordinate, the rank-one projector onto its starting state is a test that the coordinate agrees with its preparation. These tests commute. Their average has a unique eigenvector with eigenvalue one, the product state, with gap proportional to $`1/t`$. Indexing a single test in superposition uses one controlled state reflection or a forward/inverse source pair. Known routing still acts on the whole batch.

The project sets $`H`$ to identity minus that average and lets $`T=I-G+\sqrt c\,G`$. The operator $`THT`$ has bottom eigenvector proportional to $`T^{-1}\lvert\Phi\rangle`$. In that vector the marked component is multiplied by $`1/\sqrt c`$. The tilt preserves the direction of the marked component, so a final mark flag still selects the same collision state. When $`c`$ and $`\mu`$ are comparable, that component becomes appreciable. The eigenphase gap of the walk governs the cost of approaching the tilted vector.

At a useful batch size, the mark weight scales as $`t^r S_r`$. Choosing a tilt on the scale $`1/t`$ therefore balances the two weights at $`t\asymp S_r^{-1/(r+1)}`$. The [multiscale schedule](../science/spectral.md) reaches that scale using the known dimension. Successful early runs prepare the same ideal target direction, even though they occur less frequently.

## Read the bounds with their interfaces

| Claim | Interface and output | Read further |
|---|---|---|
| Coherent power preparation | Reversible preparation and its inverse. A success flag accompanies a state close in trace distance to the normalized coordinatewise power. | [Model](../science/model.md), [spectral algorithm](../science/spectral.md) |
| Ordinary forward preparation | Ordinary forward calls to an arbitrary compatible unitary completion. An explicit same-profile state pair gives the coherent lower bound. | [Forward-only theorem](../science/forward_only.md) |
| Separately budgeted copies and reflections | A known magnitude profile, unknown phases, supplied copies and a controlled reflection. Different tails can require different reflection costs. | [Reflection-budget theorem](../science/reflection_budget.md) |
| Mixed-state power | Reversible access to a purification. Discarding the auxiliary registers gives the normalized entrywise power of the reduced input. | [Sources with additional registers](../science/model.md#sources-with-additional-registers) |
| Measured-law separation for squaring | A shared function oracle under matched query access. The output is one classical label and the error measure is total variation distance. | [Benchmarks](../science/benchmarks.md) |
| Implementation cost | Coherent routing, comparisons, arithmetic and work registers count separately from the source queries. | [Resources](../science/resources.md) |

The [milestone map](MILESTONES.md) gives the full reading order. Use these targeted sections alongside it, then follow the scientific sources for the theorem hypotheses, error budgets and resource bounds.
