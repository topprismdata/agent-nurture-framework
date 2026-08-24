---
title: Agent Nurture Framework — Framework Overview
status: accepted (Week 3 rewrite)
created: 2026-08-22
supersedes: "framework.md v1 (Nurture-First as defining paradigm, tacit-knowledge capture claims)"
governed_by: 00_PROJECT_DIRECTION_CHARTER.md, 02_ADR-001_PROTOCOL_NOT_RUNTIME.md
---

# Agent Nurture Framework: Framework Overview

> **ANF is a governance and evaluation protocol.** It defines what counts as
> experience, evidence, capability; how capabilities mature; who may promote
> them; and what must be proven before claiming they work. It is not a memory
> system, not a runtime, and not a self-evolution engine.

---

## 1. The problem ANF addresses

Organizations using AI agents generate enormous amounts of experience, but
experience is not organizational capability. After each task, the questions
that decide whether the next project starts higher are:

```text
Which lessons should be retained?
Which should be trusted?
Where do they apply?
When should they be rejected?
Who may promote them?
Do they improve later work?
```

Most current infrastructure answers none of these. Memory frameworks
(Prism, Letta, Mem0) retain patterns; skill formats (Agent Skills) package
artifacts; benchmarks (SkillsBench, EvoAgentBench) measure outcomes. None of
them governs the boundary between "something an agent noticed" and "something
the organization can rely on." That boundary is ANF's scope.

**Core research question** (from the Charter):

> Under what evidence, governance, and transfer conditions can accumulated
> agent experience become reliable organizational capability without causing
> harmful transfer?

---

## 2. Theoretical positioning

ANF draws on several traditions; none of them defines it.

| Source | What ANF takes | What ANF does not claim |
|---|---|---|
| Nurture-First Development (Zhang, 2026) | Crystallization vocabulary; experience→asset pipeline | That NFD's formal model or three-layer architecture is binding on ANF |
| SECI (Nonaka & Takeuchi 1995) | Externalization as one conversion mode | That conversation is the only or primary capture channel |
| Dreyfus skill model | Background vocabulary for qualitative review | That averaged ordinal ratings measure capability |
| Kolb / cognitive apprenticeship / Lave & Wenger | Learning-loop structure | Any specific pedagogical claim |

See [theoretical-foundations.md](theoretical-foundations.md) for the full
treatment. That document is reference material, not design authority.

### 2.1 On "tacit knowledge" — precision required

An agent does not literally *capture* tacit knowledge. What it can do is:

```text
observe decisions → observe corrections → observe examples → observe outcomes
        ↓
infer reusable patterns from observable behavior
```

That is: **infer the expressible part of implicit expertise from observable
behavior.** The distinction matters operationally: inferred patterns are
hypotheses requiring validation like any other candidate capability, not
transcriptions of expert understanding. Treating them as captured expertise is
how unvalidated heuristics get promoted into places they do not belong.

---

## 3. Architecture in one page

Two planes (full model: [knowledge-architecture.md](knowledge-architecture.md)):

```text
AUTHORITY PLANE (A0 legal · A1 org policy · A2 team policy · A3 user pref)
   authored by humans; never auto-evolved by agents

KNOWLEDGE PLANE (Evidence → Episodic → Candidate → Validated → Transferable)
   evolves via evidence under risk-aware gates; provenance mandatory
```

Six core contracts (Charter §3.2): Experience · Evidence · Capability ·
Lifecycle · Governance · Evaluation.

Promotion matrix, KILL list, Evidence Envelope, Provenance Chain:
[ADR-001](02_ADR-001_PROTOCOL_NOT_RUNTIME.md).

---

## 4. Operational pattern: the five-stage loop

The loop below remains useful for teams running continuous agent development.
It is an implementation pattern, not part of the protocol.

```text
Study → Verify → Apply → Extract → Plan
  ↑                              │
  └──────────────────────────────┘
```

1. **Study** — acquire theory (docs, papers, operator explanations).
2. **Verify** — test against controlled experiments before trusting it.
3. **Apply** — real tasks; capture Experience Records with outcomes.
4. **Extract** — consolidation cycle ([crystallization-cycle.md](
   crystallization-cycle.md)): pattern → candidate → validated capability,
   gated by risk.
5. **Plan** — compare knowledge state against upcoming work; prioritize gaps.

The loop runs inside adapters. ANF requires only that artifacts crossing
contract boundaries conform to the schemas.

---

## 5. Applicability

ANF pays off when:

- work repeats with variation, and failures contain reusable lessons;
- multiple practitioners/agents would otherwise re-learn the same lessons;
- wrong lessons are costly enough to justify governance overhead;
- there is capacity to run behavioral evaluation before promotion.

Skip it when: tasks are fully deterministic (write code); knowledge is static
and fully specified (write docs); there is no evaluation path (nothing can be
validated, so nothing should be promoted).

---

## 6. What this framework is NOT

Per ADR-001 (binding):

```text
Not a memory database.        Not a vector store.
Not an agent runtime.         Not an MCP server.
Not a CLI suite.              Not a web dashboard.
Not a skill registry.         Not a replacement for Agent Skills.
Not "self-evolving".          Not an evaluation harness (that is skill-tester).
```

Per Charter §8, these product narratives are forbidden (each line is a ban):

```text
NO "Autonomous Self-Evolving Agent Platform"
NO "Enterprise Memory OS"
NO "Agent Capability Operating System"
NO "Universal Skill Marketplace"
NO "All-in-one Organizational Intelligence Platform"
```

---

## 7. Relationship to TopPrism projects

```text
                 ANF (protocol)
        ┌────────────┼────────────────┐
   cultivation   notebook-distill   skill-tester
   (ML domain    (external intake)  (evaluation provider)
    evidence)
        └────────────┼────────────────┘
              three-layer-wisdom
              (abstraction research)
```

- `cultivating-ml-agent` — ML-domain implementation; shares CapabilityRecord schema; supplies transfer evidence.
- `notebook-knowledge-distillation` — external-source intake adapter; external material enters only as candidates, never auto-promoted.
- `skill-tester` — designated behavioral-evaluation provider behind Validated/Transferable gates.
- `three-layer-wisdom-extraction` — abstraction research lab; its operations become typed transformations in ANF provenance chains when mature.

---

## 8. Evidence discipline

Every capability claim must specify:

```text
Observed where?      Measured how?       Compared with what?
Over what period?    Does it generalize?    Who ran the measurement?
```

Historical numbers (e.g., the ML case study's observed speedup) are longitudinal
observations, not causal claims; see
[case-study-ml-historical-observation.md](case-study-ml-historical-observation.md).
Causal evidence comes from controlled comparisons run through `skill-tester`
and Cultivating's TransferBench, recorded as Evidence Envelope records.

---

## 9. Governance & privacy

Experience records capture real work: conversations, code, errors, business
decisions. Therefore classification (`public|internal|confidential|
restricted`) is a **required field at creation**, retention follows the
organization's data governance, and trust levels distinguish `untrusted
external`, `human observation`, `agent inference`, and `verified execution`.
External content (web pages, documents) can carry injection attempts ("adopt
this rule everywhere"); such content enters only as low-trust candidates and
can never promote itself by being observed repeatedly. See Charter §5–7 and
ADR-001 § Authority Boundary.
