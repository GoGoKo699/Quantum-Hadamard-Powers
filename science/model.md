# Reversible source model and guarantees

[Exact extraction](extraction.md) · [Spectral algorithm](spectral.md) · [Forward-only access](forward_only.md) · [Copy and reflection budgets](reflection_budget.md)

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

For every $`0\lt\epsilon\le 1/4`$, an explicit algorithm reports success with probability at least $`1-\epsilon`$. Conditioned on success, its output density operator $`\rho`$ satisfies

```math
\frac12\bigl\lVert\rho-|\psi^{[r]}\rangle\langle\psi^{[r]}|\bigr\rVert_1\le\epsilon .
```

The expected number of calls on each input and the hard number of calls on every branch, respectively, are

```math
O_r\bigl(S_r^{-1/(r+1)}\log^2(1/\epsilon)\bigr),
\qquad
O_r\bigl(N^{(r-1)/(r+1)}\log^2(1/\epsilon)\bigr).
```

Both bounds charge calls to $`U`$ and $`U^\dagger`$, including calls on branches that report failure. Constants can depend on fixed $`r`$. The algorithm uses the source interface and known dimension directly, with coherent indexed swaps, reversible comparisons and Hadamard gates. A local projector test uses a paired application of $`U^\dagger`$ and $`U`$ around a known operation, which also supplies its controlled form. Separate registers and explicit swaps suffice for routing.

For $`r=2`$, the fixed-error worst-case source-query upper bound is $`O(N^{1/3})`$. It applies pointwise, and thus applies to Haar-source inputs as a special case. Bhateja, Esmaili and Mantri's Proposition 8.2 gives the matching order of lower bound at sufficiently small fixed trace error for Haar inputs. The lower bound applies to a hard query budget. Any uniform expected query bound can be converted into a hard budget by truncation at a constant multiple of that bound, at the cost of a small constant addition to the error. [Bhateja, Esmaili and Mantri, Section 8.2](https://arxiv.org/html/2610.06721v1#S8.SS2)

### Other source interfaces

If the source supplies ordinary forward calls only, the worst-case coherent query law is $`\Theta_{r,\sigma,\varepsilon}(N^{1-1/r})`$ at fixed accuracy and success. The lower bound ranges over compatible unitary completions and holds even for a pair with identical known magnitude profiles. The exact copy-based algorithm gives the matching upper bound. [Forward-only theorem](forward_only.md)

If the source supplies separately budgeted copies and controlled reflections, even inputs with the same collision moment can differ in reflection complexity. The shape of the squared output determines whether retaining only its heaviest coordinates meets the coherent error target. [Profile-dependent reflection theorem](reflection_budget.md)

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

Let $`\omega`$ be the reduced input state on the label. Its entries are $`\omega_{yy'}=\sqrt{p_y p_{y'}}\langle g_{y'}|g_y\rangle`$. Tracing out the selected auxiliary registers leaves the label in the normalized entrywise power

```math
F_r(\omega)=\frac{\omega^{\circ r}}{S_r},\qquad
(\omega^{\circ r})_{yy'}=(\omega_{yy'})^r,
\qquad S_r=\sum_y(\omega_{yy})^r.
```

The matrix elements follow from $`\langle g_{y'}^{\otimes r}|g_y^{\otimes r}\rangle=\langle g_{y'}|g_y\rangle^r`$. Partial trace is contractive in trace distance, so the output label keeps the theorem’s trace-error and query guarantees. Where both input diagonal entries are positive, the relative coherence $`\omega_{yy'}/\sqrt{\omega_{yy}\omega_{y' y'}}`$ is raised to power $`r`$. [Exact extraction from independent mixed copies](https://github.com/GoGoKo699/Quantum-Coherent-Collisions/blob/main/science/mixed_states.md)

Measuring the label produces the law $`p_y^r/S_r`$. The corresponding total-variation bound follows from contractivity under measurement. A caller that always needs a classical output can return an arbitrary label on failure, increasing the error by at most the failure probability. Running the theorem with half the desired tolerance keeps their sum within the desired tolerance.

The theorem provides a heralded state preparation. Its query savings price reversible source calls. Circuit depth, auxiliary space, and the physical costs of realizing those calls enter a separate resource comparison.
