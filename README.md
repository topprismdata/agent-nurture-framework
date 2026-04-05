# Agent Nurture Framework

> A systematic methodology for developing AI agents from novice to expert through conversational knowledge crystallization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Framework Version](https://img.shields.io/badge/version-1.0.0-green.svg)]()

## Overview

The Agent Nurture Framework provides a principled approach to growing AI agent capabilities over time. Rather than pre-building agents with static prompts or code pipelines, this framework treats agent development as a **continuous, conversational process** where knowledge is accumulated through daily use and periodically crystallized into structured, reusable assets.

Based on [Nurture-First Development (NFD)](https://arxiv.org/abs/2603.10808) theory and validated through months of real-world experimentation (including a demonstrated **14x capability speedup** across projects), this framework provides:

- **Three-Layer Knowledge Architecture** organizing agent knowledge by volatility and personalization
- **Knowledge Crystallization Cycle** transforming fragmented experience into structured expertise
- **Complete Toolchain** including templates, automation scripts, and example skills
- **Rigorous Theoretical Foundation** grounded in SECI, Dreyfus, and Kolb learning theories

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  L1: Constitutional Layer (Stable)                       │
│  Identity · Principles · Core Knowledge                  │
│  Loaded every session · Updated monthly                  │
├─────────────────────────────────────────────────────────┤
│  L2: Skill Layer (Evolving)                              │
│  Domain Skills · Workflows · Playbooks                    │
│  Loaded on demand · Updated per project                  │
├─────────────────────────────────────────────────────────┤
│  L3: Experiential Layer (Dynamic)                        │
│  Session Logs · Debug Traces · Observations               │
│  Semantic search · Crystallized into L1/L2               │
└─────────────────────────────────────────────────────────┘
         ↑ Crystallization ↑          ↓ Grounding ↓
```

## Quick Start

### 1. Set up your workspace

```bash
# Use the provided template structure
cp -r templates/bootstrap-config/ my-agent/
cd my-agent
```

### 2. Define your agent's identity

Edit `soul.md` to define your agent's role, principles, and boundaries.

### 3. Start nurturing

Begin interacting with your agent. After each significant session, use the session review template to identify extractable knowledge.

### 4. Crystallize regularly

Use the provided scripts to assess skill quality, detect consolidation opportunities, and schedule crystallization sessions.

```bash
# Audit your skill library
python scripts/skill_audit.py --dir ./skills

# Check for overlapping skills
python scripts/skill_consolidation_checker.py --dir ./skills

# Assess agent capabilities
python scripts/capability_assessment.py --template templates/capability-matrix-template.md

# Check crystallization schedule
python scripts/crystallization_scheduler.py --dir ./skills
```

## Core Concepts

### The Five-Stage Learning Loop

```
Study → Verify → Apply → Extract → Plan
  ↑                                 |
  └─────────────────────────────────┘
```

Each stage builds on the previous one, creating a continuous cycle of knowledge acquisition and refinement:

| Stage | Description | Output |
|-------|-------------|--------|
| **Study** | Immerse the agent in domain knowledge through conversation | Raw experiential data (L3) |
| **Verify** | Test understanding through structured validation | Verified knowledge fragments |
| **Apply** | Use knowledge in real tasks to build practical competence | Task outcomes and edge cases |
| **Extract** | Identify reusable patterns from successful applications | Candidate skill material |
| **Plan** | Determine next learning priorities and knowledge gaps | Learning roadmap updates |

### Knowledge Crystallization Cycle

```
Conversational Immersion → Experiential Accumulation → Deliberate Crystallization → Grounded Application
              ↑                                                                                |
              └────────────────────────────────────────────────────────────────────────────────┘
```

The cycle transforms tacit, session-specific knowledge into explicit, reusable assets:

1. **Conversational Immersion**: Engage deeply with domain problems through natural dialogue
2. **Experiential Accumulation**: Build a rich corpus of interactions, solutions, and observations
3. **Deliberate Crystallization**: Periodically review accumulated experience and distill structured skills
4. **Grounded Application**: Test crystallized knowledge in new scenarios and refine based on feedback

### Three-Layer Knowledge Architecture

| Layer | Volatility | Content | Update Frequency |
|-------|-----------|---------|-----------------|
| **L1: Constitutional** | Low | Agent identity, core principles, domain fundamentals | Monthly |
| **L2: Skill** | Medium | Domain skills, workflows, playbooks, troubleshooting guides | Per project |
| **L3: Experiential** | High | Session logs, debug traces, ad-hoc observations | Per session |

Knowledge flows upward through crystallization (L3 to L2 to L1) and downward through grounding (L1 shapes L2 shapes L3 interpretation).

### Applicability

This framework is most effective when:

- Domain expertise is substantially tacit (can't be fully documented upfront)
- Expertise is highly personal (different practitioners have different approaches)
- Expertise evolves continuously (static encodings become stale)
- Interaction is conversational (natural knowledge transfer during use)
- Pattern recognition from experience is valuable

This framework is **not** ideal when:

- Domain knowledge is fully formalizable (use code-first instead)
- Expertise is static and unchanging (use prompt-first instead)
- Tasks are repetitive with no learning component

## Documentation

| Document | Description |
|----------|-------------|
| [Framework Core](docs/framework.md) | Formal definitions, five-stage loop, operational framework |
| [Theoretical Foundations](docs/theoretical-foundations.md) | NFD, SECI, Dreyfus, Kolb, Cognitive Apprenticeship |
| [Knowledge Architecture](docs/knowledge-architecture.md) | Three-layer architecture with cross-layer flows |
| [Crystallization Cycle](docs/crystallization-cycle.md) | KCC phases, formal model, algorithm, triggers |
| [Fragmentation Management](docs/fragmentation-management.md) | Skill consolidation strategies |
| [Progress Measurement](docs/progress-measurement.md) | Capability matrix and growth metrics |
| [ML Case Study](docs/case-study-ml.md) | 14x speedup through knowledge crystallization |

## Templates & Examples

| Resource | Description |
|----------|-------------|
| [Skill Template](templates/skill-template.md) | Standard structure for new skills |
| [Capability Matrix](templates/capability-matrix-template.md) | Agent capability assessment |
| [Crystallization Checklist](templates/crystallization-checklist.md) | Step-by-step crystallization guide |
| [Consolidation Audit](templates/consolidation-audit-template.md) | Skill merge/review template |
| [Session Review](templates/session-review-template.md) | End-of-session knowledge extraction |
| [Bootstrap Config](templates/bootstrap-config/) | Starter workspace configuration |
| [Example Skills](examples/skills/) | L1/L2/L3 skill examples |

## Comparison with Alternatives

| Dimension | Code-First | Prompt-First | Nurture-First (This Framework) |
|-----------|-----------|-------------|-------------------------------|
| Developer | Software Engineer | Prompt Engineer | Domain Practitioner |
| Knowledge encoding | Deterministic pipelines | Static system prompts | Living knowledge base |
| Adaptation | Engineering cycles | Prompt optimization | Continuous through use |
| Scalability ceiling | Engineering capacity | Context window | Memory search quality |
| Tacit knowledge capture | Limited | Limited | Strong (conversational) |
| Personalization | Low | Medium | High |
| Maintenance cost | High (code updates) | Medium (prompt tuning) | Low (natural evolution) |

## Automation Scripts

| Script | Description |
|--------|-------------|
| [skill_audit.py](scripts/skill_audit.py) | Quality assessment and statistics for your skill library |
| [skill_consolidation_checker.py](scripts/skill_consolidation_checker.py) | Detect merge opportunities and skill overlap |
| [capability_assessment.py](scripts/capability_assessment.py) | Interactive capability matrix scoring |
| [crystallization_scheduler.py](scripts/crystallization_scheduler.py) | Monitor staleness and schedule crystallization |

## Contributing

Contributions welcome! This framework is designed to be domain-agnostic. If you've applied it in areas beyond ML (e.g., legal analysis, medical diagnosis, creative writing), we'd love to hear about your experience.

Please feel free to:

1. Open an issue to discuss proposed changes
2. Submit pull requests with new templates, scripts, or documentation
3. Share case studies from your domain
4. Suggest improvements to the theoretical framework

## References

See [references/bibliography.md](references/bibliography.md) for the complete list of cited works.

## License

[MIT License](LICENSE)
