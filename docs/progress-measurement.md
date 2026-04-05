# Progress Measurement

## 1. Capability Matrix

The capability matrix provides a structured way to assess an agent's competence across multiple dimensions. Each dimension captures a distinct aspect of agent performance, enabling targeted improvement rather than vague "better/worse" assessments.

### Generic Dimensions

| Dimension | Rating | What It Measures |
|-----------|--------|-----------------|
| Core Knowledge | 1-5 | Foundation breadth and depth in the primary domain |
| Domain Expertise | 1-5 | Specialized capability within the target domain |
| Problem Solving | 1-5 | Debugging, investigation, and root cause analysis |
| Workflow Mastery | 1-5 | Process efficiency and task execution quality |
| Knowledge Synthesis | 1-5 | Cross-domain pattern recognition and transfer |
| Autonomous Operation | 1-5 | Independent task completion without guidance |

### Rating Scale

The rating scale is aligned with the Dreyfus model of skill acquisition, which provides a well-established framework for describing how competence develops through experience.

- **1 (Novice):** Needs step-by-step guidance. Follows explicit rules without understanding context. Cannot adapt when situations deviate from documented procedures.
- **2 (Advanced Beginner):** Can follow known patterns. Applies learned solutions to recognizable problems. Begins to understand domain vocabulary and conventions but still relies heavily on reference material.
- **3 (Competent):** Can adapt patterns to new situations. Understands the reasoning behind procedures and can modify them when context changes. Begins to prioritize and plan.
- **4 (Proficient):** Can discover and validate new approaches. Sees situations holistically rather than as collections of discrete steps. Can recognize deviations from expected patterns and investigate them systematically.
- **5 (Expert):** Can innovate beyond documented techniques. Relies on deep intuitive understanding built from extensive experience. Creates new approaches, tools, and frameworks that others can follow.

### Interpreting the Matrix

An agent rated at level 3 across all dimensions is a solid, reliable performer that can handle most tasks in its domain with minimal supervision. An agent at level 5 in one dimension but level 1 in others is a specialist that may produce brilliant output in narrow contexts but struggle with general tasks.

The goal is balanced growth. Prioritize raising the lowest dimensions first, since weaknesses in foundational dimensions like Problem Solving or Autonomous Operation limit the value of high scores in specialized dimensions.

---

## 2. Knowledge Growth Metrics

These shell commands provide quantitative measures of the knowledge base's size, distribution, and freshness. Run them periodically to track how the agent's knowledge evolves.

### Total Skills

The total skill count should grow during early learning, then plateau as consolidation begins to outpace new skill creation.

```bash
# Count total skills
find $SKILL_DIR -name "SKILL.md" | wc -l
```

**Expected trajectory:** Rapid growth in weeks 1-4 (5-15 new skills per week), slowing growth in weeks 5-8 (2-5 new skills per week), plateau around week 8-12 as consolidation matches creation rate.

### Skills by Category

This shows how knowledge is distributed across domains. A healthy knowledge base shifts from many small, fragmented skills to fewer large, consolidated skills over time.

```bash
# Count skills by category prefix
ls $SKILL_DIR | sed 's/-.*//' | sort | uniq -c | sort -rn
```

**Expected trajectory:** Early distributions show many categories with 1-2 skills each. Mature distributions show fewer categories with 3-5 well-consolidated skills each.

### Memory Files

Memory files represent the experiential layer. They should cycle through creation, crystallization, and archival.

```bash
# Count total memory files
find $MEMORY_DIR -name "*.md" | wc -l
```

**Expected trajectory:** Grows continuously during active use, but the rate of new file creation should slow as more experience is crystallized into skills rather than accumulating as raw memory.

### Stale Memory Files

Stale files represent knowledge that has not been revisited. A high stale count may indicate crystallization backlog.

```bash
# Count stale memory files (not updated in 2+ weeks)
find $MEMORY_DIR -name "*.md" -mtime +14 | wc -l
```

