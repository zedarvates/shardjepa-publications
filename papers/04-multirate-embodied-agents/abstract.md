# Abstract: ShardJEPA and multi-rate embodied agents

**Author:** Sylvain Galliez
**ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
**Version:** 2026.08.01
**Status:** Repository preprint; not peer reviewed; no DOI

Resource-bounded embodied agents should not assign perception, control,
safety, memory, planning, and language interaction to one monolithic language
model. We argue instead for a multi-rate architecture in which the least costly
competent component handles each decision under explicit latency, energy,
memory, connectivity, and risk budgets. Small neural evaluators, bounded
retrieval, latent world models, and compact language models may all contribute,
but no unverified generative component directly owns the actuator boundary.
An independent run-time assurance layer checks proposed actions before the
environment can change. This position is narrower than claiming that language
models cannot run on devices or control robots: compact on-device models,
memory-aware inference, and vision-language-action systems already provide
counterexamples. The scientific claim is therefore architectural and
falsifiable: under equal task-success and safety constraints, budget-aware
multi-rate routing should improve the latency-energy-memory Pareto frontier
relative to always invoking the largest available model. ShardJEPA currently
implements several enabling contracts—deterministic micro-MLP evaluation,
exact bounded k-NN retrieval, latent prediction, quantization, planning traces,
and a privileged safety gate—but it does not yet implement sensor drivers,
hard real-time scheduling, nano-networks, language-model orchestration, or
physical control. The paper defines the missing experiments required to test
the thesis rather than presenting it as an established result. The standalone
Pattern Lab now supplies two genuinely trained Soroban verifiers, including a
961-parameter recurrent model that beats a no-propagation baseline on longer
held-out carry/borrow chains; this remains task-local evidence, not embodied
routing or general reasoning.
