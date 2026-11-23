# Forward-only access for coherent Hadamard powers

[Source model](model.md) · [Reversible algorithm](spectral.md) · [Copy and reflection budgets](reflection_budget.md)

Fix an integer $`r\ge 2`$ and an $`N`$-dimensional computational basis. Let an unknown unitary $`U`$ prepare

```math
|\psi\rangle=U|0\rangle=\sum_y\alpha_y|y\rangle,\qquad
S_r=\sum_y|\alpha_y|^{2r}.
```

The task is to herald the normalized coherent state with amplitudes $`\alpha_y^r/\sqrt{S_r}`$. Each ordinary forward query applies $`U`$ unconditionally to the chosen register. Between calls the protocol may use source-independent gates, ancillas, adaptive measurements and classical control. The theorem is about the worst case over the unitary extensions of $`U|0\rangle`$ in dimension $`N`$.

## The forward-only query law

Let the success probability be at least $`\sigma\in(0,1)`$ for every permitted source, and let the output conditioned on success have trace distance at most $`\epsilon\in[0,1/2)`$ from the target, where trace distance is half the trace norm. For fixed $`r,\sigma,\epsilon`$, the worst-case number of forward-only queries is $`\Theta_{r,\sigma,\epsilon}(N^{1-1/r})`$. This holds for a hard cap and for a uniform bound on expected queries. The lower bound already holds when the input is promised to be one of two explicitly known states with identical coordinate magnitudes. In particular, providing the common input magnitude profile and the collision moment does not weaken the lower bound.

