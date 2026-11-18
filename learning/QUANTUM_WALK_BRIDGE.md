# From quantum walk search to Hadamard powers

The project starts with a reversible circuit that prepares an unknown state. Two copies sometimes agree when measured in the computational basis. Measuring that agreement gives a useful distribution, but projecting onto agreement before measuring the labels can leave a quantum state with squared amplitudes. This bridge explains how a phase filter makes that coherent output affordable.

The educational anchor is **Frédéric Magniez, Ashwin Nayak, Jérémie Roland and Miklos Santha, _Search via Quantum Walk_**, SIAM Journal on Computing 40(1), 142–164 (2011). The section and theorem numbering below follows [arXiv:quant-ph/0608026v4](https://arxiv.org/abs/quant-ph/0608026v4), the version dated 14 February 2011. The publication identifier is [10.1137/090745854](https://doi.org/10.1137/090745854).

## Targeted reading

| In the anchor | Carry into the project | Milestones |
|---|---|---|
| §1.2, search costs | Separate setup, update and checking. Counting one black-box call per walk update leaves the known circuitry to be costed. | [M10](MILESTONES.md#m10-setup-update-and-checking) |
| §2, especially Theorem 4 | A walk converts real spectral data into unitary eigenphases. Restrict attention to the invariant subspace reached by the starting state. | [M08](MILESTONES.md#m08-eigenvalues-become-eigenphases) |
| §3.1, marked and unmarked components | Understand the two directions obtained by projecting a coherent starting state onto a marked subspace and its complement. The marked direction carries the information to be returned. | [M04](MILESTONES.md#m04-a-flag-without-reading-the-label), [M12](MILESTONES.md#m12-the-operational-question) |
| §3.2, Theorems 5–6 | The zero-phase test accepts the eigenphase zero exactly. A phase gap suppresses other eigenphases, and more tests sharpen the approximation. | [M09](MILESTONES.md#m09-a-finite-zero-phase-test), [M21](MILESTONES.md#m21-filtering-the-tilted-ground-state) |
| §3.3, especially Theorem 7 | Read a resource statement alongside its setup, update, checking and success assumptions. | [M24](MILESTONES.md#m24-searching-the-scales), [M28](MILESTONES.md#m28-pricing-the-circuit) |

The anchor develops search using a walk-based approximate reflection inside amplitude amplification. Here the walk encodes a product operator with a tilted ground state. A phase filter projects toward that vector, and the final flag identifies the marked component. The companion [spectral proof](../science/spectral.md) supplies the tilt, the gap bound and the error analysis. The [extraction proof](../science/extraction.md) supplies the collision rule that gives the marked component its meaning.

## Translate the notation

| Anchor | This project | Role |
|---|---|---|
| Coherent stationary vector $`|\pi\rangle`$ | Product state $`|\Phi\rangle`$ of source registers and a rank register | Starting direction for the search. Its coefficients can carry complex phases. |
| Marked set and its orthogonal projector | Mark projector $`G`$ on valid tuple–rank pairs | Chooses coherent configurations that encode the powered output. |
| Stationary marked probability $`p_M`$ | $`\mu=\lVert G|\Phi\rangle\rVert^2`$ | Weight of the marked component before filtering. |
| Discriminant eigenvalues or singular values, and phase gap of $`W(P)`$ | Spectrum of $`A=I-THT`$ and phase gap of its walk | An eigenvalue $`\lambda`$ gives active phases $`\pm\arccos\lambda`$ in this convention. |
| Phase-estimation output used in a reflection | Clean signal and zero-phase success flags | Repeated tests damp contributions orthogonal to the desired eigenvector. |

In the anchor, $`\epsilon`$ can denote a lower bound on marked probability. Here $`\varepsilon`$ is the requested output error. The mark weight is $`\mu`$, and the input-dependent collision moment is $`S_r=\sum_y|\alpha_y|^{2r}`$. The algorithm uses the dimension and target accuracy to set its schedule.

## Follow a three-copy example

Take two labels and prepare

```math
|\psi\rangle=\frac{\sqrt 3}{2}|0\rangle+\frac{i}{2}|1\rangle .
```

The computational-basis probabilities are $`(3/4,1/4)`$, and the probability of a collision between two independent samples is $`S_2=5/8`$. The normalized Hadamard square is

```math
|\psi^{[2]}\rangle=\frac{3|0\rangle-|1\rangle}{\sqrt{10}} .
```

The minus sign comes from $`i^2=-1`$. Measuring the target in the computational basis gives $`(9/10,1/10)`$, which cannot reveal that relative sign.

Use $`t=3`$ source copies and a rank register with four equiprobable values. In the tuple $`001`$, one position pair is valid. In $`000`$, three pairs are valid. The rule accepts one rank for the first tuple and three for the second. In both tuples, every valid rank identifies a distinct pair with equal labels.

After a successful rank, route the selected pair to the first two registers, clear the duplicate label and retain the position pair and the unselected label. In the reindexed state, each position pair and each residual label has a contribution from both candidate output labels. Their respective factors are $`(\sqrt 3/2)^2=3/4`$ and $`(i/2)^2=-1/4`$. The residual amplitude multiplies each by the same factor. Therefore the residual system and the pair index factor from the output, so discarding them leaves the pure state above.

The initial weight of the marked component is $`\binom{3}{2}S_2/4=15/32`$. The residual has just one register, so it satisfies the requirement that it have no equal pair. With longer tuples that residual condition affects the success probability. Its dependence on the residual alone is what preserves the output factorization.

## Connect the phase filter to the output

The unfiltered starting vector is a product state. For each coordinate, the rank-one projector onto its starting state is a test that the coordinate agrees with its preparation. These tests commute. Their average has a unique eigenvector with eigenvalue one, the product state, with gap proportional to $`1/t`$. Indexing a single coordinate test in superposition uses two source calls even though the known routing acts on a batch of registers.

The project sets $`H`$ to identity minus that average and lets $`T=I-G+\sqrt c\,G`$. The operator $`THT`$ has bottom eigenvector proportional to $`T^{-1}|\Phi\rangle`$. In that vector the marked component is multiplied by $`1/\sqrt c`$. The tilt preserves the direction of the marked component, so a final mark flag still selects the same collision state. When $`c`$ and $`\mu`$ are comparable, that component becomes appreciable. The eigenphase gap of the walk governs the cost of approaching the tilted vector.

At a useful batch size, the mark weight scales as $`t^r S_r`$. Choosing a tilt on the scale $`1/t`$ therefore balances the two weights at $`t\asymp S_r^{-1/(r+1)}`$. The [multiscale schedule](../science/spectral.md) reaches that scale using the known dimension. Successful early runs prepare the same ideal target direction, even though they occur less frequently.

## Read the bounds with their interfaces

| Claim | Interface and output | Read further |
|---|---|---|
| Coherent power preparation | Reversible preparation and its inverse. A success flag accompanies a state close in trace distance to the normalized coordinatewise power. | [Model](../science/model.md), [spectral algorithm](../science/spectral.md) |
| Measured-law separation for squaring | A shared function oracle under matched query access. The output is one classical label and the error measure is total variation distance. | [Benchmarks](../science/benchmarks.md) |
| Implementation cost | Coherent routing, comparisons, arithmetic and work registers count separately from the source queries. | [Resources](../science/resources.md) |

The [milestone map](MILESTONES.md) gives the full reading order. Use these targeted sections alongside it, then follow the scientific sources for the theorem hypotheses, error budgets and resource bounds.
