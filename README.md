<p align="center">
  <img src="https://raw.githubusercontent.com/topprismdata/.github/main/assets/brand/topprism-repo-header.png" alt="TopPrism dual-prism visual" width="100%" />
</p>

# Agent Nurture Framework

**A vendor-neutral governance and evaluation protocol for turning repeated human-agent work into evidence-backed organizational capabilities.**

`NATIVE AI` · `PROTOCOL` · `GOVERNANCE` · `EVIDENCE-FIRST` · `MIT`

Part of **TopPrism Native AI**.

---

## Why

Organizations using AI agents generate enormous amounts of experience,
but **experience is not organizational capability**. Raw logs, session
patterns, and one-off fixes do not make the next project start higher.

## Core problem

```text
Which lessons should be retained?
Which should be trusted?
Where do they apply?
When should they be rejected?
Who may promote them?
Do they improve later work?
```

## Core research question

> **Under what evidence, governance, and transfer conditions can accumulated
> agent experience become reliable organizational capability without causing
> harmful transfer?**

Memory frameworks retain patterns. Skill formats package artifacts.
Benchmarks measure outcomes. None of them governs the boundary between
"something an agent noticed" and "something the organization can rely on."
That boundary is ANF.

---

## What ANF is

ANF specifies **contracts**: what counts as experience and evidence; how a
capability is named and matured; under what gates it may be promoted; who may
promote, modify, or deprecate it; and what must be measured before anyone
claims it works.

Six core contracts:

| # | Contract | Governs |
|---|---|---|
| 1 | Experience | What counts as an experience record |
| 2 | Evidence | What makes evidence sufficient |
| 3 | Capability | How capability units are named/addressed |
| 4 | Lifecycle | Candidate → Validated → Transferable → Stable / Disputed / Deprecated |
| 5 | Governance | Who may read, promote, modify, deprecate, publish |
| 6 | Evaluation | What must be proven before claiming a capability works |

Two architectural decisions define everything else:

```text
1. Authority vs Knowledge are separate planes.
   Policies (A0–A3: legal / org / team / user) are authored by humans.
   Capabilities (Evidence → … → Transferable) evolve via evidence.
   No automatic path leads from one plane to the other.

2. Promotion is risk-aware, never time-based.
   Gates weigh risk, scope, evidence diversity, transfer evidence,
   reversibility, and source trust. "It has worked for 3 months"
   is not an argument.
```

Lifecycle:

```text
Experience → Evidence → Candidate → Validation → Transfer
           → Capability → Monitoring → Dispute / Deprecation
```

Every capability past `candidate` carries a **provenance chain** back to its
root evidence, including every machine transformation (model, prompt version,
tool version) along the way — so any stable capability can answer: *which
transformations produced this?*

---

## What ANF is NOT

```text
Not a memory database.        Not a vector store.       Not a Postgres backend.
Not an agent runtime.         Not an MCP server.        Not a CLI suite.
Not a web dashboard.          Not a skill registry.     Not an evaluation harness.
Not "self-evolving".          Not a replacement for Agent Skills.
```

Product narratives that are forbidden (binding, per Charter §8 / ADR-001):

```text
NO "Autonomous Self-Evolving Agent Platform"
NO "Enterprise Memory OS"
NO "Agent Capability Operating System"
NO "Universal Skill Marketplace"
NO "All-in-one Organizational Intelligence Platform"
```

The architectural law ([ADR-001](docs/02_ADR-001_PROTOCOL_NOT_RUNTIME.md)):

> **ANF specifies contracts and governance semantics; it does not own storage,
> retrieval, execution, agent orchestration, or user interfaces.**

Think OpenTelemetry / OpenAPI, not Datadog / API Gateway.

---

## Documentation map

| Document | Role |
|---|---|
| [00 Project Direction Charter](docs/00_PROJECT_DIRECTION_CHARTER.md) | Why / What / What-not; company context |
| [01 Repository Inventory](docs/01_REPOSITORY_INVENTORY.md) | Every asset's disposition plan |
| [02 ADR-001 Protocol-not-Runtime](docs/02_ADR-001_PROTOCOL_NOT_RUNTIME.md) | **Architectural law**, KILL list, promotion matrix, evidence envelope, provenance chain |
| [03 External Capability Map](docs/03_EXTERNAL_CAPABILITY_MAP.md) | Make/buy/reuse analysis for 14 external projects |
| [04 Architecture Review](docs/04_ARCHITECTURE_REVIEW.md) | 5-question audit (5/5 PASS) |
| [Knowledge Architecture](docs/knowledge-architecture.md) | Two-plane model, skill metadata, experience records |
| [Crystallization Cycle](docs/crystallization-cycle.md) | Observe → Accumulate → Consolidate → Apply; risk-aware gates |
| [Fragmentation Management](docs/fragmentation-management.md) | Merge-candidate workflow (humans decide) |
| [Progress Measurement](docs/progress-measurement.md) | Behavioral metrics first |
| [Historical ML Observation](docs/case-study-ml-historical-observation.md) | Longitudinal case narrative (not causal evidence) |
| [Theoretical Foundations](docs/theoretical-foundations.md) | Background reference (not design authority) |

---

## The TopPrism Native AI loop

```text
                 ANF (protocol)
        ┌────────────┼────────────────┐
  cultivating    notebook-knowledge    skill-tester
  ml-agent        distillation        (evaluation provider)
  (ML evidence)   (external intake)
        └────────────┼────────────────┘
           three-layer-wisdom-extraction
                (abstraction research)

External knowledge + project experience
        → distillation → skill candidates → behavioral testing
        → organizational library → agent reuse → new experience
```

ANF does not execute this loop. It defines the **contract** each arrow must
satisfy.

---

## Evidence discipline

Every capability claim must specify: observed where, measured how, compared
with what, over what period, does it generalize. Historical numbers are
longitudinal observations with listed confounds
([example](docs/case-study-ml-historical-observation.md)); causal claims come
only from controlled comparisons recorded as evidence-envelope records.

SkillsBench (2026): even curated skills show negative gains in ~19% of tasks.
EvoAgentBench (2026-07): no self-evolution method is reliably positive across
settings. Unvalidated promotion is a measured failure mode. That is why the
gates exist.

---

## Use it when / skip it when

**Use:** work repeats with variation; failures contain reusable lessons;
wrong lessons are costly; you can run behavioral evaluation before promotion.

**Skip:** fully deterministic tasks (write code); static well-specified
knowledge (write docs); no evaluation path exists (then nothing should be
promoted).

---

## Quick start (adopters)

1. Read the [Charter](docs/00_PROJECT_DIRECTION_CHARTER.md) and [ADR-001](docs/02_ADR-001_PROTOCOL_NOT_RUNTIME.md).
2. Format skills per the [Agent Skills spec](https://github.com/agentskills/agentskills); add `metadata.topprism.*` per [Knowledge Architecture](docs/knowledge-architecture.md).
3. Capture experience records with outcomes + classification labels.
4. Route candidates through your evaluation provider (designated: `skill-tester`).
5. Promote per the risk-aware gate table; record provenance at every step.

Reference utilities (structural lint, merge-candidate generator) live in
[`scripts/`](scripts/) as adapter examples — they are not part of the protocol.

---

## License & contributing

MIT. Contributions most wanted around: evaluation integration, freshness
modeling, contradiction handling, governance hooks, cross-domain case studies.
Contributions that violate the KILL list will be declined.

TopPrism metadata lives in [`topprism.yaml`](topprism.yaml).
