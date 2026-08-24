---
title: ADR-001 — ANF is a Protocol, not a Runtime
status: accepted (signed by maintainer via chat confirmation, 2026-08-22)
created: 2026-08-22
supersedes: implicit "methodology + scripts" positioning
deciders: TopPrism maintainers
consulted: Prism authors (via public docs), SkillsBench 2026, EvoAgentBench 2026-07
informed: MSCE 2026, MUSE-Autoskill 2026
---

# 02 · ADR-001 — ANF is a Protocol, not a Runtime

> **Status:** ACCEPTED. This ADR is an Architectural Law of the repository.
> Signed 2026-08-22 following the Architecture Review (`04_ARCHITECTURE_REVIEW.md`, 5/5 PASS).

---

## Context

The original ANF repository positioned itself as a "general methodology for
turning repeated AI-agent work into reusable, compounding organizational
capability." It shipped seven markdown docs, four Python scripts, five
templates, and three example skills.

Between the original framing (early 2026) and now (August 2026), the
external landscape has changed materially:

| External project | What it now covers |
|---|---|
| ProsusAI / Prism | Persistent memory, session-pattern extraction, validators, confidence, decay, project/global engrams, team registry, MCP retrieval, correction, knowledge lifecycle |
| Agent Skills spec | Open standard: SKILL.md, scripts/, references/, assets/, progressive disclosure, validator |
| Letta, Mem0, LangMem | Production memory frameworks |
| SkillsBench 2026 | Behavioral evaluation; shows 16/84 curated skills produce negative gains |
| EvoAgentBench 2026-07 | Self-evolution benchmark; no method reliably positive across all settings |
| MSCE 2026 | Evidence-grounded skill with applicability boundaries, verification rules, reliability estimates |
| MUSE-Autoskill 2026 | Skill creation / memory / management / evaluation / refinement lifecycle |

Re-implementing any of these inside ANF would violate TopPrism's Reuse First
principle and would put ANF in direct, losing competition with mature
upstream projects.

ANF must therefore **stop building infrastructure and start specifying
contracts.** This ADR formalizes that decision.

---

## Decision

**Agent Nurture Framework is a protocol.**

It specifies contracts, lifecycle semantics, governance rules, evidence
envelopes, and authority boundaries. It does **not** own:

```text
- Storage (databases, vector stores, file layout as authoritative)
- Retrieval (search engines, semantic indices, retrieval APIs)
- Execution (agent runtimes, tool invokers, job schedulers)
- Orchestration (multi-agent coordination, workflow engines)
- User interfaces (CLI commands, web dashboards, APIs)
- Evaluation (running behavioral tests, scoring, ranking)
- Ingestion (parsing, transforming, embedding external sources)
```

**Architectural law:**

> **ANF specifies contracts and governance semantics; it does not own storage,
> retrieval, execution, agent orchestration, or user interfaces.**

Any contribution that conflicts with this law shall be rejected during review,
even if it is technically attractive.

---

## Non-goals / KILL list

### Infrastructure (technology)

```text
NO Postgres
NO SQLite
NO Vector DB (Qdrant, Milvus, Weaviate, Chroma, pgvector)
NO Graph DB (Neo4j, Memgraph)
NO ORM (SQLAlchemy, Prisma equivalent)
NO HTTP server (FastAPI, Flask, Express)
NO gRPC / message queue
NO Web framework
NO CLI command suite (anf init / anf capture / anf memory / anf retrieve / anf agent / anf registry / anf mcp)
NO MCP server
NO Web UI / dashboard
NO React / Vue / Svelte component
NO Docker / Kubernetes deployment YAML
NO authentication / authorization infrastructure (OAuth, JWT, RBAC, ABAC)
```

### Product narratives (marketing)

```text
NO "Autonomous Self-Evolving Agent Platform"
NO "Enterprise Memory OS"
NO "Agent Capability Operating System"
NO "Universal Skill Marketplace"
NO "General Agent Runtime"
NO "All-in-one Organizational Intelligence Platform"
NO "AGI Memory Layer"
NO "Personal Knowledge Vault"
NO "Auto-curating" without human review
NO "Self-improving" without explicit promotion evidence
```

If any of these phrases appears in a commit message, README, or issue title,
the contribution must be reframed or rejected.

---

## Authority boundary

ANF recognizes exactly two ontological planes:

```text
Authority Plane (A-plane):
  A0 External Policy / Legal
  A1 Organization Policy
  A2 Team Policy
  A3 User Preference

Knowledge / Capability Plane (K-plane):
  Evidence
  → Episodic Memory
  → Candidate Knowledge
  → Validated Capability
  → Transferable Capability
```

A-plane entries are authored by humans under explicit governance processes.
They cannot be auto-promoted from K-plane entries regardless of how often the
underlying capability has proven useful.

K-plane entries evolve under risk-aware automation, but **only within K-plane**.

---

## Promotion direction (the 2-D state machine)

Every promotion in ANF is governed by **two independent dimensions**:

