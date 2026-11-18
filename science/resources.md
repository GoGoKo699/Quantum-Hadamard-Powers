# Circuit resources

Let $`t`$ be a dyadic batch size, $`w_y=\lceil\log_2 N\rceil`$ the label width and $`w`$ the full source width. The full width includes any source garbage. Use one reversible source port and $`t`$ sample registers. The counts below charge both $`U`$ and $`U^\dagger`$ regardless of any coherent control in the known part of the circuit.

## Source calls and routing

The local-projector average uses a $`2t`$-address coin. There are $`t`$ addresses for the sample registers, one for the rank register and $`t-1`$ identity addresses. For a sample address $`j`$, swap register $`j`$ into the port, apply $`U^\dagger`$, flip a signal on the complement of the known reset state, apply $`U`$ and undo the swap. This block is a coherent test for the prepared state. The inverse pair is unconditional, including on branches for the rank, identity, tilt or phase-clock controls. Turn off the known source test on those branches. The unconditional inverse and forward source calls then cancel. The rank branch performs its own known test for the uniform rank state. A controlled qubiterate therefore uses one $`U`$ and one $`U^\dagger`$ and requires control of the known gates only.

One explicit router uses the first sample register as the port. For each of the other $`t-1`$ addresses, compute equality of the coin with that address, conditionally swap its $`w`$ qubits with the port and uncompute equality. Undo this network after the source test. The two routing passes use $`2(t-1)w`$ bitwise controlled swaps and $`O(t\log t)`$ gates for the known address tests. The router may run on both branches of the outer control because its forward and reverse passes cancel whenever the source test is inactive. This circuit uses no memory primitive or implicitly free indexed access.

In one phase-filter round with $`L`$ clock values, controlled powers of the qubiterate use $`L-1`$ steps. The binary clock bit of weight $`2^j`$ controls $`2^j`$ consecutive steps, which gives this count when summed over its bits. A complete batch of $`J`$ filter rounds uses at most $`t+J(L-1)`$ calls to $`U`$ and $`J(L-1)`$ calls to $`U^\dagger`$. The subsequent test and extraction use known gates only. A failed round can abort its batch and save the remaining operations. An attempted batch still costs the calls executed before failure.

## Known gates and workspace

For a concrete mark circuit, sort $`(\text{label},\text{original position})`$ pairs using a reversible bitonic network. Keep one comparison decision per comparator so the sorting can be undone after computing the mark. The $`t=2^a`$ network has $`t a(a+1)/4`$ comparators. Comparing and conditionally exchanging a pair costs $`O(w_y+\log t)`$ gates with reversible comparison scratch. After sorting, scan the runs of identical labels. The predicate needs exactly one run of length between $`r`$ and $`2r-1`$, with its rank index below the number of admissible $`r`$-subsets of that run. Reversible counters use $`O(\log t)`$ bits and their histories may be retained until the inverse scan. The rank check itself acts on a set of bounded size for fixed $`r`$. Compute the mark, use it and reverse the scan and sorting.

The marked branch of the tilt preparation applies Hadamards to a $`\log_2 t`$-qubit register, which has clean-state amplitude $`1/\sqrt t`$. The unmarked branch acts identically on that register. Select the local-projector block only when the tilt register is zero and uncompute the tilt preparation after selection. This realizes the $`c=1/t`$ coefficient without synthesizing a variable rotation. The outer clock, local coin and rank register also use exact uniform states of power-of-two sizes. The remaining exact known gates can be built from Boolean reversible gates, Hadamards and fixed controlled versions of those gates.

The extraction run records original selected positions before reversing the sort and removes the rank by its inverse ranking map. Then a fixed sequence of conditional adjacent swaps moves the selected positions to the front in order. One sweep of $`O(t)`$ swaps suffices per selected position for fixed $`r`$. The remaining registers keep their relative order. Bitwise XOR clears the duplicated labels. Source garbage travels with its original sample register, but marking and comparison act only on labels. The circuit erases the rank and sorting records before discarding the retained position and residual registers.

