---
title: Project Direction Charter — Agent Nurture Framework
status: draft (Architecture Reset, Week 1)
created: 2026-08-22
supersedes: implicit positioning from README v0.x
scope: project-level, not implementation-level
audience: TopPrism maintainers, contributors, governance reviewers
---

# 00 · Project Direction Charter

> **One-sentence positioning**
> ANF specifies contracts and governance semantics for organizational agent capability.
> It does not own storage, retrieval, execution, agent orchestration, or user interfaces.

**Architectural law of this charter**

> **Protocol, not Runtime. Governance, not Memory. Evidence, not self-claimed intelligence.**

---

## 1. TopPrism company context

TopPrism is building a Native AI capability stack in which the unit of value is
**validated, evidence-backed, transferable organizational capability**, not raw model
output and not stored conversation logs.

TopPrism already operates (or is building) the following companion projects:

| Project | Role | Implements |
|---|---|---|
| `cultivating-ml-agent` | ML-domain **implementation** | ML engineering capability crystallization + TransferBench |
| `skill-tester` | **Behavioral evaluation** provider | Skill Tester 4-stage pipeline + 4D rubric |
| `notebook-knowledge-distillation` | External knowledge **intake** | External source → validated skill candidate |
| `three-layer-wisdom-extraction` | **Abstraction research** lab | Event → domain knowledge → transferable principle |
| **`agent-nurture-framework` (this repo)** | **Governance protocol** | Contracts, lifecycle, promotion rules, evidence envelope, authority boundary |

These five projects together form a single Native AI capability loop. None of them
is a customer-facing Decision Engine. None of them is a standalone product. Their
combined output is what TopPrism calls "organizational intelligence."

---

## 2. Why ANF exists (the problem only ANF solves)

Most agent systems focus on what an agent can do today:

```text
Model + Prompt + Tools → Task
```

TopPrism's external research partnerships and EvoAgentBench 2026-07 results show
that curated abilities can transfer across models, but **no current self-evolution
method reliably produces positive transfer in all settings**. SkillsBench 2026
finds that even curated skills produce negative gains in ~19% of evaluated tasks.

Three gaps remain after the model / prompt / tools / task loop:

1. **Which lessons should be retained?** — most frameworks keep raw experience, not validated evidence.
2. **Which lessons should be trusted?** — most frameworks conflate trust levels.
3. **Where do they apply, when do they expire, who may promote them, do they actually improve later work?** — most frameworks either skip these questions or answer them heuristically.

ANF is the **protocol layer** that answers these questions.

It is not the memory layer.
It is not the runtime layer.
It is not the registry layer.
It is not the evaluation layer.

It is the **contract** between those layers.

---

## 3. What ANF is

### 3.1 Definition (formal)

> **Agent Nurture Framework is a vendor-neutral governance and evaluation protocol for turning repeated human-agent work into evidence-backed organizational capabilities.**

### 3.2 What ANF delivers

ANF delivers **six Core Contracts**:

| # | Contract | What it specifies | What it does NOT do |
|---|---|---|---|
| 1 | Experience Contract | What counts as an Experience record | It does not capture, store, or transport experience |
| 2 | Evidence Contract | What makes evidence sufficient | It does not execute the validation |
| 3 | Capability Contract | How a capability unit is named and addressed | It does not store capabilities |
| 4 | Lifecycle Protocol | Candidate → Observed → Validated Local → Validated Transfer → Stable → Disputed / Deprecated | It does not execute transitions |
| 5 | Governance Protocol | Who may read / promote / modify / deprecate / publish | It does not enforce; humans + adapters do |
| 6 | Evaluation Protocol | What evidence is required to claim a capability works | It does not run the tests |

### 3.3 What ANF is NOT (the negative definition)

```text
NOT a memory database.
NOT a vector store.
NOT a Postgres / Graph DB / Vector DB backend.
NOT a Web UI.
NOT a dashboard.
NOT an MCP server.
NOT an agent runtime.
NOT a CLI command suite (anf init / anf capture / anf retrieve / anf agent).
NOT a skill registry.
NOT a replacement for Agent Skills specification.
NOT a replacement for any existing memory framework (Prism, Letta, Mem0, LangMem).
```

If a feature is being designed and it falls into one of the categories above,
**it does not belong in ANF**. It belongs in an adapter, an implementation, or
an external project.

---

## 4. ANF vs Cultivating ML Agent — locked boundary

```text
                    Agent Nurture Framework
              Normative / Governance / Protocol
                           │
          ┌────────────────┼────────────────┐
          │                │                │
 Capability Schema    Lifecycle       Evaluation Rules
 Governance           Provenance      Promotion Policy
          │                │                │
          └────────────────┬────────────────┘
                           ↓
                 Domain Implementations
                           │
             ┌─────────────┼─────────────┐
             │             │             │
      Cultivating ML     OR/Optimization  Future domains
          Agent
```

