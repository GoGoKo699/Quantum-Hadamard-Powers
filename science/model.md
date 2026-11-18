# Reversible source model and guarantees

[Exact extraction](extraction.md) · [Spectral algorithm](spectral.md)

Let $`\alpha_y`$ denote the complex amplitude of basis label $`y\in\{0,\ldots,N-1\}`$ in a normalized state $`|\psi\rangle`$. A source query applies either $`U`$ or $`U^\dagger`$, where a known computational-basis input $`|0\rangle`$ satisfies

```math
U|0\rangle=|\psi\rangle=\sum_{y=0}^{N-1}\alpha_y|y\rangle .
```

An encoding into qubits can pad unused labels with zero amplitudes. The source may have any unitary extension consistent with this column. Let $`p_y=|\alpha_y|^2`$. For a fixed integer $`r\ge 2`$, define the moment $`S_r`$ and the desired output by

```math
S_r=\sum_y p_y^r,
\qquad
|\psi^{[r]}\rangle=\frac{1}{\sqrt{S_r}}\sum_y\alpha_y^r|y\rangle .
```

The power is coordinatewise in the specified basis. In particular, the complex phase of a nonzero amplitude is multiplied by $`r`$. A common phase of the input contributes only a common phase to the output. The source dimension $`N`$ and the power $`r`$ are known. The algorithm uses the same circuit schedule for every input of that dimension, with stopping determined by its own flags.

## Theorem

For every $`0<\epsilon\le 1/4`$, an explicit algorithm reports success with probability at least $`1-\epsilon`$. Conditioned on success, its output density operator $`\rho`$ satisfies

```math
\frac12\bigl\|\rho-|\psi^{[r]}\rangle\langle\psi^{[r]}|\bigr\|_1\le\epsilon .
```

The expected number of calls on each input and the hard number of calls on every branch, respectively, are

```math
O_r\bigl(S_r^{-1/(r+1)}\log^2(1/\epsilon)\bigr),
\qquad
O_r\bigl(N^{(r-1)/(r+1)}\log^2(1/\epsilon)\bigr).
```

Both bounds charge calls to $`U`$ and $`U^\dagger`$, including calls on branches that report failure. Constants can depend on fixed $`r`$. The algorithm uses the source interface and known dimension directly, with coherent indexed swaps, reversible comparisons and Hadamard gates. A local projector test uses a paired application of $`U^\dagger`$ and $`U`$ around a known operation, which also supplies its controlled form. Separate registers and explicit swaps suffice for routing.

For $`r=2`$, the fixed-error worst-case source-query upper bound is $`O(N^{1/3})`$. It applies pointwise, and thus applies to Haar-source inputs as a special case. Bhateja, Esmaili and Mantri's Proposition 8.2 gives the matching order of lower bound at sufficiently small fixed trace error for Haar inputs. The lower bound applies to a hard query budget. Any uniform expected query bound can be converted into a hard budget by truncation at a constant multiple of that bound, at the cost of a small constant addition to the error. [Bhateja, Esmaili and Mantri, Section 8.2](https://arxiv.org/html/2610.06721v1#S8.SS2)

## Sources with additional registers

A reversible sampler can instead prepare a purification

```math
U|0\rangle=\sum_y\sqrt{p_y}|y\rangle|g_y\rangle,
\qquad \langle g_y|g_y\rangle=1
```

for labels of positive probability, with arbitrary auxiliary states. Each addressed source slot then comprises the whole label and auxiliary register. Collision eligibility uses the label alone. The accepted ideal branch leaves the auxiliary registers associated with the selected $`r`$ samples attached to the output label. Its normalized joint state is

```math
\frac{1}{\sqrt{S_r}}\sum_y p_y^{r/2}|y\rangle|g_y\rangle^{\otimes r}.
```

Measuring the label produces the law $`p_y^r/S_r`$. The theorem's source costs and trace-distance guarantee apply to this joint state. The corresponding total-variation bound on measured labels follows from contractivity under measurement. A caller that always needs a classical output can return an arbitrary label on failure, increasing the error by at most the failure probability. Running the theorem with half the desired tolerance keeps their sum within the desired tolerance.

The theorem provides a heralded state preparation. Its query savings price reversible source calls. Circuit depth, auxiliary space, and the physical costs of realizing those calls enter a separate resource comparison.
