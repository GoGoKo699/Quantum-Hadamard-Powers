# Spectral filtering and the unknown-moment schedule

[Source model](model.md) · [Exact extraction](extraction.md)

The mark from exact extraction identifies the desired direction inside the tensor product of source states. The algorithm changes the product projector so that its distinguished eigenvector has more amplitude in that marked direction. A spectral filter then isolates that eigenvector. Marking and extracting after this filter preserves the state announced in the source model.

## A product operator with a known gap

Choose a dyadic batch size $`t\ge r`$ and let $`P_i`$ project the $`i`$th complete source slot onto $`|\psi\rangle`$. Let $`P_{\mathrm{rank}}`$ project the rank register onto its uniform state. All these projectors commute. Define

```math
R=\frac{1}{2t}\left(\sum_{i=1}^t P_i + P_{\mathrm{rank}}+(t-1)I\right),
\qquad H=I-R.
```

The identity terms make it possible to select among $`2t`$ terms using a uniform register of Hadamards. Their deficits in $`H`$ are zero. The nonzero deficits from the other terms are commuting projectors. Their joint zero space is the span of $`|\Phi\rangle`$. Every positive eigenvalue of $`H`$ is at least $`1/(2t)`$, and $`0\le H\le I`$.

Set $`c=1/t`$ and use the diagonal contraction and the modified operator

```math
T=I-G+\sqrt c\,G,
\qquad
A=I-THT=I-T^2+TRT.
```

The unique unit vector spanning the eigenvalue-one subspace of $`A`$ is

```math
|\xi\rangle=\frac{T^{-1}|\Phi\rangle}{\|T^{-1}|\Phi\rangle\|}.
```

Since $`0\le THT\le I`$, $`A`$ is a positive contraction. The positive eigenvalues of $`THT`$ equal those of $`H^{1/2}T^2H^{1/2}`$ by equality of the nonzero spectra of $`BB^\dagger`$ and $`B^\dagger B`$, with $`B=TH^{1/2}`$. The latter operator dominates $`cH`$. The two matrices have equal nullity and the second-smallest eigenvalue of $`cH`$ is at least $`c/(2t)`$. The first excited eigenvalue of $`A`$ is consequently separated from one by at least $`c/(2t)=1/(2t^2)`$.

