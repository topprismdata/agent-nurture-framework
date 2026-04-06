# Agent Nurture Framework: A Nurture-First Approach to Domain-Specific Agent Development

## Abstract

Large language models (LLMs) possess remarkable general-purpose capabilities, yet deploying them as effective domain-specific agents remains a significant engineering challenge. Existing approaches---Code-First and Prompt-First paradigms---treat agent configuration as a static design problem, producing agents whose expertise is bounded by the explicit knowledge encoded at development time. This document introduces the **Agent Nurture Framework (ANF)**, grounded in the Nurture-First Development (NFD) paradigm (Zhang, 2026), which reconceptualizes agent development as a continuous process of experiential learning, knowledge crystallization, and collaborative evolution between human expert and artificial agent. Drawing on established theories of knowledge creation (Nonaka & Takeuchi, 1995), skill acquisition (Dreyfus & Dreyfus, 1986), and cognitive apprenticeship (Collins et al., 1989), the framework provides formal definitions, operational patterns, and platform-agnostic guidelines for nurturing agents from general-purpose assistants into domain-specific experts through sustained conversational interaction.

---

## 1. Introduction

### 1.1 The Configuration Gap

Modern large language models demonstrate broad competence across diverse tasks, from code generation to scientific reasoning. However, a substantial gap persists between this raw capability and the domain-specific expertise required for production deployment. This gap manifests along several dimensions:

- **Tacit knowledge**: Much expert knowledge is implicit, context-dependent, and resistant to straightforward codification (Polanyi, 1966).
- **Personalization**: Effective domain practice reflects individual cognitive styles, organizational norms, and situational preferences that vary across practitioners.
- **Continuous evolution**: Domain knowledge is not static; it evolves with new tools, discoveries, and shifting best practices.
- **Contextual judgment**: Expert decision-making depends on nuanced pattern recognition acquired through accumulated experience, not merely access to reference documentation.

Bridging this configuration gap requires an approach that goes beyond static prompting or programmatic tooling.

### 1.2 Three Paradigms of Agent Development

We identify three distinct paradigms for developing domain-specific AI agents, each embodying fundamentally different assumptions about the nature of expertise and how it transfers to artificial systems.

| Dimension | Code-First | Prompt-First | Nurture-First |
|-----------|-----------|-------------|---------------|
| **Epistemology** | Expertise is algorithmic | Expertise is articulable | Expertise is experiential |
| **Development Model** | Software engineering | Technical writing | Cognitive apprenticeship |
| **Knowledge Source** | Developer's understanding | Prompt engineer's understanding | User's lived expertise |
| **Transfer Mechanism** | API/tool integration | System prompt instructions | Conversational immersion |
| **Adaptability** | Requires code changes | Requires prompt revision | Continuous and automatic |
| **Personalization** | Low (generic tools) | Medium (parameterized prompts) | High (user-specific patterns) |
| **Tacit Knowledge** | Cannot capture | Limited capture | Primary capture mechanism |
| **Maintenance Cost** | High (code maintenance) | Medium (prompt tuning) | Low (self-maintaining) |
| **Initial Setup** | Complex | Simple | Minimal |
| **Maturation Time** | Immediate (if correct) | Immediate (if well-prompted) | Weeks to months |
| **Theoretical Basis** | Software engineering | Instruction design | Knowledge creation theory |

### 1.3 Why Nurture-First?

The Nurture-First paradigm recognizes that the most valuable domain expertise is often tacit---knowledge that practitioners use daily but would struggle to articulate in a system prompt or API specification. As Polanyi (1966) observed, "we know more than we can tell." The nurture-first approach captures this knowledge through sustained interaction, extracting patterns from the user's reasoning processes, decision-making habits, and contextual judgments as they naturally occur.

This paradigm offers three decisive advantages:

1. **Tacit knowledge capture**: By observing expert reasoning in situ, the agent accumulates knowledge that the expert themselves may not explicitly recognize.
2. **Personalization**: The agent naturally aligns with the specific user's workflow, preferences, and cognitive style, rather than adopting a generic "best practice."
3. **Continuous evolution**: The agent's expertise evolves with the domain, adapting to new tools, shifting conventions, and the user's own developing understanding.

---

## 2. Core Concepts

### 2.1 Formal Definitions

We formalize the agent's knowledge state and the operations that transform it. These definitions follow the NFD formal model (Zhang, 2026).

**Definition 1: Agent Knowledge State.** At any time $t$, the agent's knowledge is characterized by a triple:

