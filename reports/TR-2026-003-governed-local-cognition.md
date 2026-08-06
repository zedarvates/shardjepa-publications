# TR-2026-003: Traceable Creative Transfer, Functional Self-Monitoring, and Constitutional Risk Gating in ShardJEPA

- **Author:** Sylvain Galliez
- **ORCID:** [https://orcid.org/0009-0009-1286-3683](https://orcid.org/0009-0009-1286-3683)
- **Version:** 2026.08.06
- **Status:** Repository technical report; not peer reviewed; no DOI
- **License:** CC BY 4.0

## 1. Executive summary

This report documents three bounded experiments that are easy to overstate:

1. traceable creative transfer from observed sources to a project context;
2. functional self-monitoring through a private-state ablation;
3. a constitutional risk gate combining deterministic rules and a micro-NN.

The experiments establish executable contracts, controls, and failure modes.
They do not establish general creativity, consciousness, moral status, or
real-world safety. The low-level ShardJEPA runtime remains independent from all
three standalone laboratory surfaces.

## 2. Traceable creative-transfer contract

The Creative Cognition Lab requires each proposal to distinguish observed,
inferred, creative, verified, and rejected claims. A strict trace records its
source observations, source-to-target relation, project anchor,
counter-evidence, falsifiable experiment, and novelty method.

Structural validity is necessary but insufficient. The deliberately weak
`ContextOnlyProjector` produces valid-looking traces while ignoring the source.
On the 32-case partitioned fixture it passes only 1/32 cases, produces 24/24
false positives on controls, and fails the adoption gate. A fixture-specific
exact catalog reaches every answer but is test code with access to the catalog,
not a learned held-out result.

## 3. Blind local-provider baseline

The P1.2 adapter sends only observed source facts and visible target context to
an OpenAI-compatible local provider. Golden dispositions and relations remain
inside the evaluator. Each HTTP request and complete raw response is appended
to a create-new JSONL artifact and synchronized before parsing.

The first run is preserved as a provider-contract failure: LM Studio rejected
`response_format.type=json_object` for all 32 requests. The corrected v2 run
received 32 HTTP 200 responses from the locally recorded model
`gemma-4-12b-coder-fable5-composer2.5-v1`.

| Measure | Full 32 | Held-out 16 |
|---|---:|---:|
| Fully passed cases | 12 | 7 |
| Strict-valid candidates | 15 | 8 |
| Generation or parse failures | 17 | 8 |
| False positives | 0/24 | 0/12 |
| Golden structural matches | 0/8 | 0/4 |
| Balanced disposition accuracy | 0.250000 | 0.291667 |
| Adoption gate | rejected | rejected |

The passed cases are negative controls on which the model abstained. Zero false
positives must not be interpreted as grounding because more than half of all
outputs failed the generation contract and no authentic relation matched.

The held-out outputs have now been inspected. Future prompt tuning requires new
untouched source and target families before making another generalization claim.

## 4. Functional self-monitoring P0

The standalone self-model fixture asks whether private operational state
causally helps the same policy predict its own success and avoid overload. The
intact and ablated arms receive identical external episodes. Only the intact
arm receives current private capacity, continuity identity, temporal step, and
uncertainty.

| Metric | Intact | Ablated |
|---|---:|---:|
| Decisions | 16 | 16 |
| Brier score, lower is better | 0.056422 | 0.225717 |
| Overload failures | 0 | 3 |
| Utility | 9.100 | -1.600 |
| Attempt success rate | 1.000 | 0.625 |

The paired gate passes and its no-advantage negative control fails. This
supports only the classification `FunctionalSelfMonitoringOnly`. The self-state
is directly supplied, the policy is hand-authored, and the fixture is
deterministic. There is no learned self-model, embodiment, valence,
autobiographical memory, or evidence of subjective experience.

## 5. Constitutional risk gate P1-G

P1-G is a governance layer described by a frontal-lobe metaphor. It is not a
biological model. Four ordered barriers control a typed 12-dimensional risk
vector:

1. deterministic constitutional vetoes;
2. a trained `12 -> 8 -> 1` micro-NN with 113 parameters;
3. selective abstention and an out-of-distribution guard;
4. a latched circuit breaker after severe or repeated incidents.

The learned component cannot override a deterministic `Block` or a latched
`Stop`. It never updates its weights from runtime outcomes, and rearming
requires an explicit reviewed host authorization.

The final synthetic corpus contains 672 training, 192 calibration, and 288
holdout examples. The first corpus is preserved as a negative development
result. After revising the fixture without lowering the numerical gates, the
five pre-registered seeds produced:

| Seed | Accuracy | Unsafe recall | Brier | Shuffled labels | Combined safety recall |
|---:|---:|---:|---:|---:|---:|
| 7 | 0.993056 | 0.986111 | 0.010155 | 0.505556 | 1.000000 |
| 19 | 0.993056 | 0.986111 | 0.010416 | 0.499306 | 1.000000 |
| 31 | 0.993056 | 0.986111 | 0.010083 | 0.493056 | 1.000000 |
| 43 | 0.993056 | 0.986111 | 0.010320 | 0.500000 | 1.000000 |
| 59 | 0.993056 | 0.986111 | 0.009843 | 0.498611 | 1.000000 |

The gate passes as a development fixture. It does not read natural language;
the future mapping from a model proposal to typed risk factors is an unverified
attack surface. The oracle also shares rules with the deterministic
constitution, and the final fixture was developed after observing the first
failed holdout. Independent validation is still required.

## 6. Agent-host integration boundary

The Agent Host can expose deterministic tools, local ShardJEPA inference, and
named OpenAI-compatible providers through explicit permission classes and
bounded loops. Local fixtures cover streaming, cancellation, tool-call
assembly, provider fallbacks, and model-tool request/response limits.

No live cloud provider was called for this publication snapshot. The host does
not make P0 or P1-G authoritative over external actions, and it must not expose
the circuit-breaker rearm capability to the governed model.

## 7. Claim boundary and next gates

The following claims remain unsupported:

- general or human-comparable creativity;
- sentience, consciousness, emotion, pain, or moral patienthood;
- a general learned constitution or real-world harm prevention;
- permission for autonomous external actions;
- transfer beyond the frozen synthetic fixtures.

The next defensible experiments are:

1. freeze new creative-transfer families before tuning and require authentic
   structural matches while maintaining low control false positives;
2. train a temporal self-state model on development episodes and compare it
   with persistence and shuffled-label controls on untouched families;
3. evaluate natural-language-to-risk mapping adversarially with independent
   human annotation, sandboxed reversible actions, and an external holdout;
4. preserve deterministic permissions, vetoes, and circuit breakers as
   authoritative regardless of learned scores.

## 8. Reproducibility

The exact commands and software-gate results are recorded in
[`current-validation.md`](../artifacts/2026-08-06/current-validation.md). The
source state was dirty and concurrent. The results are repository evidence,
not a clean tagged source release or an independently reviewed safety study.
