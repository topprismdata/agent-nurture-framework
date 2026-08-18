# Agent Nurture Framework

**A general methodology for turning repeated AI-agent work into
reusable, compounding organizational capability.**

`NATIVE AI` · `FRAMEWORK` · `LONGITUDINAL INTERNAL EVIDENCE` · `MIT`

> **Core question:** How can an agent become better across projects
> instead of restarting from the same static prompt every time?

Part of **TopPrism Native AI**.

------------------------------------------------------------------------

## Why this exists

Most agent systems focus on what an agent can do **today**:

``` text
Model + Prompt + Tools → Task
```

The Agent Nurture Framework focuses on a different problem:

> **What should happen after the task is finished so that the next
> project starts from a higher capability baseline?**

The framework treats agent development as a longitudinal learning
process:

``` text
Project
   ↓
Experience
   ↓
Validated lesson
   ↓
Knowledge crystallization
   ↓
Reusable skill / principle
   ↓
Better agent
   ↓
Next project
```

This is the general methodology behind TopPrism's project-evolving
agents.

------------------------------------------------------------------------

## Relationship to Cultivating ML Agent

This distinction should be explicit.

``` text
Agent Nurture Framework
        ↓
general methodology
        ↓
knowledge layers
crystallization
learning loop
evaluation principles
        ↓
Cultivating ML Agent
        ↓
ML-domain implementation
        ↓
real ML projects
experiments
failures
skills
automatic reuse
```

**Agent Nurture Framework** asks how an agent should learn across work.

**Cultivating ML Agent** is a concrete longitudinal implementation in
machine learning.

------------------------------------------------------------------------

## The core mechanism

### 1. Work creates experience

Real projects produce:

-   decisions;
-   successful patterns;
-   failed approaches;
-   debugging traces;
-   domain-specific heuristics;
-   unresolved knowledge gaps.

### 2. Experience is not automatically knowledge

Raw logs are noisy and highly contextual.

The framework therefore separates:

``` text
L3 — Experiential
session traces · observations · failures

          ↓ crystallize

L2 — Skill
workflows · playbooks · domain methods

          ↓ consolidate

L1 — Constitutional
identity · principles · stable knowledge
```

### 3. Knowledge must return to work

Crystallized knowledge only matters if it improves later tasks.

The framework therefore uses a recurring learning loop:

``` text
Study → Verify → Apply → Extract → Plan
  ↑                                 |
  └─────────────────────────────────┘
```

------------------------------------------------------------------------

## Three-layer knowledge architecture

  -----------------------------------------------------------------------
  Layer             Role              Volatility        Typical content
  ----------------- ----------------- ----------------- -----------------
  L1 Constitutional stable identity   low               role, boundaries,
                    and principles                      core principles

  L2 Skill          reusable domain   medium            workflows,
                    capability                          playbooks,
                                                        troubleshooting

  L3 Experiential   raw project       high              logs, failures,
                    experience                          observations
  -----------------------------------------------------------------------

Knowledge moves upward through crystallization and downward through
grounding.

The point is not to store everything forever. It is to move the **right
abstraction** into the right layer.

------------------------------------------------------------------------

## Knowledge crystallization

``` text
Conversation / Project
        ↓
Experiential accumulation
        ↓
Review & validation
        ↓
Pattern extraction
        ↓
Skill candidate
        ↓
Evaluation / consolidation
        ↓
Reusable organizational capability
```

A useful skill should be:

-   reusable beyond one session;
-   grounded in observed evidence;
-   specific enough to trigger correctly;
-   abstract enough to transfer;
-   revisable when later evidence contradicts it.

------------------------------------------------------------------------

## Evidence

The framework repository references a longitudinal ML case study in
which knowledge crystallization was associated with an observed **14×
capability-speedup measure** across the documented project sequence.

That number must be presented carefully:

> **14× is an observed result in the referenced ML longitudinal case
> study, not a universal claim that the framework makes every agent 14×
> better.**

The stronger evidence is longitudinal:

-   knowledge was extracted from real project work;
-   reusable skills accumulated over time;
-   later projects could activate prior knowledge;
-   the framework produced concrete artifacts, templates, audits, and
    capability assessments rather than only a conceptual model.

See the repository's ML case study for the exact methodology and metric
definition.

------------------------------------------------------------------------

## What this framework is --- and is not

### Use it when

-   expertise is partly tacit;
-   projects repeat with variation;
-   failures contain reusable lessons;
-   knowledge evolves over time;
-   agents are used repeatedly by a person or organization;
-   the cost of restarting from zero is meaningful.

