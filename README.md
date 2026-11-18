# Quantum Hadamard Powers

**How many calls to a state-preparation circuit are needed to square its unknown amplitudes coherently?** A collision filter and a spectral projection prepare the normalized square of an arbitrary quantum state in $`O_\varepsilon(N^{1/3})`$ source queries at fixed trace error. The algorithm uses the preparation circuit and its inverse. It does not need an oracle for the amplitudes or a collision-moment estimate.

For an input $`|\psi\rangle=\sum_y\alpha_y|y\rangle`$, the successful output approximates

```math
|\psi^{[r]}\rangle=\frac{\sum_y\alpha_y^r|y\rangle}{\sqrt{S_r}},\qquad S_r=\sum_y|\alpha_y|^{2r},\qquad r\geq 2.
```

The output retains the complex phases of the powered amplitudes. The extraction assigns every accepted collision its proper multiplicity so that the selected label factors from the residual samples. A spectral filter increases the weight of this component using local checks on the coherent tuple. The result extends to every fixed integer power $`r`$, with expected query cost $`O_{r,\varepsilon}(S_r^{-1/(r+1)})`$ and hard query budget $`O_{r,\varepsilon}(N^{(r-1)/(r+1)})`$.

| Task | Query result at fixed accuracy |
|---|---|
| Coherent Hadamard square on an arbitrary clean input | $`O(N^{1/3})`$ quantum, with an existing $`\Omega(N^{1/3})`$ lower bound on Haar inputs |
| Sample the squared law on the matched function-evaluation benchmark | $`\Theta(N^{1/3})`$ quantum and $`\Theta(\sqrt{N})`$ classical |
| Prepare a fixed higher power on a clean input | $`O_{r,\varepsilon}(S_r^{-1/(r+1)})`$ expected quantum queries |

## Read the science

Start with the [model and guarantees](science/model.md). The [collision extraction](science/extraction.md) explains how the powered state factors without measuring its label. The [spectral filter](science/spectral.md) gives the oracle circuit, error bound and schedule for an unknown moment. The [benchmarks](science/benchmarks.md) derive the matched classical comparison. The [resource account](science/resources.md) prices the known gates, workspace and calls to the inverse source.

The [related-work account](references/RELATED_WORK.md) credits the earlier exact copy-based filter and compares the query result with prior collision sampling, coherent Hadamard products and nonlinear amplitude transformations.

## Learn the project

The educational anchor is Magniez, Nayak, Roland and Santha’s *Search via Quantum Walk*. The [quantum walk bridge](learning/QUANTUM_WALK_BRIDGE.md) connects its eigenphase and projection tools to this construction. The [30 milestones](learning/MILESTONES.md) take you from state-preparation access through the upper and lower bounds. The [LLM guide](llms.txt) maps questions to the relevant sources.

## Reproduce the finite checks

Run from the repository root. See the [verification guide](verification/README.md) for the expected output and the scope of each check.

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

## Scope

The coherent result is a heralded state preparation. The matched classical comparison concerns the measured output law and uses the same evaluator access on both sides. The query counts charge both directions of the state-preparation circuit. Tuple routing and reversible occupancy checks add known gates, so circuit costs depend on the price of the source and its inverse.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
