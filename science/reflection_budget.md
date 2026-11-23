# Native copies and paid reflections for coherent squares

[Source model](model.md) · [Spectral algorithm](spectral.md) · [Forward-only access](forward_only.md)

## Same collision moment, different reflection costs

Take an integer $`K`$ tending to infinity, ambient dimension $`K^2`$, and a hard budget $`t`$ of native copies satisfying $`t\gtrsim K^{1/3}`$ and $`t=o(\sqrt K)`$. The algorithm receives the complete magnitude profile $`p`$. Relative phases are arbitrary. An algorithm may apply a controlled reflection about the unknown state, with each invocation charged. All native specimens, including retries, count toward $`t`$. Require success at least a fixed $`s_0\in(0,1)`$ and conditional trace distance at most a fixed $`0<\varepsilon\le1/8`$ on every input. A reflection acts as $`2|\psi\rangle\langle\psi|-I`$ on the queried register when enabled. The target is the physical coherent square. The lower bounds test phase information that a computational-basis sample discards.

All three profiles have $`S_2=\sum_i p_i^2=1/K`$. The flat profile uses $`K`$ nonzero labels. A second profile puts weight $`a`$ on each of two distinguished labels and $`b=(1-2a)/M`$ on each of $`M=K^2-2`$ other labels. A third uses the same construction with $`M=2K`$, padding the remaining labels with zero. For either value of $`M`$, set

```math
a=\frac{1+\sqrt{M(M+2-K)/(2K)}}{M+2}.
```

This is the root of $`2a^2+(1-2a)^2/M=1/K`$ with $`a>b`$, for large $`K`$.

| Profile | Powered mass on the uniform tail | Optimal charged reflections |
| --- | --- | --- |
| Flat on $`K`$ labels | All of it | $`\Theta(\sqrt{K/t})`$ |
| Two heavy labels, diffuse tail $`M=K^2-2`$ | $`\Theta(1/K)`$ | $`\Theta(K^{1/4})`$ |
| Two heavy labels, broad tail $`M=2K`$ | $`1/2+o(1)`$ | $`\Theta(\sqrt{K/t})`$ |

At $`t=\Theta(K^{1/3})`$, the two reflection exponents are $`1/4`$ and $`1/3`$. Both nonflat profiles have maximum probability of order $`K^{-1/2}`$. The share of the powered state carried by the tail distinguishes them.

### Broad-tail converse

For the lower bound give the two heavy phases to the algorithm and vary only the $`M`$ tail phases $`\theta`$ independently. Dilate adaptive measurements and controls, retain the success flag and private memory, and pad the $`t`$ copies up front. Oracle calls on halted branches use the inactive control. Let the Fourier charge of the dilated state be $`n\in\mathbb Z^M`$, with normalized Haar measure on the torus. Known gates commute with the projection onto charge sets. Call a charge good if every $`n_i\in\{0,1\}`$. The initial bad norm is at most $`\sqrt{\binom t2 M b^2}`$ by the union bound on repeated tail labels. After $`k`$ reflections all actual charges have $`\sum_i n_i\le t+k`$, because a projection onto the source can raise this sum by at most one.

Write the lifted source projection as $`VV^\dagger`$. The isometry $`V`$ appends the oracle-port label $`i`$ with weight $`\sqrt{p_i}`$ and adds $`e_i`$ on tail labels (zero shift on the known head, with its known phases included as scalars). For good input to $`V^\dagger`$, an intermediate charge $`z`$ either has entries zero or one, with at most $`t+k`$ ones, or has one entry $`-1`$ at $`j`$ and zeros or ones elsewhere.

- In the nonnegative blocks, $`V`$ sends a component to bad charge only when it adds a tail unit vector to an occupied position. Its bad block has norm at most $`\sqrt{(t+k)b}`$. Outputs from distinct $`z`$ are orthogonal in the pair of charge and port label, before and after charge projection.
- In a block with one negative entry at $`j`$, $`V^\dagger`$ acting from a good charge can only have removed label $`j`$, of weight $`\sqrt b`$. The operator norm of that part is at most $`\sqrt b`$. Subsequent $`V`$ and projection are contractions.

