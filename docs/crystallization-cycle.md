---
title: The Knowledge Crystallization Cycle
status: accepted (Week 3 rewrite)
created: 2026-08-22
supersedes: "crystallization-cycle.md v1 (time-based maturity gates, reasoning-trace gate, L2→L1 promotion)"
governed_by: 02_ADR-001_PROTOCOL_NOT_RUNTIME.md
---

# The Knowledge Crystallization Cycle

The Knowledge Crystallization Cycle (KCC) describes how raw experience becomes
structured organizational capability inside the K-plane. It is an operational
pattern that adapters implement; ANF itself specifies the gates and the record
formats.

> **What changed in this revision.** The four-phase cycle is retained. What is
> gone: time-based maturity thresholds (weeks/months), the `HasReasoningTrace`
> gate, layer-count heuristics ("20+ records"), and any path from capability to
> constitutional/policy status. Gates are now **risk-aware**, keyed on evidence
> quality and transfer breadth — never on elapsed time.

---

## 1. The four phases

```text
1. OBSERVE            work happens; adapters capture Experience Records
        ↓
2. ACCUMULATE         episodic memory grows; searchable, append-only
        ↓
3. CONSOLIDATE        deliberate extraction → candidate → validated capabilities
        ↓
4. APPLY              capabilities serve real tasks; outcomes become new Evidence
        └──────────────── back to 1 ────────────────┘
```

### Phase 1 — Observe

Adapters (an agent runtime, a session harness, a human filling a template)
capture Experience Records per the schema in
[knowledge-architecture.md §5](knowledge-architecture.md). Each record contains:
task, context, decision + decision_summary, action, execution_trace references,
outcome, correction, classification, timestamp.

**No model-internal reasoning is recorded.** If a rationale matters, the human
or adapter writes a `decision_summary`. This keeps records portable across
platforms and safe for organizational retention policies.

### Phase 2 — Accumulate

Episodic memory is append-only and searchable. Records carry classification
labels (`public|internal|confidential|restricted`) from creation; retention and
deletion follow the organization's data governance, which ANF does not own.

### Phase 3 — Consolidate

Deliberate, reviewable operation with five sub-steps:

| Step | Operation | Output |
|---|---|---|
| 3a | Pattern extraction across episodic corpus | candidate patterns with supporting evidence refs |
| 3b | Structuring into Agent Skills format | skill drafts with topprism metadata |
| 3c | De-contextualization (generalize tool names, parameterize values) | transferable formulation |
| 3d | Validation against full corpus + behavioral evaluation | contradictions surfaced; eval metrics attached |
| 3e | Integration + provenance write | promoted skill with lineage |

Step 3d requires an **evaluation provider** (designated: `skill-tester`) for
promotion beyond `candidate`. Lexical or LLM self-assessment alone is not
validation.

### Phase 4 — Apply

Capabilities serve live tasks. Outcomes flow back as new Evidence Records,
including **negative** outcomes (`task_failure`, `negative_transfer`,
`correction`, `contradiction`). A capability that only ever collects positive
evidence is not being measured.

---

## 2. Risk-aware promotion gates

Gates are functions of the promotion's **risk profile**, not of calendar time:

```text
gate = f(
  risk_level,          # blast radius if the capability is wrong
  scope,               # personal < project < team < organization
  evidence_diversity,  # distinct tasks/contexts, not repeat counts
  transfer_evidence,   # validation in ≥2 contexts for transferable claims
  reversibility,       # can a bad application be undone cheaply?
  authority_target,    # within K-plane only; A-plane targets are prohibited
  source_trust         # trust level of producing adapter/operator
)
```

Default gate table (adapters may tighten, never loosen):

| Promotion | Minimum gate |
|---|---|
| Evidence → Candidate | Envelope complete; provenance chain opened |
| Candidate → Validated | Behavioral evaluation by designated provider; no unresolved contradiction |
| Validated → Transferable | Independent validation in ≥ 2 distinct contexts |
| Transferable → General Principle | Stronger evidence + explicit human review (still K-plane) |
| *Capability → Policy* | **Prohibited by default** (ADR-001 Promotion Matrix) |

Risk classification examples:

- **Low risk** (reversible, personal scope): formatting preferences, lint
  configs — automation may promote on modest evidence.
- **Medium risk** (affects deliverables): model-selection heuristics, CV
  strategies — multi-context evidence required.
- **High risk** (irreversible, security/privacy/legal adjacent, org scope):
  anything touching credentials, customer data, external transmissions —
  independent validation + human approval required, regardless of how often
  it has worked before.

**Explicitly removed:** "Bootstrap/Structured/Mature phases" gated on weeks
1–3 / months 1–3 / month 3+, and reduced observation minimums at "maturity".
An agent running for three months has merely run for three months.

---

## 3. Contradiction handling

When new evidence contradicts a validated capability:

1. The capability enters `Disputed` state with links to contradicting evidence.
2. Downstream promotions are frozen while disputed.
3. Resolution paths: refute (attach counter-evidence), refine (narrow
   applicability conditions), or deprecate.
4. Both the contradiction and its resolution remain in the provenance chain.
   Silent overwriting is prohibited.

This mechanism exists because SkillsBench (2026) shows even curated skills
produce negative gains in a meaningful fraction of tasks; unmonitored
propagation of stale skills is a measured failure mode, not a hypothetical one.

---

## 4. Record formats

Consolidation consumes and produces three artifact types (full schemas in
ADR-001):

- **ExperienceRecord** — observable behavior + outcome (§ Phase 1).
- **EvidenceRecord** — evaluation-provider output wrapped in the Evidence
  Envelope (`metric_name/value/version`, `measurement_protocol`,
  `protocol_version`, executor identity).
- **CapabilityRecord** — the skill plus topprism metadata, lifecycle state,
  and provenance chain id. Shared schema with `cultivating-ml-agent`;
  drift is tracked as a defect.

---

## 5. Formal notes (retained, non-normative)

The prior revision's formal model ($K_t = (C_t, S_t, E_t)$, value function
$V(K)$, efficiency $\eta$) was carried over from NFD (Zhang, 2026). It remains
available in git history and in [theoretical-foundations.md](
theoretical-foundations.md) as background. It is **not normative** here: a
scalar value function over heterogeneous knowledge is not measurable with the
rigor the formalism implies, and this revision avoids presenting it as an
operational guarantee. The non-decreasing-value "proposition" depended on
user-validated crystallization for its alignment term; under risk-aware gates
the equivalent claim is weaker and stated plainly:

> Consolidation must be reviewable and reversible; no consolidation step may
> destroy provenance or lower evidence integrity.

---

## 6. Acceptance checks for this document

- [x] No gate depends on elapsed time.
- [x] No gate requires model-internal reasoning traces.
- [x] No promotion path from capability to policy/constitutional status.
- [x] Negative evidence is first-class (failure, contradiction, negative transfer).
- [x] Validation requires a behavioral evaluation provider beyond `candidate`.