This construction uses state preparation and phase filtering on a product projector. Interpolation ideas for marked-set search and phase estimation for approximate reflections are earlier ingredients. [Krovi, Magniez, Ozols and Roland](https://arxiv.org/abs/1002.2419) · [Magniez, Nayak, Roland and Santha](https://arxiv.org/abs/quant-ph/0608026)

## Implement the encoded operator

A block encoding here is a unitary whose matrix element between zero ancilla states is the specified operator on the tuple and rank. For any selected projector $`P`$, the Hermitian unitary $`P\otimes I+(I-P)\otimes X`$ has zero-signal block $`P`$. Select the projectors of $`R`$ using the uniform $`2t`$-way index and conjugate by the Hadamards that prepared it. This gives a Hermitian unitary with zero-ancilla block $`R`$. The local projector tests are implemented as follows.

- For a source slot, bring it to a fixed oracle port with known index-controlled swaps. Apply $`U^\dagger`$, flip the signal if the source port differs from its known input, then apply $`U`$. Undo the indexing swaps.
- For the rank register, apply its Hadamards, perform the same kind of known flip when the rank differs from zero, and undo the Hadamards.
- For identity terms, the signal stays unchanged.

A single paired source call per controlled selection suffices. The pair acts on the same port on every branch, with the known flip controlled by the appropriate selector. On a branch whose source flip is disabled, its two calls cancel. The rank test and the known outer gates can be controlled directly.

To encode $`A`$, add a tilt register of $`\log_2 t`$ qubits in zero. Apply Hadamards to the tilt register controlled on the mark $`G`$. Its zero component on the data is $`T`$. For every nonzero tilt string, its component is $`G/\sqrt t`$. Select the encoded $`R`$ on zero tilt and the identity otherwise, then undo the mark-controlled Hadamards. Taking the zero-ancilla block gives

```math
TRT+\sum_{z\ne 0}\frac{G^2}{t}
=TRT+(1-c)G
=A .
```

This is a Hermitian unitary encoding $`V`$ of $`A`$. The mark can be computed and uncomputed before and after each controlled known operation. Every state preparation used for indexing, rank, tilt, and clock relies on a dyadic uniform register. Multi-controlled reversible gates and Hadamards therefore realize all the known operations exactly in the ideal gate model. Controlled Hadamards can also be synthesized exactly over Clifford and $`T`$ with a known basis change of the Pauli reflection. The unknown source is called through its ordinary forward and inverse gates.

## Filter the eigenvalue one component

Let $`P_0`$ project all block-encoding ancillas onto zero, leaving the data unchanged. Use the step $`W=(2P_0-I)V`$. For an eigenvector $`|x_\lambda\rangle`$ of $`A`$, start in $`|0\rangle|x_\lambda\rangle`$. The vector obtained by applying $`V`$ has clean component $`\lambda|0\rangle|x_\lambda\rangle`$ and orthogonal component of norm $`\sqrt{1-\lambda^2}`$. The span of these vectors is invariant under both $`V`$ and $`2P_0-I`$, because $`V^2=I`$. In that span $`W`$ is a rotation through $`\arccos\lambda`$. At $`\lambda=1`$, the clean vector is fixed.

Prepare a uniform clock of size $`L=8t`$, apply $`W^j`$ conditioned on clock value $`j`$, and undo the clock Hadamards. Postselecting zero clock and clean signal ancillas implements the scalar filter

```math
f_L(\lambda)=\frac1L\sum_{j=0}^{L-1}\cos(j\arccos\lambda)
```

on each eigenvector of $`A`$. At most $`L-1`$ controlled steps implement all these powers by a binary schedule. For $`\theta=\arccos\lambda>0`$, the eigenvalue gap gives $`|\sin(\theta/2)|\ge1/(2t)`$. Summing a geometric series gives

```math
|f_L(\lambda)|
\le \frac{1}{L|\sin(\theta/2)|}
\le \frac14
\qquad (\lambda<1).
```

Repeat the successful filter $`J`$ times with clean ancillas and then measure the mark. The unnormalized data vector on the branch where all tests pass is $`G f_L(A)^J|\Phi\rangle`$. Each failed test ends the attempt, and the query analysis counts up to $`J(L-1)`$ controlled steps for each attempt.

## Bound the error after conditioning

The gap bound controls absolute excited amplitude. A second bound is needed because the mark can be rare at early scales. Write $`\mu=\|G|\Phi\rangle\|^2`$, $`a=\sqrt{1-\mu}`$, $`b=\sqrt\mu`$, and $`n^2=a^2+b^2/c`$. For $`\mu>0`$, the norm $`g`$ of the ideal ground-state part after marking, and the excited norm $`e`$ before filtering, are

```math
g=\frac{(a^2+b^2/\sqrt c)(b/\sqrt c)}{n^2},
\qquad
e=\frac{ab(1/\sqrt c-1)}{n}.
```

These follow by writing $`|\Phi\rangle`$ and $`|\xi\rangle`$ in the orthonormal directions of the unmarked and marked components. Both formulas extend to $`\mu=1`$. Their ratio obeys

```math
\frac{e}{g}
=\frac{a(1-\sqrt c)n}{a^2+b^2/\sqrt c}
\le \sqrt{1+\mu/c}.
```

The ideal vector of norm $`g`$ is parallel to $`G|\Phi\rangle`$, and the norm of the remaining error after filtering and marking is at most $`4^{-J}e`$. Thus whenever $`\mu/c`$ stays bounded, the relative error of the marked vector is $`O(4^{-J})`$. The normalized actual and ideal vectors differ in Euclidean norm by at most twice the relative error, which also bounds their trace distance. Extraction and discarding registers cannot increase the trace distance. If $`\mu=0`$, $`|\Phi\rangle`$ is already the eigenvalue-one vector and the final mark never accepts.

When $`\mu/c`$ is bounded both above and below by positive constants, $`g`$ is bounded below. Indeed, $`a^2+b^2/\sqrt c\ge1`$ for $`c\le1`$. Hence at these scales an attempt succeeds with probability bounded below by a positive constant, provided $`J`$ makes the relative error at most $`1/2`$.

## Find a useful scale without knowing the moment

Take $`t_0`$ to be the smallest power of two at least $`r`$ and set the analysis constant $`\gamma_r=2^{-r-2}`$. Let $`t_\star`$ be the first dyadic $`t\ge t_0`$ satisfying $`t^{r+1}S_r\ge\gamma_r`$. This threshold size appears only in the analysis.

If $`t_\star=t_0`$, the residual length is less than $`r`$, so $`Q_r(t_0-r,p)=1`$. In the other case $`t_\star^{r+1}S_r<2^{r+1}\gamma_r=1/2`$. For each $`t\le t_\star`$ in this case, $`\binom{t-r}{r}S_r\le t^r S_r\le1/(2t)`$, so $`Q_r(t-r,p)\ge1/2`$. At $`t=t_\star`$, the formula for $`\mu`$ shows that $`\mu/c`$ has positive upper and lower bounds depending only on $`r`$. Here $`\binom tr/t^r`$ is bounded below by a positive constant depending only on $`r`$ when $`t\ge r`$. At every earlier dyadic size $`\mu/c`$ stays bounded above as well.

Use increasing dyadic caps $`t_0,2t_0,4t_0,\ldots`$. At each cap, attempt every dyadic size from $`t_0`$ up to the cap in increasing order, with $`h`$ fresh attempts at each size. Stop on the first successful mark. Let the largest cap be the smallest dyadic size at least $`t_0`$ whose $`\left(r+1\right)`$st power is at least $`N^{r-1}`$. It includes $`t_\star`$ because $`S_r\ge N^{1-r}`$.

At all sizes through $`t_\star`$, choose $`J=O_r(\log(1/\epsilon))`$ so that each successful output is within $`\epsilon/2`$ of the target. At the balanced size $`t_\star`$, choose $`h=O_r(\log(1/\epsilon))`$ so that the probability of failing all its attempts is at most $`\beta=\min(1/4,\epsilon/8)`$. Since each cap tests in increasing order, the total probability of outputting at a size above $`t_\star`$ is at most $`\beta`$. Overall failure also has probability at most $`\beta`$. The conditional output error is then at most $`\epsilon/2+\beta/(1-\beta)<\epsilon`$ by convexity of trace distance.

One attempt at size $`t`$ costs $`t`$ preparations and $`O(Jt)`$ source calls in the filter. A cap costs $`O(hJ)`$ times its largest size, since all sizes together form a geometric sum. Reaching a cap $`i`$ doublings past $`t_\star`$ requires failing at least $`i`$ independent batches of attempts at $`t_\star`$, so it has probability at most $`\beta^i`$. The expected and hard source counts are thus proportional to $`hJt_\star`$ and $`hJ`$ times the largest cap, respectively. These are the bounds stated in the [source model](model.md#theorem).
