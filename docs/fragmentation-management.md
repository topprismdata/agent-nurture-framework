---
title: Fragmentation Management — Merge Candidate Workflow
status: accepted (Week 3 rewrite)
created: 2026-08-22
supersedes: "fragmentation-management.md v1 (fixed Jaccard thresholds as merge decisions, 30/60-day staleness rules)"
governed_by: 02_ADR-001_PROTOCOL_NOT_RUNTIME.md
---

# Fragmentation Management

Fragmentation is the natural byproduct of incremental capability acquisition:
many narrow skills accumulate, retrieval gets noisy, and per-skill value
declines. The remedy is deliberate consolidation with **human decisions** and
**machine-generated candidates** — never automated merging.

> **What changed.** The prior revision hard-coded thresholds (Jaccard > 0.5 ⇒
> recommend merge; > 5 skills per prefix ⇒ consolidate; 30 days without trigger
> ⇒ stale) as if textual overlap implied semantic redundancy. It does not:
>
> - "Don't use random CV for time series" and "use time-series splits" share
>   little vocabulary but mean nearly the same thing.
> - "Use embeddings for product names" and "do not use embeddings for IDs"
>   share most vocabulary and mean opposite things.
>
> Lexical similarity is now a **prefilter only**. Merge candidates must survive
> semantic, evidence-level, and contradiction checks, then pass human review.

---

## 1. Decision framework: separate vs merge

### Keep separate when

- Trigger conditions are genuinely distinct (different failure modes that
  merely look similar).
- Skills serve different audiences/domains despite structural similarity.
- A skill is the canonical reference for one narrowly defined problem;
  merging dilutes precision.

### Merge when (all checked by a human)

- Capabilities answer the same question in the same context, verified at the
  evidence level (their Evidence Records cover overlapping tasks with
  consistent outcomes).
- One capability's applicability conditions subsume another's.
- Maintaining both creates a real synchronization burden observed in practice,
  not merely inferred from text similarity.

### Signals that are NOT sufficient alone

- Token/Jaccard similarity of descriptions or bodies.
- Shared directory prefix.
- Age since last activation (see §4).

---

## 2. The candidate workflow

```text
cheap lexical prefilter          (merge_candidate_generator.py)
        ↓  candidate pairs + clusters, requires_human_review: true
semantic / trigger overlap       (LLM-assisted comparison, recorded in provenance)
        ↓  filtered pairs with rationale
evidence overlap                 (shared task_family coverage in Evidence Records)
        ↓  pairs confirmed redundant-in-effect
contradiction detection          (opposite guidance on same trigger?)
        ↓  contradictions routed to Disputed state instead
merge proposal                   (human-written or human-approved diff)
        ↓
human review & apply             (version-controlled change; provenance updated)
        ↓
post-merge validation            (trigger coverage walk-through; behavioral eval)
```

Every machine step writes to the provenance chain (`operation`, `producer`,
`producer_version`, `input_ids`). A reviewer must be able to ask *"which
comparisons produced this proposal?"* and get an answer.

---

## 3. Audit phase (periodic, cadence set by the team)

1. Count capabilities by domain/category; large categories are review
   triggers, not verdicts.
2. Generate lexical prefilter candidates (`merge_candidate_generator.py`);
   treat output as a triage list.
3. Review each cluster against the §1 framework.
4. Produce an audit note listing: cluster → decision (merge / keep / needs
   evidence) → rationale.

Output feeds the consolidation audit template; no automatic actions are taken.

---

## 4. On dormancy and staleness

"Skill not triggered in N days" is weak evidence. Low activation can mean
redundancy, but equally: seasonal relevance, poor description (trigger
precision problem), or a capability whose knowledge moved into a broader one.
Dormancy flags route skills into the normal review queue with dormancy noted —
they do not by themselves mark anything stale or merged. Freshness is judged
on evidence (last_verified, source volatility, dependency changes,
contradictions), not mtime; see crystallization-cycle.md §2.

---

## 5. Worked example (illustrative, thresholds illustrative too)

Eight API-integration capabilities, three of them auth variants:

```text
rest-auth-basic / rest-auth-bearer / rest-auth-oauth     ← auth cluster
rest-error-handling / rest-retry-logic / rest-rate-limit ← resilience cluster
rest-pagination / rest-connection-debug                  ← keep separate
```

Pipeline outcome:

1. Prefilter flags both clusters (high token overlap). Pagination and
   connection-debug also flag against error-handling lexically — semantic
   check clears them.
2. Auth cluster: evidence check shows all three validated on overlapping
   tasks; no contradiction; merge into `api-authentication.md` structured as a
   decision tree. Human approves.
3. Resilience cluster: retry and rate-limit share backoff logic (confirmed via
   shared execution traces); error-handling kept as entry point with
   cross-references. Partial merge approved.
4. Post-merge: trigger-condition walk-through passes; behavioral eval rerun on
   the merged skill; provenance chains of absorbed skills linked as inputs to
   the new lineage.

---

## 6. Acceptance checks for this document

- [x] No numeric threshold decides a merge; humans decide.
- [x] Lexical similarity scoped to prefiltering.
- [x] Contradiction detection precedes any merge.
- [x] Every machine comparison is provenance-recorded.
- [x] Dormancy is a review signal, not a lifecycle verdict.
