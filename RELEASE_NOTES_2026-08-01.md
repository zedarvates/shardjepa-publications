# Publication snapshot 2026.08.01

This release updates the public ShardJEPA research snapshot with advances that
were locally validated on 2026-08-01.

## Added

- `PUB-2026-004`, the English multi-rate embodied-agents position paper and its
  complete French companion;
- `TR-2026-002`, a technical report on task-local learning, latent dynamics,
  and bounded planning;
- the fixed-snapshot CogniARC/Botte nano-network audit;
- the reasoner benchmark v2 report and raw JSON;
- a current validation record for 208 tests, Neural Soroban P0/P1, and the
  latent-compression replay;
- updated evidence-based conclusions dated 2026-08-01.

## Corrected or clarified

- P0's 100% longer-carrier result is described as local-feature invariance, not
  learned carry/borrow or general arithmetic.
- P1's 68.23–73.96% OOD accuracy is compared with the 50% no-propagation
  baseline and 100% exact oracle.
- The trained Soroban experts are separated from the still-untrained JEPA
  pattern-encoder scaffolding.
- Historical compression values are retained as dated evidence; the current
  source replays different exact distortions while preserving the INT8 choice.
- GitHub repository publication is separated from Zenodo, arXiv/HAL, peer
  review, DOI assignment, and ORCID record mutation.

## Validation summary

- `cargo fmt --all -- --check`: passed.
- `cargo check --workspace --all-targets`: passed.
- `cargo test --workspace --all-targets`: 208 passed across 69 suites.
- `cargo clippy --workspace --all-targets -- -D warnings`: passed.
- Neural Soroban P0 and P1 three-seed benchmark commands: passed and replayed.
- Latent-compression example: two identical consecutive replays.

The source evidence came from commit `b94646a` plus uncommitted and untracked
development work. This publication bundle is versioned, but it is not a clean
tagged release of the ShardJEPA source code.
