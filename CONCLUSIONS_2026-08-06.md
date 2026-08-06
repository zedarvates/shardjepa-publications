# ShardJEPA current conclusions — 2026-08-06

## Status

ShardJEPA is a broader and better-instrumented local research platform, but it
remains preliminary. The strongest progress since the 2026-08-01 snapshot is
methodological: several attractive hypotheses were given explicit controls and
rejected instead of being promoted from a single favorable metric.

## What the current evidence establishes

- **Covered software behavior:** formatting and compilation pass; 258 standard
  workspace tests pass across 75 suites. The standalone Creative Cognition and
  Sentience laboratories add 20 and 17 passing tests respectively.
- **P1 remains an explicit-trace verifier:** its earlier 68.23–73.96% OOD result
  used explicit carry/borrow channels and remains behind the exact oracle.
- **P2 rejects hidden propagation in the tested RNN:** five-seed OOD accuracy is
  50.73% recurrent versus 51.46% with state reset.
- **P3 rejects the auxiliary-supervision hypothesis:** validity reaches 49.79%
  OOD versus 51.98% for a paired `aux=0` control. A 95.19% auxiliary score is
  not recurrent evidence because reset-state decoding reaches 97.80%.
- **A fixed speculative draft size is insufficient:** no tested `draft_k` meets
  the combined speed and Poincaré-ranking fidelity gate across candidate scales.
- **Traceable local-provider evaluation works:** the Creative Cognition Lab
  captures, fingerprints, replays, and fails closed on malformed generation.
  The tested local model fails adoption and matches no authentic structural
  relation in the frozen 32-case fixture.
- **Narrow governance fixtures are executable:** private operational state
  causally helps a deterministic policy on one paired fixture, and a
  113-parameter classifier passes its synthetic P1-G development gate behind
  deterministic vetoes. Both paths explicitly reject any sentience claim.
- **Provider orchestration remains outside the runtime:** the Agent Host passes
  its local protocol tests for streaming, cancellation, named providers,
  bounded model tools, and permission classes without a live cloud call.

## What the evidence does not establish

- No experiment establishes improved dialogue, general reasoning, autonomous
  capability acquisition, consciousness, moral patienthood, or real-world
  safety.
- The Soroban experiments do not solve arithmetic; exact arithmetic remains
  authoritative.
- The creative-transfer fixture is synthetic and exact-match based. Its frozen
  local model failed the adoption gate.
- P1-G does not read natural language and its final fixture was developed after
  inspecting an earlier failed holdout. It is development evidence, not an
  independent validation.
- The reasoner timings come from one dirty source state and one machine.
- The source checkout still has no configured remote and is not a clean tagged
  source release.
- The in-progress P4 causal bottleneck is excluded because strict Clippy and
  its adoption decision were not complete at snapshot time.

## Current assessment

The most defensible conclusion is not that one architecture has succeeded. It
is that ShardJEPA now exposes useful falsification machinery: paired controls,
reset-state ablations, shuffled labels, exact oracles, immutable provider
captures, conjunctive gates, and fail-closed boundaries.

P2 and P3 narrow the interpretation of P1. Explicit propagation channels can
support a learned trace verifier, but the current experiments do not show that
the RNN discovered a hidden carry/borrow state. Likewise, a high auxiliary
decoding score does not imply useful recurrent memory when the score improves
after state reset.

The governance experiments should be read with the same discipline. Functional
self-monitoring and a trained risk classifier can be measured without calling
either component conscious, autonomous, or safe in the world.

## Recommended next evidence gates

1. Finish P4 only after strict linting, a fixed five-seed protocol, paired
   controls, and an explicit adoption decision.
2. Test an adaptive reasoner policy that bypasses speculation for small
   candidate sets and retains exact ranking as fallback.
3. Create new untouched creative-transfer families before any prompt or schema
   tuning and require non-zero authentic structural matches.
4. Evaluate P1-G with an independently authored corpus, adversarial natural
   language-to-risk mapping, human review, and sandboxed reversible actions.
5. Reproduce the accepted publication claims from a clean source tag on a
   second machine before making portable performance claims.

## Evidence

- [`artifacts/2026-08-06/current-validation.md`](artifacts/2026-08-06/current-validation.md)
- [`artifacts/2026-08-06/reasoner-draft-sweep-v3.md`](artifacts/2026-08-06/reasoner-draft-sweep-v3.md)
- [`reports/TR-2026-002-task-local-learning-planning.md`](reports/TR-2026-002-task-local-learning-planning.md)
- [`reports/TR-2026-003-governed-local-cognition.md`](reports/TR-2026-003-governed-local-cognition.md)
- [`RELEASE_NOTES_2026-08-06.md`](RELEASE_NOTES_2026-08-06.md)
