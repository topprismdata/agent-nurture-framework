# Knowledge Architecture: The Three-Layer Cognitive Architecture

## 1. Architecture Overview

The Agent Nurture Framework organizes agent knowledge into three distinct layers, each optimized for different access patterns, volatility profiles, and developmental functions. This architecture, derived from the Three-Layer Cognitive Architecture proposed in the Nurture-First Development paradigm (Zhang, 2026), provides the structural foundation for knowledge crystallization and continuous agent development.

```
+===================================================================+
|                    CONSTITUTIONAL LAYER (L1)                       |
|   Role Definition | Behavioral Principles | Capability Indices     |
|   Volatility: LOW          Load: Every Session                     |
|   Size: 10-15% of context window                                    |
+===================================================================+
         |                                    ^
         v                                    |
+===================================================================+
|                      SKILL LAYER (L2)                              |
|   Modular Skill Documents | Domain Knowledge | Procedures           |
|   Volatility: MEDIUM       Load: On Demand                         |
|   Structure: YAML frontmatter + structured content                 |
+===================================================================+
         |                                    ^
         v                                    |
+===================================================================+
|                   EXPERIENTIAL LAYER (L3)                          |
|   Interaction Records | Reasoning Traces | Pattern Observations    |
|   Volatility: HIGH         Access: Semantic Search                 |
|   Lifecycle: Create -> Crystallize -> Archive/Delete               |
+===================================================================+
```

The layers are organized along a volatility gradient: the Constitutional Layer (L1) is the most stable, the Skill Layer (L2) changes at project-cycle frequency, and the Experiential Layer (L3) is continuously modified during active operation. Information flows downward (grounding) and upward (crystallization), with lateral coordination mediated through shared experiential records.

---

## 2. Layer 1: Constitutional (Core Capabilities)

### 2.1 Characteristics

| Property | Value |
|----------|-------|
| **Volatility** | Low (monthly or less) |
| **Loading Strategy** | Loaded at start of every session |
| **Persistence** | File-based, version-controlled |
| **Access Pattern** | Sequential read |
| **Size Constraint** | 10--15% of effective context window |

### 2.2 Design Principles

The constitutional layer serves as the agent's persistent identity and behavioral foundation. It should be designed according to the following principles:

**Principle 1: Contain Indices, Not Content.** The constitutional layer should contain pointers to and summaries of capabilities, not the detailed knowledge itself. It functions as a table of contents and behavioral compass, not as an encyclopedia. Detailed domain knowledge resides in the skill layer, where it can be loaded selectively.

**Principle 2: Establish Behavioral Invariants.** The constitutional layer defines the behavioral boundaries within which the agent operates: ethical constraints, communication style, decision-making principles, and quality standards. These invariants provide the stable framework within which domain-specific skills are exercised.

**Principle 3: Declare Capability Affordances.** The constitutional layer informs the agent (and the user) about what the agent can do, listing available skills and their applicability conditions. This enables the agent to reason about its own capabilities and to request skill loading when needed.

**Principle 4: Maintain Parsimony.** Every token in the constitutional layer is loaded at every session start. Unnecessary content wastes context window capacity that could be allocated to task-relevant information. The constitutional layer should be ruthlessly edited to contain only what is needed at every interaction start.

### 2.3 Content Structure

A well-designed constitutional layer typically contains:

1. **Role Definition**: A concise statement of the agent's role and primary purpose (2--4 sentences).
2. **Behavioral Principles**: The rules governing how the agent interacts with the user, makes decisions, and handles uncertainty (5--10 principles).
3. **Skill Index**: A list of available skills with brief descriptions and applicability conditions, enabling the agent to determine which skills to load.
4. **Operational Constraints**: Session-level constraints such as output format preferences, communication language, and quality thresholds.
5. **Development Status**: Current development phase, known gaps, and priorities for the current interaction period.

### 2.4 Update Protocol

Constitutional updates are infrequent and consequential. They should follow this protocol:

1. **Proposal**: A specific change is proposed, motivated by accumulated evidence from experiential or skill layers.
2. **Impact Assessment**: The proposed change is evaluated against the full knowledge state to identify potential conflicts or redundancies.
3. **User Validation**: The user reviews and approves the change, ensuring alignment with their expectations.
4. **Atomic Update**: The change is applied in a single, version-controlled commit with clear documentation of the motivation and expected impact.
5. **Validation Period**: The updated constitutional layer is monitored for 1--2 weeks to verify that behavioral changes align with expectations.

---

## 3. Layer 2: Skill (Domain Knowledge)

### 3.1 Characteristics

| Property | Value |
|----------|-------|
| **Volatility** | Medium (per project or experience cycle) |
| **Loading Strategy** | On demand, selected by relevance |
| **Persistence** | File-based, version-controlled |
| **Access Pattern** | Index scan, selective load |
| **Size Constraint** | 200--500 lines per skill document |

