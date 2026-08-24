---
title: External Capability Map — make/buy/reuse analysis
status: draft (Architecture Reset, Week 1)
created: 2026-08-22
purpose: For every external project in scope, document (a) what it already solves,
         (b) what ANF should reuse, (c) what ANF must not duplicate, (d) what
         remains unsolved, (e) integration boundary, (f) decision.
---

# 03 · External Capability Map

This map is the evidence base for the Reuse First principle of the Project
Direction Charter. Every ANF v1 contract must point to an entry here explaining
why ANF is the right place for that contract (or why ANF is **not** the right
place and an adapter must do it instead).

Decision codes:

- **REUSE** — Use this project as-is via reference; do not redefine.
- **ADAPT** — Build a thin ANF-specific layer on top.
- **REFERENCE** — Cite for vocabulary / lineage; no technical dependency.
- **DO NOT BUILD** — Explicit prohibition in ANF; route to this project.

---

## 1. Memory / Runtime layers (MUST NOT duplicate)

### 1.1 ProsusAI / Prism

| Field | Value |
|---|---|
| Repository | `ProsusAI/prism` |
| Mapped need | Persistent memory for Claude Code / Cursor; session pattern extraction |
| What it already solves | Captures patterns from sessions, validates them with AI, surfaces as skills, project/global engrams, team registry, MCP retrieval, correction, forget, knowledge lifecycle, confidence + decay |
| What ANF should reuse | Pattern storage mechanics; team registry concept |
| What ANF must NOT duplicate | Pattern capture; storage engine; session observation; validation pipeline |
| What remains unsolved | Authority boundary (K vs A plane); risk-aware promotion gates; evidence envelope; provenance chain — Prism does not separate "what is policy" from "what is capability" |
| Integration boundary | ANF defines **contracts** that Prism may emit. Prism remains the runtime; ANF governs promotion decisions Prism must consult. |
| Decision | **DO NOT BUILD** a memory engine. **ADAPT** a Prism integration by defining what evidence Prism-collected patterns must carry to be ANF-promotable. |

### 1.2 Letta

| Field | Value |
|---|---|
| Mapped need | Stateful agent memory with reasoning traces |
| What it already solves | Memory blocks, recursive summarization, agent state, tool integration |
| What ANF should reuse | (nothing direct — Letta is a runtime) |
| What ANF must NOT duplicate | Memory blocks; agent state; recursive summarization |
| What remains unsolved | Authority boundary; promotion semantics |
| Integration boundary | Letta could be the K-plane storage target for an ANF adapter; ANF specifies what Letta must record in evidence envelope |
| Decision | **DO NOT BUILD** a parallel memory runtime. **REFERENCE** as one possible runtime target for ANF adapters. |

### 1.3 Mem0

| Field | Value |
|---|---|
| Mapped need | Lightweight persistent memory layer |
| What it already solves | Memory CRUD, fact extraction, retrieval |
| What ANF should reuse | (nothing direct) |
| What ANF must NOT duplicate | Storage; retrieval; fact extraction |
| What remains unsolved | Authority boundary; risk-aware gates; provenance chain |
| Decision | **DO NOT BUILD** parallel infrastructure. **REFERENCE** as alternative runtime. |

### 1.4 LangMem

| Field | Value |
|---|---|
| Mapped need | LangChain-integrated memory |
| What it already solves | Memory search; user profile extraction; procedural memory |
| What ANF should reuse | (vocabulary) |
| What ANF must NOT duplicate | Storage; LangChain-specific integration |
| Decision | **DO NOT BUILD** parallel infrastructure. **REFERENCE**. |

---

## 2. Standards & Specifications

### 2.1 Agent Skills specification

