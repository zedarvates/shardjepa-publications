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
the stated numerical gates; the particle-graph suite passed 21 tests at that stage.

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
particle-graph suite passed 33 tests at that stage. Five analytic flight cases and four
coupled SPH cases pass the stated validation checks; all exercise
contact, including repeated and corner impacts.

This establishes the narrower geometric contact and bookkeeping properties
described in the report. Force-kick/drift splitting does not solve exact curved
impact times under acceleration, and the coupled cases do not validate fluid
trajectory accuracy. SPH wall-density support, no-slip treatment, calibrated
water behaviour and trained prediction remain outside this evidence.

At that stage, the next learning comparison was the affine baseline on the existing
frozen scenes, with training-only fitting and validation-only selection. Boundary
verification cases are separate fixtures and do not change those learning
splits. No ShardJEPA runtime or learning result is claimed by this update.

### External affine baseline update — 2026-09-13

**Implemented (external):** the [CogniARC affine runner](https://github.com/zedarvates/cogniarc/blob/2dadc7f34b2e32e21bdbc7813a1db11a7f71c9d1/experiments/particle_graph/affine.py)
fits a separate direct horizon regression at steps 1/10/50, using only initial
centred positions/velocities and known gravity. Three scenes supply training;
two select regularization. A separate command scores the saved model on five
test scenes. The [protocol was committed before scoring](https://github.com/zedarvates/cogniarc/blob/5e39eb67db3526eeea63d525ba7b9aeafc4b0677/experiments/particle_graph/affine_protocol.json).
The frozen manifest and snapshot bytes are unchanged; public test targets were
reserved from fitting and selection, not kept blind from readers.

**Measured (external, synthetic fixtures):** [the dated evidence](https://github.com/zedarvates/cogniarc/blob/2dadc7f34b2e32e21bdbc7813a1db11a7f71c9d1/experiments/particle_graph/AFFINE_BASELINE.md)
records 45 passing focused tests, the five candidate scores, selected alpha
0.0001, coefficients, per-scene/horizon errors, exact commands, environment and
input/source hashes. Affine position and velocity errors are below persistence,
constant velocity and known-gravity ballistic prediction in each of the five
scenes at all three horizons. At step 50 (dimensionless time 0.1), mean scene
position RMSE is 7.376996e-4 versus ballistic 1.252737e-3 (41.11% lower);
mean velocity RMSE is 1.463711e-2 versus 2.487859e-2 (41.17% lower).

Raw artifacts: [selected model](https://github.com/zedarvates/cogniarc/blob/2dadc7f34b2e32e21bdbc7813a1db11a7f71c9d1/experiments/particle_graph/evidence/2026-09-13-affine/model.json)
and [test evaluation](https://github.com/zedarvates/cogniarc/blob/2dadc7f34b2e32e21bdbc7813a1db11a7f71c9d1/experiments/particle_graph/evidence/2026-09-13-affine/evaluation.json).
Both schemas, byte sizes, SHA-256 values, the actual reader, deterministic target
generator and repository MIT license are linked in the evidence document.

The stiffness case retains the largest error. Development uses one material
configuration and the model has no material inputs, so these results do not
identify physical parameter dependence. Five tiny scenes and correlated
horizons do not establish broad generalisation, calibrated water accuracy,
autoregressive stability, conservation or resource savings. Direct predictions
restart at t=0; no learned rollout or wall interaction was evaluated.

This measured baseline is CogniARC code; it neither implements nor evaluates
the ShardJEPA task-local affine/action-conditioned runtime from TR-2026-002.
That runtime must still be located and adapted explicitly. No ShardJEPA
learning result, dataset release, neural training or runtime change is claimed.

**Planned:** review the external reader/contract under the dataset gates; freeze
a v2 corpus with material variation in development and new test seeds before
changing the predictor features, then compare material-conditioned affine
prediction and longer autoregressive trajectories. Preserve the v1 result.
The ShardJEPA runtime comparison and conditional-compute priorities remain open.

### External paired-material comparison — 2026-09-13

**Implemented (external):** [CogniARC v2](https://github.com/zedarvates/cogniarc/blob/038457dfca5ac8bb749c1de0c00d45d70bd75dd1/experiments/particle_graph/MATERIAL_BASELINE.md)
adds four material variants per initial-condition group. The manifest and
protocol were committed at [0751eb36ca1b01d7a1cc2f1484f49cd563d900e9](https://github.com/zedarvates/cogniarc/commit/0751eb36ca1b01d7a1cc2f1484f49cd563d900e9)
before generation and scoring. Sixteen training, eight validation and twelve
test scenes derive from only 4/2/3 initial-condition groups. Groups never cross
partitions and all seeds are absent from v1. The unchanged v1 model and a blind
v2 refit are controls for a ridge model with six material–state interactions.
It is affine in expanded features, not linear in raw materials and state.

**Measured (external, synthetic fixtures):** all 36 scenes pass dense RK4
resolution and conservation checks; the combined focused suite passes 57 tests.
Blind v2 selects alpha 0.01 and material v2 selects 1e-6, using validation only.
Both models are saved before separate test scoring. At step 50, material v2
mean scene position RMSE is 6.703571e-4, versus blind v2 8.409680e-4 (20.29% lower)
and frozen v1 7.863229e-4 (14.75% lower). Mean velocity RMSE falls by 20.48% and
14.95%, respectively. The v1 experiment's earlier percentage belongs to a
different test corpus and is not a directly comparable score.

**Retained negative results:** relative to blind v2, mean step-50 position RMSE
rises by 10.89% at 27 particles and 31.57% on the joint-interpolation material.
Material v2 wins 27/36 scene/horizon pairs against blind v2 and 24/36 against
frozen v1; these are correlated observations. All 27 paired material-change
contrasts improve over a zero response, but better parameter response does not
guarantee lower absolute trajectory error. The lower overall mean does not
establish improvement across all held-out conditions.

Source/reader, commands, environment, license, schemas, byte sizes and SHA-256
values are in the [evidence document](https://github.com/zedarvates/cogniarc/blob/038457dfca5ac8bb749c1de0c00d45d70bd75dd1/experiments/particle_graph/MATERIAL_BASELINE.md).
Raw [numerical checks](https://github.com/zedarvates/cogniarc/blob/038457dfca5ac8bb749c1de0c00d45d70bd75dd1/experiments/particle_graph/evidence/2026-09-13-materials/numerics.json),
[selected models](https://github.com/zedarvates/cogniarc/blob/038457dfca5ac8bb749c1de0c00d45d70bd75dd1/experiments/particle_graph/evidence/2026-09-13-materials/models.json)
and [evaluation, including regressions](https://github.com/zedarvates/cogniarc/blob/038457dfca5ac8bb749c1de0c00d45d70bd75dd1/experiments/particle_graph/evidence/2026-09-13-materials/evaluation.json)
are committed alongside the deterministic generator and split snapshot files.
V1 implementations, manifest, model and raw evidence remain unchanged.

This completes the external v2 direct-prediction comparison proposed above.
The corpus has no walls and only one lattice family; direct predictions still
restart at t=0. No ShardJEPA runtime, action-conditioned learning result, dataset
release, neural training, calibrated water, rollout stability or resource gain
is claimed. ShardJEPA's actual runtime comparison and dataset publication gates
remain open; the conditional-compute priorities are preserved.

**Planned:** predeclare longer autoregressive evaluation of the frozen step-1
maps and retain error growth/conservation failures by material and particle
count. Any geometry-feature revision needs a separate future protocol and fresh
scenes; these test results must not become a tuning set. No automatic activation
or merge follows from the averaged gain.

### External frozen-model rollout evaluation — 2026-09-13

**Implemented (external):** [CogniARC's rollout runner](https://github.com/zedarvates/cogniarc/blob/f1a35b9fdbbaf68c8df33dccc84a2abac7987400/experiments/particle_graph/rollouts.py)
repeatedly applies the saved step-1 maps to their own predicted state for 500
steps at dt 0.002, without fitting, resets, corrections or future-state input.
The [protocol](https://github.com/zedarvates/cogniarc/blob/3737d3e256acc654954b0d0a5359b20096cc0c8b/experiments/particle_graph/rollout_protocol.json)
was committed before implementation and measurements. It pins all model/data
inputs and predeclares numerical qualification, abort rules and aggregation
without survivor-only means. The same 12 v2 variants from three groups are
extended to T=1.0; this is not a fresh blind benchmark.

**Measured (external, synthetic fixtures):** [the dated evidence](https://github.com/zedarvates/cogniarc/blob/f1a35b9fdbbaf68c8df33dccc84a2abac7987400/experiments/particle_graph/ROLLOUT_EVALUATION.md)
records 66 passing focused tests. All 84 comparison trajectories finish, all 72
reference checkpoints qualify, and 36 short-prefix checks reproduce v2 exactly.
Dense RK4 runs at dt 0.0005 and 0.00025; maximum resolution disagreement is
6.426019e-10 for position and 1.848105e-9 for velocity. These checks concern the
same simplified equations, not physical water accuracy.

**Retained negative result:** at step 500, material v2 mean scene position RMSE
is 1.188473e-1 versus blind v2 6.796472e-2, a 74.87% increase. It is also 104.39%
higher than frozen v1 and 19.28% higher than known-gravity ballistic prediction.
The SPH Euler comparator reaches 1.913961e-4; no relative compute-cost claim is
made. The material model's earlier average advantage does not persist over this
interval. High stiffness has a 324.62% increase relative to blind v2; across the
27-particle variants the increase is 90.68%.

All three learned maps fail the predeclared 1e-8 momentum tolerance on all twelve
final scenes. Maximum momentum errors are 8.999100e-5 (v1), 1.002475e-2 (blind v2)
and 1.012499e-6 (material v2). SPH Euler and known-gravity ballistic prediction pass
all twelve. Masses are carried as fixed observations; zero mass error is not
learned conservation. Kinetic energy is recorded, not assumed conserved under
gravity, pressure and viscosity. Finite completion is separate from accuracy
and conservation.

The [raw evaluation](https://github.com/zedarvates/cogniarc/blob/f1a35b9fdbbaf68c8df33dccc84a2abac7987400/experiments/particle_graph/evidence/2026-09-13-rollouts/evaluation.json)
and [reference snapshots](https://github.com/zedarvates/cogniarc/blob/f1a35b9fdbbaf68c8df33dccc84a2abac7987400/experiments/particle_graph/evidence/2026-09-13-rollouts/reference.jsonl)
include source/input hashes, exact command, environment, schemas and failure
records; byte sizes, checksums, generator/reader and MIT license are linked in
the evidence document. Earlier source files, models and raw evidence remain
unchanged. Source code and these results belong to CogniARC; no ShardJEPA
runtime, learning result, dataset release, neural capability or resource gain
is claimed. Existing publication gates and conditional-compute priorities remain.

**Planned:** before a predictor revision, predeclare explicit treatment of known
gravity and zero net internal momentum change on fresh reserved scenes. Diagnose
high-stiffness drift and changing neighbour support separately. Better
conservation alone would not establish accuracy. These negative results do not
justify replacing the physical solver or activating a learned runtime; no merge
or automatic promotion follows.
