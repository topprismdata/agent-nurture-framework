---
title: Knowledge Architecture — Two-Plane Model
status: accepted (Week 3 rewrite)
created: 2026-08-22
supersedes: "Three-Layer Cognitive Architecture (L1/L2/L3)"
governed_by: 02_ADR-001_PROTOCOL_NOT_RUNTIME.md
---

# Knowledge Architecture: The Two-Plane Model

> **Architectural law** (from ADR-001):
> Policy and Capability are not parent-child knowledge. They are different
> authority ontologies. No automatic promotion path exists between them.

The earlier revision of this document organized all agent knowledge into three
layers (L1 Constitutional / L2 Skill / L3 Experiential) and allowed upward
promotion between them. That design had a governance flaw: it placed rules of
different **authority** ("never upload customer data") and statements of
different **maturity** ("prefer stratified split") on a single promotion path,
so that a frequently-useful capability could drift into the authority layer
through accumulation alone.

This revision separates the two concerns into independent planes.

---

## 1. The two planes

```text
+==========================================================+
|  AUTHORITY PLANE (A-plane) — authored by humans           |
|                                                          |
|  A0  External Policy / Legal / Regulatory                |
|  A1  Organization Policy                                 |
|  A2  Team Policy                                         |
|  A3  User Preference                                     |
|                                                          |
|  Volatility: governed by policy processes, not by agents |
|  Evolution: human authorship + explicit governance only  |
+==========================================================+

+==========================================================+
|  KNOWLEDGE / CAPABILITY PLANE (K-plane) — evolves via     |
|  evidence                                                |
|                                                          |
|  Evidence                                                |
|    → Episodic Memory                                     |
|      → Candidate Capability                              |
|        → Validated Capability                            |
|          → Transferable Capability                       |
|            → General Principle                           |
|                                                          |
|  Lifecycle states: Draft · Active · Refining · Stable ·  |
|                    Disputed · Deprecated                 |
|  Evolution: risk-aware automation WITHIN K-plane only    |
+==========================================================+
```

### 1.1 Authority Plane (A-plane)

| Level | Content | Examples | Authored by |
|---|---|---|---|
| A0 | External / legal constraints | GDPR, license terms, client contracts | Legal, regulators |
| A1 | Organization policy | "Never upload customer data to third-party APIs" | Org leadership |
| A2 | Team policy | "All PRs require one reviewer" | Team leads |
| A3 | User preference | "Answer in Chinese; concise tone" | Individual user |

Properties:

- A-plane entries are **binding**, not advisory. They constrain which
  capabilities may execute at all.
- A-plane entries are **version-controlled and change-reviewed by humans**.
- An agent may *propose* an A-plane edit through the governance channel, but
  proposal ≠ promotion; see §3.

### 1.2 Knowledge Plane (K-plane)

| Stage | Meaning | Gate to enter |
|---|---|---|
| Evidence | Raw observation with context (decision, action, outcome) | Captured by an adapter conforming to the Evidence Envelope |
| Episodic Memory | Structured experience records, searchable | Automatic from Evidence |
| Candidate Capability | Pattern extracted and structured as a skill draft | Risk-aware automation |
| Validated Capability | Passes behavioral evaluation in its origin context | Evaluation provider output (`skill-tester`) required |
| Transferable Capability | Validated in ≥ 2 distinct contexts | Multi-context validation evidence |
| General Principle | Abstract, domain-independent guidance | Stronger evidence + human review (still K-plane) |