$$K_t = (C_t, S_t, E_t)$$

where:
- $C_t$ is the **Constitutional Layer**: stable, high-level principles, behavioral constraints, and core capability indices. This layer exhibits low volatility and is loaded at the start of every session.
- $S_t$ is the **Skill Layer**: modular, domain-specific knowledge units organized as discrete, composable skill documents. This layer exhibits medium volatility and is loaded on demand.
- $E_t$ is the **Experiential Layer**: raw accumulated observations, interaction records, and contextual annotations from conversational engagement. This layer exhibits high volatility and is accessed via semantic search.

**Definition 2: Experiential Accumulation.** Through each interaction turn $I_t$, the agent extracts and appends experiential knowledge:

$$E_{t+1} = E_t \cup \{\delta(I_t)\}$$

where $\delta$ is the experience extraction function that maps a conversational interaction to a structured experiential record containing decisions made, reasoning traces observed, outcomes achieved, and contextual annotations.

**Definition 3: Knowledge Crystallization.** At crystallization checkpoint $\tau$, the knowledge crystallization operator $\kappa$ consolidates accumulated experiential data into structured skill knowledge:

$$K'_{\tau} = \kappa(K_{\tau}) = (C'_{\tau}, S'_{\tau}, E'_{\tau})$$

subject to the constraints:
- $|E'_{\tau}| \leq |E_{\tau}|$ (experiential data is consolidated, not merely copied)
- $H(S'_{\tau}) \geq H(S_{\tau})$ (skill layer entropy---structural information content---does not decrease)

where $H$ denotes the structural entropy function measuring the information content and organizational quality of the skill layer.

**Definition 4: Value Function.** The overall value of an agent's knowledge state is defined as:

$$V(K_t) = \alpha \cdot \text{Breadth}(E_t) + \beta \cdot \text{Structure}(S_t) + \gamma \cdot \text{Align}(C_t, U)$$

where:
- $\text{Breadth}(E_t)$ measures the coverage and diversity of accumulated experiences
- $\text{Structure}(S_t)$ measures the organization, modularity, and retrieval quality of skill knowledge
- $\text{Align}(C_t, U)$ measures alignment between constitutional principles and the specific user $U$'s needs and preferences
- $\alpha, \beta, \gamma$ are weighting parameters reflecting operational priorities

**Definition 5: Crystallization Efficiency.** The efficiency of a crystallization operation is:

$$\eta(\kappa, E) = \frac{\Delta \text{Structure}(S)}{|E_{\text{consumed}}|}$$

where $\Delta \text{Structure}(S)$ is the improvement in skill layer structure and $|E_{\text{consumed}}|$ is the volume of experiential data consolidated. Efficient crystallization maximizes structural gain while minimizing knowledge loss.

**Proposition 1: Non-decreasing Value.** A valid crystallization operation must satisfy:

$$V(K'_{\tau}) \geq V(K_{\tau}) \quad \forall \tau$$

This ensures that crystallization never diminishes the agent's overall knowledge value. The proof follows from the constraints in Definition 3: structure does not decrease, breadth is maintained through indexed archiving, and alignment is preserved through user-validated crystallization.

### 2.2 The Five-Stage Learning Loop

The agent's developmental process is organized as a cyclic five-stage loop.

```
Study (Theory Input) --> Verify (Experimentation) --> Apply (Practice)
    ^                                                    |
    |                                                    v
Plan (Gap Analysis) <-- Extract (Crystallization) <-----+
```

#### Stage 1: Study (Theory Input)

**Description**: The agent acquires new theoretical knowledge through explicit instruction, documentation review, or guided exploration. This stage corresponds to the abstract conceptualization phase of Kolb's learning cycle.

**Input**: Domain documentation, user explanations, reference materials, or self-directed research topics identified during planning.

**Output**: Structured understanding of concepts, procedures, and principles recorded in the skill or experiential layer.

**Domain examples**:
- *Machine Learning*: Reading papers on new architectures, studying competition strategies.
- *Software Engineering*: Learning a new framework's API, understanding design patterns.
- *Legal Practice*: Reviewing case law, studying regulatory updates.
- *Medical Diagnosis*: Examining clinical guidelines, reviewing diagnostic criteria.

#### Stage 2: Verify (Experimentation)

**Description**: The agent tests newly acquired knowledge through controlled experiments, validating understanding against observable outcomes. This stage reduces the risk of incorporating incorrect or incomplete knowledge into the skill layer.

**Input**: Theoretical knowledge from Study stage; test scenarios provided by the user or self-generated.

**Output**: Validated knowledge with empirical confirmation; error records for knowledge that failed verification.

**Domain examples**:
- *Machine Learning*: Running baseline models, testing hyperparameter configurations.
- *Software Engineering*: Writing test cases, building proof-of-concept implementations.
- *Legal Practice*: Applying legal reasoning to hypothetical cases, checking citations.
- *Medical Diagnosis*: Comparing diagnostic reasoning against known case outcomes.

#### Stage 3: Apply (Practice)

**Description**: The agent deploys verified knowledge in real operational tasks, gaining practical experience and encountering edge cases that theory alone cannot anticipate. This is the primary stage for experiential accumulation.

**Input**: Validated knowledge; real-world tasks and problems from the user's workflow.

**Output**: Experiential records including decisions, outcomes, reasoning traces, and contextual annotations.

**Domain examples**:
- *Machine Learning*: Building production ML pipelines, conducting domain-specific experiments.
- *Software Engineering*: Developing features, debugging production issues, conducting code reviews.
- *Legal Practice*: Drafting legal documents, analyzing real cases, negotiating contracts.
- *Medical Diagnosis*: Assessing real patient presentations, developing treatment plans.

#### Stage 4: Extract (Crystallization)

**Description**: The agent systematically reviews accumulated experience, identifies recurring patterns, and consolidates them into structured skill knowledge. This stage implements the knowledge crystallization operation $\kappa$.

**Input**: Accumulated experiential records; existing skill and constitutional layers.

**Output**: Updated skill documents, consolidated experiential records, and (if warranted) revised constitutional principles.

**Domain examples**:
- *Machine Learning*: Documenting feature engineering patterns, codifying competition strategies.
- *Software Engineering*: Recording debugging heuristics, structuring code review guidelines.
- *Legal Practice*: Systematizing contract review checklists, organizing case analysis frameworks.
- *Medical Diagnosis*: Developing diagnostic decision trees, formalizing pattern recognition rules.

#### Stage 5: Plan (Gap Analysis)

**Description**: The agent evaluates its current knowledge state against operational demands, identifying gaps that require further study or experience. This stage drives the next iteration of the learning loop.

**Input**: Current knowledge state $K_t$; upcoming task requirements; performance metrics from recent operations.

**Output**: Prioritized learning agenda; identified skill gaps; recommended focus areas for the next Study phase.

**Domain examples**:
- *Machine Learning*: Identifying unfamiliar data domains, recognizing missing technique coverage.
- *Software Engineering*: Noting knowledge gaps in unfamiliar codebases, planning technology exploration.
- *Legal Practice*: Recognizing jurisdictional knowledge gaps, identifying regulatory areas needing study.
- *Medical Diagnosis*: Identifying rare conditions not yet encountered, planning continuing education.

### 2.3 Applicability Conditions

The Agent Nurture Framework is not universally applicable. Drawing on the NFD analysis (Zhang, 2026, Section 3.3), we identify five conditions under which the nurture-first approach provides maximal advantage:

1. **Domain expertise is substantially tacit.** When the most valuable knowledge cannot be fully articulated in documentation or system prompts, experiential accumulation becomes the primary acquisition channel. Domains where "knowing how" exceeds "knowing that" are strong candidates.

2. **Expertise is highly personal.** When effective practice varies significantly across practitioners---reflecting individual cognitive styles, organizational contexts, or workflow preferences---the personalization afforded by sustained one-on-one interaction provides decisive advantages over generic approaches.

3. **Expertise evolves continuously.** When domain knowledge shifts rapidly due to tool updates, new research, or changing best practices, the continuous learning loop ensures the agent remains current without requiring manual reprogramming.

4. **The interaction pattern is conversational.** The framework is designed for environments where user-agent interaction naturally occurs through dialogue---code review sessions, strategic discussions, collaborative problem-solving---rather than purely transactional request-response patterns.

5. **Experiential pattern recognition is valuable.** When the domain rewards the ability to recognize patterns across accumulated experience---identifying recurring problem structures, predicting likely failure modes, or recognizing optimal intervention points---the crystallization mechanism provides compounding returns.

When fewer than three of these conditions hold, a simpler Prompt-First or Code-First approach may be more cost-effective.

---

## 3. Operational Framework

### 3.1 The Dual-Workspace Pattern

Effective agent nurturing requires a clear separation between development and runtime environments. The Dual-Workspace Pattern establishes two distinct operational contexts:

**Surgical Workspace (Development Environment)**

The surgical workspace is the controlled environment where batch operations, knowledge crystallization, and skill development occur. Its characteristics include:

- **Batch-oriented operations**: Crystallization runs, skill restructuring, and knowledge base maintenance are performed as deliberate, reviewable operations.
- **Full context access**: Complete access to all knowledge layers for comprehensive analysis and restructuring.
- **Human-in-the-loop validation**: Crystallization outputs are reviewed by the user before integration into the active knowledge base.
- **Version control integration**: All knowledge asset changes are tracked, enabling rollback and audit.
- **Offline processing**: Operations can be performed outside active task execution, preventing interference with daily workflow.

**Nurturing Workspace (Runtime Environment)**

The nurturing workspace is the live environment where daily conversational interaction, experiential accumulation, and real-time knowledge application occur. Its characteristics include:

- **Interactive, conversational operation**: The agent engages in natural dialogue with the user, accumulating experience through genuine collaboration.
- **Selective context loading**: Only relevant skills and recent experience are loaded, respecting context window constraints.
- **Autonomous experiential recording**: The agent automatically extracts and records experiential knowledge from each interaction.
- **Non-disruptive operation**: Knowledge accumulation occurs transparently, without requiring explicit user intervention.
- **Real-time application**: Crystallized knowledge is actively applied to current tasks, generating feedback for the next crystallization cycle.

The surgical workspace feeds improved knowledge assets into the nurturing workspace, while the nurturing workspace generates the raw experiential data that the surgical workspace processes. This creates a continuous improvement cycle.

### 3.2 The Spiral Development Model

Agent development proceeds through a spiral model, where each cycle deepens expertise and expands capability.

**Phase 0: Bootstrap (Days 1--2)**

The agent is initialized with minimal scaffolding: a constitutional document establishing core behavioral principles, initial role definition, and basic operational guidelines. No domain-specific skills are loaded; the agent begins as a capable generalist with the right disposition for learning.

Deliverables:
- Constitutional document (CLAUDE.md or equivalent)
- Initial workspace configuration
- Logging and experiential recording setup

**Phase 1: Initial Nurturing (1--3 Weeks)**

The user engages the agent in normal operational tasks. During this phase:
- The agent accumulates experiential knowledge through daily interaction.
- The user provides natural corrections, explanations, and guidance.
- No explicit crystallization occurs; the focus is on raw experience accumulation.
- The agent begins to recognize recurring patterns in the user's workflow.

**Crystallization Checkpoint 1**

The first deliberate crystallization event:
- Review accumulated experiential data (typically 50--200 interaction records).
- Extract 3--5 high-confidence skill patterns.
- Create initial skill documents.
- Establish extraction quality standards for future cycles.

**Phase 2: Structured Nurturing (1--3 Months)**

With foundational skills in place, the agent enters a structured development phase:
- Crystallized skills are actively applied and validated against real tasks.
- The learning loop operates at full capacity: Study, Verify, Apply, Extract, Plan.
- Skill documents are refined based on application feedback.
- The agent begins proposing solutions informed by crystallized patterns.
- Regular crystallization cycles (weekly or biweekly) maintain knowledge quality.

**Crystallization Checkpoint 2**

A comprehensive review and restructuring:
- Validate all existing skills against accumulated experience.
- Restructure skill organization for improved retrieval and modularity.
- Identify and fill remaining knowledge gaps.
- Assess constitutional alignment and adjust principles if warranted.

**Phase 3+: Mature Operation (Ongoing)**

The agent operates as a domain expert with self-maintaining knowledge:
- Crystallization operates as a background process, triggered automatically.
- Skills evolve continuously with the domain.
- The agent proactively identifies knowledge gaps and requests targeted learning.
- Experiential data is efficiently managed through automated archival.
- The human-agent collaboration deepens into a genuine cognitive partnership.

---

## 4. Platform Adaptation

The Agent Nurture Framework is designed to be platform-agnostic. The following table provides concrete adaptation guidance for major agent platforms.

| Component | Claude Code | Codex CLI | Gemini CLI | Custom Agent |
|-----------|-------------|-----------|------------|--------------|
| **Constitutional Layer** | `CLAUDE.md` in project root | System prompt or config file | System instruction in GEMINI.md | System prompt configuration |
| **Skill Layer** | Markdown files in `.claude/skills/` | Skill files in project directory | Skill files in `.gemini/skills/` | Configurable skill directory |
| **Experiential Layer** | `.claude/experience/` with semantic search | Session logs with custom indexing | `.gemini/memory/` files | Vector database or file store |
| **Surgical Workspace** | Separate project or branch | Dedicated workspace directory | Separate project context | Admin interface or CLI tool |
| **Nurturing Workspace** | Daily project workspace | Active project directory | Active project context | Production runtime |
| **Crystallization Trigger** | Manual or scripted | Manual or CI/CD pipeline | Manual or scheduled task | Event-driven automation |
| **Version Control** | Git-tracked skill files | Git-tracked configuration | Git-tracked files | Database versioning |
| **Context Management** | Automatic with CLAUDE.md | Manual prompt construction | Automatic with GEMINI.md | Custom context assembly |
| **Skill Loading** | On-demand via glob patterns | Explicit import | On-demand via configuration | Plugin/module system |

---

## 5. Critical Success Factors

Drawing on practical experience with nurture-first agent development, we identify the following factors that critically influence outcomes.

### 5.1 Start Minimal, Iterate Relentlessly

Resist the temptation to create a comprehensive initial configuration. A lean bootstrap that captures core principles outperforms an exhaustive specification that attempts to anticipate every scenario. The agent's knowledge should grow organically from real experience, not from speculative design.

### 5.2 Protect the Crystallization Quality

Not every experience deserves to become a skill. Over-extraction dilutes the skill layer, making relevant knowledge harder to find and degrading retrieval quality. Apply strict extraction criteria: reusable, non-trivial, specific, and verified (see [Crystallization Cycle](crystallization-cycle.md) for detailed criteria).

### 5.3 Maintain Constitutional Discipline

The constitutional layer should remain lean and stable. It exists to provide orientation and behavioral principles, not to encode detailed domain knowledge. When constitutional documents grow beyond 10--15% of the effective context window, the agent's performance degrades due to attention dilution.

### 5.4 Embrace Asymmetric Expertise

The goal is not to create an agent that knows everything the user knows. Rather, it is to create an agent that excels at the specific intersection of tasks, patterns, and reasoning styles that characterize the user's domain practice. Specialized expertise outperforms broad but shallow capability.

### 5.5 Respect the Maturation Timeline

Nurture-first development requires patience. The first weeks produce an agent that appears little different from a baseline LLM, but this apparent stasis masks the accumulation of experiential data that will drive crystallization. Premature crystallization from insufficient data produces low-quality skills; delayed crystallization risks losing contextual richness. Trust the spiral model.

### 5.6 Separate Workspaces Rigorously

Conflation of development and runtime environments is the most common architectural failure. Crystallization operations require focused attention and full context; performing them during active task execution degrades both the task and the crystallization. Maintain the dual-workspace separation.

### 5.7 Validate Against Real Tasks

Every crystallized skill must be validated against real operational tasks, not merely against the experiential data from which it was extracted. Skills that work in theory but fail in practice must be revised or discarded. The Apply stage serves this validation function.

### 5.8 Invest in the Experiential Recording Pipeline

The quality of crystallization is bounded by the quality of experiential records. Invest early in establishing what is recorded, how it is structured, and how it is indexed. A well-designed experiential recording pipeline pays compounding returns across the entire development lifecycle.

---

## References

- Bhargava, A. (2026). Modular Intelligence: Skill-Based Paradigm for Scalable Agent Architecture. *Journal of Innovations in Software Engineering Methodology (JISEM)*.
- Collins, A., Brown, J. S., & Newman, S. E. (1989). Cognitive Apprenticeship: Teaching the Craft of Reading, Writing, and Mathematics. In L. B. Resnick (Ed.), *Knowing, Learning, and Instruction: Essays in Honor of Robert Glaser*. Lawrence Erlbaum Associates.
- Dreyfus, H. L., & Dreyfus, S. E. (1986). *Mind over Machine: The Power of Human Intuition and Expertise in the Era of the Computer*. Free Press.
- Kolb, D. A. (1984). *Experiential Learning: Experience as the Source of Learning and Development*. Prentice-Hall.
- Nonaka, I., & Takeuchi, H. (1995). *The Knowledge-Creating Company*. Oxford University Press.
- Polanyi, M. (1966). *The Tacit Dimension*. Doubleday.
- Zhang, K. (2026). Nurture-First Development: A Knowledge Crystallization Approach to Domain-Specific AI Agent Development. *arXiv preprint arXiv:2603.10808*.
- tanaikech. (2026). Recursive Knowledge Crystallization (RKC) Framework. Google Cloud.