A controlled reflection, including an inactive branch, adds at most $`2(\sqrt{(t+k)b}+\sqrt b)`$ to the norm in the bad sector. Existing bad amplitude contributes at most its previous norm since the full step is unitary. Thus the final bad norm is bounded by

```math
B(t,q)\le \sqrt{\binom t2 M b^2}+2q\big(\sqrt{(t+q)b}+\sqrt b\big).
```

Let $`|\tau_\theta\rangle=M^{-1/2}\sum_{j\in\mathrm{tail}}e^{2i\theta_j}|j\rangle`$ be the powered tail direction. Contract the successful component with this vector. Its norm on the good sector is bounded by $`1/\sqrt M`$: subtraction of $`2e_j`$ produces a charge with a unique negative entry at $`j`$, and for fixed $`j`$ the shift is injective. The contraction on the bad sector has norm at most one. Its whole output norm is the square root of the phase-averaged probability of success and passing the tail-direction test. This probability is at least $`s_0(w-\varepsilon)`$, where $`w=M b^2/S_2`$ is the ideal tail mass, by the operational definition of trace distance.

Hence $`\sqrt{s_0(w-\varepsilon)}\le 1/\sqrt M+B(t,q)`$. For $`M=2K`$, $`b\asymp K^{-1}`$, $`w\to1/2`$, and the initial bad norm tends to zero. If $`q\lt t`$, the bound gives $`q=\Omega(\sqrt{K/t})`$; if $`q\ge t`$, this already holds since $`t\gtrsim K^{1/3}`$. The same proof gives the flat lower bound by taking an empty head, $`M=K`$, $`b=1/K`$, and $`w=1`$.

### Diffuse-tail converse and construction

Fix all except the second heavy phase and choose that phase to be $`+\pi/4`$ or $`-\pi/4`$. The powered head directions $`(|0\rangle\pm i|1\rangle)/\sqrt2`$ are orthogonal. The full targets each have a common tail of mass $`w=O(1/K)`$. On success, test for the plus head direction and guess plus if it passes. On failure, guess by fair coin. At fixed accuracy and success this has a constant probability gap across the two inputs for large $`K`$.

The two source states have single-copy trace distance $`d=\sqrt{2a(1-a)}=O(K^{-1/4})`$, so $`t`$ copies have distance at most $`\sqrt t\,d=o(1)`$. Their source reflections differ in operator norm $`2d`$, including the controlled form. Contractivity and a query hybrid give final trace distance at most $`\sqrt t\,d+2qd`$, establishing $`q=\Omega(K^{1/4})`$.

For the upper bound, use the known two-label projector and the source reflection to amplify each native specimen into the head in $`O(a^{-1/2})`$ calls at constant probability. Successful projection into the head returns exactly the normalized head state because Grover rotation stays in the plane spanned by the head and its complement. Two such successful states, followed by coherent equality and cleanup, give the head square with constant probability. Repeat a fixed number of times to match the success guarantee. This consumes a fixed number of native copies and $`O(K^{1/4})`$ reflections. The successful head square differs from the full normalized square by trace distance $`\sqrt w=O(K^{-1/2})`$.

### Broad and flat constructions

For a dyadic batch $`m`$ equal to a small fixed fraction of $`t`$, use the ordered-rank mark with $`\mu=\binom m2 S_2 Q_2(m-2,p)/B_2`$. The union bound gives $`Q_2\ge 1-\binom{m-2}2/K`$, so $`\mu\asymp m^2/K`$. Known $`K,m`$ suffice to choose a dyadic tilt $`c\asymp\mu`$, with the ratio bounded above and below by constants. Supply the $`m`$ source slots as native copies. Each local projector test is a controlled source reflection conjugated by Hadamards on the signal bit. The reflection interface supplies the source-dependent operations.

