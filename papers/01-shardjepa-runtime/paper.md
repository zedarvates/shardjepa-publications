# ShardJEPA: A Low-Level Rust Runtime for Latent Joint Embedding Predictive Architecture Experiments

**Author:** Sylvain Galliez  
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)  
**Version:** 2026.08.01
**Status:** Repository preprint; not peer reviewed; no DOI  
**License:** CC BY 4.0

## Abstract

ShardJEPA is an independent Rust prototype for deterministic experiments over
latent representations. The runtime separates prediction, latent
transformation, hyperbolic ranking, bounded caching, read-only memory-mapped
storage, quantization, observation, and external integration contracts. This
paper documents the implemented interfaces and reports local release-mode
baselines for 512-dimensional prediction and packed INT8/INT4 quantization.
The measurements are single-machine loop averages and do not establish learned
representation quality or comparative superiority.

## 1. Scope

Joint Embedding Predictive Architectures predict targets in representation
space rather than reconstructing every input detail [1]. ShardJEPA provides a
small systems substrate for testing such mechanisms. It is not a trained JEPA
model, training framework, distributed runtime, or evidence that a particular
representation has been learned.

The repository keeps application orchestration and adjacent-project state
outside the low-level runtime. External integrations use typed ports rather
than application-specific schemas inside `src/`.

## 2. Implemented runtime contract

The 0.1.0 crate exposes these principal surfaces:

- `latent`: validated dense and columnar shards, prediction requests,
  reference and multi-step predictors, and weight manifests;
- `hyperbolic`: Poincare and Lorentz geometry plus candidate reasoners;
- `dendritron`: deterministic latent transformations;
- `storage`: a byte-bounded cache and read-only memory mappings;
- `quantization`: symmetric per-tensor INT8 and packed INT4 conversion;
- `observer`: bounded runtime observation;
- `interfaces`: transport-neutral request and response types.

All inputs at public boundaries are checked for the dimensions and finite
values required by their operation. Errors are returned as typed `Result`
values.

### 2.1 Reference prediction

`MeanPoolPredictor` averages equally shaped context shards. The deterministic
`PackagePredictor` used by the benchmark applies one finite weight per latent
element to the mean-pooled context. It is a reference CPU path, not a dense
matrix model or trained network.

For context vectors \(x_1, \ldots, x_n \in \mathbb{R}^d\) and element weights
\(w \in \mathbb{R}^d\), the benchmarked path is equivalent to

\[
\hat{y}_j = w_j \left(\frac{1}{n}\sum_{i=1}^{n} x_{i,j}\right).
\]

### 2.2 Hyperbolic ranking

`PoincareBall` validates, projects, and compares finite vectors. Candidate
ranking computes distance for each candidate and sorts the resulting
`(index, distance)` pairs. The specialized implementation and its measured
baseline are described in `PUB-2026-002`.

### 2.3 Storage

`DiskStreamer::open` creates a read-only `memmap2::Mmap` while retaining the
source file handle. `MappedShard::bytes()` returns a borrowed byte slice. The
runtime does not define or parse a `SHARDJEPA_V1` file header.
`MappedShard::read_f32_le(offset, count)` checks byte arithmetic and bounds,
then decodes little-endian floats into a newly allocated `Vec<f32>`. It is
therefore incorrect to describe the decoded-float path as zero-copy.

### 2.4 Symmetric quantization

For bit width \(b \in \{4, 8\}\), let
\(q_{max}=2^{b-1}-1\), \(a=\max_i |x_i|\), and
\(s=a/q_{max}\) when \(a>0\), otherwise \(s=1\). The implementation computes

\[
q_i = \operatorname{round}(x_i/s)\ \text{clamped to}\ [-q_{max}, q_{max}].
\]

INT8 stores one byte per value. INT4 stores two signed nibbles per byte.
Reported compression ratios count packed payload bytes only; object metadata
and allocator overhead are excluded.

### 2.5 Development additions after the first snapshot