For $`t\geq2`$, write $`B(t)=w+\log^2t\,(w_y+\log t)`$. The following are conservative circuit counts with unconditional source calls and individually available controlled swaps and reversible binary gates.

| Resource | Bound |
| --- | --- |
| Known gates per qubiterate | $`O_r(t B(t))`$ |
| Known gates per complete batch | $`O_r(J t^2 B(t))`$ with $`L=8t`$ |
| Peak working width | $`O(t w+t\log^2 t)`$, plus internal workspace of the source implementation |
| Conservative serial depth per complete batch | $`O_r(J t^2 B(t)+J t(D_U+D_{U^\dagger}))`$, where $`D_U`$ and $`D_{U^\dagger}`$ are the source depths |

The width includes the tuple, comparison histories, position tags, reusable comparator scratch and the phase clock. Bitonic network layers can be parallelized at a cost in comparator scratch. The table counts a single complete batch. Retesting smaller dyadic sizes at a cap costs only a constant-factor increase in the fixed-error gate bound at that cap, because the early-stage terms form a geometric sum. Over the random stopping cap, the tail bound controls the expected gate count as well as the expected query count. In particular, if the probability of missing the successful-size trial at a cap is at most $`1/8`$, the $`t^2`$ factor grows by four per doubling while the survival probability falls by eight. The extra constant repetitions needed for that choice leave the query exponent unchanged.

## When a query saving can reduce total gates

Let $`C_{\mathrm{src}}`$ denote the total gate count of one forward and one inverse source operation. For a fixed error budget, the balanced square batch scale is $`t\asymp S_2^{-1/3}`$. The gate model above bounds its cost, including attempts, by

```math
O\bigl(t C_{\mathrm{src}}+t^2 B(t)\bigr).
```

A direct square by equality amplitude amplification starts with two source slots. The good amplitude is $`\sqrt{S_2}`$, so at small $`S_2`$ the standard Grover rotation takes $`\Theta(S_2^{-1/2})=\Theta(t^{3/2})`$ steps for constant success. Each step reflects about the two-slot product state and about label equality. The product-state reflection applies the source and its inverse on both slots. Its corresponding budget is $`O(t^{3/2}(C_{\mathrm{src}}+w_y))`$. For these explicit constructions, the spectral route has the smaller asymptotic gate budget if $`C_{\mathrm{src}}\gg \sqrt t\,B(t)`$. In that regime the routing and predicate overhead is smaller than even the direct algorithm's leading source bill, while the spectral source bill uses fewer calls. This comparison uses a serial gate-count model with the two source costs charged in the same units. When the source is cheap, the known-gate term can dominate. The measured-law comparison with classical evaluation is a query comparison and does not imply a quantum-to-classical clock-time advantage.

## A finite accounting example

Take a clean $`N=16`$ source with flat magnitudes and arbitrary phases, $`r=2`$, and one batch with $`t=4`$. Then $`w=4`$, the rank has four values, and $`S_2=1/16`$. The initial good probability is

```math
\mu=\frac{\binom 42\,(1/16)\,(15/16)}4=\frac{45}{512}.
```

For this batch the tilt has $`c=1/4`$ and the clock has $`L=32`$ values. Four filter rounds use at most $`4+2\cdot4\cdot31=252`$ source calls and $`2\cdot3\cdot4\cdot4\cdot31=2976`$ bitwise controlled swaps for slot routing. The swap count covers routing only. Reversible marking and the other known gates are additional. The ideal marked component after ground-space projection has norm about $`0.51045`$. The initial excited norm is about $`0.25187`$ and four rounds reduce it by a factor at most $`4^{-4}`$. Thus the first full attempt succeeds with probability at least $`0.2595`$ and gives trace error below $`0.004`$ conditional on success, using the norm bound for normalization in the spectral proof. Repetitions to reach a required overall success probability are additional. These counts illustrate the conservative filter circuit at a small input size, where a direct equality circuit can be cheaper.
