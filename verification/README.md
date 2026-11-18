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

The deterministic suite runs 73 extraction cases, 7 spectral cases and 2 evaluator cases. It includes nonuniform complex inputs and small or zero marked mass. The analytic claims and asymptotic bounds are proved in the [extraction](../science/extraction.md), [spectral filter](../science/spectral.md) and [benchmark](../science/benchmarks.md) chapters. The finite checks target the algebra and normalization steps used in those proofs.