| Field | Value |
|---|---|
| Repository | `agentskills/agentskills` |
| Mapped need | Open format for skill artifacts |
| What it already solves | `SKILL.md` layout; `scripts/`, `references/`, `assets/`; progressive disclosure; metadata schema; validator |
| What ANF should reuse | **Everything physical.** ANF must not redefine physical format. |
| What ANF must NOT duplicate | `SKILL.md` schema; folder layout; validator |
| What remains unsolved | ANF's organizational layer (governance, lifecycle, evidence envelope) **sits above** Agent Skills but does not redefine it |
| Integration boundary | ANF skills are Agent Skills compliant. ANF-specific metadata goes in `metadata.topprism.*` namespace |
| Decision | **REUSE** Agent Skills wholesale. **ADAPT** only at metadata namespace level. |

### 2.2 OpenTelemetry

| Field | Value |
|---|---|
| Mapped need | Vendor-neutral observability protocol |
| What it already solves | Signals (traces, metrics, logs); semantic conventions; exporters; SDKs |
| What ANF should reuse | **Design philosophy**: vendor-neutral, protocol-first, implementation-agnostic. Semantic-convention pattern for naming things. |
| What ANF must NOT duplicate | Trace/metric/log infrastructure |
| What remains unsolved | Capability-as-a-signal is not in OpenTelemetry's scope. ANF may define semantic conventions for `agent.capability.*` signals |
| Integration boundary | ANF can recommend OpenTelemetry exporters for capability events but must not ship an OTel SDK |
| Decision | **REFERENCE** OpenTelemetry as design philosophy. **ADAPT** the semantic-convention pattern for ANF's evidence envelope. |

### 2.3 OpenLineage

| Field | Value |
|---|---|
| Mapped need | Vendor-neutral data lineage |
| What it already solves | Job/Dataset/Run lineage; facet specifications; cross-tool lineage |
| What ANF should reuse | **Design philosophy**: lineage is a first-class concept, not metadata. Facet pattern for typed lineage. |
| What ANF must NOT duplicate | Job/Run/Dataset ontology |
| What remains unsolved | Capability lineage has different semantics than data lineage (no "Run" per se) |
| Integration boundary | ANF's provenance chain contract borrows from OpenLineage's facet model but is a distinct contract |
| Decision | **REFERENCE** OpenLineage as design philosophy. **ADAPT** the facet pattern for ANF provenance. |

### 2.4 MLflow

| Field | Value |
|---|---|
| Mapped need | Experiment and model tracking |
| What it already solves | Run tracking; artifact storage; model registry; project lifecycle |
| What ANF should reuse | (vocabulary; lifecycle stages) |
| What ANF must NOT duplicate | Tracking infrastructure; artifact storage; model registry |
| What remains unsolved | Authority boundary; promotion gates |
| Decision | **REFERENCE** as one possible backend for evidence envelope artifacts. **DO NOT BUILD** parallel infrastructure. |

---

## 3. Evaluation & Benchmarks

### 3.1 SkillsBench (2026)

| Field | Value |
|---|---|
| Paper | arXiv:2602.12670 |
| Mapped need | Behavioral evaluation of agent skills |
| Key finding | Curated skills help on average but **16 of 84 tasks show negative gains**; model-self-generated skills show no average improvement |
| What it implies for ANF | Skills **must not be auto-promoted** without behavioral validation. "Curated" is not the same as "validated" |
| What ANF should adopt | Behavioral evaluation as gate; explicit negative-result tracking |
| What ANF must NOT duplicate | Benchmark harness; per-task scoring |
| Decision | **ADAPT**: ANF requires evaluation evidence (per skill-tester) for promotion beyond Validated Local. **DO NOT BUILD** evaluation infrastructure — `skill-tester` is the ANF-designated evaluation provider. |

### 3.2 EvoAgentBench (2026-07)

| Field | Value |
|---|---|
| Paper | arXiv:2607.05202 |
| Mapped need | Benchmark for agent self-evolution |
| Key finding | Curated abilities transfer across models; **no self-evolution method reliably positive across all settings** |
| What it implies for ANF | "Self-evolving" is currently a marketing term, not an empirical result. ANF must not promise what the field has not demonstrated |
| What ANF should adopt | Explicit transfer-condition enumeration; risk-aware promotion |
| What ANF must NOT duplicate | Benchmark harness; transfer-condition enumeration logic |
| Decision | **REFERENCE** as evidence base for the core research question. **ADOPT** the explicit-transfer-condition framing. |