The upper bound uses one forward call on a fresh $`|0\rangle`$ per copy, followed by the exact collective instrument in [Quantum Coherent Collisions](https://github.com/GoGoKo699/Quantum-Coherent-Collisions/blob/219f590010247124f48feffaf244a60f306335f4/science/model.md). It gives an exact ideal successful output and fixed-success hard cap $`O_r(N^{1-1/r})`$. Independent repetitions raise success to any prescribed constant below one while preserving exactness. The expected copy bound $`O_r(S_r^{-1/r})`$ also transfers directly to forward queries.

### A hard pair with identical magnitudes

For $`N\ge4`$, set $`n=N-2`$ and $`a=(r-1)/r`$. Let $`|u\rangle`$ be the uniform superposition over labels $`2,\ldots,N-1`$. The positive number $`p`$ is fixed by

```math
\frac{p}{1-p}=n^{-a}.
```

Define the two candidates

```math
|\psi_\pm\rangle=\sqrt{1-p}\,|u\rangle+
e^{\pm i\pi/(2r)}\sqrt p\,|1\rangle.
```

The bulk coordinates contribute $`(1-p)^r n^{1-r}`$ to $`S_r`$ and the spike contributes $`p^r`$. These contributions are equal by the choice of $`p`$, so the two powered targets are

```math
|\beta_\pm\rangle=\frac{|u\rangle\pm i|1\rangle}{\sqrt2}.
```

The targets are orthogonal, but their source states have squared overlap $`1-\Delta`$, where

```math
\Delta=4p(1-p)\sin^2\!\left(\frac{\pi}{2r}\right).
```

In particular, $`\Delta=\Theta_r(N^{-a})`$.

### Transfer from forward queries to copies

Let an algorithm use at most $`q`$ forward queries. On success, distinguish the powered targets with a known projective measurement and on failure guess a fair bit. Under an equal prior for $`\psi_+`$ and $`\psi_-`$, the resulting decision is correct with probability at least

```math
\frac12+\sigma\left(\frac12-\epsilon\right)
```

for every choice of the compatible unitary in either case. This uses the trace-distance bound on the probability of any event, applied to the conditional successful state. For each sign, average the algorithm's complete output over Haar-random unitary completions of $`U|0\rangle=|\psi_\pm\rangle`$. The success guarantee survives this averaging.

The two candidates live in the same known two-dimensional linear subspace, $`\operatorname{span}\{|u\rangle,|1\rangle\}`$, which is orthogonal to the source input $`|0\rangle`$. Isogai, Yoshida and Murao's [Theorem 3.3, equation (35), arXiv:2609.38403v2](https://arxiv.org/html/2609.38403v2#S3) gives one channel that uses $`q`$ copies of either candidate and approximates the corresponding Haar-averaged output within trace distance $`q/(N-1)`$ for $`q<N-1`$. The channel can retain the success flag or the final decision bit. The requirement $`q<N-1`$ causes no loss for the asymptotic bound, since $`q\ge N-1`$ is already larger than the claimed order.

By contractivity of trace distance and the triangle inequality, the distance between the two Haar-averaged outputs is at most

```math
\sqrt{1-(1-\Delta)^q}+\frac{2q}{N-1}
\le
2\sin\!\left(\frac{\pi}{2r}\right)\sqrt{qp}+\frac{2q}{N-1}.
```

The decision guarantee therefore implies

```math
\sigma(1-2\epsilon)
\le
2\sin\!\left(\frac{\pi}{2r}\right)\sqrt{qp}+\frac{2q}{N-1}.
```

Since $`p=\Theta_r(N^{-a})`$ and $`a<1`$, this forces $`q=\Omega_{r,\sigma,\epsilon}(N^a)`$. The simulation uses the original $`N`$-dimensional oracle. Each hard state has $`N-1`$ nonzero coordinates, while the linear span of the pair has dimension two.

For expected queries, first turn the heralded algorithm into the same binary decision procedure. If the expected query count is uniformly at most $`T`$, truncate it at a constant multiple of $`T/[\sigma(1-2\epsilon)]`$ and guess on timeout. By Markov's inequality the truncation loses at most half the constant decision advantage. The hard-cap lower bound then gives the same scaling for $`T`$. The argument controls the success probability of the decision procedure directly.

## Measured output

Suppose the successful output is only a classical sample, within total variation $`\epsilon<1/2`$ of the computational-basis law of the powered state. There is also a worst-case forward lower bound $`\Omega_{r,\sigma,\epsilon}(N^{1-1/r})`$ for this task. For $`N\ge5`$, use $`n=N-3`$ bulk labels $`3,\ldots,N-1`$, reserve source label $`0`$ and take the two possible spike labels $`1,2`$. Fix a desired powered spike probability $`\lambda\in(2\epsilon,1)`$, set

```math
\frac{p}{1-p}=\left(\frac{\lambda}{1-\lambda}\right)^{1/r}n^{-a},
```

and use $`\sqrt{1-p}\,|u\rangle+\sqrt p\,|j\rangle`$ for spike $`j\in\{1,2\}`$. The candidates have the same moment and the same multiset of input probabilities. Their powered distributions place probability $`\lambda`$ on the respective spike and $`1-\lambda`$ on the common uniform bulk. Guess according to the spike if one is seen and guess uniformly otherwise. The correct decision probability on success is at least $`(1+\lambda)/2-\epsilon`$. On failure guess uniformly.

The known linear span has dimension at most three. The copy-simulation error per candidate is at most $`2q/(N-1)`$ for $`2q<N-1`$. The squared source overlap is $`(1-p)^2`$, so the same argument gives

```math
\sigma(\lambda-2\epsilon)\le\sqrt{2qp}+\frac{4q}{N-1},
```

and hence the lower bound. Measuring the copy-based coherent output gives a matching hard-cap upper bound. The coherent hard pair above has identical basis measurement laws, so the measured statement uses this separate pair.

## Relation to the reversible algorithm and prior work

With both $`U`$ and $`U^\dagger`$, [the reversible algorithm](spectral.md) constructs an approximate powered state using $`O_{r,\epsilon}(N^{(r-1)/(r+1)})`$ queries at fixed error and high success. The spectral filter uses paired source calls to act on a slot in a coherent tuple. Thus the forward-only lower bound isolates the role of inverse access in the worst-case improvement for every fixed power. At sufficiently small fixed positive trace error the square costs $`\Theta(\sqrt N)`$ with forward access and $`\Theta(N^{1/3})`$ with reversible access, using the existing reversible lower bound. For higher powers the reversible upper bound suffices for a strict separation.

The quantum copy simulator is inherited. The transformation-specific step is choosing a pair whose source states are separated by $`\Theta_r(N^{-(r-1)/(2r)})`$ in trace distance and whose normalized powers are orthogonal. This two-dimensional construction supplies a dimension-$`N`$ lower bound even though the powered state has many nonzero coordinates.

- Isogai, Yoshida and Murao, [arXiv:2609.38403v2, Theorem 3.3 and Definition 3.1](https://arxiv.org/html/2609.38403v2#S3), prove the general copy simulator and apply it to PAC learning. Their query model is ordinary forward-only and their theorem approximates the Haar-completion average. The argument above applies that result to the coordinatewise-power task.
- Wang, Carolan and Childs, [arXiv:2610.05389v1, Theorem 1.1 and Section 4](https://arxiv.org/html/2610.05389v1#S4), study deciding which of two known states is prepared. Their discrete theorem treats trace separation $`\delta`$ with dimension at least order $`\delta^{-8}`$ and covers controlled forward access. Applying their stated dimension requirement directly to the pair above does not give the dimension-$`N`$ exponent. The Isogai simulator instead gives an explicit error linear in $`q/N`$ for this low-dimensional span. The bound here uses ordinary forward access.
- Tang and Wright, [arXiv:2507.23787v2](https://arxiv.org/html/2507.23787v2), establish related forward-only obstructions for amplitude amplification and estimation. Their tasks concern amplifying or estimating a marked component, while the coherent pair above gives two orthogonal relative-phase targets under the same known magnitude profile.
- Bhateja, Esmaili and Mantri, [arXiv:2610.06721v1, Sections 6 and 8](https://arxiv.org/html/2610.06721v1#S8), give a reversible-source construction for flat-magnitude products and the reversible Haar-square lower bound. The ordinary forward-only completion lower bound is a different access and input claim.
- Holmes et al., [Physical Review Research 5, 013105 (2023), Section II.C](https://doi.org/10.1103/PhysRevResearch.5.013105), establish the elementary postselected Hadamard product and repeated powers. The matching forward-only upper bound here uses the later collective extraction, which reduces the copy count.
- Guo, Mitarai and Fujii, [Physical Review Research 6, 043227 (2024)](https://doi.org/10.1103/PhysRevResearch.6.043227), and Rattew and Rebentrost, [arXiv:2309.09839v1](https://arxiv.org/abs/2309.09839v1), give general amplitude transformations using stronger source primitives.
