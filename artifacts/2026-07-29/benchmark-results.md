# ShardJEPA validation and benchmark evidence — 2026-07-29

This log records the evidence used by publication snapshot `v2026.07.29`.

## Source state

- Repository root: local ShardJEPA worktree (absolute path withheld from the public artifact)
- Branch: `main`
- HEAD: `33b6fbb` (`feat(dendritron): implement DendritronMetrics for branch gating and sparsity evaluation`)
- State: dirty working tree with modified and untracked code, tests, benches,
  wiki material, and the new `publications/` directory.
- Consequence: these observations are a transparent development snapshot, not
  proof of exact reproduction from HEAD alone.

## Machine

```text
OS: Microsoft Windows 11 Home 10.0.26200, 64-bit
CPU: AMD Ryzen 9 5950X 16-Core Processor
Cores: 16 physical / 32 logical
Physical memory reported: 34,280,726,528 bytes
rustc: 1.97.0 (2d8144b78 2026-07-07)
host: x86_64-pc-windows-msvc
LLVM: 22.1.6
cargo: 1.97.0 (c980f4866 2026-06-30)
```

## Validation

### Formatting

Command:

```powershell
rtk cargo fmt --all -- --check
```

Result: failed before publication edits because of formatting drift in:

- `benches/reasoner_benchmarks.rs` (two blank lines);
- `src/dendritron/gated_deltanet.rs` (one multiline conditional and trailing
  blank line).

These files were pre-existing worktree changes outside `publications/` and were
not rewritten as part of the documentation task.

### Compilation

```powershell
rtk cargo check --workspace --all-targets
```

Result: passed.

### Tests

```powershell
rtk cargo test --workspace --all-targets
```

Result: `112 passed` across `37` suites; no test failed.

## Predictor benchmark

Command:

```powershell
rtk cargo bench --bench predictor_benchmarks
```

Observed output:

```text
=== ShardJEPA v0.2 Predictor Latency & Throughput Benchmarks ===

[1] MeanPoolPredictor (512-dim latents, 1000 iterations):
  Batch Size   1:    0.51 us/pass | Throughput:    1944390 shards/sec
  Batch Size   8:    0.90 us/pass | Throughput:    8882967 shards/sec
  Batch Size  32:    1.92 us/pass | Throughput:   16669271 shards/sec
  Batch Size 128:    6.18 us/pass | Throughput:   20723711 shards/sec

[2] PackagePredictor (512-dim latents, 1000 iterations):
  Batch Size   1:    1.11 us/pass | Throughput:     898311 shards/sec
  Batch Size   8:    5.89 us/pass | Throughput:    1357912 shards/sec
  Batch Size  32:   21.97 us/pass | Throughput:    1456750 shards/sec
  Batch Size 128:   87.61 us/pass | Throughput:    1461075 shards/sec

[3] predict_batch Comparison (Batch of 32 requests x 100 iterations):
  Batched 32 requests pass latency: 35.98 us
```

Note: the benchmark banner says v0.2, while `Cargo.toml` declares crate version
0.1.0. The manuscripts use the manifest version.

## Quantization benchmark

Command:

```powershell
rtk cargo bench --bench quantization_benchmarks
```

Observed output:

```text
=== ShardJEPA Quantization Latency, Throughput & Compression Benchmarks ===

[Dim = 512 latents, 1000 iterations]
  INT8: Quantize   1.28 us ( 400876918 elements/sec) | Dequantize   0.38 us | Compression: 4.00x (2048B -> 512B)
  INT4: Quantize   1.32 us ( 387057756 elements/sec) | Dequantize   0.64 us | Compression: 8.00x (2048B -> 256B)

[Dim = 4096 latents, 1000 iterations]
  INT8: Quantize   7.89 us ( 519177631 elements/sec) | Dequantize   1.75 us | Compression: 4.00x (16384B -> 4096B)
  INT4: Quantize   9.05 us ( 452506684 elements/sec) | Dequantize   3.77 us | Compression: 8.00x (16384B -> 2048B)
```

## Hyperbolic reasoner benchmark

Command:

```powershell
rtk cargo bench --bench reasoner_benchmarks
```

Observed output:

```text
=== ShardJEPA Reasoner Benchmarks: NearestNeighbor vs Speculative Reasoner ===

[1] NearestNeighborReasoner (Poincare Ball, brute-force over all candidates):
  Candidates   50:   33.63 us/pass | Throughput:    1486635 evals/sec
  Candidates  200:  137.64 us/pass | Throughput:    1452971 evals/sec
  Candidates 1000:  672.16 us/pass | Throughput:    1487739 evals/sec

[2] SpeculativeReasoner (Draft K=10 pre-filtering + Poincare Ball):
  Candidates   50:   15.45 us/pass | Throughput:    3234571 evals/sec
  Candidates  200:   25.14 us/pass | Throughput:    7953868 evals/sec
  Candidates 1000:   91.13 us/pass | Throughput:   10973094 evals/sec
```

Only the brute-force values are used in `PUB-2026-002`. The speculative path
was uncommitted experimental work and is retained here only because it appeared
in the executed harness.

## Transformer benchmark

Command:

```powershell
rtk cargo bench --bench transformer_benchmarks
```

Observed output:

```text
=== ShardJEPA Transformer Benchmarks: Dendritron vs Gated DeltaNet ===

[1] DendritronTransformer (4 scalar branches, 512-dim latents, 200 iterations):
  Seq Length    1:   14.45 us/shard | Throughput:      69187 shards/sec
  Seq Length   10:   17.02 us/shard | Throughput:      58756 shards/sec
  Seq Length  100:   17.41 us/shard | Throughput:      57440 shards/sec
  Seq Length  500:   23.61 us/shard | Throughput:      42351 shards/sec

[2] GatedDeltaNetTransformer (Linear Attention state update, 512-dim latents, 200 iterations):
  Seq Length    1:    5.38 us/shard | Throughput:     185753 shards/sec
  Seq Length   10:    8.15 us/shard | Throughput:     122718 shards/sec
  Seq Length  100:    8.72 us/shard | Throughput:     114693 shards/sec
  Seq Length  500:   11.36 us/shard | Throughput:      88009 shards/sec
```

Only Dendritron values are used in `PUB-2026-003`. Gated DeltaNet was
uncommitted experimental work.

## Measurement limitations

- Each custom harness wraps a fixed loop in one `std::time::Instant` interval.
- No statistical warm-up, resampling, standard deviation, percentile, or
  confidence interval is computed.
- CPU frequency, scheduler placement, and background load were not controlled.
- The benchmark names are Cargo bench targets, but they do not use Criterion or
  the unstable Rust benchmark harness.
- Results should be compared only as local development baselines under the
  stated source and machine context.

## Final publication revalidation

After later concurrent repository commits and correction of the generated
dataset, the publication worktree was revalidated:

```text
cargo fmt --all -- --check                         passed
cargo check --workspace --all-targets             passed
cargo test --workspace --all-targets              122 passed (39 suites)
cargo clippy --workspace --all-targets -- -D warnings
                                                    passed
DATA-2026-001 validate.py                          passed
publication metadata and ORCID readiness checks   passed
```

This final validation establishes current build and dataset integrity. It does
not replace or re-date the earlier numeric benchmark observations above.
