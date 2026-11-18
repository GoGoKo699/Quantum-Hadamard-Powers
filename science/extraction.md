# Exact extraction from a batch

[Source model](model.md) · [Spectral algorithm](spectral.md)

The extraction uses the multiplicity correction of Quantum Coherent Collisions. The ordered-tuple form below exposes a reversible mark for the spectral algorithm. [Quantum Coherent Collisions, exact coherent collision extraction](https://github.com/GoGoKo699/Quantum-Coherent-Collisions/blob/219f590010247124f48feffaf244a60f306335f4/science/coherent_extraction.md)

## Mark a valid choice of positions

Let a batch contain $`t\ge r`$ source slots. Fix a power of two $`B_r\ge\binom{2r-1}{r}`$. Append a rank register in the uniform state on the integers from zero to $`B_r-1`$.

For one basis tuple of labels, a choice of $`r`$ positions is valid if all its labels agree and every label occurs fewer than $`r`$ times among the remaining slots. A tuple with valid choices has exactly one label of multiplicity at least $`r`$. Its multiplicity is at most $`2r-1`$, since removing $`r`$ occurrences must leave fewer than $`r`$. The valid choices are therefore bounded in number by $`B_r`$. Sort choices by their increasing position lists in lexicographic order. The mark accepts exactly those tuple and rank pairs in which the rank indexes a valid choice within this order.

Define $`G`$ to be the diagonal orthogonal projector onto the marked computational basis states. Only their label and rank registers are inspected. The tuple state before marking is

```math
|\Phi\rangle=|\psi\rangle^{\otimes t}\otimes |u_{B_r}\rangle,
\qquad
|u_{B_r}\rangle=\frac{1}{\sqrt{B_r}}\sum_{k=0}^{B_r-1}|k\rangle .
```

A reversible implementation can sort the labeled positions, compute their run lengths, and use the original position tags to manage the rank. Reversible comparison of the rank against the number of valid choices evaluates the mark. Uncomputing the comparison workspace restores the tuple and rank.

## Factor the ideal marked vector

On a marked basis state, replace the rank by the selected position list $`J`$. The original rank is a deterministic function of the tuple and $`J`$ and can be erased by recomputation. Route the selected positions to the front and leave the residual positions in their original relative order. Duplicate computational-basis labels in the selected slots can be cleared by bitwise XOR from the first selected label. Together with $`J`$, the surviving label and the residual tuple determine the original tuple and rank. Thus the operation is reversible on the marked subspace.

Write $`y`$ for the selected label and $`z=(z_1,\ldots,z_{t-r})`$ for the ordered residual tuple. The amplitude of $`(y,J,z)`$ in the resulting unnormalized state is

```math
\frac{\alpha_y^r}{\sqrt{B_r}}\prod_{i=1}^{t-r}\alpha_{z_i}
```

whenever each residual multiplicity is less than $`r`$. Any such $`z`$ and any $`r`$-subset $`J`$ are permitted independently of $`y`$. Re-inserting $`r`$ copies of $`y`$ makes $`J`$ valid even if $`y`$ already occurs in $`z`$. The amplitude therefore factors as an output vector, a uniform position-list vector, and a residual vector. Discarding those latter registers preserves the pure powered state.

An evaluation of the mark may temporarily store the repeated label, the list of candidates, and the transcript of the sorting network. Erase all label-dependent workspace before output. The position list $`J`$ can be kept through the final routing and then discarded, since it factors from the output.

If each source slot has auxiliary state $`|g_y\rangle`$ when its label is $`y`$, route the complete slots. Clearing the duplicate label registers still leaves the $`r`$ selected auxiliary factors in their original joint branch. The residual and position list continue to factor. This gives the joint state and measured law in the [source model](model.md#sources-with-additional-registers).

## Compute the marked probability

Let $`Q_r(\ell,p)`$ be the probability that each label occurs fewer than $`r`$ times in $`\ell`$ independent draws from $`p`$. The squared norm of the factored marked vector is

```math
\mu=\|G|\Phi\rangle\|^2
=\frac{\binom tr}{B_r} S_r Q_r(t-r,p).
```

For each $`r`$-subset of the residual positions, its labels all coincide with probability $`S_r`$. A union bound gives

```math
Q_r(\ell,p)\ge 1-\binom{\ell}{r}S_r .
```

The binomial coefficient is zero when $`\ell<r`$. Directly measuring the mark takes $`t`$ source preparations per attempt. The [spectral algorithm](spectral.md) keeps the same marked direction and raises the probability of reaching it at a smaller batch size.
