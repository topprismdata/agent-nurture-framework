---
title: Repository Inventory & Disposition Plan
status: draft (Architecture Reset, Week 1)
created: 2026-08-22
purpose: Architecture Reset inventory of every asset in agent-nurture-framework,
         with KEEP / RENAME / REWRITE / DOWNGRADE / REPLACE / DELETE / EXTERNALIZE
         disposition for each.
---

# 01 · Repository Inventory & Disposition Plan

This inventory is **not** a `tree` dump. It is an Architecture Reset inventory:
every asset receives an explicit disposition tied to the new Project Direction
Charter (`00_PROJECT_DIRECTION_CHARTER.md`) and ADR-001 (`02_ADR-001_PROTOCOL_NOT_RUNTIME.md`).

## Disposition legend

| Code | Meaning |
|---|---|
| **KEEP** | Stays as-is. Already aligned with charter. |
| **RENAME** | File or function renamed for accuracy (e.g. removing "Quality Score"). |
| **REWRITE** | Same path, new content. Conceptual basis changes. |
| **DOWNGRADE** | Reduced scope: utility stays but stops claiming evaluation authority. |
| **REPLACE** | New file replaces it. Old file deleted. |
| **DELETE** | Removed entirely. |
| **EXTERNALIZE** | Move to an adapter repo (e.g. skill-tester, cultivating). ANF no longer owns it. |

---

## Top-level files

| File | Lines | Current role | Actual value (2026-08) | Problem | Target role | Disposition |
|---|---:|---|---|---|---|---|
| `README.md` | 410 | Project homepage | Good positioning text; inherits weak claims | Mentions 14× even with caveat; calls itself "methodology" not "protocol"; conflates Authority/Knowledge in L1/L2/L3 | New homepage aligned with charter, ADR, evidence map | **REWRITE** |
| `topprism.yaml` | ~50 | TopPrism metadata | Correct company context | Lists `evidence: longitudinal-internal` (legacy); missing ANF v1 schema refs | Add evidence envelope reference; link to charter | **REWRITE** |
| `LICENSE` | n/a | MIT | Fine | None | Keep | **KEEP** |
| `ACKNOWLEDGMENTS.md` | ? | Credits | Acknowledgement of authors / prior work | May need new acknowledgements for external refs (Prism, SkillsBench, etc.) | Update | **RENAME** → `ACKNOWLEDGMENTS.md` (no path change) |
| `CONTRIBUTING.md` | ? | Contributor guide | Useful | Currently encourages adding scripts; needs new charter-aligned guidance | Rewrite contributor paths | **REWRITE** |

---

## `docs/`