### 3.2 Design Principles

The skill layer embodies the Modular Intelligence principle (Bhargava, 2026): knowledge is organized as discrete, composable modules, each conforming to the Single Responsibility Principle.

**Principle 1: Single Responsibility.** Each skill document addresses one coherent domain capability. A skill for "database query optimization" should not also address "frontend performance tuning." This modularity enables independent evolution, targeted retrieval, and compositional flexibility.

**Principle 2: Self-Contained Applicability.** Each skill declares its own applicability conditions, enabling the agent to determine when the skill is relevant without loading the full content. Applicability conditions should include domain, task type, trigger keywords, and prerequisite skills.

**Principle 3: Structured for Retrieval.** Skill documents use a consistent structure with metadata in YAML frontmatter, enabling both programmatic indexing and natural language understanding of the skill's scope and content.

**Principle 4: Evidence-Grounded.** Every skill should contain a provenance record indicating the experiential data from which it was crystallized, the date of crystallization, and validation evidence. This enables quality auditing and supports decisions about when skills need updating.

**Principle 5: Version-Aware.** Skills evolve with the domain. Each skill document should track its version history, recording what changed, why, and with what validation.

### 3.3 Skill Document Structure

Each skill document follows a standardized structure:

```yaml
---
# YAML Frontmatter (machine-readable metadata)
skill_id: unique-identifier
name: Human-readable skill name
version: "1.2"
domain: [primary domain]
applicability:
  task_types: [list of relevant task types]
  trigger_keywords: [keywords indicating relevance]
  prerequisites: [other skills required]
provenance:
  crystallized_from: [reference to experiential records]
  crystallization_date: YYYY-MM-DD
  validation_evidence: [summary of validation]
last_validated: YYYY-MM-DD
complexity: beginner|intermediate|advanced
---

# Skill Name

## Context
Brief description of when and why this skill is needed.

## Principles
Core principles governing application of this skill.

## Procedures
Step-by-step procedures for applying this skill.

## Patterns
Common patterns and their solutions.

## Anti-Patterns
Common mistakes and how to avoid them.

## Examples
Concrete examples of application.

## References
Links to related skills, external documentation, or resources.
```

### 3.4 Skill Lifecycle

Skills progress through a defined lifecycle:

1. **Draft**: Newly crystallized, awaiting validation through real-world application.
2. **Active**: Validated through successful application; loaded for relevant tasks.
3. **Refining**: Updated based on new experiential evidence; temporarily marked for review.
4. **Stable**: Well-validated, rarely modified; serves as a reliable knowledge asset.
5. **Deprecated**: Superseded by newer skills; retained for provenance but no longer actively loaded.

---

## 4. Layer 3: Experiential (Contextual Memory)

### 4.1 Characteristics

| Property | Value |
|----------|-------|
| **Volatility** | High (continuously during active sessions) |
| **Loading Strategy** | Semantic search, selective retrieval |
| **Persistence** | File-based or database, append-optimized |
| **Access Pattern** | Write-heavy, search-friendly |
| **Lifecycle** | Create, Crystallize, Archive/Delete |

### 4.2 Design Principles

The experiential layer functions as the agent's episodic memory: a rich, context-heavy record of specific interactions that serves as the raw material for crystallization.

**Principle 1: Append-Only with Staleness Tracking.** Experiential records are never modified after creation; they are annotated with staleness metadata. This append-only design preserves the complete experiential history for crystallization analysis while enabling efficient management through staleness-based archival.

**Principle 2: Search-Friendly Structure.** Records are structured for efficient semantic search, with clear categorization, keyword tagging, and temporal indexing. The primary access pattern is "find records related to X," not sequential browsing.

**Principle 3: Context Preservation.** Each record captures not just the outcome of an interaction but the full context: the problem, the reasoning process, the decision made, the outcome, and any user feedback. This contextual richness is essential for pattern extraction during crystallization.

**Principle 4: Categorical Organization.** Records are classified into six categories, each serving a distinct function in the crystallization process.

### 4.3 Six Categories of Experiential Knowledge

1. **Operational Records**: Document decisions made, actions taken, and outcomes observed during task execution. These form the behavioral baseline for pattern extraction.
   - Structure: `{task, decision, action, outcome, timestamp}`

2. **Reasoning Traces**: Capture the explicit reasoning process behind decisions, including alternatives considered and the rationale for the chosen path.
   - Structure: `{context, alternatives, chosen_path, rationale, timestamp}`

3. **Pattern Observations**: Record regularities noticed across multiple experiences. These are pre-crystallization observations---patterns that have been noticed but not yet validated or structured.
   - Structure: `{observation, evidence_instances, confidence, domain, timestamp}`

