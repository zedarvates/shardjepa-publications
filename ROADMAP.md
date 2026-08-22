# ShardJEPA Research Roadmap

_Last updated: 2026-08-22_

This roadmap tracks research directions that are promising but **not yet validated claims**. New results must pass the repository's reproducibility and publication gates before they are promoted into papers, reports, or conclusions.

## P0 — Dynamic conditional compute inspired by FreeToken / sparse MoE serving

Goal: determine whether ShardJEPA can reduce local inference cost by activating and moving only the capabilities needed for the current task instead of keeping every specialist resident on GPU.

### Architecture hypothesis

- Treat compute capabilities as independently schedulable specialists/experts.
- Maintain a three-tier residency policy:
  - **hot**: resident in GPU VRAM;
  - **warm**: resident in system RAM and eligible for fast promotion;
  - **cold**: stored on disk and loaded only when predicted useful.
- Make routing conditional on task state, confidence, predicted next operation, memory pressure, and measured transfer cost.
- Prefer sparse/conditional activation over loading a larger monolithic model when equivalent quality can be demonstrated.
- Keep routing observable and deterministic enough to audit: every promotion, eviction, fallback, and abstention must be attributable to a policy decision.

### P0 experiments

- [ ] Define a `ResidencyClass { Hot, Warm, Cold }` abstraction independent of CUDA implementation details.
- [ ] Add an expert/module registry containing size, device affinity, last use, hit rate, promotion cost, and reliability metadata.
- [ ] Implement a CPU-only simulator for promotion/eviction policies before touching GPU code.
- [ ] Compare LRU, LFU, cost-aware, and predictive prefetch policies on recorded task traces.
- [ ] Add explicit memory budgets for GPU0, GPU1, system RAM, and storage.
- [ ] Record cache hit rate, bytes transferred, promotion latency, task latency, energy proxy, and failure/retry rate.
- [ ] Add an OOM-prevention gate: predicted residency must fit before promotion is attempted.
- [ ] Add rollback to static placement if dynamic routing regresses latency, fidelity, or reliability.

### P1 — Predictive expert prewarming

- [ ] Learn or derive a lightweight predictor for the next likely specialist(s) from current latent/task state.
- [ ] Benchmark deterministic heuristics against a tiny classifier; do not introduce a neural predictor unless labels and calibration are auditable.
- [ ] Allow prefetch only when predicted benefit exceeds measured transfer cost.
- [ ] Measure false-positive prefetches and VRAM churn, not only average speed.

### P1 — Self/speculative execution

- [ ] Evaluate self-speculative and draft-assisted execution where a cheap path proposes work and the full path verifies it.
- [ ] Keep verifier authority separate from proposer authority.
- [ ] Track acceptance rate, rejected speculative work, total compute, wall-clock latency, and fidelity.
- [ ] Test whether conditional specialists can act as drafts without destabilizing task-local planning.

### P2 — Multi-GPU local scheduling

Target reference hardware: commodity local systems including 2 × 12 GB GPUs.

- [ ] Treat two GPUs as separate constrained resources rather than assuming pooled VRAM.
- [ ] Benchmark replicated hot experts vs partitioned experts vs asymmetric roles (primary + speculative/draft GPU).
- [ ] Measure PCIe transfer overhead explicitly.
- [ ] Add topology-aware placement so an apparent VRAM win is rejected if transfer latency dominates.
- [ ] Test degraded mode with one GPU unavailable.

## Validation gates

A dynamic-residency result may be promoted into a ShardJEPA technical report only when all of the following are recorded:

1. reproducible hardware/software configuration;
2. static-placement baseline;
3. repeated measurements with median and p95 latency;
4. task-fidelity or ranking-fidelity comparison;
5. peak VRAM and RAM use;
6. transfer volume / cache hit rate;
7. failure, fallback, and OOM behavior;
8. raw artifacts sufficient to reproduce the conclusion.

## Cross-project reuse

The abstractions should remain generic enough to be reused by local-first systems such as Botte Secrète, StoryCore, and game/agent runtimes without importing project-specific policy into ShardJEPA research claims.

## Non-goals for the first iteration

- claiming that system RAM and VRAM form a transparent unified memory pool;
- maximizing model parameter count at the expense of usable latency;
- hiding failed promotions/retries behind aggregate throughput;
- activating uncalibrated learned routing in production;
- copying a third-party runtime wholesale instead of validating the underlying scheduling ideas independently.