| File | Lines | Current role | Actual value | Problem | Target role | Disposition |
|---|---:|---|---|---|---|---|
| `case-study-ml.md` | 265 | ML longitudinal observation | Honest historical record of cultivation journey | Headline claims "14× speedup" without denominator / metric / control details | Becomes a Historical Observation, not a benchmark | **REWRITE** + **RENAME** → `case-study-ml-historical-observation.md` |
| `crystallization-cycle.md` | 663 | Detailed 4-phase KCC specification | Lots of operational detail | Includes reasoning-trace requirement (per #13 risk); time-based maturity gates (per #11); L1 promotion pathway (per #7) | Rewrite to align with Lifecycle Protocol + Risk-Aware Gates | **REWRITE** |
| `fragmentation-management.md` | 220 | How to detect / merge duplicate skills | Conceptually useful; addresses real problem | Current checker uses 0.5 Jaccard threshold and English stopwords; treats merge as auto (per #15) | Becomes description of the **merge candidate generator** pattern, with explicit human-review requirement | **REWRITE** |
| `framework.md` | 413 | Top-level framework narrative | High-level map; uses Code-First / Prompt-First / Nurture-First framing | NFD framing overstated (per #8); tacit-knowledge framing overstated (per #9) | New narrative aligned with charter | **REWRITE** |
| `knowledge-architecture.md` | 355 | L1/L2/L3 layered cognitive architecture | Provides useful vocabulary | Conflates Authority with Knowledge via L1 = Constitutional (per #5, #6); allows L2→L1 promotion (per #7); uses staleness = mtime (per #16) | Replace with two-plane model: Authority (A0-A3) + Knowledge (Evidence → Capability) | **REWRITE** |
| `progress-measurement.md` | 245 | How to measure progress | Discusses Dreyfus scoring | Uses Dreyfus 1-5 averaged ordinal (per #17); no behavioral measurement guidance | New measurement doctrine: behavioral metrics only | **REWRITE** |
| `theoretical-foundations.md` | 320 | References to NFD, SECI, Dreyfus, Kolb | Useful as **reference**, not architecture | Risk of being treated as design authority (per #8) | Keep as background reading; clearly mark "reference, not authority" | **KEEP** + header note |
| **NEW** `00_PROJECT_DIRECTION_CHARTER.md` | ~250 | New charter | Highest priority | n/a | Already created | **KEEP** |
| **NEW** `01_REPOSITORY_INVENTORY.md` | ~400 | This file | n/a | n/a | Already created | **KEEP** |
| **NEW** `02_ADR-001_PROTOCOL_NOT_RUNTIME.md` | ~400 | Architectural decision record | Critical | n/a | To be created next | **KEEP** |
| **NEW** `03_EXTERNAL_CAPABILITY_MAP.md` | ~500 | Make/buy/reuse analysis | Required by Reuse First principle | n/a | To be created next | **KEEP** |

---

## `scripts/`

| File | Lines | Current role | Actual value | Problem | Target role | Disposition |
|---|---:|---|---|---|---|---|
| `skill_audit.py` | 377 | Quality score for skill docs | Frontmatter parsing is genuinely useful | "Quality Score" measures doc looks, not capability behavior (per #14); risks promoting long docs over working skills | Downgrade to structural lint only | **REWRITE** + **RENAME** → `structural_lint.py` |
| `skill_consolidation_checker.py` | 392 | Detects overlapping / mergeable skills | Candidate generator is real value | Jaccard threshold treats literal similarity as semantic overlap (per #15); does not detect contradictions; recommends merge automatically | Output merge candidates with explicit `requires_human_review: true`; never recommend auto-merge | **REWRITE** + **RENAME** → `merge_candidate_generator.py` |
| `crystallization_scheduler.py` | 306 | When to re-crystallize | Directory walking is useful | Staleness = mtime only (per #11, #16); uses layer-path to classify L1/L2/L3 | Replace mtime-based stale with evidence-freshness model | **REWRITE** (keep path) — but only after Evidence Contract defines freshness fields |
| `capability_assessment.py` | 256 | Dreyfus 1-5 averaging into capability score | Interactive prompt is useful for team reflection | Mean of ordinal scores is statistically weak (per #17); score is treated as evidence | Downgrade to qualitative reflection notes (no score output) | **REWRITE** + **RENAME** → `capability_review.py` |

After dispositions, **no script in ANF shall claim authority over behavioral
evaluation** — that authority belongs to `skill-tester`.

---

## `templates/`

| File | Lines | Current role | Actual value | Problem | Target role | Disposition |
|---|---:|---|---|---|---|---|
| `bootstrap-config/` | dir | Initial scaffolding for new agents | Useful for new adopters | None major | Keep but simplify; remove "Constitutional" framing | **KEEP** + rename inner files (e.g. drop "constitutional") |
| `capability-matrix-template.md` | 111 | Dreyfus-style capability matrix | Useful for human reflection | Tied to capability_assessment.py scoring; conflates ordinal dimensions | Rename + remove average score | **RENAME** → `capability-review-template.md` + **REWRITE** (drop score) |
| `consolidation-audit-template.md` | 149 | Audit checklist for skill consolidation | Useful | Currently paired with auto-merge recommendation | Keep audit framing; remove auto-merge references | **REWRITE** |
| `crystallization-checklist.md` | 166 | Step-by-step crystallization procedure | Useful | Implies single correct cadence (time-based) | Replace with risk-aware gate checklist | **REWRITE** |
| `session-review-template.md` | 165 | Capture session-level experience | Useful | None major | Keep; align with Experience Contract v1 | **KEEP** + **REWRITE** light edits |
| `skill-template.md` | 93 | Skill document template | Standard SKILL.md format | Already mostly aligned with Agent Skills spec | Keep; explicitly cite Agent Skills compliance | **KEEP** + header note |

---

## `examples/`

| File | Lines | Current role | Actual value | Problem | Target role | Disposition |
|---|---:|---|---|---|---|---|
| `skills/01-core-expertise.md` | 280 | Example constitutional / identity doc | Useful for adopters | "Constitutional" wording; lives at L1 in old architecture | Move identity into Authority Plane examples | **RENAME** → `01-authority-plane-user-preferences.md` + **REWRITE** |
| `skills/02-domain-workflow.md` | 263 | Example domain skill | Useful | Standard skill doc — already aligned | Minimal edits; cite Agent Skills compliance | **KEEP** + header note |
| `skills/03-bug-fix-skill.md` | 217 | Example debugging skill | Useful | Same as above | Same | **KEEP** + header note |
| `case-study/ml-competition-journey.md` | 186 | ML competition longitudinal story | Real narrative | Implies 14× attribution without denominator | Becomes Historical Observation reference; pair with rewritten `case-study-ml.md` | **RENAME** → `ml-competition-historical-observation.md` + **REWRITE** |

---

## Disposition summary

| Action | Count |
|---|---:|
| KEEP | 5 (LICENSE, theoretical-foundations, session-review-template, skill-template, 02-domain-workflow, 03-bug-fix-skill) |
| RENAME | 7 |
| REWRITE | 14 |
| DOWNGRADE | 0 (downgrade is captured via RENAME+REWRITE) |
| REPLACE | 0 |
| DELETE | 0 |
| EXTERNALIZE | 0 |
| **NEW** | 4 (the 00/01/02/03 charter docs) |

No DELETEs in this inventory — every current asset has informational value.
The strategy is **RENAME + REWRITE** rather than deletion to preserve
provenance and reduce contributor friction.

---

## Week 4 additions (2026-08-22)

| File | Role | Disposition |
|---|---|---|
| `schemas/README.md` | Schema registry: versioning, compatibility, freshness model, cross-plane encoding rule | **NEW · KEEP** |
| `schemas/experience-record.schema.json` | ExperienceRecord contract v0.1.0 | **NEW · KEEP** |
| `schemas/evidence-envelope.schema.json` | EvidenceRecord envelope v0.1.0 | **NEW · KEEP** |
| `schemas/capability-record.schema.json` | CapabilityRecord v0.1.0 incl. freshness block; jointly owned with cultivating | **NEW · KEEP** |
| `schemas/policy-record.schema.json` | PolicyRecord v0.1.0; guidance_refs only — no promotion field by construction | **NEW · KEEP** |
| `tools/check_boundaries.sh` | ADR-001 KILL-list enforcement (paths / imports / narratives); legacy allowlist for pre-migration scripts | **NEW · KEEP** |
| `.githooks/pre-commit` | Delegates to checker; enable via `git config core.hooksPath .githooks` | **NEW · KEEP** |
| `CONTRIBUTING.md` | Added "Boundary Hooks" install section | **EDITED** (per earlier REWRITE disposition; full rewrite still pending) |

### Script migration executed (2026-08-22, closes ADR-001 acceptance #6)

| Old path | New path | Change |
|---|---|---|
| `scripts/skill_audit.py` | `scripts/structural_lint.py` | Quality Score removed; Agent-Skills + topprism metadata structural checks; broken-link detection |
| `scripts/skill_consolidation_checker.py` | `scripts/merge_candidate_generator.py` | Candidates only, `requires_human_review: true`; explicit "never merge on similarity" notice |
| `scripts/crystallization_scheduler.py` | `scripts/evidence_freshness_check.py` | mtime/day thresholds removed; classifies from CapabilityRecord freshness block; contradicted ⇒ exit 1 freeze |
| `scripts/capability_assessment.py` | `scripts/capability_review.py` | Dreyfus scoring removed; free-text reflection + evidence refs, marked non-evidence |
| — | `scripts/anf_frontmatter.py` | NEW shared frontmatter parser/discovery (dedupes former copy-paste) |

`tools/check_boundaries.sh` LEGACY_ALLOWLIST emptied accordingly.
Templates referencing the old tools (`capability-matrix-template.md`,
`consolidation-audit-template.md`) still carry their earlier dispositions
(RENAME/REWRITE) — not yet executed.

## Items NOT in this inventory (deliberately)

These do not belong in ANF and are excluded from this repo's responsibilities:

- Any persistence backend (PostgreSQL, SQLite, Vector DB, Graph DB)
- Any HTTP server / API gateway
- Any CLI command suite (anf init / anf capture / anf memory / anf retrieve / anf agent)
- Any MCP server
- Any Web UI / Dashboard
- Any agent runtime / orchestrator
- Any model evaluation harness (this belongs to `skill-tester`)
- Any ML experiment tracker (this belongs to MLflow or `cultivating-ml-agent`)
- Any external knowledge ingestion (this belongs to `notebook-knowledge-distillation`)

If a future contributor wants any of these, they must either:
1. Reuse an existing open-source project (per Reuse First principle), or
2. Build it in the appropriate adapter repo, never in ANF.

---

## Acceptance test for this inventory

Execution status (Week 3, 2026-08-22): doc dispositions EXECUTED.
Rewritten: knowledge-architecture / crystallization-cycle / framework /
fragmentation-management / progress-measurement / README.
Renamed+rewritten: case-study-ml → case-study-ml-historical-observation.
Header-noted (reference-only): theoretical-foundations.
Signed: ADR-001. Added post-inventory with entry: 04_ARCHITECTURE_REVIEW.md.
Pending (code migration, gated on separate approval): the four scripts/ renames
and examples/skills/01 rename — see ADR-001 § Migration Implications.

## Acceptance test for this inventory

- [x] Every file in the repo has one of: KEEP, RENAME, REWRITE, DOWNGRADE, REPLACE, DELETE, EXTERNALIZE applied to it.
- [x] No file has been silently DELETED (preserves provenance; old case-study path preserved via git history).
- [x] No new file has been added without an inventory entry (04 added above).
- [x] The charter docs (`00`, `01`, `02`, `03`, plus `04` review) are present and aligned.