The current development surface adds `LatentColumnarBatch` for validated
column-major batches and `MultiStepPredictor` for recursively applying an
injected predictor over an explicit horizon. These are inference contracts,
not evidence that a representation or transition model was trained.

Training, latent-dynamics fitting, hierarchical planning, task-local experts,
and agent sessions remain in independent workspace tools. They do not add
training or orchestration dependencies to the low-level crate.

## 3. Local baseline

Measurements were taken on 2026-07-29 with Rust 1.97.0, Windows 11, and an AMD
Ryzen 9 5950X. `cargo bench` selects the optimized bench profile, but the custom
harnesses use one `Instant` around a fixed loop. See the raw evidence for exact
commands and source-state caveats.

### 3.1 Predictor, 512 dimensions, 1,000 iterations

| Predictor | Context shards | Mean time per pass | Reported throughput |
|---|---:|---:|---:|
| Mean pool | 1 | 0.51 us | 1,944,390 shards/s |
| Mean pool | 8 | 0.90 us | 8,882,967 shards/s |
| Mean pool | 32 | 1.92 us | 16,669,271 shards/s |
| Mean pool | 128 | 6.18 us | 20,723,711 shards/s |
| Package predictor | 1 | 1.11 us | 898,311 shards/s |
| Package predictor | 8 | 5.89 us | 1,357,912 shards/s |
| Package predictor | 32 | 21.97 us | 1,456,750 shards/s |
| Package predictor | 128 | 87.61 us | 1,461,075 shards/s |

A separate loop over 32 single-context requests observed 35.98 us per batch.

### 3.2 Quantization, 1,000 iterations

| Dimensions | Encoding | Quantize | Dequantize | Payload ratio |
|---:|---|---:|---:|---:|
| 512 | INT8 | 1.28 us | 0.38 us | 4.00x |
| 512 | INT4 | 1.32 us | 0.64 us | 8.00x |
| 4,096 | INT8 | 7.89 us | 1.75 us | 4.00x |
| 4,096 | INT4 | 9.05 us | 3.77 us | 8.00x |

The harness did not compute reconstruction error, downstream ranking accuracy,
energy use, allocation counts, or comparisons with other frameworks.

## 4. Validation and reproducibility

At benchmark time, the workspace passed `cargo check --workspace --all-targets`
and 112 tests across 37 suites. Four benchmark executables also completed. The
measurement source state was commit `33b6fbb` plus uncommitted working-tree
changes; it was not a clean tagged source release. Before the first publication
packaging, formatting, workspace check, 122 tests across 39 suites, and strict
Clippy all passed on the then-current worktree. On 2026-08-01, the enlarged
current workspace passed formatting, compilation, strict Clippy, and 208 tests
across 69 suites. The numeric tables still belong to the earlier recorded
measurement state and were not silently relabeled as new measurements.

These facts limit exact reproduction from the documentation repository alone.
The evidence is suitable as a transparent development snapshot, not as a
stable cross-machine performance study.

## 5. Limitations

- No training loop or learned weights are evaluated.
- The public Poincare fixture is a deterministic numerical dataset; no trained
  model corpus or learned latent dataset is included.
- Benchmarks have no warm-up policy, repeated samples, variance, confidence
  intervals, or CPU-frequency controls.
- mmap access is not compared against buffered I/O.
- The publication snapshot does not prove end-to-end model accuracy,
  throughput under concurrency, or portability to other operating systems.

## 6. Conclusion

ShardJEPA 0.1.0 supplies a bounded, inspectable Rust substrate for latent-space
experiments. The present contribution is the runtime contract, expanded
inference boundaries, and dated local baselines. Task-local training now exists
in a standalone tool, but claims about learned JEPA quality, hierarchy
representation, and production performance remain future experimental work.

## References

1. Yann LeCun. *A Path Towards Autonomous Machine Intelligence*, version
   0.9.2, 2022.
2. Maximilian Nickel and Douwe Kiela. *Poincare Embeddings for Learning
   Hierarchical Representations*. NeurIPS 2017.
