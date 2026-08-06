# Reasoner draft-size acceptance sweep — 2026-08-06

Evidence class: **Measured development snapshot**.

This experiment tests whether one fixed Euclidean draft size can preserve a
minimum Poincare-ranking fidelity while remaining faster than exhaustive
ranking across the tested candidate counts.

## Source state

- Source commit: `b94646a`
- Source state: dirty worktree with concurrent modified and untracked work
- OS and architecture: Windows x86_64
- Raw result:
  [`reasoner-draft-sweep-v3.json`](reasoner-draft-sweep-v3.json)

Because the source state is dirty, this is bounded development evidence rather
than a clean-release measurement.

## Command

```powershell
$env:SHARDJEPA_BENCH_OUTPUT = "publications/artifacts/2026-08-06/reasoner-draft-sweep-v3.json"
rtk cargo bench --bench reasoner_benchmarks
```

## Fixed acceptance gate

A draft size is accepted only when every condition passes:

- minimum top-1 agreement across all fidelity cells: at least 99%;
- minimum recall@K across all fidelity cells: at least 80%;
- median speedup at 1,000 candidates: at least 3x;
- median speedup at every tested candidate count: at least 1x.

The sweep covers `K = 4, 8, 10, 16, 32, 64, 128`, candidate counts 50, 200,
and 1,000, dimensions 2, 16, and 128, and 100 deterministic fidelity trials per
cell. Each timing case uses 20 warmups, 30 samples, 20 iterations per sample,
and `black_box` inputs and outputs.

## Decision summary

| K | Minimum top-1 | Minimum recall@K | Speedup at 1,000 | Minimum speedup | Decision |
|---:|---:|---:|---:|---:|---|
| 4 | 91.00% | 73.00% | 9.29x | 4.37x | Reject |
| 8 | 98.00% | 74.12% | 8.74x | 3.24x | Reject |
| 10 | 99.00% | 74.80% | 9.15x | 2.51x | Reject |
| 16 | 100.00% | 76.38% | 7.58x | 1.87x | Reject |
| 32 | 100.00% | 77.75% | 6.66x | 1.06x | Reject |
| 64 | 100.00% | 79.73% | 4.82x | 0.75x | Reject |
| 128 | 100.00% | 84.80% | 3.11x | 0.72x | Reject |

## Conclusion

No fixed draft size passes the gate.

Small drafts preserve speed but lose ranking fidelity. Large drafts recover
fidelity but become slower than exhaustive ranking for small candidate sets.
Changing only `draft_k` therefore cannot satisfy the current cross-scale
contract.

The next implementation should not loosen the threshold merely to obtain a
passing result. It should test an adaptive policy that bypasses speculative
ranking for small candidate sets and selects draft size from candidate count
and measured latent-distribution requirements. Exact ranking remains the
fallback whenever the gate is not met.

## Limitations

- The timing distributions are from one invocation on one machine.
- The synthetic Poincare fixtures are deterministic and are not learned latent
  distributions.
- The gate expresses a repository engineering decision, not a universal
  scientific threshold.
- A clean committed revision and cross-machine replay remain required before
  publication-grade performance claims.
