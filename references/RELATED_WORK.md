# Related work

## Collective collision extraction

[Quantum Coherent Collisions](https://github.com/GoGoKo699/Quantum-Coherent-Collisions/blob/219f590010247124f48feffaf244a60f306335f4/science/coherent_extraction.md) gives the exact multiplicity-corrected filter, its residual factorization and a sharp copy-only law. The present construction inherits that filter and expresses it with a rank register over eligible subsets. Reversible source calls allow a spectral operation on the entire tuple, which changes the cost exponent from the copy-only $`1/r`$ to $`1/(r+1)`$ in the inverse moment. See the [ordered-register extraction](../science/extraction.md) and the [spectral filter](../science/spectral.md).

## Collision sampling and coherent Hadamard products

Bhateja, Esmaili and Mantri establish the cube-root query law for the collision distribution in the Haar and Fourier ensembles. Their Theorem 6.6 controls total variation on average over the ensemble. Their Theorem 8.1 prepares the coherent coordinatewise product of two inputs with flat coordinate magnitudes. Proposition 8.2 gives the Haar-state Hadamard square lower bound and leaves its upper bound open. The present construction supplies that upper bound with pointwise trace error and arbitrary complex amplitudes. Its measured-law extension permits sampler garbage and proves a separate worst-case benchmark on a shared evaluator. [Bhateja, Esmaili and Mantri, §§6 and 8](https://arxiv.org/html/2610.06721v1#S8)

## Spectral filtering and amplitude transforms

The phase-detection technique follows the quantum-walk framework of Magniez, Nayak, Roland and Santha. The reweighting of the marked component is motivated by interpolated walks of Krovi, Magniez, Ozols and Roland. Here the operator is built directly from local source-state projectors and a computational-basis collision predicate. Its zero mode determines the particular marked direction, which is what keeps the output phases coherent. [Search via Quantum Walk](https://doi.org/10.1137/090745854) · [Quantum walks can find a marked element on any graph](https://arxiv.org/abs/1002.2419)

Guo, Mitarai and Fujii construct amplitude block encodings and use quantum singular value transformations for complex-amplitude transforms. Rattew and Rebentrost analyze nonlinear transformations with normalization and importance sampling. The relevant comparison here is a normalized monomial on one unknown state. Directly applying the diagonal encoding of the amplitudes to the input produces the square subnormalized by $`\sqrt{S_2}`$. Standard amplification of that branch costs $`O(S_2^{-1/2})`$ source uses. The tuple construction changes the success mechanism by using many possible collision subsets and inferring a marked spectral direction. The [benchmark chapter](../science/benchmarks.md) makes the comparison at the relevant input and output contract. [Guo, Mitarai and Fujii](https://arxiv.org/abs/2107.10764) · [Rattew and Rebentrost](https://arxiv.org/abs/2309.09839)

## Decision-to-sampling reduction

The proof uses Kutin’s small-range collision decision lower bound for one-to-one versus two-to-one functions. The two-tag evaluator translates that promise into a constant gap in the squared-law tag probability. This supplies a lower bound for the measured task even when the classical algorithm may choose evaluator inputs adaptively. [Kutin, Theorem 1.1](https://theoryofcomputing.org/articles/v001a002/)

The [bibliography](references.bib) records the source versions used in these comparisons.
