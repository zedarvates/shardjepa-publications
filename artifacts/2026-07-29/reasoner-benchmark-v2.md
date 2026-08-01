# Reasoner benchmark v2 — 2026-07-29

This evidence record measures both local latency and ranking fidelity for the
bounded Euclidean draft used by `SpeculativeReasoner`.

## Source state

- HEAD before the benchmark changes: `b94646a`
- Worktree: dirty, including the benchmark implementation and fidelity tests
- OS: Windows x86_64
- Benchmark profile: optimized Cargo bench profile
- Raw machine-readable result:
  [`reasoner-benchmark-v2.json`](reasoner-benchmark-v2.json)

The dirty source state means this is development evidence. Exact reproduction
from a repository revision requires committing the implementation first and
rerunning the same command from that revision.

## Command

```powershell
$env:SHARDJEPA_BENCH_OUTPUT = "publications/artifacts/2026-07-29/reasoner-benchmark-v2.json"
rtk cargo bench --bench reasoner_benchmarks
```

## Method

- 20 untimed warm-up iterations per reasoner and candidate count;
- 30 timed samples;
- 20 ranking operations per sample;
- `std::hint::black_box` applied to benchmark inputs and outputs;
- mean, median, population standard deviation, p95, minimum, and maximum stored
  in JSON;
- deterministic fidelity seed `20260729`;
- 100 independently generated query/candidate fixtures per matrix cell;
- Poincare-ball candidate distributions at dimensions 2, 16, and 128;
- speculative draft size `K=10`.

## Timing result

| Candidates | Exact median | Exact p95 | Speculative median | Speculative p95 | Median speedup |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 50 | 32.97 us | 42.38 us | 13.21 us | 16.62 us | 2.49x |
| 200 | 132.31 us | 139.82 us | 23.17 us | 28.57 us | 5.71x |
| 1,000 | 679.30 us | 693.37 us | 81.65 us | 83.83 us | 8.32x |

These are local distributions from one invocation, not cross-machine
performance guarantees.

## Fidelity result

| Dimension | Candidates | Top-1 agreement | Recall@10 |
| ---: | ---: | ---: | ---: |
| 2 | 50 | 100% | 88.9% |
| 2 | 200 | 100% | 89.5% |
| 2 | 1,000 | 100% | 93.6% |
| 16 | 50 | 100% | 87.8% |
| 16 | 200 | 100% | 81.8% |
| 16 | 1,000 | 99% | 74.8% |
| 128 | 50 | 100% | 95.6% |
| 128 | 200 | 100% | 89.7% |
| 128 | 1,000 | 100% | 79.8% |

The matrix found one top-1 disagreement in 900 deterministic trials. A separate
checked counterexample also demonstrates that a bounded Euclidean draft can
exclude the exact Poincare nearest neighbor. The speculative reasoner is
therefore approximate even when top-1 agreement is high on these fixtures.

## Conclusion

The speed result remains promising: median acceleration increased with the
candidate set and reached 8.32x at 1,000 candidates in this run. The quality
result narrows the claim: top-1 agreement was 99-100% in the sampled matrix,
but recall@10 fell as low as 74.8%, and exactness is not guaranteed.

The next comparison should sweep `draft_k`, use released latent distributions,
report confidence intervals across independent invocations, and select a
minimum acceptable fidelity threshold before optimizing further.
