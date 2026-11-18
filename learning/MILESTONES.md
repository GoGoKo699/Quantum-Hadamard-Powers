# Project understanding map

These 30 milestones follow the route from a reversible source to a coherent state with powered amplitudes. The first 12 develop the objects and interfaces that define the problem. The remaining 18 follow the collision extraction, spectral algorithm, query bounds and circuit costs. The [quantum walk bridge](QUANTUM_WALK_BRIDGE.md) identifies the relevant material from one educational anchor and works through a three-copy example.

## Route through the project

| Milestones | Understanding gained |
|---|---|
| [M01](#m01-computational-basis-amplitudes)–[M06](#m06-residual-occupancy) | The target state, source access and collision statistics |
| [M07](#m07-product-projectors-and-gaps)–[M12](#m12-the-operational-question) | Product spectra, phase detection and the operational question |
| [M13](#m13-valid-subsets-of-positions)–[M17](#m17-a-collision-scale-for-copies) | Exact coherent extraction and the copy scale |
| [M18](#m18-tilt-the-marked-component)–[M22](#m22-accuracy-after-postselection) | How a tilted spectral filter accesses the same output |
| [M23](#m23-the-balanced-batch-size)–[M25](#m25-expected-and-hard-query-budgets) | Balancing and finding the useful batch size |
| [M26](#m26-the-haar-square-lower-bound)–[M30](#m30-the-complete-algorithm-and-its-scope) | Optimality, matched benchmarks, and implementation scope |

## Phase I — Background and preliminaries


### M01 Computational-basis amplitudes

**Central question.** What does the source prepare, and what is visible in a computational-basis sample?

**Understanding target.** Read $`|\psi\rangle=\sum_y\alpha_y|y\rangle`$ as a unit vector. Connect the sample distribution to $`p_y=|\alpha_y|^2`$ and relative phase to interference.

**Prerequisites.** This is the starting point.

**Conceptual connection.** Use two states with the same label probabilities and different phases to explain why their sampled labels alone cannot specify the coherent output.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Three-copy example](QUANTUM_WALK_BRIDGE.md#follow-a-three-copy-example)


### M02 The normalized Hadamard power

**Central question.** How can amplitudes be raised to a power and still define a state?

**Understanding target.** Explain the normalization $`S_r=\sum_y p_y^r`$ and the target amplitudes $`\alpha_y^r/\sqrt{S_r}`$ for an integer $`r\ge 2`$. Compute the target label law $`p_y^r/S_r`$.

**Prerequisites.** [M01](#m01-computational-basis-amplitudes).

**Conceptual connection.** Raising an amplitude to a power changes its magnitude and multiplies its phase angle. The coherent target carries both changes, and its measurement retains the new magnitudes.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Three-copy example](QUANTUM_WALK_BRIDGE.md#follow-a-three-copy-example)


### M03 Reversible source access

**Central question.** Which operations does the algorithm receive from the source?

**Understanding target.** Distinguish a call to prepare $`U|0\rangle`$, a call to $`U^\dagger`$, a stored copy and a classical sample. Account for each use of either source direction.

**Prerequisites.** [M01](#m01-computational-basis-amplitudes).

**Conceptual connection.** Conjugating a known zero-state test by $`U`$ implements a test for the prepared state. This is the operation that coherence and reversibility add.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Resource accounting](../science/resources.md)


### M04 A flag without reading the label

**Central question.** How can an algorithm check whether two labels agree while keeping the answer in superposition?

**Understanding target.** Distinguish a reversible equality flag from measurement of either label. Explain what projecting onto a flag means and when the surviving target can be pure.

**Prerequisites.** [M01](#m01-computational-basis-amplitudes), [M03](#m03-reversible-source-access).

**Conceptual connection.** An agreement flag can keep contributions for all labels coherent. Reversible routing must also remove records that would distinguish the surviving labels.

**Canonical sources.** [Coherent extraction](../science/extraction.md) · [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading)


### M05 Occupations and collision moments

**Central question.** Why does the same moment occur in both normalization and an agreement probability?

**Understanding target.** Reason from independent coordinates to the probability $`S_r`$ that a specified $`r`$ of them agree. Identify how occupation counts summarize the equality pattern of a tuple.

**Prerequisites.** [M01](#m01-computational-basis-amplitudes), [M02](#m02-the-normalized-hadamard-power).

**Conceptual connection.** Use the collision probability to predict why elementary equality postselection can be rare on a broad distribution. The normalization of the desired state already tells us that cost.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Coherent extraction](../science/extraction.md)


### M06 Residual occupancy

**Central question.** What should be required of the registers left after a set of matching positions is removed?

**Understanding target.** Describe a residual with all multiplicities below $`r`$ and explain how a union bound over residual position sets guarantees a useful probability for a sufficiently short tuple.

**Prerequisites.** [M04](#m04-a-flag-without-reading-the-label), [M05](#m05-occupations-and-collision-moments).

**Conceptual connection.** The remaining registers must obey a condition that is independent of the selected label. This condition allows the output factor to survive discarding those registers.

**Canonical sources.** [Coherent extraction](../science/extraction.md) · [Three-copy example](QUANTUM_WALK_BRIDGE.md#follow-a-three-copy-example)


### M07 Product projectors and gaps

**Central question.** What does a sum of commuting register tests reveal about a product state?

**Understanding target.** Explain why the product of the specified register states is the only vector that passes all the local tests, and how one failed test produces a gap of order $`1/t`$ in their average.

**Prerequisites.** [M03](#m03-reversible-source-access).

**Conceptual connection.** A coherent index can select one local test at a time. The spectrum of their average records the all-pass state without requiring a walk step to retest every slot separately.

**Canonical sources.** [Spectral algorithm](../science/spectral.md)


### M08 Eigenvalues become eigenphases

**Central question.** Why can a unitary walk make an operator's small gap easier to distinguish?

**Understanding target.** Connect the real eigenvalues of a Hermitian block to walk phases. Near one, explain why an eigenvalue deficit comparable to $`\Delta`$ produces a phase on the order of $`\sqrt{\Delta}`$.

**Prerequisites.** [M07](#m07-product-projectors-and-gaps).

**Conceptual connection.** Identify the invariant subspace reached by the prepared signal state. Phase-zero eigenvectors outside that subspace do not contribute to its filter.

**Canonical sources.** [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading) · [Spectral algorithm](../science/spectral.md)


### M09 A finite zero-phase test

**Central question.** How does a finite window of controlled powers select an eigenphase?

**Understanding target.** Explain why amplitudes from different powers add with the same sign for eigenphase zero and can cancel for separated nonzero phases.

**Prerequisites.** [M08](#m08-eigenvalues-become-eigenphases).

**Conceptual connection.** Relate window length to the inverse phase gap and repeated clean-filter rounds to stronger suppression. Heralding the clean signal makes the filter an operation on the retained state.

**Canonical sources.** [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading) · [Spectral algorithm](../science/spectral.md)


### M10 Setup update and checking

**Central question.** Which operations should be priced before comparing algorithms?

**Understanding target.** Separate preparation of a full batch, selecting a local source test, computing the known collision predicate and reading the flag. Distinguish their query, gate and space costs.

**Prerequisites.** [M03](#m03-reversible-source-access), [M04](#m04-a-flag-without-reading-the-label), [M07](#m07-product-projectors-and-gaps), [M09](#m09-a-finite-zero-phase-test).

**Conceptual connection.** Reusing a batch can reduce the number of expensive source calls while still requiring work on many registers at each coherent indexed step.

**Canonical sources.** [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading) · [Resource accounting](../science/resources.md)


### M11 Fair query comparisons

**Central question.** When does a classical–quantum query comparison use matched access?

**Understanding target.** Check that both algorithms query the same underlying evaluator and solve the same classical output task at the same error scale. Distinguish this from a quantum-state preparation comparison.

**Prerequisites.** [M02](#m02-the-normalized-hadamard-power), [M03](#m03-reversible-source-access), [M10](#m10-setup-update-and-checking).

**Conceptual connection.** A lower bound for generating labels under matched access does not answer every question about a coherent state. Classical query baselines are also sensitive to free samples or extra oracle access.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Benchmarks](../science/benchmarks.md)


### M12 The operational question

**Central question.** What would an end-to-end solution need to establish?

**Understanding target.** Combine the output specification, reversible input interface, flag, trace error and source query budget. Identify separately the proof obligations for the output direction and the cost of reaching it.

**Prerequisites.** [M02](#m02-the-normalized-hadamard-power), [M04](#m04-a-flag-without-reading-the-label), [M06](#m06-residual-occupancy), [M07](#m07-product-projectors-and-gaps), [M09](#m09-a-finite-zero-phase-test), [M10](#m10-setup-update-and-checking), [M11](#m11-fair-query-comparisons).

**Conceptual connection.** The project needs a collision operation that isolates the right quantum state and a spectral algorithm that reaches its marked component efficiently.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading)


## Phase II — Narrative and innovation


### M13 Valid subsets of positions

**Central question.** What does it mean for a particular collision inside a tuple to be valid?

**Understanding target.** Check that the selected positions agree and that removal of those positions leaves no $`r`$-fold repetition. Relate validity to one exceptional label with occupancy between $`r`$ and $`2r-1`$.

**Prerequisites.** [M05](#m05-occupations-and-collision-moments), [M06](#m06-residual-occupancy), [M12](#m12-the-operational-question).

**Conceptual connection.** For a triple of identical labels in the square case, three different position pairs can be valid. Their multiplicity matters even though they represent the same output label.

**Canonical sources.** [Coherent extraction](../science/extraction.md) · [Three-copy example](QUANTUM_WALK_BRIDGE.md#follow-a-three-copy-example)


### M14 Multiplicity through ranks

**Central question.** How can several valid subsets receive their proper weight?

**Understanding target.** Use a known uniform rank register to give equal amplitude to a tuple's valid subset ranks. Explain why a fixed bounded rank range suffices for fixed $`r`$.

**Prerequisites.** [M04](#m04-a-flag-without-reading-the-label), [M13](#m13-valid-subsets-of-positions).

**Conceptual connection.** Keeping only a preferred collision would eliminate valid position choices. Equal-amplitude ranks allow the subsequent reindexing to have the same coefficient for each designated subset.

**Canonical sources.** [Coherent extraction](../science/extraction.md) · [Three-copy example](QUANTUM_WALK_BRIDGE.md#follow-a-three-copy-example)


### M15 Extracting one coherent label

**Central question.** Why can the residual registers be discarded after successful extraction?

**Understanding target.** Trace the reversible route from tuple and valid rank to the selected positions, residual tuple and surviving label. Factor the surviving label's amplitude from the residual amplitude.

**Prerequisites.** [M02](#m02-the-normalized-hadamard-power), [M06](#m06-residual-occupancy), [M13](#m13-valid-subsets-of-positions), [M14](#m14-multiplicity-through-ranks).

**Conceptual connection.** Clearing the duplicate labels and scratch records ensures the remaining registers do not encode the output label. This preserves the powered relative phases.

**Canonical sources.** [Coherent extraction](../science/extraction.md) · [Three-copy example](QUANTUM_WALK_BRIDGE.md#follow-a-three-copy-example)


### M16 Exact marked mass

**Central question.** How often would the marked state be obtained without a phase filter?

**Understanding target.** Derive the marked probability as the number of position subsets times the probability for one equal subset and a valid residual, divided by the rank range.

**Prerequisites.** [M05](#m05-occupations-and-collision-moments), [M06](#m06-residual-occupancy), [M14](#m14-multiplicity-through-ranks), [M15](#m15-extracting-one-coherent-label).

**Conceptual connection.** This calculation counts the amplitude weight before spectral processing. It determines a useful regime even though the ideal marked output direction is exact for every successful batch.

**Canonical sources.** [Coherent extraction](../science/extraction.md)


### M17 A collision scale for copies

**Central question.** What can repeated direct attempts achieve if only copies are available?

**Understanding target.** Balance the number of position subsets against the moment to see where a batch can succeed with constant probability. Compare the resulting batch size with single-collision repetition.

**Prerequisites.** [M12](#m12-the-operational-question), [M16](#m16-exact-marked-mass).

**Conceptual connection.** The exact extraction mechanism is already useful without inverse-source calls. Its copy scale gives a reference for the improvement from spectral access.

**Canonical sources.** [Coherent extraction](../science/extraction.md) · [Benchmarks](../science/benchmarks.md)


### M18 Tilt the marked component

**Central question.** How can a change of operator increase the weight of the desired component?

**Understanding target.** Explain why $`THT`$ has a ground state proportional to $`T^{-1}|\Phi\rangle`$ when $`H|\Phi\rangle=0`$. Identify which part of the state receives the factor $`1/\sqrt c`$.

**Prerequisites.** [M07](#m07-product-projectors-and-gaps), [M12](#m12-the-operational-question), [M15](#m15-extracting-one-coherent-label), [M16](#m16-exact-marked-mass).

**Conceptual connection.** The tilt changes probability weight and leaves the direction of the marked component intact. This preserves the label-state proof from extraction.

**Canonical sources.** [Spectral algorithm](../science/spectral.md) · [Phase-filter bridge](QUANTUM_WALK_BRIDGE.md#connect-the-phase-filter-to-the-output)


### M19 The gap survives the tilt

**Central question.** What bounds the spectral cost of making the marked component larger?

**Understanding target.** Relate the nonzero spectrum of $`THT`$ to that of $`H^{1/2}T^2H^{1/2}`$ and use $`T^2\ge cI`$ to explain the lower bound on the gap.

**Prerequisites.** [M07](#m07-product-projectors-and-gaps), [M08](#m08-eigenvalues-become-eigenphases), [M18](#m18-tilt-the-marked-component).

**Conceptual connection.** Choosing a smaller $`c`$ can improve the marked weight and reduce the guaranteed separation from the rest of the spectrum. The algorithm must price both effects.

**Canonical sources.** [Spectral algorithm](../science/spectral.md)


### M20 One selected test per query step

**Central question.** How can the tilted operator be encoded using inexpensive source calls?

**Understanding target.** Route a coherently indexed register through the same source port. Use a conjugated zero test to realize the selected projector and a known flag to incorporate the tilt.

**Prerequisites.** [M03](#m03-reversible-source-access), [M07](#m07-product-projectors-and-gaps), [M10](#m10-setup-update-and-checking), [M18](#m18-tilt-the-marked-component), [M19](#m19-the-gap-survives-the-tilt).

**Conceptual connection.** Two source calls cancel on the disabled control branch. This supplies controlled walk steps without taking availability of a controlled unknown oracle as an extra input.

**Canonical sources.** [Spectral algorithm](../science/spectral.md) · [Resource accounting](../science/resources.md)


### M21 Filtering the tilted ground state

**Central question.** Which component survives the clean signal and zero-phase checks?

**Understanding target.** Identify the ground state with eigenphase zero and explain how the finite filter suppresses its orthogonal components. Connect the final collision flag to the desired marked direction.

**Prerequisites.** [M08](#m08-eigenvalues-become-eigenphases), [M09](#m09-a-finite-zero-phase-test), [M18](#m18-tilt-the-marked-component), [M19](#m19-the-gap-survives-the-tilt), [M20](#m20-one-selected-test-per-query-step).

**Conceptual connection.** The anchor's walk phase detection motivates the filter. Here the tilted state is the intermediate target and projecting it produces the desired powered state.

**Canonical sources.** [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading) · [Spectral algorithm](../science/spectral.md)


### M22 Accuracy after postselection

**Central question.** Why must error be compared with the size of the successful amplitude?

**Understanding target.** Distinguish error on the unnormalized filtered vector from trace error after heralding. Explain how a relative bound controls conditional error even at early stages with small marked weight.

**Prerequisites.** [M16](#m16-exact-marked-mass), [M18](#m18-tilt-the-marked-component), [M21](#m21-filtering-the-tilted-ground-state).

**Conceptual connection.** Without relative control, a small unwanted amplitude might dominate a rare accepted branch. The proof compares the unwanted and wanted parts after accounting for the marked mass.

**Canonical sources.** [Spectral algorithm](../science/spectral.md)


### M23 The balanced batch size

**Central question.** Where do the number of copies and the price of filtering balance?

**Understanding target.** Combine the mark scale $`t^r S_r`$ with the tilt scale $`1/t`$ to obtain $`t\asymp S_r^{-1/(r+1)}`$. Connect this batch size to the source calls needed to resolve the walk phase gap.

**Prerequisites.** [M16](#m16-exact-marked-mass), [M18](#m18-tilt-the-marked-component), [M19](#m19-the-gap-survives-the-tilt), [M20](#m20-one-selected-test-per-query-step), [M21](#m21-filtering-the-tilted-ground-state).

**Conceptual connection.** The extra power of $`t`$ in the balance comes from tolerating a marked weight of order $`1/t`$. This is why the batch can be shorter than a copy-only collision batch.

**Canonical sources.** [Spectral algorithm](../science/spectral.md) · [Phase-filter bridge](QUANTUM_WALK_BRIDGE.md#connect-the-phase-filter-to-the-output)


### M24 Searching the scales

**Central question.** How can the algorithm find a useful batch size when the moment is unknown?

**Understanding target.** Explain the increasing dyadic caps and the retesting of previous batch sizes. Use the relative error guarantee to justify accepting a successful early attempt.

**Prerequisites.** [M12](#m12-the-operational-question), [M22](#m22-accuracy-after-postselection), [M23](#m23-the-balanced-batch-size).

**Conceptual connection.** Different scales change the flag probability while sharing one ideal marked output. Retesting a useful scale gives repeated chances to finish even if much larger batches have poor marked weight.

**Canonical sources.** [Spectral algorithm](../science/spectral.md) · [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading)


### M25 Expected and hard query budgets

**Central question.** Why do the two query bounds depend on different pieces of information?

**Understanding target.** Relate the expected cost to the first useful batch size and the largest allowed cost to $`S_r\ge N^{1-r}`$. Explain how geometric survival controls the sum of costs after the useful scale.

**Prerequisites.** [M10](#m10-setup-update-and-checking), [M23](#m23-the-balanced-batch-size), [M24](#m24-searching-the-scales).

**Conceptual connection.** The instance can finish early when collisions are frequent. The dimension cap still gives a worst-case query limit and allows a failure flag.

**Canonical sources.** [Spectral algorithm](../science/spectral.md) · [Model and guarantees](../science/model.md)


### M26 The Haar square lower bound

**Central question.** What is known to be optimal for coherent squaring?

**Understanding target.** Interpret the lower bound for Haar inputs alongside an upper bound that holds for each input. For fixed trace error, connect these to the matching exponent for the worst-case number of queries.

**Prerequisites.** [M02](#m02-the-normalized-hadamard-power), [M11](#m11-fair-query-comparisons), [M25](#m25-expected-and-hard-query-budgets).

**Conceptual connection.** Squaring is the case with a matching coherent exponent. The construction gives an upper bound for other fixed powers and leaves their sharp lower bounds open.

**Canonical sources.** [Benchmarks](../science/benchmarks.md) · [Model and guarantees](../science/model.md)


### M27 The shared evaluator comparison

**Central question.** How can one sampled label reveal a promise about a hidden function?

**Understanding target.** Trace the tagged construction that gives one branch known occupancies and the other branch an unknown one-to-one or two-to-one evaluator. Relate the resulting tag probabilities to the matched lower bounds.

**Prerequisites.** [M02](#m02-the-normalized-hadamard-power), [M11](#m11-fair-query-comparisons), [M16](#m16-exact-marked-mass), [M25](#m25-expected-and-hard-query-budgets).

**Conceptual connection.** The tag has different probability under the two normalized squared laws, yielding a decision procedure from a sampling procedure. This compares the same classical output under shared evaluator access.

**Canonical sources.** [Benchmarks](../science/benchmarks.md)


### M28 Pricing the circuit

**Central question.** What needs to be charged beyond the oracle calls?

**Understanding target.** Account for workspace, slot routing, occupancy computation, phase control and the inverse-state circuit. Identify when a costly source leaves room for savings and when known gates can dominate.

**Prerequisites.** [M10](#m10-setup-update-and-checking), [M20](#m20-one-selected-test-per-query-step), [M23](#m23-the-balanced-batch-size), [M25](#m25-expected-and-hard-query-budgets).

**Conceptual connection.** Each coherent selected test can use few oracle calls while still moving across many registers. This connects the abstract exponent to the real cost model.

**Canonical sources.** [Resource accounting](../science/resources.md) · [Targeted anchor reading](QUANTUM_WALK_BRIDGE.md#targeted-reading)


### M29 Garbage and the measured law

**Central question.** What can still be output when a sampler keeps a hidden register?

**Understanding target.** Track the garbage associated with each selected label. Explain why discarding it preserves the intended label law while it can remove coherence from the surviving quantum register.

**Prerequisites.** [M01](#m01-computational-basis-amplitudes), [M04](#m04-a-flag-without-reading-the-label), [M15](#m15-extracting-one-coherent-label), [M27](#m27-the-shared-evaluator-comparison).

**Conceptual connection.** The evaluator benchmark can use a source with retained addresses. The clean coherent theorem requires the output to carry the powered amplitudes themselves.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Coherent extraction](../science/extraction.md) · [Benchmarks](../science/benchmarks.md)


### M30 The complete algorithm and its scope

**Central question.** How do the extraction, spectral algorithm and comparisons combine into one result?

**Understanding target.** Explain the route from input to heralded output and relate phase preservation, the moment-dependent cost, the optimal square exponent and the matched measured-law separation.

**Prerequisites.** [M12](#m12-the-operational-question), [M15](#m15-extracting-one-coherent-label), [M21](#m21-filtering-the-tilted-ground-state), [M24](#m24-searching-the-scales), [M25](#m25-expected-and-hard-query-budgets), [M26](#m26-the-haar-square-lower-bound), [M27](#m27-the-shared-evaluator-comparison), [M28](#m28-pricing-the-circuit), [M29](#m29-garbage-and-the-measured-law).

**Conceptual connection.** Use the interface and error guarantee to decide which statement applies to a new task. Separate the coherent proof, measured-law comparison, and circuit cost before drawing conclusions about an application.

**Canonical sources.** [Model and guarantees](../science/model.md) · [Spectral algorithm](../science/spectral.md) · [Benchmarks](../science/benchmarks.md) · [Resource accounting](../science/resources.md)