Lifecycle states: `Draft → Active → Refining → Stable`, plus `Disputed` and
`Deprecated`. State transitions follow the Lifecycle Protocol (Charter §3.2,
contract #4).

---

## 2. Why L1/L2/L3 was retired

| Old concept | Problem | Replacement |
|---|---|---|
| L1 Constitutional containing both principles *and* capability indices | Mixed binding rules (authority) with descriptive summaries (capability) | Authority plane holds binding rules; K-plane holds capability descriptions |
| L2 → L1 promotion after "cross-domain validation + 3 months stability" | Frequency of success is not authority. "Prefer TDD" proven in 100 projects still must not become an immovable constitutional rule by accumulation alone | Capability → General Principle stays in K-plane; Capability → Policy is prohibited without human approval + audit |
| Time-based maturity ("stable for 3 months") | Age does not imply validity; a volatile API skill can expire in weeks while a theorem never stales | Promotion gates = f(risk, scope, evidence diversity, transfer evidence, reversibility, source trust). No time term |
| `HasReasoningTrace(k)` crystallization gate | Requires model-internal reasoning; not portable across platforms, and a privacy/governance liability | Decision/Evidence Trace: `decision_summary`, `evidence_refs`, `execution_trace`, `outcome` |

The historical text remains available in git history for provenance.

---

## 3. Cross-plane rules

```text
K-plane ──→ A-plane   DEFAULT PROHIBITED.
                      Requires human approval + independent audit (ADR-001
                      Promotion Matrix). There is no automatic path.

A-plane ──→ K-plane   NOT PROMOTION.
                      Policies can generate implementation guidance
                      (e.g., a data-handling policy produces a checklist
                      capability), but the policy itself never becomes a
                      capability or vice versa.

K-plane ──→ K-plane   Risk-aware automation allowed per Promotion Matrix.

A-plane ──→ A-plane   Human governance. ANF has no opinion.
```

Any artifact that claims to have been promoted from K-plane to A-plane without
a recorded human approval + audit record is invalid under this architecture.

---

## 4. Skill documents

Physical format follows the **Agent Skills specification** (`SKILL.md`,
`scripts/`, `references/`, `assets/`). ANF adds organizational metadata in its
own namespace:

```yaml
---
name: my-skill                     # Agent Skills standard fields
description: ...
# ... standard Agent Skills frontmatter ...

metadata:
  topprism:
    capability_id: cap-2026-0822-001
    lifecycle_status: validated    # draft|active|refining|stable|disputed|deprecated
    risk_level: low|medium|high
    scope: personal|project|team|organization
    evidence_ids: [ev-...]
    provenance_chain_id: prov-...
    last_verified: 2026-08-22
    last_contradicted: null
---
```

### 4.1 Required provenance

Every capability at `validated` or beyond MUST reference a provenance chain
(see ADR-001 § Provenance chain contract):

- `root_evidence_ids[]` → raw observations
- `lineage[]` → each transformation step with producer identity
- `transformations[]` → every LLM transformation with model + prompt_version +
  tool_version

A capability that cannot answer *"which machine transformations produced
this?"* is not promotable past `candidate`.

---

## 5. Experience records

Experience records are the raw material of the K-plane. Each record captures
observable behavior, not model internals:

```yaml
experience_record:
  record_id: exp-...
  task: what was being attempted
  context: environmental factors
  decision: what was decided
  decision_summary: 1-3 sentence rationale (human-readable)
  action: what was executed
  execution_trace: tool calls / commands run (references, not full dumps)
  outcome: observed result (success/failure/partial + metric if available)
  correction: any operator correction applied afterward
  classification: public|internal|confidential|restricted
  timestamp: ISO-8601 UTC
```

Note the deliberate absence of `chain_of_thought` / `reasoning_trace` fields.
What matters for crystallization is the **decision, its observable evidence,
and the outcome** — not the model's internal monologue.

---

## 6. Information flow summary

```text
Grounding (A → K influence):
  Policies shape which capabilities may load and how they apply.
  Example: an A1 rule forbidding PII export disables capabilities that
  would transmit customer rows to external services.

Crystallization (within K):
  Evidence → Episodic → Candidate → Validated → Transferable → Principle,
  gated by risk-aware promotion (ADR-001), with provenance recorded at every
  transformation step.

Lateral coordination (within K):
  Capabilities declare dependencies in Agent Skills frontmatter; shared
  episodic records link capabilities that co-occur on tasks, enabling
  merge-candidate discovery without tight coupling.
```

---

## 7. Acceptance checks for this document

- [x] No layer conflates authority with capability.
- [x] No automatic K-plane → A-plane path exists.
- [x] No time-based maturity gate remains.
- [x] Skill physical format defers to Agent Skills spec.
- [x] Provenance chain required before `validated`.