1. **Knowledge Maturity**: how well-evidenced and stable is the candidate?
2. **Authority Boundary**: is the destination within K-plane or A-plane?

### Promotion matrix (the law)

| Source → Destination | Default policy |
|---|---|
| Evidence → Candidate Capability | Automatic |
| Candidate → Validated Capability | Risk-aware automation |
| Validated → Transferable | Multi-context validation required |
| Transferable → General Principle | Medium risk; stronger evidence required |
| **Capability → Team Policy (A2)** | **Default prohibited** |
| **Capability → Organization Policy (A1)** | **Human approval + independent audit required** |
| **Capability → External Policy (A0)** | **Human + legal governance only** |
| External Policy → Organization Policy | Human/legal governance (not ANF's domain) |
| Policy → Capability | **Not promotion**. Produces implementation guidance only |

### The rule that must be visible in every PR

> **Policy and Capability are not parent-child knowledge. They are different
> authority ontologies. No automatic promotion path exists between them.**

---

## Evidence envelope (the minimal contract)

Every evidence record submitted to ANF must include:

```yaml
evidence_envelope:
  evidence_id:                    # globally unique, stable

  capability_id:                  # the capability being evidenced
  skill_id:                       # Agent-Skills-compliant skill identifier

  evidence_type:                  # task_success | task_failure | negative_transfer
                                  # | correction | contradiction | dispute

  source_system:                  # cultivating | skill-tester | human-review
                                  # | external-adapter

  measurement_protocol:           # how this evidence was generated
  protocol_version:               # version of the protocol used

  metric_name:                    # e.g. "balanced_accuracy", "harmful_transfer_count"
  metric_value:                   # numeric or categorical
  metric_version:                 # which version of the metric definition

  task_id:                        # identifier of the specific task
  task_family:                    # cluster identifier for transfer analysis

  executor:
    name:                         # which agent / model / human produced this
    version:                      # version of the executor

  artifact_refs: []               # IDs of supporting artifacts

  provenance_chain_id:            # pointer to full lineage record

  timestamp:                      # ISO-8601 UTC
```

This envelope is **minimal**, not maximal. ANF accepts additional fields from
adapters but does not require them. Adapters that strip fields ANF requires
must fail closed.

---

## Provenance chain contract

Provenance is **a first-class contract**, not a metadata field.

```yaml
provenance:
  root_evidence_ids: []            # original raw observations

  lineage:
    - artifact_id:                # unique within lineage
      artifact_type:               # raw | transformation | extraction | candidate
      operation:                   # summarize | deduplicate | abstract | merge | correct
      producer:                    # which process produced this step
      producer_version:
      input_ids: []                # artifacts consumed
      output_id:                   # artifact produced
      timestamp:

  current_artifact_id:

  transformations:
    - type:                       # llm_transformation | summarization | deduplication
                                  # | abstraction | merge | human_correction
      model:                      # if LLM was used
      prompt_version:
      tool_version:
```

The most dangerous knowledge-poisoning attacks happen not at raw observation,
but during **LLM transformation** (summarization, abstraction, merge). ANF
therefore requires every transformation to be recorded with producer identity
and prompt/tool version, so that any Stable Capability can be questioned by
asking:

> **"Which machine transformations produced this, and what were their inputs?"**

This is the line of inquiry that pure memory frameworks (Prism, Mem0) do not
inherently support, and it is one of ANF's strongest added values.

---

## Runtime boundary

ANF v1 contains **no runnable runtime**. Anything that needs to "do something
to evidence / capabilities" must do so via:

```text
- External adapter (e.g. cultivating-ml-agent, skill-tester)
- Human-governed procedure documented in the charter
- Reference implementation in a downstream repo (clearly marked as such)
```

The four current scripts in `scripts/` (skill_audit, skill_consolidation_checker,
crystallization_scheduler, capability_assessment) are **adapters that consume
ANF contracts**, not part of the ANF protocol. They shall be:

| Current | Target name | Role |
|---|---|---|
| `skill_audit.py` | `structural_lint.py` | Validates skill docs against Agent Skills spec + ANF frontmatter schema |
| `skill_consolidation_checker.py` | `merge_candidate_generator.py` | Generates merge candidates; never auto-merges |
| `crystallization_scheduler.py` | `evidence_freshness_check.py` (after freshness schema exists) | Flags stale evidence based on multi-dimensional freshness, not mtime |
| `capability_assessment.py` | `capability_review.py` | Captures qualitative reflection notes; emits no score |

After rename, none of these scripts may output a "quality score" or
"capability score." That authority belongs to `skill-tester`.

---

## Reuse policy

Before defining any v1 contract, ANF must produce a `03_EXTERNAL_CAPABILITY_MAP.md`
entry showing:

- What external projects already cover this need
- Whether to REUSE / ADAPT / REFERENCE / DO NOT BUILD
- Integration boundary with the external project

ANF will not redefine what Agent Skills, OpenTelemetry, OpenLineage, or MLflow
already define. ANF will only define the **organizational-capability layer**
above them.

---

## Consequences

### Positive

- ANF stays small, reviewable, and reviewable across years.
- Adapter ecosystem can grow without ANF core changes.
- Schema drift between ANF and Cultivating becomes impossible by construction (shared schema).
- No risk of ANF becoming a product and competing with its own adopters.
- Aligns with TopPrism Reuse First principle.

### Negative

- ANF cannot demonstrate value via a one-command install. Adoption requires reading docs and implementing adapters.
- Contributors who want to ship CLI tools will be redirected to adapter repos.
- The "value" of ANF becomes hard to communicate via screenshots; it must be communicated via governance discipline.

### Mitigations

- Publish a **reference adapter** in `cultivating-ml-agent` that consumes ANF contracts.
- Provide a **schema validation tool** (`structural_lint.py`) so adopters can check their artifacts cheaply.
- Maintain a **case-study directory** showing real adopters (using their permission), to demonstrate value without productizing.

---

## Rejected alternatives

### Alt A: Build a minimal CLI + SQLite runtime

**Rejected.** Would compete directly with Prism, Letta, Mem0. Violates Reuse
First. Risk of becoming the "platform" we are explicitly avoiding.

### Alt B: Build only YAML schemas and let adopters implement everything

**Rejected.** Insufficient; adopters would reinvent 80% of the same scaffolding.
ANF should provide **structural lint**, **merge candidate generation**, and
**evidence freshness checks** as reference implementations of the contract.

### Alt C: Acquire / partner with an existing memory framework

**Out of scope for this ADR.** Could be revisited later as a strategic question.

### Alt D: Stay methodology-only, do not specify contracts

**Rejected.** "Methodology" wording is what enabled scope drift in the first
place. "Protocol with contracts" makes the boundary explicit and reviewable.

---

## Migration implications

### Scripts

```text
skill_audit.py                 → structural_lint.py            (REWRITE + RENAME)
skill_consolidation_checker.py → merge_candidate_generator.py  (REWRITE + RENAME)
crystallization_scheduler.py   → evidence_freshness_check.py   (REWRITE after freshness schema)
capability_assessment.py       → capability_review.py          (REWRITE + RENAME, no score)
```

### Docs

```text
case-study-ml.md               → case-study-ml-historical-observation.md (REWRITE + RENAME)
crystallization-cycle.md       → (rewrite aligned with Lifecycle Protocol)
fragmentation-management.md    → (rewrite aligned with merge-candidate-generator pattern)
framework.md                   → (rewrite aligned with charter)
knowledge-architecture.md      → (rewrite: two planes, not three layers)
progress-measurement.md        → (rewrite: behavioral metrics only)
theoretical-foundations.md     → KEEP + header note
README.md                      → (rewrite aligned with charter)
topprism.yaml                  → (rewrite aligned with charter)
```

### Templates

```text
capability-matrix-template.md  → capability-review-template.md (drop score)
crystallization-checklist.md   → (rewrite aligned with risk-aware gates)
consolidation-audit-template.md → (rewrite, remove auto-merge refs)
session-review-template.md     → KEEP light edits
skill-template.md              → KEEP + header note
bootstrap-config/              → (light rewrite, remove "Constitutional" framing)
```

### Examples

```text
examples/skills/01-core-expertise.md → 01-authority-plane-user-preferences.md (RENAME)
examples/skills/02-domain-workflow.md → KEEP + header note
examples/skills/03-bug-fix-skill.md   → KEEP + header note
examples/case-study/ml-competition-journey.md → ml-competition-historical-observation.md (RENAME)
```

---

## Acceptance test for this ADR

This ADR is honored when:

1. [ ] No ANF v1 source file imports a vector DB / SQL DB / ORM / web framework.
2. [ ] No ANF v1 source file ships an HTTP server, CLI command group, or MCP server.
3. [ ] Every ANF v1 doc mentions Authority Plane and Knowledge Plane explicitly when discussing promotion.
4. [ ] The Evidence Envelope fields are present in every sample evidence record.
5. [ ] Provenance chain is recorded for every Stable Capability.
6. [x] All four Python scripts have been renamed + rewritten to remove evaluation authority. (Done 2026-08-22: structural_lint / merge_candidate_generator / evidence_freshness_check / capability_review; shared parser in scripts/anf_frontmatter.py.)
7. [ ] `03_EXTERNAL_CAPABILITY_MAP.md` exists and covers at minimum: Prism, Agent Skills, SkillsBench, EvoAgentBench, MUSE-Autoskill, MSCE, HSI, Letta, Mem0, LangMem, OpenTelemetry, OpenLineage, MLflow.
8. [ ] No "quality score", "capability score", or "self-evolving" claim appears anywhere in ANF.
9. [ ] No promoted A-plane entry can be traced back to a K-plane promotion.
10. [ ] If all four Python scripts are deleted tomorrow, ANF's value is unchanged.
