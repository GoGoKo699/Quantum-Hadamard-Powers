# Quantum Hadamard Powers

**How much does reversible access help when squaring unknown quantum amplitudes?** A collision filter and a spectral projection prepare the normalized square of an arbitrary pure state in $`O_\varepsilon(N^{1/3})`$ reversible source queries at fixed trace error. With ordinary forward calls alone, the same coherent task needs $`\Theta(\sqrt{N})`$ queries in the worst case. The preparation algorithm uses the source circuit and its inverse without an amplitude oracle or a collision-moment estimate.

For an input $`|\psi\rangle=\sum_y\alpha_y|y\rangle`$, the successful output approximates

```math
|\psi^{[r]}\rangle=\frac{\sum_y\alpha_y^r|y\rangle}{\sqrt{S_r}},\qquad S_r=\sum_y|\alpha_y|^{2r},\qquad r\geq 2.
```

The output retains the complex phases of the powered amplitudes. The extraction assigns every accepted collision its proper multiplicity so that the selected label factors from the residual samples. A spectral filter increases the weight of this component using local checks on the coherent tuple. The result extends to every fixed integer power $`r`$, with expected query cost $`O_{r,\varepsilon}(S_r^{-1/(r+1)})`$ and hard query budget $`O_{r,\varepsilon}(N^{(r-1)/(r+1)})`$.

| Task | Query result at fixed accuracy |
|---|---|
| Coherent square with reversible preparation | $`\Theta(N^{1/3})`$ in the worst case at sufficiently small fixed trace error |
| Coherent square with ordinary forward preparation | $`\Theta(\sqrt{N})`$ in the worst case over compatible unitary completions |
| Sample the squared law on the matched function-evaluation benchmark | $`\Theta(N^{1/3})`$ quantum and $`\Theta(\sqrt{N})`$ classical |
| Prepare a fixed higher power on a clean input | $`O_{r,\varepsilon}(S_r^{-1/(r+1)})`$ expected reversible queries |

With a separate budget of supplied copies, the cost of controlled reflections can depend on the full magnitude profile. Two profiles can share the collision moment, the largest input probability and the sum of the largest input probabilities up to the copy budget, yet have different asymptotic reflection costs. [Copy and reflection budgets](science/reflection_budget.md)

For independent copies and exact collision extraction, see the sister project [Quantum Coherent Collisions](https://github.com/GoGoKo699/Quantum-Coherent-Collisions). Its [mixed-copy algorithm](https://github.com/GoGoKo699/Quantum-Coherent-Collisions/blob/main/science/mixed_states.md) uses the same ordered mark. With reversible access to a purification, Hadamard Powers prepares the same normalized mixed-state power on the output label. [Purification access](science/model.md#sources-with-additional-registers)

## Run the coherent power circuit

1. **Prepare a fresh tuple and rank.** At each scheduled dyadic batch size, apply the supplied source circuit `U` to zero in every slot. Use Hadamards to prepare a uniform rank register. Compute a reversible flag for whether the rank selects `r` equal-label positions whose removal leaves each residual multiplicity below `r`. Keep the rank and label registers coherent. [Rank and mark](science/extraction.md#mark-a-valid-choice-of-positions)
2. **Filter the tuple.** To test a selected slot, route it to the source port, apply `U†`, flip a signal bit on a nonzero port, apply `U` and undo the routing. For the rank test, undo the rank Hadamards, flip the signal on nonzero rank, and restore the Hadamards. Use the collision flag to control the tilt-register Hadamards and uncompute the flag after each controlled operation. The [clock circuit](science/spectral.md#filter-the-eigenvalue-one-component) averages controlled steps and accepts only zero clock and clean signal ancillas. After the required repetitions, measure the collision flag. On a failed test, discard the attempt and continue the [dyadic schedule](science/spectral.md#find-a-useful-scale-without-knowing-the-moment). The paired `U†` and `U` calls are unconditional within each source selection. They cancel when the known flip is disabled, and both calls are charged.
3. **Return the powered register.** On success, route the selected slots forward and erase the rank by recomputing it from the tuple and chosen positions. Clear duplicate label registers and discard the position list and residual. Return the surviving label without reading it. For a purification, test and route the complete source slots, compute collision eligibility on labels alone, and trace out the selected auxiliary registers to obtain the mixed-state power. [Routing and cleanup](science/extraction.md#factor-the-ideal-marked-vector)

With [ordinary forward-only access](science/forward_only.md), use `U` on zero to supply copies to the ordered filter and its pilot, with no spectral step. With [native copies and paid controlled reflections](science/reflection_budget.md#broad-and-flat-constructions), use reflection calls for the local source tests and choose the tilt from the known profile for the flat and broad-tail constructions. The [diffuse-tail construction](science/reflection_budget.md#diffuse-tail-converse-and-construction) amplifies onto the two known heavy labels and then applies coherent equality. Its approximation discards the small powered tail. Count all consumed copies and controlled reflections in their respective budgets.

## Read the science

Start with the [model and guarantees](science/model.md). The [collision extraction](science/extraction.md) explains how the powered state factors without measuring its label. The [spectral filter](science/spectral.md) gives the oracle circuit, error bound and schedule for an unknown moment. The [benchmarks](science/benchmarks.md) derive the matched classical comparison. The [resource account](science/resources.md) prices the known gates, workspace and calls to the inverse source.

The [forward-only result](science/forward_only.md) gives the sharp ordinary-query law for every fixed power. The [reflection-budget result](science/reflection_budget.md) gives matching bounds for specified known profiles when copies and controlled reflections are charged separately.

The [related-work account](references/RELATED_WORK.md) credits the earlier exact copy-based filter and compares the query result with prior collision sampling, coherent Hadamard products and nonlinear amplitude transformations.

## Learn the project

The shared educational anchor is Ronald de Wolf’s *Quantum Computing: Lecture Notes*. The [learning bridge](learning/QUANTUM_WALK_BRIDGE.md) connects its tools to the extraction and spectral filter. The [30 milestones](learning/MILESTONES.md) cover the results under each source interface. The [LLM guide](llms.txt) maps questions to the relevant sources.

## Reproduce the finite checks

Run from the repository root. See the [verification guide](verification/README.md) for the expected output and the scope of each check.

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

## Scope

The coherent result is a heralded state preparation. The matched classical comparison uses the same evaluator interface on both sides and concerns the measured output law. The reversible count charges both directions of the source circuit. Tuple routing and reversible occupancy checks add known gates, so circuit costs also depend on the cost of implementing the source.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