### 3.3 MUSE-Autoskill

| Field | Value |
|---|---|
| Mapped need | Skill lifecycle research |
| What it already covers | Skill creation / memory / management / evaluation / refinement |
| What it implies for ANF | Lifecycle stages must be explicit; refinement must be evidence-driven |
| Decision | **REFERENCE** for lifecycle vocabulary. **DO NOT BUILD** parallel lifecycle engine. |

### 3.4 MSCE — Memory to Skills: Evidence-Grounded Co-Evolution (2026)

| Field | Value |
|---|---|
| Paper | arXiv:2607.16621 |
| Mapped need | Evidence-grounded skill with applicability boundaries |
| What it already covers | Evidence grounding; applicability boundaries; verification rules; reliability estimates |
| What it implies for ANF | **Strong validation.** ANF's evidence envelope and provenance chain both align with MSCE framing |
| Decision | **ADOPT** vocabulary (applicability boundaries, verification rules, reliability estimates). **REFERENCE** as theoretical backing. |

### 3.5 HSI — Human-Skill Interaction

| Field | Value |
|---|---|
| Mapped need | Human-in-the-loop skill curation |
| What it implies for ANF | Promotion policies must account for human review time; human review is a primary evidence source, not optional |
| Decision | **REFERENCE** for human-loop evidence weighting. |

### 3.6 skill-tester (TopPrism companion)

| Field | Value |
|---|---|
| Repository | `topprismdata/skill-tester` |
| Mapped need | Behavioral evaluation gate for skills |
| What it already covers | 4-stage pipeline (Analysis → Generation → Execution → Evaluation); 4D rubric (Documentation / Code / Completeness / Usability) |
| What ANF should adopt | skill-tester is the **designated evaluation provider** for ANF promotion gates |
| What ANF must NOT duplicate | Baseline-vs-with-skill comparison; rubric definitions |
| Integration boundary | ANF defines what evidence a promotion gate requires; skill-tester produces that evidence |
| Decision | **ADOPT** as evaluation provider. ANF Evidence Envelope must accommodate skill-tester output schema. |

---

## 4. Theoretical grounding

### 4.1 Nurture-First Development (NFD) — Zhang 2026

| Field | Value |
|---|---|
| Paper | arXiv:2603.10808 |
| Mapped need | Theoretical underpinning of the nurture-first approach |
| What it implies for ANF | Knowledge crystallization is one valid theoretical lens; not the only one |
| What ANF should adopt | Crystallization vocabulary; experience-validated lessons |
| What ANF must NOT duplicate | NFD itself; NFD is a theory, ANF is a protocol that may be inspired by it |
| Decision | **REFERENCE** as one of several theoretical sources. **DO NOT** treat NFD as the defining architecture of ANF. |

### 4.2 SECI / Nonaka-Takeuchi

| Field | Value |
|---|---|
| Mapped need | Knowledge conversion theory |
| Decision | **REFERENCE** only. Do not let SECI drive architecture decisions. |

### 4.3 Dreyfus skill model

| Field | Value |
|---|---|
| Mapped need | Skill acquisition stages (Novice → Expert) |
| What it implies for ANF | Mean of ordinal 1-5 scores is statistically weak (per ADR-001 § Rejected Alt) |
| Decision | **REFERENCE** as background reading. **DO NOT** use averaged ordinal scores as evidence. |

### 4.4 Kolb learning cycle / cognitive apprenticeship

| Field | Value |
|---|---|
| Decision | **REFERENCE** only. |

---

## 5. Cultivating ML Agent (TopPrism companion)

