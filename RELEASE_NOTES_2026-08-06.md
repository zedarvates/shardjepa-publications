# Publication snapshot 2026.08.06

This release updates the public ShardJEPA research snapshot with results
validated or frozen between 2026-08-04 and 2026-08-06.

## Added

- a five-seed reproduction of Neural Soroban P2 and P3;
- a fixed-draft speculative-reasoner sweep with raw JSON;
- `TR-2026-003`, covering traceable creative transfer, functional
  self-monitoring, and constitutional risk gating;
- a current validation record for 258 standard workspace tests, standalone
  laboratory gates, and the remaining strict-lint limitation;
- evidence-based conclusions dated 2026-08-06.

## Main decisions

- P2 is retained as a negative result: recurrent OOD accuracy is 50.73% versus
  51.46% with state reset.
- P3 is rejected: OOD validity is 49.79% versus 51.98% for the paired `aux=0`
  control, with only two seed wins out of five.
- The 95.19% P3 auxiliary score is not described as recurrent memory because
  reset-state decoding reaches 97.80%.
- No fixed reasoner draft size passes the combined speed/fidelity gate.
- The frozen local creative-transfer generator fails adoption: 17/32 outputs
  fail the contract and no authentic structural relation matches its golden.
- Functional self-monitoring and P1-G risk classification are published only
  under narrow software-fixture claims; both explicitly reject sentience and
  real-world safety claims.
- The in-progress P4 causal bottleneck is excluded from scientific claims.

## Validation summary

- formatting: passed;
- workspace compilation: passed;
- standard workspace tests: 258 passed across 75 suites;
- Agent Host: 28 tests and strict Clippy passed;
- Creative Cognition Lab: 20 passed, 2 ignored, strict Clippy passed;
- Sentience Lab: 17 passed, strict Clippy passed, executable metrics replayed;
- workspace strict Clippy: not green because four findings remain in the
  concurrent P4 causal-bottleneck implementation.

The source evidence came from commit
`b94646aa38d9397bd7f306ee132984a2715822e3` plus modified and untracked
development work. This publication bundle is versioned, but it is not a clean
tagged release of the ShardJEPA source code.
