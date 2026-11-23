# Verification

From the repository root, use Python 3.10+ with NumPy.

```bash
python3 -m pip install -r verification/requirements.txt
python3 verification/run_all.py
```

| Check | What is compared |
|---|---|
| Coherent extraction | Routed complex amplitudes and success mass against the factored formula on small tuples with explicit rank labels |
| Spectral filter | The local-projector gap, Hermitian block encoding, polynomial filter and conditional error against direct matrix calculations |
| Matched evaluator | The two tag probabilities against the normalized squared law for a permutation and a two-to-one function |
| Matched magnitude profiles | Collision moment, largest probability and sum of the largest probabilities at the copy budget across the constructed profiles, plus the tail weight of each squared state |
| Forward-only hard pair | Source magnitudes and overlap against the two-state formula, and orthogonality of the normalized powered targets |
| Purification | The reduced output and success probability of the ordered-rank circuit against the normalized entrywise power of the input density matrix and the collision formula |

The deterministic suite runs 73 extraction cases, 7 spectral cases, 2 evaluator cases, 3 magnitude-profile cases, 3 forward hard pairs and 2 purification cases. It includes nonuniform complex inputs and small or zero marked mass. The checks address finite algebra and normalization identities. See the [extraction](../science/extraction.md), [spectral filter](../science/spectral.md), [benchmark](../science/benchmarks.md), [reflection budget](../science/reflection_budget.md), [forward-only access](../science/forward_only.md) and [purification model](../science/model.md#sources-with-additional-registers) for the corresponding arguments and query bounds.