| Field | Value |
|---|---|
| Repository | `topprismdata/cultivating-ml-agent` |
| Role | ML-domain implementation of nurture-first ideas; TransferBench |
| What it provides | Real evidence base for ANF contracts; ML CapabilityRecord format |
| What ANF should adopt | CapabilityRecord schema (shared) |
| What ANF must NOT duplicate | ML-specific TransferBench logic |
| Integration boundary | ANF CapabilityRecord schema MUST match Cultivating CapabilityRecord schema v1 — no schema drift |
| Decision | **ADOPT** shared CapabilityRecord. **REFERENCE** Cultivating as evidence provider for ML-domain capabilities. |

---

## 6. notebook-knowledge-distillation (TopPrism companion)

| Field | Value |
|---|---|
| Repository | `topprismdata/notebook-knowledge-distillation` |
| Role | External knowledge → skill candidate pipeline |
| What it implies for ANF | External source → validated candidate flow aligns with K-plane |
| Decision | **REFERENCE** as External Knowledge Intake adapter for ANF. |

---

## 7. three-layer-wisdom-extraction (TopPrism companion)

| Field | Value |
|---|---|
| Repository | `topprismdata/three-layer-wisdom-extraction` |
| Role | Abstraction research lab (Event → Domain Knowledge → Transferable Principle) |
| Status | Currently restricted to proving abstraction structure; downstream decision impact not yet proven |
| What it implies for ANF | Abstraction operations (summarize, merge, abstract) are the highest-risk transformations; they need provenance tracking |
| Decision | **REFERENCE** as research lab. When mature, the abstraction operations become ANF-defined `transformations` in the provenance chain. |

---

## 8. Make/Buy/Reuse summary

| Need | Status | Where it lives |
|---|---|---|
| Physical skill format | REUSE | Agent Skills spec |
| Memory engine | DO NOT BUILD | Prism / Letta / Mem0 / LangMem |
| Memory observability philosophy | REFERENCE | OpenTelemetry |
| Data lineage philosophy | REFERENCE | OpenLineage |
| Experiment tracking | REFERENCE | MLflow |
| Behavioral evaluation | ADOPT | `skill-tester` (designated provider) |
| ML-domain capability evidence | ADOPT | `cultivating-ml-agent` |
| External knowledge intake | REFERENCE | `notebook-knowledge-distillation` |
| Abstraction research | REFERENCE | `three-layer-wisdom-extraction` |
| Theoretical grounding | REFERENCE | NFD / SECI / Dreyfus / Kolb |
| Evidence-grounded vocabulary | ADOPT | MSCE 2026 |
| Skill lifecycle vocabulary | REFERENCE | MUSE-Autoskill |
| Transfer-condition framing | ADOPT | EvoAgentBench 2026-07 |
| Promotion policy lessons | ADOPT | SkillsBench 2026 negative-gain finding |
| Human-loop evidence weighting | REFERENCE | HSI |
| Authority boundary (K vs A) | **DEFINE HERE** | ANF |
| Risk-aware promotion gates | **DEFINE HERE** | ANF |
| Evidence envelope contract | **DEFINE HERE** | ANF |
| Provenance chain contract | **DEFINE HERE** | ANF |
| CapabilityRecord shared schema | **DEFINE HERE + Cultivating** | joint ownership |

**Conclusion.** Of the 20 needs surveyed, ANF should define exactly **5**
contracts (Authority boundary, Promotion gates, Evidence envelope, Provenance
chain, shared CapabilityRecord schema). All other needs have an existing home.

---

## 9. Acceptance test for this map

This map is honored when:

1. [ ] Every ANF v1 contract cites at least one entry here explaining its scope.
2. [ ] No ANF v1 contract duplicates what REUSE / DO NOT BUILD entries cover.
3. [ ] At least one ADAPT entry (skill-tester, cultivating, notebook-distillation) has a documented schema-version compatibility test.
4. [ ] All DO NOT BUILD entries are also reflected in ADR-001 KILL list.