**Expected trajectory:** Stale file count should stay below 30% of total memory files. If stale files exceed 30%, schedule a crystallization session.

### Skill Age Distribution

```bash
# Skills created in the last 7 days
find $SKILL_DIR -name "SKILL.md" -mtime -7 | wc -l

# Skills created in the last 30 days
find $SKILL_DIR -name "SKILL.md" -mtime -30 | wc -l

# Skills older than 90 days (may need review)
find $SKILL_DIR -name "SKILL.md" -mtime +90 | wc -l
```

---

## 3. Efficiency Indicators

Efficiency indicators measure how effectively the agent converts experience into useful, retrievable knowledge.

| Indicator | What It Measures | Target | Trend |
|-----------|-----------------|--------|-------|
| Time to competence | Overall agent capability for new project types | Decreasing over projects | Should show clear reduction as knowledge accumulates |
| Skills triggered per task | Knowledge activation rate | High (relevant skills surface automatically) | Should increase as skills mature and descriptions improve |
| New skills per session | Learning rate | Steady (1-3 per session) | Should remain consistent during active learning phases |
| Skills consolidated per month | Knowledge maturity | Increasing | Should rise as the knowledge base grows and fragmentation increases |
| Repeated mistakes rate | Learning effectiveness | Decreasing toward zero | Should drop sharply after each crystallization cycle |
| Crystallization efficiency (eta) | Knowledge consolidation quality | Improving over cycles | Should trend upward as the operator refines extraction skills |

### Crystallization Efficiency (eta)

Crystallization efficiency measures the ratio of useful, triggered skills to total crystallization effort.

```
eta = (skills_triggered_in_last_30_days) / (total_skills_created_in_last_90_days)
```

- eta close to 1.0: Nearly all created skills are actively used. Excellent crystallization quality.
- eta between 0.5 and 0.8: Most skills are useful, some may need consolidation or improved descriptions.
- eta below 0.5: Many skills are dormant. Review crystallization process and description quality.

### Tracking Repeated Mistakes

A repeated mistake occurs when the agent encounters a problem it has previously solved (documented in a skill) but fails to apply the skill. Track these events to measure knowledge retrieval effectiveness.

```bash
# Count repeated mistakes (requires manual logging)
grep -r "repeated-mistake" $MEMORY_DIR --include="*.md" | wc -l
```

---

## 4. Value Function Over Time

The overall value of the agent's knowledge state at time t is modeled as:

```
V(K_t) = alpha * Breadth(E) + beta * Structure(S) + gamma * Align(C, U)
```

Where:

- **Breadth(E)** measures the coverage of accumulated experiences. How many different problems, domains, and contexts does the knowledge base address?
- **Structure(S)** measures the organization and retrievability of knowledge. Are skills well-structured, properly indexed, and semantically discoverable?
- **Align(C, U)** measures the alignment between the agent's capabilities (C) and the user's actual needs (U). Does the knowledge base address the problems the user actually encounters?

The coefficients alpha, beta, and gamma shift over the agent lifecycle, reflecting the changing priorities of knowledge development.

### Early Phase (Weeks 1-4): Alpha Dominates

In the early phase, the agent is accumulating raw experience. Every new problem encountered, every bug fixed, every workflow learned adds breadth to the knowledge base. Structure is less critical because the knowledge base is small enough to navigate manually. Alignment is still being established as the agent learns what the user actually needs.

- **Alpha (Breadth):** High. New experiences are extremely valuable.
- **Beta (Structure):** Low. The knowledge base is small; rough organization is sufficient.
- **Gamma (Alignment):** Low. The agent is still learning the user's needs.

**Indicator:** Rapid skill count growth, high new-skills-per-session rate.

### Middle Phase (Weeks 5-12): Beta Dominates

In the middle phase, the agent has accumulated substantial breadth but the knowledge base is becoming difficult to navigate. Structure becomes the primary value driver. Well-organized skills are discoverable and usable; poorly organized skills are effectively invisible.