### Do not use it when

-   the task is fully deterministic and should simply be code;
-   knowledge is static and already well specified;
-   there is no repeated-use learning loop;
-   storing experience creates more risk than value;
-   success cannot be evaluated at all.

------------------------------------------------------------------------

## Why this is Native AI infrastructure

``` text
Employee / Team
      ↓
Persistent Agent
      ↓
Projects
      ↓
Experience
      ↓
Knowledge Crystallization
      ↓
Skills
      ↓
Evaluation
      ↓
Higher organizational capability
```

This is not a customer-facing Decision Engine. It is infrastructure for
making an AI-enabled organization compound what it learns.

------------------------------------------------------------------------

## Framework components

  Component                   Purpose
  --------------------------- ------------------------------------------
  Knowledge architecture      decide where knowledge belongs
  Five-stage learning loop    structure continuous learning
  Crystallization cycle       convert experience into reusable assets
  Skill audit                 inspect quality and fragmentation
  Consolidation checker       identify overlap and merge opportunities
  Capability assessment       track agent growth
  Crystallization scheduler   decide when review is needed
  Templates                   standardize operational use

------------------------------------------------------------------------

## Quick start

The framework is intentionally methodology-first rather than a
one-command agent scaffold.

1.  review the workspace structure reference;
2.  define the agent's role, principles, and boundaries;
3.  use the agent on real work;
4.  capture significant experience;
5.  review and crystallize reusable knowledge;
6.  evaluate and consolidate skills;
7.  measure whether later tasks improve.

Example utilities:

``` bash
python scripts/skill_audit.py --dir ./skills
python scripts/skill_consolidation_checker.py --dir ./skills
python scripts/capability_assessment.py \
  --template templates/capability-matrix-template.md
python scripts/crystallization_scheduler.py --dir ./skills
```

------------------------------------------------------------------------

## Related TopPrism projects

### Cultivating ML Agent

Concrete ML-domain implementation of the nurture-first idea.

### Skill Tester

Quality and trigger-evaluation gate for reusable agent skills.

### Notebook Knowledge Distillation

A source-to-skill path for converting external knowledge into candidate
organizational capability.

### Three-Layer Wisdom Extraction

Experiments with lifting project events into domain knowledge and
transferable principles.

Together they form a broader Native AI loop:

``` text
External knowledge + Project experience
                 ↓
             Distillation
                 ↓
           Skill candidates
                 ↓
              Testing
                 ↓
        Organizational library
                 ↓
             Agent reuse
                 ↓
            New experience
```

------------------------------------------------------------------------

## Theoretical grounding

The framework draws on Nurture-First Development and connects the
operational model to learning / knowledge-management traditions such as
SECI, Dreyfus, Kolb, and cognitive apprenticeship.

The README should summarize these foundations; detailed theory belongs
in `docs/theoretical-foundations.md`.

The value of the repository should be judged primarily by:

> **whether the mechanism creates reusable capability that improves
> later work**, not by the number of theories cited.

------------------------------------------------------------------------

## Boundaries & open questions

Important open questions include:

1.  how to measure causal improvement from crystallized knowledge;
2.  when accumulated skills become stale;
3.  how to prevent incorrect lessons from propagating;
4.  how to evaluate trigger precision and skill selection;
5.  how to handle conflicting experience;
6.  how to govern privacy and sensitive project memory;
7.  how much of organizational learning should remain human-reviewed.

These are core research and engineering questions for Native AI.

------------------------------------------------------------------------

## Recommended evidence discipline

Every future capability claim should specify:

``` text
Observed where?
Measured how?
Compared with what?
Over what period?
Does it generalize?
```

Avoid generic statements such as "14× faster" without immediately
linking the exact case, denominator, and metric.

------------------------------------------------------------------------

## TopPrism metadata

``` yaml
topprism:
  purpose: native-ai
  capability: agent-capability-evolution
  platform_layer: organizational-intelligence
  maturity: framework
  evidence:
    type: longitudinal-internal-evidence
    scope: "documented ML case study and framework artifacts"
  related:
    - cultivating-ml-agent
    - skill-tester
    - notebook-knowledge-distillation
    - three-layer-wisdom-extraction
```

## License

MIT.

## Contributing

Contributions are especially useful around evaluation, stale-knowledge
detection, skill consolidation, governance, longitudinal measurement,
and cross-domain case studies.