4. **Error Records**: Document mistakes, failures, and their analysis. Error records are particularly valuable for crystallization because they encode negative knowledge---what not to do---that is often difficult to articulate positively.
   - Structure: `{error, context, root_cause, correction, prevention, timestamp}`

5. **Contextual Annotations**: Record environmental metadata---tools available, project constraints, team conventions---that provides the situational context for other records.
   - Structure: `{context_type, metadata, validity_period, timestamp}`

6. **Insight Fragments**: Capture standalone principles, heuristics, or rules-of-thumb that emerge during interaction. These are often the seeds of future skill documents.
   - Structure: `{insight, domain, evidence, confidence, timestamp}`

### 4.4 Staleness and Lifecycle Management

Experiential records have a defined lifecycle:

```
CREATE --> ACTIVE --> MATURING --> STALE --> ARCHIVED
                 |                           ^
                 +--> CRYSTALLIZED ----------+
```

- **Active**: Recently created; potentially relevant to current tasks.
- **Maturing**: 1--2 weeks old; decreasing immediate relevance but still valuable for crystallization.
- **Stale**: 2+ weeks without reference; candidate for archival or crystallization-triggered review.
- **Crystallized**: Knowledge has been extracted and consolidated into the skill layer; the original record is archived but retained for provenance.
- **Archived**: No longer in active access; retained for audit and provenance purposes.

The staleness threshold of 2+ weeks without reference serves as a crystallization trigger: when a significant volume of experiential data reaches this threshold, it signals that sufficient raw material has accumulated to warrant a crystallization cycle.

---

## 5. Cross-Layer Information Flow

### 5.1 Downward Flow (Grounding)

Downward flow refers to the use of higher-layer knowledge to interpret and contextualize lower-layer data. This flow is continuous and automatic during active sessions.

**Constitutional to Skill**: Constitutional principles determine which skills are relevant for a given session and how they should be applied. The behavioral principles in L1 govern the agent's approach to tasks defined by L2 skills.

**Constitutional and Skill to Experiential**: When recording experiential data, constitutional principles and active skills provide the interpretive framework. A decision recorded in L3 is enriched by the L2 skill that informed it and the L1 principle that guided the choice among alternatives.

**Grounding Example**: When the agent encounters a novel debugging scenario, the constitutional layer provides the problem-solving approach (systematic, evidence-based), the relevant skill layer documents provide domain-specific debugging heuristics, and together they frame how the new experience is recorded in the experiential layer.

### 5.2 Upward Flow (Crystallization)

Upward flow refers to the consolidation of lower-layer data into higher-layer knowledge structures. This flow occurs during deliberate crystallization operations in the surgical workspace.

**Experiential to Skill (Most Common)**: Pattern extraction from accumulated experience produces new skill documents or refines existing ones. This is the primary crystallization pathway and occurs at every crystallization checkpoint.

**Skill to Constitutional (Rare)**: When skill-level knowledge proves stable across multiple domains and crystallization cycles, it may be generalized into constitutional principles. This occurs infrequently---typically once every few months---and requires cross-domain validation. For example, a debugging skill specific to Python that proves equally effective for Rust debugging may be abstracted into a general "systematic debugging" principle in the constitutional layer.

**Crystallization Constraints**: Upward flow is governed by the non-decreasing value proposition (Proposition 1, framework.md): every crystallization must maintain or improve the overall knowledge value. This constrains crystallization operations to produce validated, structured knowledge that genuinely enhances the agent's capability.

### 5.3 Lateral Flow (Memory-Mediated Coordination)

Lateral flow refers to coordination between skills within the same layer, mediated through shared experiential records rather than direct invocation.

**Shared Experiential Records**: When multiple skills are applied to a single task, the experiential records from that task serve as a coordination point. During crystallization, patterns that span multiple skills can be identified because the experiential records link the skills through shared context.

**Skill Dependency Declaration**: Skills declare their dependencies through YAML frontmatter, enabling the agent to load prerequisite skills when a dependent skill is activated. This declaration-based coordination avoids the coupling problems of direct invocation while ensuring necessary context is available.

**Memory-Based Mediation**: Rather than skills directly invoking each other (which creates tight coupling and scalability problems), skills communicate through the experiential layer. Skill A's outputs are recorded as experiential data that Skill B can reference when activated. This mediation pattern maintains skill independence while enabling compositional behavior.

---

## 6. Layer Migration Patterns

Knowledge migration between layers follows predictable patterns governed by the crystallization cycle.

### 6.1 L3 to L2: Crystallization (Most Common)

This is the primary migration path and the core operation of the Knowledge Crystallization Cycle. It occurs when:

- Sufficient experiential data has accumulated (typically 20+ relevant records).
- Patterns in the data meet extraction quality criteria (reusable, non-trivial, specific, verified).
- The user validates the crystallized pattern during a crystallization checkpoint.

