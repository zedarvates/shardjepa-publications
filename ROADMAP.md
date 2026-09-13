# ShardJEPA Research Roadmap

_Last updated: 2026-09-13_

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

## Parallel research track — physical prediction on particle graphs (2026-09-10)

**Claim class: Planned.** This track complements conditional compute; it does not
replace the existing P0 priorities or assert a newly trained ShardJEPA runtime.
ShardJEPA remains an independent research project; consumer demand is not a
scientific validation gate.

### P0 — reproducible reference and data

- [x] Identify an external, public starting fixture: [CogniARC particle operators](https://github.com/zedarvates/cogniarc/blob/a4aac4a5f42e546c4a4ad777c508e4a1b0f0f136/experiments/particle_graph/README.md). Its own implementation/tests are fixture observations, not ShardJEPA results.
- [ ] Define an action-conditioned observation schema with positions, velocities, masses, units, frames, actions, time steps and provenance.
- [ ] Freeze train/validation/test splits by scene and seed; reserve particle counts, material parameters and longer horizons for out-of-distribution evaluation.
- [ ] Validate numerical targets with time-step refinement and an independent reference solver before calling the corpus water data.
- [ ] Package the generator, schema, license, checksums and exact artifacts under the dataset publication gates.

### P1 — baseline ladder before learned rollout

- [ ] Compare persistence and constant velocity with the task-local affine action-conditioned baseline already described in [TR-2026-002](reports/TR-2026-002-task-local-learning-planning.md).
- [ ] Locate the actual runtime source and define an explicit adapter before modifying or training the predictor. This publications repository does not contain that runtime.
- [ ] Evaluate learned graph-message or latent prediction only after freezing the baseline protocol. A neighbourhood graph alone is not a neural model.
- [ ] Report errors separately by horizon (initially 1/10/50), scene and held-out condition; include rollout failures, drift, calibration, compute and memory.
- [ ] Keep exact/reference checks authoritative for proposed actions; abstain or fall back when predictions fail the admissibility checks.

**Promotion gate:** reproducible improvement over the strongest applicable
baseline on held-out scenes, with error growth and resource costs reported.
Retain negative results; small fixture parity tests do not establish physical
generalisation, rollout stability, sample efficiency or speedup. Measurements
must follow [GUIDELINES.md](GUIDELINES.md) and include raw evidence, source,
configuration and environment.

### Primary sources

- [Müller et al., 2003: Particle-Based Fluid Simulation for Interactive Applications](https://matthias-research.github.io/pages/publications/sca03.pdf): physical kernel reference.
- [Sanchez-Gonzalez et al., 2020: Learning to Simulate Complex Physics with Graph Networks](https://arxiv.org/abs/2002.09405): learned graph simulator and rollout evaluation.

The interpretation of the initial water idea as a particle-neighbour graph is a
working hypothesis, not a recovered specification or novelty claim.

### Numerical prerequisite update — 2026-09-13

**Observed fixture (external):** the
[CogniARC numerical follow-up](https://github.com/zedarvates/cogniarc/blob/693a68b18529dd7af6d305198e5850096383e769/experiments/particle_graph/NUMERICAL_VALIDATION.md)
now provides 10 synthetic scenes, a frozen 3/2/5 train/validation/test split,
reserved particle counts and material parameters, and sparse snapshots at
steps 0/1/10/50. Three Euler resolutions are compared at the same physical time
against independently coded dense RK4 at two resolutions. All ten scenes pass
the stated numerical gates; the combined particle-graph suite passes 21 tests.

The linked report includes exact recipes, schema, source and data hashes,
execution commands and environment. This is an external numerical prerequisite,
not a ShardJEPA result or a newly released ShardJEPA dataset. Both solvers use
the same simplified equations; boundaries, calibrated water behaviour, longer
rollouts and a trained predictor remain unvalidated.

**Next for this repository:** review/import the versioned snapshot contract under
the dataset gates, then compare the existing affine baseline using training
scenes only and validation-only selection. Preserve the test split for separate
reporting; do not infer learned generalisation from the numerical checks.

### Box-contact prerequisite update — 2026-09-13

**Observed fixture (external):** the
[CogniARC box-contact follow-up](https://github.com/zedarvates/cogniarc/blob/7df23110477f763503e23a670eb01c9bc40595c0/experiments/particle_graph/BOUNDARY_VALIDATION.md)
adds fixed frictionless walls, a wall-contact radius, swept straight-line drift,
normal restitution, and explicit wall impulse/energy ledgers. The combined
particle-graph suite now passes 33 tests. Five analytic flight cases and four
coupled SPH cases pass the stated validation checks; all exercise
contact, including repeated and corner impacts.

This establishes the narrower geometric contact and bookkeeping properties
described in the report. Force-kick/drift splitting does not solve exact curved
impact times under acceleration, and the coupled cases do not validate fluid
trajectory accuracy. SPH wall-density support, no-slip treatment, calibrated
water behaviour and trained prediction remain outside this evidence.

The next learning comparison remains the affine baseline on the existing frozen
scenes, with training-only fitting and validation-only selection. Boundary
verification cases are separate fixtures and do not change those learning
splits. No ShardJEPA runtime or learning result is claimed by this update.
