# Recommended Workspace Structure

This document describes the recommended directory structure for a new agent workspace.
Each directory serves a specific purpose within the Agent Nurture Framework's
three-layer architecture.

## Directory Layout

```
agent-workspace/
├── skills/                        # Skill Layer (L2)
│   ├── domain-workflow/
│   │   └── SKILL.md              # Domain-specific workflow skills
│   ├── debugging-patterns/
│   │   └── SKILL.md              # Debugging and troubleshooting skills
│   ├── configuration/
│   │   └── SKILL.md              # Environment and configuration skills
│   ├── integration/
│   │   └── SKILL.md              # Tool and API integration skills
│   └── ...
├── memory/                        # Experiential Layer (L3)
│   ├── YYYY-MM-DD.md             # Daily session notes
│   ├── decisions/                # Architecture Decision Records (ADR)
│   │   └── NNNN-title.md        # Numbered decision records
│   ├── patterns/                 # Observed patterns and heuristics
│   │   └── pattern-name.md      # Named pattern descriptions
│   ├── errors/                   # Error patterns and solutions
│   │   └── error-name.md        # Named error pattern descriptions
│   └── archive/                  # Crystallized or obsolete entries
│       ├── sessions/
│       ├── decisions/
│       └── errors/
├── config/
│   ├── soul.md                   # Constitutional Layer (L1) - Identity
│   ├── principles.md             # Constitutional Layer (L1) - Principles
│   └── memory-index.md           # Memory catalog and health metrics
├── scripts/                      # Automation and maintenance tools
│   ├── crystallize.sh            # Crystallization session helper
│   ├── audit.sh                  # Consolidation audit helper
│   └── metrics.sh                # Knowledge growth metrics
├── templates/                    # Local copies of framework templates
│   ├── skill-template.md
│   ├── session-review-template.md
│   └── capability-matrix-template.md
└── references/                   # Domain reference materials
    ├── docs/                     # Downloaded or symlinked documentation
    └── notes/                    # Reference notes and summaries
```

## Layer Mapping

### Constitutional Layer (L1)

The constitutional layer defines who the agent is and how it behaves. It is the
most stable layer and is updated infrequently.

| File | Purpose |
|------|---------|
| `config/soul.md` | Agent identity, role, personality, and behavioral boundaries |
| `config/principles.md` | Core principles that guide all agent decisions |

### Skill Layer (L2)

The skill layer contains reusable, structured knowledge that the agent can
retrieve and apply to tasks. Skills are created through crystallization and
maintained through consolidation.

| Directory | Purpose |
|-----------|---------|
| `skills/domain-workflow/` | Skills for the agent's primary domain workflows |
| `skills/debugging-patterns/` | Skills for common debugging scenarios |
| `skills/configuration/` | Skills for environment and tool configuration |
| `skills/integration/` | Skills for API, tool, and service integration |

Skills can be organized into additional subdirectories as needed. The naming
convention is `kebab-case` for directory names, with each skill stored as
`SKILL.md` within its directory.

### Experiential Layer (L3)

The experiential layer captures raw experience as it happens. It is the
source material for crystallization.

| Directory | Purpose |
|-----------|---------|
| `memory/YYYY-MM-DD.md` | Daily session notes: what happened, what was learned |
| `memory/decisions/` | Architecture and design decisions with reasoning |
| `memory/patterns/` | Observed patterns awaiting crystallization |
| `memory/errors/` | Error patterns and their solutions |
| `memory/archive/` | Entries that have been crystallized or are obsolete |

## Configuration Files

### config/soul.md

The agent's identity document. Defines the agent's role, personality, core
principles, behavioral boundaries, and domain focus. See
`templates/bootstrap-config/soul.md.example` for a template.

### config/principles.md

The agent's operational principles. These are the rules that govern how the
agent approaches problems, communicates with the user, and handles edge cases.
Principles are discovered through experience and refined through reflection.

### config/memory-index.md

A catalog of all memory files, their status, and the crystallization log.
See `templates/bootstrap-config/memory.md.example` for a template.

## Scripts Directory

The scripts directory contains automation tools for maintaining the knowledge
base. These are optional but recommended for consistent maintenance.

| Script | Purpose |
|--------|---------|
| `crystallize.sh` | Guides the operator through a crystallization session |
| `audit.sh` | Runs consolidation metrics and generates an audit report |
| `metrics.sh` | Computes knowledge growth metrics for progress tracking |

## Getting Started

1. Copy the workspace structure to a new directory.
2. Edit `config/soul.md` to define the agent's identity and principles.
3. Create the first skill directory based on the primary domain.
4. Begin using the agent and recording session notes in `memory/`.
5. After 5-7 sessions, conduct the first crystallization session.
6. Schedule weekly audits and monthly capability assessments.