- **ANF** answers: "What governance rules should all domains follow?"
- **Cultivating** answers: "Do these rules actually make the next ML project stronger?"

ANF proposes. Cultivating tests. ANF updates its confidence based on Cultivating
evidence. This forms a closed loop in which ANF never has to fabricate evidence
itself, and Cultivating never has to invent governance rules.

The two projects **must share CapabilityRecord schema** so evidence can be
referenced across them without translation. Schema drift between ANF and
Cultivating is a known failure mode and is tracked.

---

## 5. Authority vs Knowledge — two planes, never mixed

> **The single most important architectural decision in this charter.**

Different things have different authority. They must not be promoted into each
other through the same mechanism.

### Authority Plane (A-plane)

```text
A0 External Policy / Legal
A1 Organization Policy
A2 Team Policy
A3 User Preference
```

A-plane entries **cannot be auto-evolved by agent experience**. They are
authored by humans under explicit governance processes. "Never upload customer
data" and "Always use stratified split for tabular CV" must never sit in the
same promotion pathway, no matter how many times the latter proves correct.

### Knowledge / Capability Plane (K-plane)

```text
Evidence
   ↓
Episodic Memory
   ↓
Candidate Knowledge
   ↓
Validated Capability
   ↓
Transferable Capability
```

K-plane entries **can evolve** based on evidence, but only within risk-bounded
promotion gates (see ADR-001 § Promotion Direction).

### The boundary

```text
K-plane ──→ A-plane  =  DEFAULT PROHIBITED (human approval + audit required)
A-plane ──→ K-plane  =  NOT PROMOTION; produces implementation guidance only
K-plane ──→ K-plane  =  Risk-aware automation allowed
A-plane ──→ A-plane  =  Human governance; ANF has no opinion
```

This boundary is the architectural firewall against the failure mode where an
agent promotes a frequently-useful heuristic into an immovable principle, or
mistakes an organizational constraint for a capability it can refine.

---

## 6. Core research question (research-grade statement)

> **Under what evidence, governance, and transfer conditions can accumulated agent experience become reliable organizational capability without causing harmful transfer?**

This question replaces the older, vaguer framing of "how should an agent learn
across work?" It is precise on four dimensions (evidence, governance,
transfer, harm) and falsifiable. Every ANF v1 proposal must answer at least
one of these four sub-questions; proposals that do not are out of scope.

---

## 7. Reuse First principle

Before any ANF v1 component is designed, an explicit **make / buy / reuse**
analysis must be performed against:

- Agent Skills specification (SKILL.md / scripts / references / assets)
- ProsusAI / Prism
- Letta, Mem0, LangMem
- OpenTelemetry (signals, exporters, semantic conventions)
- OpenLineage (data lineage model)
- MLflow (experiment and model tracking)
- SkillsBench, EvoAgentBench, MUSE-Autoskill, MSCE, HSI

Only when no external project covers a need does ANF define its own contract.

---

## 8. Out-of-scope products (the anti-product list)

To prevent scope creep from manifesting as README marketing language, the
following product narratives are explicitly forbidden:

```text
NO "Autonomous Self-Evolving Agent Platform"
NO "Enterprise Memory OS"
NO "Agent Capability Operating System"
NO "Universal Skill Marketplace"
NO "General Agent Runtime"
NO "All-in-one Organizational Intelligence Platform"
NO "AGI Memory Layer"
NO "Personal Knowledge Vault"
```

Once these phrases enter README or commit messages, downstream scope creep
(database, API, registry, dashboard, runtime, tenant management) becomes
inevitable.

---

## 9. Relationship to current ANF repository

This charter **supersedes** the implicit positioning of the current README
("A general methodology for turning repeated AI-agent work into reusable,
compounding organizational capability") in three ways:

1. It changes the noun from **methodology** to **protocol**.
2. It makes explicit what ANF is not (memory, runtime, registry).
3. It locks the Authority / Knowledge separation as the central architectural decision.

The current repository will be **architecturally reset** under this charter
over the next 8 weeks per the ADR-001 plan.

---

## 10. Acceptance test for this charter

This charter is considered implemented only when **all** of the following are true:

- [ ] `02_ADR-001_PROTOCOL_NOT_RUNTIME.md` exists and is signed.
- [ ] `01_REPOSITORY_INVENTORY.md` exists and every asset has a disposition (KEEP / RENAME / REWRITE / DOWNGRADE / REPLACE / DELETE / EXTERNALIZE).
- [ ] No ANF v1 source file imports a vector DB / SQL DB / ORM / web framework.
- [ ] No ANF v1 source file ships an HTTP server, CLI command group, or MCP server.
- [ ] Every ANF v1 doc mentions Authority Plane and Knowledge Plane explicitly.
- [ ] Schema cross-reference to Cultivating CapabilityRecord exists and is bidirectional.

If any of these is false, this charter has not yet been honored.
