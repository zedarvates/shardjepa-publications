# TR-2026-002: Task-Local Learning, Latent Dynamics, and Bounded Planning in ShardJEPA

**Author:** Sylvain Galliez
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
**Version:** 2026.08.01
**Status:** Repository technical report; not peer reviewed; no DOI
**License:** CC BY 4.0

## 1. Executive summary

ShardJEPA now includes its first genuine small-model training experiments in
the standalone Pattern Lab, together with broader deterministic latent-dynamics
and planning fixtures. This report separates three kinds of evidence:

1. learned task-local behavior from Neural Soroban P0/P1;
2. fitted or deterministic research baselines in the Planning Lab;
3. software contracts that have tests but no learned-quality claim.

The low-level `shard-jepa` runtime still has no training-framework dependency.
Exact arithmetic, game rules, permissions, and safety remain authoritative;
learned components may score or propose.

## 2. Neural Soroban P0

P0 is a 217-parameter two-layer verifier for one explicit local `AddOne` or
`SubtractOne` bead transition. The trainer uses seeded initialization and epoch
ordering, binary cross-entropy, analytical backpropagation, momentum SGD,
calibration, and versioned JSON artifacts.

At 80 epochs, seeds 7, 17, and 29 each reached 100% on 384 holdout examples and
384 examples embedded in longer 4–6 digit carrier states. Shuffled-label
controls remained at 49.48%, 51.82%, and 50.00%.

The seven input features describe a local transition independently of total
carrier length. The longer-carrier split therefore tests invariance of that
local verifier. It does not test multicolumn propagation.

## 3. Neural Soroban P1

P1 uses a distinct variable-length trace schema and a 961-parameter Elman RNN.
Fourteen per-column features expose the input, operand, proposed result,
operation, propagation-in/out, and end marker. Training uses weighted step BCE,
full backpropagation through time, gradient clipping, seeded shuffling, and
momentum SGD.

Semantic families and exact signatures remain split-disjoint. Training
propagation ends at length 3; the OOD split contains only lengths 4–7.

| Seed | Interpolation holdout | OOD propagation 4–7 | Shuffled labels |
|---:|---:|---:|---:|
| 7 | 77.50% | 71.88% | 50.42% |
| 17 | 77.92% | 73.96% | 52.50% |
| 29 | 77.08% | 68.23% | 53.75% |

The mechanical no-propagation baseline reached 70% on interpolation and 50%
on OOD. The exact oracle reached 100%. P1 therefore provides evidence of a
modest learned OOD improvement on longer propagation chains, not solved
arithmetic or general reasoning.

## 4. Latent dynamics and planning

The Planning Lab now exposes:

- recursive multi-horizon prediction evaluation with per-horizon RMSE;
- a persistence predictor evaluated on the same rollout origins;
- an action-conditioned affine baseline
  `next = bias + A × current + B × action` fitted by deterministic ridge
  regression from complete training sequences;
- hierarchical macro-goal and micro-rollout fixture contracts;
- deterministic pattern-guided planning across chess, Xiangqi, and four-player
  rule profiles.

The affine predictor recovers a controlled affine fixture and beats persistence
on its complete held-out sequence. It uses normal equations and is intended for
small controlled systems; it is not a neural JEPA, uncertainty model, or
production trainer.

The hierarchical and game-domain experiments currently establish interface,
rules, and bounded-search behavior. They do not establish learned hierarchical
representations or learned game competence.

## 5. Runtime boundary

The independent runtime gains columnar latent and multi-step prediction
contracts, while training and agent orchestration remain in workspace tools.
The Agent Host similarly lives outside the low-level crate and owns provider,
session, protocol, and tool-execution concerns.

This separation is intentional:

- `src/` owns bounded latent inference contracts;
- Pattern Lab owns task-local training and artifact export;
- Planning Lab owns deterministic evaluation and search fixtures;
- Agent Host owns conversation and tool orchestration;
- exact gates remain outside learned proposal authority.

## 6. Reproducibility

The 2026-08-01 workspace passed formatting, compilation, strict Clippy, and 208
tests across 69 suites. P0/P1 three-seed commands were replayed separately.
Exact commands and per-seed values are archived in
[`current-validation.md`](../artifacts/2026-08-01/current-validation.md).

The underlying source state was commit `b94646a` plus uncommitted and untracked
development work. Reproduction from a clean source tag remains required.

## 7. Limitations and next experiment

- All learned results use synthetic Soroban data from one generator family.
- No untouched cross-domain transfer task has been evaluated.
- No stable wall-clock, energy, or memory protocol is reported for P0/P1.
- The exact oracle remains necessary and authoritative.
- Game-curriculum learned-encoder claims remain blocked until a trained encoder
  is compared against the deterministic baseline on frozen holdouts.

The next scientific gate should preregister an untouched transfer task and
compare P1 with matched-parameter recurrent and feed-forward baselines under the
same data, compute, and oracle policy.
