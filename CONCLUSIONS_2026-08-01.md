# ShardJEPA current conclusions — 2026-08-01

## Status

ShardJEPA remains a promising but preliminary research platform. It now has a
larger verified software surface and its first genuine task-local training
experiments, while the low-level runtime remains independent from training,
agent orchestration, and game-domain policy.

## What the current evidence establishes

- **Workspace integrity:** formatting, workspace compilation, strict Clippy,
  and 208 tests across 69 suites passed on the current development state.
- **Task-local learned experts:** Neural Soroban P0 learned a 217-parameter
  local transition verifier and reached 100% on its generated-family holdout
  and longer-carrier split for three seeds. Because its feature schema is local
  and fixed-size, this is an invariance result rather than multicolumn
  arithmetic.
- **Longer propagation is partially learned:** the separate 961-parameter P1
  Elman RNN reached 77.08–77.92% interpolation accuracy and 68.23–73.96% on
  held-out carry/borrow lengths 4–7, beating the 50% no-propagation OOD
  baseline for all three seeds but remaining far below the 100% exact oracle.
- **Latent-dynamics evaluation is more concrete:** the Planning Lab includes
  recursive multi-horizon evaluation, a persistence control, and an
  action-conditioned affine predictor trained only on complete training
  sequences.
- **Planning fixtures are broader:** deterministic contracts now cover
  hierarchical latent planning, pattern-guided selection, chess, Xiangqi, and
  four-player variants. They test software and rules; they are not learned game
  competence.
- **Compression choice is evidence-led:** the current autoresearch fixture again
  favors INT8 over INT4 under its combined hyperbolic-distortion objective.
  Exact distortion values changed from the earlier development snapshot, so
  only the dated measurements are defensible.

## What the evidence does not establish

- P0/P1 results do not show improved dialogue, general reasoning, transfer to a
  new domain, or autonomous capability acquisition.
- The Pattern Lab exact oracles remain authoritative. Learned outputs do not
  redefine arithmetic, rules, permissions, or safety.
- The game curriculum does not yet contain a trained JEPA pattern encoder with
  matched deterministic baselines, frozen holdouts, calibration, latency, and
  end-to-end task outcomes.
- H-JEPA uses deterministic reference predictors and fixture-level assertions;
  it is not evidence of learned hierarchical representations.
- The source state is dirty and has no configured source-repository remote.
  Reproduction from a clean tagged source revision remains an open gate.
- There is still no physical sensor/actuator loop, hard real-time guarantee,
  device-energy measurement, or statistically controlled cross-machine study.

## Current assessment

The strongest new scientific result is narrow but real: a small Rust-only RNN
learns enough explicit carry/borrow trace structure to beat a no-propagation
baseline on longer unseen propagation lengths. The result is deliberately kept
behind an exact oracle and should be described as task-local OOD improvement,
not arithmetic mastery.

The broader platform is increasingly useful for controlled comparisons among
deterministic rules, small learned experts, retrieval, latent prediction, and
bounded planning. The next leap in credibility requires clean source releases
and transfer experiments, not more architectural labels.

## Recommended next evidence gates

1. Commit the current source surface and reproduce all published results from a
   clean tag on at least one second machine.
2. Add an untouched transfer task for P1 and compare against matched-parameter
   MLP/RNN and deterministic baselines.
3. Replace untraceable game-curriculum summary numbers with generated raw
   reports for recall, calibration, utility regret, node reduction, and latency.
4. Extend the repeated-sample reasoner benchmark method to quantization,
   serialization, predictors, and transformers.
5. Add a measured edge adapter while preserving the privileged pre-mutation
   safety boundary.

## Evidence

- [`artifacts/2026-08-01/current-validation.md`](artifacts/2026-08-01/current-validation.md)
- [`artifacts/2026-07-29/reasoner-benchmark-v2.md`](artifacts/2026-07-29/reasoner-benchmark-v2.md)
- [`artifacts/2026-07-29/nano-nn-huggingface-audit.md`](artifacts/2026-07-29/nano-nn-huggingface-audit.md)
- [`RELEASE_NOTES_2026-08-01.md`](RELEASE_NOTES_2026-08-01.md)
