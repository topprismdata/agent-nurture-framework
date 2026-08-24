---
title: Progress Measurement — Behavioral Metrics First
status: accepted (Week 3 rewrite)
created: 2026-08-22
supersedes: "progress-measurement.md v1 (Dreyfus 1–5 averaged scores, mtime staleness counts, value-function phase model)"
governed_by: 02_ADR-001_PROTOCOL_NOT_RUNTIME.md
---

# Progress Measurement

> **Principle.** Capability growth is claimed only from behavioral evidence:
> task outcomes, time, error rates, human intervention, transfer gains, and
> negative transfer. Document-shape metrics and self-rated ordinal scales are,
> at best, secondary signals — they are never evidence.

---

## 1. Primary behavioral metrics

These come from evaluation runs (designated provider: `skill-tester`) and from
instrumented work, recorded as Evidence Envelope records.

| Metric | Definition | Healthy direction |
|---|---|---|
| Task success rate | Tasks completed to acceptance / attempted, per task family | ↑ within a family after relevant capabilities activate |
| Time-to-competence | Wall-clock to reach a defined quality bar on a new project type | ↓ across successive projects |
| Repeated-mistake rate | Problems previously solved by an existing capability that recur unapplied | ↓ toward zero; each occurrence is a retrieval/trigger defect |
| Negative-transfer count | Tasks made worse by applying an existing capability | Monitored per capability; > 0 forces `Disputed` review |
| Human-intervention rate | Corrections per task where a capability was active | ↓ as validated capabilities mature |
| Trigger precision/recall | Of capabilities auto-activated: correct activations vs missed + spurious | Both ↑; measured by `skill-tester` trigger evaluation |
| Transfer gain | Delta on target-context tasks with vs without a transferable capability | Positive and significant before `Transferable` promotion |

Minimum instrumentation for any team adopting ANF: task success, repeated
mistakes, negative transfers. Everything else is refinable later.

---

## 2. Qualitative capability review (replaces scored matrix)

The prior revision asked operators to rate six dimensions 1–5 (Dreyfus-aligned)
and average them into a score. Averaging ordinal stage ratings is statistically
meaningless, and a self-assessed score is not evidence of anything.

Keep the **reflection**, drop the **score**:

```text
capability-review-template.md — per dimension, free-text notes:
  - What changed since last review? (with linked Evidence Records)
  - Where did the agent struggle? (failure modes, not vibes)
  - Which capability gaps caused rework this period?
  - One concrete action for the next period.
```

Dimensions remain useful as *prompts for observation*: domain knowledge, task
execution, error recovery, reasoning quality (as judged from decisions and
outcomes), autonomy, adaptability. They structure attention; they do not
produce numbers.

---

## 3. Secondary knowledge-base signals (non-evidence)

Useful for maintenance planning; none may back a capability claim:

```bash
# capability count and distribution
find $SKILL_DIR -name "SKILL.md" | wc -l
ls $SKILL_DIR | sed 's/-.*//' | sort | uniq -c | sort -rn

# episodic volume and classification coverage
find $MEMORY_DIR -name "*.md" | wc -l
```

Interpretation guardrails:

- Count growth is meaningful only early; a mature library grows slowly because
  consolidation outpaces creation. Growth is not progress.
- Distribution shifts (many narrow → fewer broad) hint consolidation is
  happening; verify via merge-candidate workflow outcomes, not counts.
- File-age queries (`-mtime`) are explicitly **not** staleness measures.
  Freshness lives in metadata (`last_verified`, `last_contradicted`,
  source volatility); see crystallization-cycle.md §2.

---

## 4. Lifecycle-phase expectations (qualitative)

The prior revision modeled value as $V(K)=\alpha\,\text{Breadth}+
\beta\,\text{Structure}+\gamma\,\text{Align}$ with week-numbered phases.
Unmeasurable coefficients and calendar phases are dropped. The qualitative
sequence survives:

```text
Early     breadth dominates   → expect fast candidate growth, thin validation
Middle    structure dominates → expect consolidation activity, rising eval pass rates
Mature    alignment dominates → expect pruning, applicability narrowing, high precision
```

Phase transitions are observed in the behavioral metrics themselves
(consolidation throughput up, repeated mistakes down), never inferred from
elapsed time.

---

## 5. Measurement workflow

| Cadence | Activity | Output |
|---|---|---|
| Per session | Capture Experience Records with outcomes; log corrections | episodic records |
| Weekly | Behavioral metric snapshot; skim corrections; flag anomalies | short note |
| Monthly | Full behavioral eval batch via skill-tester on active capabilities; qualitative capability review; merge-candidate audit | evidence batch + review note |
| Quarterly | Trend review across projects; prune deprecated; confirm shared-schema compatibility with adapters | strategy note |

Rule of thumb: if a number cannot be traced to an Evidence Record or an
evaluation run, it does not go into a report.

---

## 6. Acceptance checks for this document

- [x] No averaged ordinal scoring.
- [x] No mtime-based staleness claims.
- [x] Negative transfer and contradictions are first-class metrics.
- [x] All quantitative claims route through Evidence Envelope records.