Choose $`c=2^{-j}`$ for an integer $`j`$. In the [block encoding](spectral.md#implement-the-encoded-operator), apply Hadamards on $`j`$ tilt qubits rather than tying their number to the batch. The zero component is $`T=I-G+\sqrt c\,G`$ and the nonzero components contribute $`(1-c)G`$ in total to the clean block. The positive gap of $`THT`$ is at least $`c/(2m)`$. For any active nonzero phase $`\theta`$ the half-angle sine is at least $`\sqrt{c/(4m)}`$. The finite clock therefore achieves a constant off-target attenuation with dyadic length $`L=O(\sqrt{m/c})`$. Repeating a fixed number of filters costs $`O(\sqrt{m/c})`$ reflection calls per fixed-accuracy attempt. As in the [conditioned-error analysis](spectral.md#bound-the-error-after-conditioning), the ideal ground-state overlap and its marked weight are bounded below when $`\mu/c`$ is bounded above and below, and the conditioned error is controlled by fixed repetitions of the filter. A fixed number of fresh batches gives any fixed success probability $`s_0<1`$ within the hard copy budget (adjust the fraction in $`m`$). The resulting reflection budget matches the lower bound for the broad and flat profiles. The optimal tradeoff for arbitrary magnitude profiles remains open.

### Matching three input summaries exactly

The fast and slow profiles can share $`S_2`$, the largest probability, and the sum of the $`t`$ largest probabilities. Let the diffuse profile have head $`(a,a)`$ and tail value $`d=(1-2a)/(K^2-2)`$. Construct a slow profile with three head values $`(a,c,c)`$, $`t-3`$ tail entries of size $`b=1/(2K)`$, and additional tail entries at most $`b`$, where

```math
c=\frac{a+(t-2)d-(t-3)b}{2}.
```

Since $`t=o(\sqrt K)`$, $`c\sim a/2`$ and $`a>c>b`$ for large $`K`$. The top-$`t`$ sum is exactly $`2a+(t-2)d`$, and the maximum is exactly $`a`$. Pad with zeros to the same ambient dimension.

The remaining entries must have mass $`R=1-a-2c-(t-3)b`$ and squared mass $`W=1/K-a^2-2c^2-(t-3)b^2`$. Here $`R\to1`$ and $`W\sim1/(4K)`$. On $`8K`$ entries, the uniform choice with total $`R`$ has squared mass $`R^2/(8K)`$ below $`W`$. The choice filling entries up to $`b`$ then placing the remainder in the next entry has squared mass at least $`b(R-b)`$, above $`W`$. Both lie in the box $`[0,b]^{8K}`$ at the same total mass. Their line segment contains a choice with squared mass exactly $`W`$. Thus the slow profile has exact $`S_2=1/K`$ and tail squared mass $`\sim1/(4K)`$.

The tail-charge proof still works for nonuniform tail probabilities: replace $`M b^2`$ in the initial bound by their actual squared mass $`S_{2,\mathrm{tail}}`$, use their maximum $`b`$ in the reflection bound, and replace $`1/\sqrt M`$ in the output bound by $`b/\sqrt{S_{2,\mathrm{tail}}}`$. The latter is the largest amplitude in the normalized squared tail. Its norm still bounds the good-sector contraction because a unique negative charge identifies the output label. The slow profile therefore requires $`\Theta(\sqrt{K/t})`$ calls at the same fixed accuracy and success, whereas the diffuse profile uses $`\Theta(K^{1/4})`$. The three matched summaries therefore leave the reflection exponent undetermined.

## Ownership and prior work

The [copy-only collision instrument and occupation converse](https://github.com/GoGoKo699/Quantum-Coherent-Collisions) supply the native-copy endpoint. The [ordered mark](extraction.md) and [tilted filter](spectral.md) supply the spectral upper bound when a controlled reflection is available. Bhateja, Esmaili and Mantri’s Theorem 8.1 gives a related stored-copy upper bound for flat magnitudes using their reversible source model. The profile dependence here follows from the tail Fourier bound and the two-state query hybrid. [Related work](../references/RELATED_WORK.md#copy-and-reflection-budgets)

Call counts measure the stated interface. A forward/inverse pair implements one controlled reflection around a known reset state. Additional preparation columns define a different interface. The gate and space costs of the ordered mark and tuple routing are accounted for separately in the [resource analysis](resources.md).
