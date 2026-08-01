# External nano-network snapshot audit

- Date: 2026-07-29
- Scope: evidence cited by `PUB-2026-004`; not a ShardJEPA runtime benchmark

## Sources and fixed snapshots

| Repository | Audited commit | Repository timestamp reported by the Hugging Face API |
|---|---|---|
| [zedgamer/cogniarc-nano-nn](https://huggingface.co/zedgamer/cogniarc-nano-nn) | `775c27f303bf0d23fea29bad68e113b0bfbd707e` | 2026-06-29T08:14:46Z |
| [zedgamer/botte-nano-nn](https://huggingface.co/zedgamer/botte-nano-nn) | `2a1faa904f8aae0f600930b8683ae2b41654d7af` | 2026-06-26T17:23:03Z |

The audit used clean, depth-one clones of these commits. Parameter counts are
the sum of every serialized weight and bias. Numerical replay used the
published row-major JSON layout and the same deterministic synthetic generators
as the CogniARC training scripts.

## CogniARC Nano-NN

| Model | Architecture | Parameters | Published claim | Replayed result |
|---|---:|---:|---|---|
| domain classifier | 6→12→4, ReLU + softmax | 136 | 75% synthetic; 3/4 games | 55/100 on the generated synthetic holdout; 3/4 canonical vectors |
| action-success predictor | 8→16→1, ReLU + sigmoid | 161 | 77.6% test | 388/500, or 77.6%, on the generated synthetic holdout |

The action result is reproducible from the published weights. The domain-card
percentage is not reproducible from the published weights and current
`generate_synthetic_data(600)` split; the discrepancy must be resolved before
using 75% as a result. The four canonical domain vectors are not an independent
test set: they are hand-authored examples of the same task schema.

The repository also contains a 256→64→32→6 CAPTCHA classifier with 18,726
parameters. It is outside the 50--310-parameter routing examples considered in
the position paper and is not used as nano-network evidence there.

`cargo test` builds all CogniARC Rust test targets successfully, but the audited
source defines zero Rust unit tests. This is a build smoke check, not behavioral
coverage.

## Botte Nano-NN

| Serialized model | Architecture | Parameters | JSON bytes |
|---|---:|---:|---:|
| `binary_router.json` | 3→8→2 | 50 | 1,554 |
| `anomaly_detector.json` | 5→10→2 | 82 | 2,495 |
| `effort_classifier.json` | 4→12→3 | 99 | 2,936 |
| `priority_estimator.json` | 12→12→3 | 195 | 5,672 |
| `token_estimator.json` | 14→12→3 | 219 | 6,348 |
| `error_classifier.json` | 12→16→6 | 310 | 8,915 |

The Rust suite reports 10 passing unit tests. These cover matrix operations,
activations, JSON shape validation, output shape, determinism, and input-size
errors. They establish inference-engine behavior, not model accuracy.

The snapshot does not contain the `training/train.py` path shown in the model
card, a training dataset, split manifest, labels inside the JSON weights, seed
matrix, accuracy table, calibration report, or raw latency samples. Only three
of the six serialized models are named by the Python CLI metadata.

## Claims that remain unverified

The following model-card statements are not publication-grade measurements in
the audited snapshots:

- deterministic inference in approximately 5 microseconds;
- 394 KB or 50 KB compiled-binary sizes across target toolchains;
- 80% of CogniARC decisions handled at the nano tier;
- 60--90% token savings in an agent pipeline;
- replacement of a six-second V-JEPA call without a task-quality regression.

To promote these statements to measured evidence, archive the CPU and target,
compiler flags, numerical mode, warm-up policy, iteration count, p50/p95/p99,
raw samples, task distribution, escalation threshold, baseline prompts, task
success, safety outcomes, and end-to-end token accounting.

## Publication interpretation

The snapshots support three narrow statements:

1. 50--310-parameter feed-forward routers can be serialized in a small JSON
   representation and evaluated by a dependency-light Rust runtime.
2. The published CogniARC action predictor reproduces its reported synthetic
   holdout accuracy.
3. These external prototypes are suitable candidates for a controlled
   ShardJEPA adapter experiment.

They do not establish a ShardJEPA system-level energy, latency, accuracy,
safety, or token-efficiency improvement.
