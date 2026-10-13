---
title: ADR-002 — Canonical Lifecycle Vocabulary
status: proposed (awaiting maintainer signature)
created: 2026-10-13
supersedes: capability-record.schema.json 0.1.0 enum (draft|active|refining|stable|disputed|deprecated)
deciders: TopPrism maintainers
consulted: cultivating-ml-agent (sole machine consumer, G4 draft-only producer), prism-ontology GOVERNANCE.md (proposal state machine — separate namespace, unaffected)
informed: skill-tester (produces EvidenceRecords, no lifecycle writes)
---

# 05 · ADR-002 — Canonical Lifecycle Vocabulary

> **Status:** PROPOSED. Until signed, treat both vocabularies as unstable (0.x rule,
> `schemas/README.md`).

## Context

ANF shipped **three** lifecycle vocabularies:

| Source | Vocabulary | Nature |
|---|---|---|
| Charter §3.2 Contract 4 | Candidate → Observed → Validated Local → Validated Transfer → Stable → Disputed / Deprecated | governance law |
| Charter K-plane diagram | Candidate Knowledge → Validated Capability → Transferable Capability | narrative prose |
| `capability-record.schema.json` 0.1.0 | draft \| active \| refining \| stable \| disputed \| deprecated | machine enum |

The machine enum encodes **neither** the law's gates nor the narrative: `refining`
has no Charter meaning, and the enum **lacks any state for Validated Transfer** —
precisely the transfer gate ANF exists to encode. `cultivating-ml-agent`'s
promotion policy (`min_task_families=2`, `min_negative_transfer=1`) implements
exactly that gate, yet the machine vocabulary cannot represent its passing.
Additionally `docs/knowledge-architecture.md` §4 used `validated`, a value in no
vocabulary at all.

Schema sign-off is still pending (`schemas/README.md`: "expect field
adjustments"), and the only machine consumer emits a single constant
(`lifecycle_status="draft"`, G4). The correction window is open and the blast
radius is minimal.

## Decision

**The Charter §3.2 Lifecycle Protocol is canonical.** The machine enum adopts it,
kebab-cased:

```text
candidate | observed | validated-local | validated-transfer | stable | disputed | deprecated
```

Old→new mapping (applied jointly in both repos, same day):

| 0.1.0 enum | canonical | rationale |
|---|---|---|
| draft | candidate | Charter initial state |
| active | observed | evidence of use, not yet validated |
| refining | validated-local | proven in native context |
| — | validated-transfer | **new**: the transfer gate (≥2 task families + negative-transfer evidence) |
| stable | stable | unchanged |
| disputed / deprecated | disputed / deprecated | unchanged |

The K-plane diagram remains **narrative prose**, not a state vocabulary; it is not
renamed. `capability-record.schema.json` bumps to **0.2.0** (0.x breaking = minor,
per the rule recorded in `schemas/README.md`).

## Consequences

- **ANF**: enum + `structural_lint.py` LIFECYCLE set + provenance WARN moved from
  `active` to `observed` (faithful translation; the pre-existing gap that
  refining/stable were never checked is **not** widened here); doc example fixed.
  `evidence_freshness_check.py` uses only `disputed` — unaffected.
- **cultivating-ml-agent**: `promotion.py` G4 literal `"draft"` → `"candidate"`;
  SPEC-007, promotion-policy schema description, and 3 test asserts updated in the
  same coordinated change. G4 semantics unchanged: the interface only ever emits
  the initial state; activation remains a human/A2 act.
- **Cross-repo contract**: DecisionTrace→experience-record projection does not
  carry lifecycle_status (ExperienceRecord has no such field) — projection tests
  stay green either way; the capability-record producer path is what aligns.
- **Rejected alternative**: declaring the schema enum canonical and mapping the
  Charter onto it — collapses Validated Transfer into `stable`, deleting the
  governance gate from the machine contract; projection must follow law, not
  the reverse.
- **Rollback if unsigned**: revert enum to 0.1.0 vocabulary in both repos (single
  coordinated commit each); no persisted records in the wild use either
  vocabulary yet (G4 producer emits only the initial state).
