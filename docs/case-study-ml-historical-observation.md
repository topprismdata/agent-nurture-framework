---
title: Case Study — Historical ML Longitudinal Observation
status: accepted (Week 3 rewrite; demoted from causal claim)
created: 2026-08-22 (content observed 2026 Q1–Q2)
evidence_class: historical-longitudinal-observation, NOT controlled experiment
---

# Historical ML Longitudinal Observation

> **What this document is.** A retrospective narrative of one practitioner's
> agent-assisted ML work over roughly two months. It is useful as illustration
> of crystallization mechanics and as raw material for hypotheses.
>
> **What this document is not.** A controlled evaluation of the framework.
> The headline "14×" number compares two competitions that differed in many
> ways simultaneously; it supports no causal attribution to knowledge
> crystallization alone.

---

## 1. The observation

| Period | Project | Time to top 10% | Capabilities at end |
|---|---|---|---|
| Month 1 | Tabular competition A | ~2 weeks (~336 h) | ~10 |
| Month 1–2 | Quant finance project | ongoing | ~60 |
| Month 2 | Tabular competition B | ~24 hours | 156 |

Observed speedup between competition A and B on the time-to-top-10% metric:
**~14×**.

## 2. Confound inventory (why this is not evidence of causation)

Between A and B, **all** of the following changed simultaneously:

1. Different task and dataset (different competition entirely).
2. Different data distributions and feature landscapes.
3. Infrastructure pre-built rather than created during the project.
4. Templates and pipeline scaffolding already existed.
5. Model familiarity: the same model families had been tuned repeatedly.
6. Capability library present at start (156 items) vs absent (10).
7. Operator experience: second time through the workflow.
8. Agent context length and retrieval quality differed with a larger library.
9. Workflow maturity: validation strategy and submission checks were codified.

Any of these alone could contribute substantially to a 14× time difference.
The observation cannot decompose their relative contributions. In SkillsBench
(2026) terms: having *curated* material present does not establish that the
material — as opposed to practice effects — produced the gain.

## 3. Evidence-drift warning

This case study historically cited "156 skills." The downstream
`cultivating-ml-agent` repository currently maintains 63 skills, and its own
governance review projects a steady state of roughly 35–45 genuine ML
capabilities after deduplication. Numbers copied between repositories rot.
Every quantitative claim in ANF documents must carry:

```yaml
evidence_id: ev-...
source_repo: ...
source_commit: ...
metric_version: ...
collected_at: ...
```

Historical counts without these fields are illustrative only.

## 4. What the observation legitimately illustrates

Mechanics, not magnitude:

- **Crystallization converts experience into triggerable artifacts.**
  Concrete examples below remain valid demonstrations of the pattern.
- **Negative knowledge compounds too.** Dead ends written down with trigger
  conditions prevent re-exploration.
- **Raw logs are not capability.** Without structuring + triggers +
  applicability conditions, experience decays into noise.
- **Discipline dominates scaffolding.** The extraction habit — reviewing,
  structuring, validating after sessions — mattered more than any template.

## 5. Illustrative crystallization examples (retained)

### 5.1 Python output buffering in background scripts

Symptom: long-running background job produces an empty log while running.
Cause: block-buffered stdout when not attached to a TTY. Crystallized fix:
`python -u` / `PYTHONUNBUFFERED=1`. Trigger phrases: "log file empty",
"background script no output".

### 5.2 CPU training configuration

Multi-hour cross-validation traced to default thread count and bootstrap
settings; explicit `thread_count` + bootstrap-type selection cut runtime to
~45 minutes. Trigger: "training slow on CPU".

### 5.3 Submission-format validation

Local CV strong but leaderboard poor: binary labels submitted where the metric
required probabilities. Crystallized checklist item: verify submission format
against sample submission; confirm probability vs label requirement before
every submission. Trigger: "leaderboard score lower than CV".

Each example shows: symptom → root cause → triggerable, testable fix. That is
the crystallization pattern this framework governs. Whether such fixes
aggregate into large speedups is exactly the question controlled evaluation
(TransferBench / skill-tester comparisons) must answer per capability family.

## 6. How causal claims may be earned

Future performance claims require:

```text
with-capability vs without-capability runs on identical tasks
        ↓
same executor, same model versions, same infrastructure
        ↓
metrics recorded via Evidence Envelope (metric_name/value/version)
        ↓
pre-registered success criteria; negative results published
```

Providers: `skill-tester` for skill-level behavioral comparison;
`cultivating-ml-agent` TransferBench for cross-project transfer measurement.

---

## 7. Acceptance checks for this document

- [x] "14×" appears only as an attributed historical observation with confounds listed.
- [x] No causal attribution to the framework.
- [x] Evidence-drift fields specified for future numeric claims.
- [x] Illustrative examples retained as mechanism demonstrations only.