**Migration Process**:
1. Pattern extraction from experiential corpus.
2. Structuring into skill document format.
3. De-contextualization to remove situation-specific details.
4. Validation against full experiential corpus.
5. User review and approval.
6. Integration into skill layer with version tracking.
7. Archival of source experiential records.

### 6.2 L2 to L1: Generalization (Rare)

This migration path occurs when skill knowledge proves sufficiently general to warrant constitutional status. It requires:

- Cross-domain validation: the knowledge has been verified across at least two distinct domains.
- Temporal stability: the knowledge has remained valid for at least 3 months.
- User consensus: the user explicitly endorses the generalization.

**Migration Process**:
1. Identification of candidate skill for generalization.
2. Cross-domain validation review.
3. Abstraction from domain-specific to general principle.
4. Integration into constitutional layer.
5. Skill layer update to reference the new constitutional principle.
6. Extended validation period (2--4 weeks).

### 6.3 L3 to Archive: Stale Knowledge Cleanup

Experiential records that have not been referenced for an extended period (typically 4+ weeks) and have not contributed to crystallization are candidates for archival. Archival is a housekeeping operation that maintains the experiential layer's search quality.

**Archival Criteria**:
- Record age exceeds staleness threshold.
- No references in recent sessions.
- Not identified as relevant during the most recent crystallization cycle.
- No pending pattern observations associated with the record.

**Archival Process**:
1. Identify stale records meeting archival criteria.
2. Verify no pending crystallization relevance.
3. Move to archive with full metadata preservation.
4. Update experiential layer indices.
5. Record archival in crystallization log.

---

## 7. Implementation Patterns for Different Platforms

| Architecture Element | Claude Code | Codex CLI | Gemini CLI | Custom Agent |
|---------------------|-------------|-----------|------------|--------------|
| **L1: Constitutional** | `CLAUDE.md` in project root | System prompt file | `GEMINI.md` system instructions | Config file or system prompt |
| **L2: Skill Storage** | `.claude/skills/*.md` | `skills/*.md` in project | `.gemini/skills/*.md` | Configurable skill directory |
| **L2: Skill Format** | Markdown + YAML frontmatter | Markdown + YAML frontmatter | Markdown + YAML frontmatter | Markdown + YAML frontmatter |
| **L2: Skill Loading** | Auto-load via CLAUDE.md index | Explicit import or reference | Auto-load via GEMINI.md index | Plugin/module loader |
| **L3: Experience Storage** | `.claude/experience/` directory | Session log directory | `.gemini/memory/` directory | Vector database |
| **L3: Experience Access** | File-based semantic search | Custom indexing required | File-based retrieval | Vector similarity search |
| **L3: Staleness Tracking** | File modification dates | Custom metadata | File modification dates | Database timestamps |
| **Cross-layer Flow** | Manual via surgical workspace | Scripted pipeline | Manual via surgical workspace | Automated pipeline |
| **Version Control** | Git (recommended) | Git (recommended) | Git (recommended) | Database or Git |
| **Crystallization** | Manual session in surgical workspace | Script or CI/CD trigger | Manual session in workspace | Automated or triggered |
| **Migration (L3->L2)** | User-guided extraction | Automated with review | User-guided extraction | Automated with human approval |
| **Migration (L2->L1)** | Edit CLAUDE.md with review | Edit system prompt | Edit GEMINI.md with review | Edit config with approval |

### Platform-Specific Notes

**Claude Code**: The CLAUDE.md convention provides natural constitutional layer support. Skills can be loaded via glob patterns referenced in CLAUDE.md. The experiential layer requires custom file structures but benefits from Claude's strong semantic understanding for search.

**Codex CLI**: Lacks native skill management, requiring explicit construction of all three layers. However, its extensibility enables sophisticated scripted pipelines for crystallization and layer management.

**Gemini CLI**: The GEMINI.md convention mirrors Claude's approach with platform-specific syntax. Skill loading and experiential management follow similar patterns with platform-appropriate adjustments.

**Custom Agents**: Full architectural control enables the most sophisticated implementation, potentially using vector databases for the experiential layer, plugin systems for skill loading, and automated crystallization pipelines. However, this control comes at the cost of implementation complexity.

---

## References

- Bhargava, A. (2026). Modular Intelligence: Skill-Based Paradigm for Scalable Agent Architecture. *Journal of Innovations in Software Engineering Methodology (JISEM)*.
- Nonaka, I., & Takeuchi, H. (1995). *The Knowledge-Creating Company*. Oxford University Press.
- tanaikech. (2026). Recursive Knowledge Crystallization (RKC) Framework. Google Cloud.
- Zhang, K. (2026). Nurture-First Development: A Knowledge Crystallization Approach to Domain-Specific AI Agent Development. *arXiv preprint arXiv:2603.10808*.