- **Alpha (Breadth):** Moderate. New experiences still add value, but marginal returns are decreasing.
- **Beta (Structure):** High. Organizing, consolidating, and indexing existing knowledge yields the greatest improvement.
- **Gamma (Alignment):** Growing. The agent can now identify which knowledge aligns with the user's needs.

**Indicator:** Consolidation activity increases, crystallization efficiency improves, repeated mistake rate drops.

### Mature Phase (Weeks 12+): Gamma Differentiates

In the mature phase, the agent has broad coverage and a well-structured knowledge base. The remaining value comes from alignment: ensuring that the knowledge base is precisely tuned to the user's evolving needs. This includes pruning obsolete skills, deepening frequently-used skills, and identifying gaps in coverage.

- **Alpha (Breadth):** Low. New experiences add marginal value unless they address genuine gaps.
- **Beta (Structure):** Moderate. The knowledge base is well-organized; structural improvements yield smaller gains.
- **Gamma (Alignment):** High. Fine-tuning the knowledge base to the user's specific workflow and priorities provides the greatest value.

**Indicator:** Skill count plateaus, quality of triggered skills improves, user satisfaction increases.

### Visualizing the Shift

```
Value Contribution Over Time:

Week  1-4:  Alpha ████████████  Beta ██          Gamma █
Week  5-8:  Alpha ██████        Beta ██████████  Gamma ███
Week  9-12: Alpha ████          Beta ██████      Gamma ████████
Week  13+:  Alpha ███           Beta ████        Gamma ████████████
```

---

## 5. Measurement Workflow

Periodic capability assessments ensure the agent is progressing along the intended trajectory and reveal areas that need targeted intervention.

### Weekly Assessment

**Frequency:** Every 7 days.

**Duration:** 15-30 minutes.

**Steps:**

1. **Run knowledge growth metrics.** Execute the shell commands in Section 2 to get current counts and distributions.
2. **Review session logs.** Skim the past week's memory files for notable events, mistakes, and discoveries.
3. **Check efficiency indicators.** Calculate or estimate the indicators in Section 3.
4. **Update the capability matrix.** Re-rate each dimension based on the week's observations. Note any changes.
5. **Identify action items.** Based on the assessment, decide what to focus on in the coming week.

**Output:** A brief weekly assessment note in the memory directory.

### Monthly Deep Assessment

**Frequency:** Every 30 days.

**Duration:** 1-2 hours.

**Steps:**

1. **Complete capability matrix assessment.** Use the full template (`templates/capability-matrix-template.md`). Rate each dimension with specific evidence.
2. **Conduct consolidation audit.** Use the consolidation audit template (`templates/consolidation-audit-template.md`). Identify fragmentation and merge candidates.
3. **Run crystallization session.** Extract new skills from the past month's experience.
4. **Calculate value function coefficients.** Estimate alpha, beta, and gamma based on the current lifecycle phase. Assess whether the knowledge strategy aligns with the current priorities.
5. **Compare to previous assessment.** Track changes in ratings, skill counts, and efficiency indicators over time.
6. **Adjust learning strategy.** If certain dimensions are stagnating, adjust the learning approach. For example, if Problem Solving is stuck at level 2, introduce structured debugging exercises.

**Output:** A comprehensive monthly assessment document.

### Quarterly Strategy Review

**Frequency:** Every 90 days.

**Duration:** 2-4 hours.

**Steps:**

1. **Review all past assessments.** Identify long-term trends in capability growth, knowledge base evolution, and value function trajectory.
2. **Evaluate alignment with user needs.** Has the user's workflow or priorities changed? Does the knowledge base still address their primary needs?
3. **Archive obsolete knowledge.** Skills and memory files that have not been triggered in 90+ days and are no longer relevant to the user's workflow should be archived.
4. **Set learning objectives for the next quarter.** Based on the assessment, define specific, measurable goals for each capability dimension.
5. **Update constitutional layer if needed.** If the assessment reveals fundamental gaps in the agent's principles or behavioral boundaries, update the soul.md and principles.md files.

**Output:** A quarterly strategy document with objectives and milestones.
