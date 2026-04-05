# Crystallization Operation Checklist

Date: [YYYY-MM-DD]
Operator: [Name]
Scope: [What knowledge domain or session is being crystallized]

---

## Pre-Crystallization

These steps ensure the crystallization session is properly scoped and prepared.

- [ ] Identified scope of experiential data to crystallize (specific date range, project, or domain)
- [ ] Reviewed recent session logs for extractable knowledge
- [ ] Checked for existing skills that might overlap with anticipated new skills
- [ ] Prepared surgical workspace (development environment with access to skill directory)
- [ ] Noted any patterns or recurring themes observed during the scope period
- [ ] Confirmed that the experiential data is complete (no missing session logs within scope)

---

## Pattern Extraction

These steps identify candidate patterns from the raw experiential data.

- [ ] Scanned experiential records for recurring patterns
- [ ] Identified at least [N] potential patterns (set a target based on scope)
- [ ] Categorized each pattern by type:
  - Bug fix: Error encountered, root cause identified, solution applied
  - Workflow: Process improvement or optimization discovered
  - Domain knowledge: Domain-specific insight gained
  - Configuration: Optimal settings or setup procedure discovered
- [ ] Documented each pattern with trigger conditions (specific error messages, symptoms, or scenarios)
- [ ] Assessed each pattern for non-triviality (is this knowledge that would not be obvious from documentation alone?)
- [ ] Assessed each pattern for reusability (would this apply to future sessions, or was it specific to this one?)

---

## Validation

These steps ensure each candidate pattern meets the quality bar for crystallization into a skill.

- [ ] Each pattern is reusable (not session-specific; applies to future contexts)
- [ ] Each pattern is non-trivial (not information that could be found by reading basic documentation)
- [ ] Each pattern has been verified to work (the solution was tested and produced the expected result)
- [ ] Each pattern has specific trigger conditions (can be matched by semantic search when relevant)
- [ ] Checked against full experiential corpus for support (does the pattern hold across multiple sessions, or was it a one-time observation?)
- [ ] Verified that no existing skill already covers this pattern (if one does, the pattern should be an update rather than a new skill)

---

## Structuring

These steps convert validated patterns into well-structured skill files.

- [ ] Created skill files following the skill-template.md format
- [ ] YAML frontmatter is complete and accurate:
  - [ ] `name` field uses descriptive-kebab-case
  - [ ] `description` field includes use cases, trigger conditions, and problem statement
  - [ ] `author`, `version`, `date`, and `tags` fields are filled
- [ ] Description contains trigger conditions for semantic matching (specific error messages, symptoms, scenarios)
- [ ] Solution is step-by-step and actionable (can be followed without additional research)
- [ ] Verification method included (how to confirm the solution worked)
- [ ] Example section provides a concrete application of the skill
- [ ] Cross-references added to related skills in the Notes section
- [ ] Skill is assigned to the correct layer:
  - L1 (Constitutional): Core principles and identity -- rarely created during crystallization
  - L2 (Skill): Reusable, domain-specific knowledge -- most crystallization output
  - L3 (Memory): Session-specific notes -- raw material, not a crystallization target

---

## Integration

These steps add the new skills to the knowledge base and maintain the overall structure.

- [ ] New skills saved to appropriate directory in the skill layer (L2)
- [ ] File and directory naming follows the established convention
- [ ] Version numbers assigned (start at 1.0.0 for new skills, increment for updates)
- [ ] Stale experiential entries archived (moved from active memory to archive)
- [ ] Memory index updated to reflect new skills and archived entries
- [ ] Constitutional layer updated if principles or behavioral boundaries were discovered during the session

---

## Post-Crystallization

These steps verify the crystallization session's output and maintain knowledge base health.

- [ ] Skill count audit completed (total skills before and after)
- [ ] Fragmentation check performed (any new skills that overlap significantly with existing ones?)
- [ ] Capability matrix updated to reflect new knowledge areas
- [ ] Crystallization efficiency metric calculated:
  ```
  eta = (skills expected to be triggered) / (skills created)
  ```
- [ ] Session summary recorded in memory:
  - Date and scope of crystallization
  - Number of patterns identified, validated, and crystallized
  - Any patterns rejected and why
  - Skills created or updated
- [ ] Next crystallization session scheduled (recommended: weekly during active learning, bi-weekly during maintenance)

---

## Quick Reference: Crystallization Decision Criteria

| Criterion | Pass | Fail |
|-----------|------|------|
| Reusable? | Applies to future sessions | Specific to one event |
| Non-trivial? | Not in basic documentation | Easily found via search |
| Verified? | Solution tested and works | Solution untested or theoretical |
| Specific triggers? | Clear error messages or symptoms | Vague or generic conditions |
| Novel? | Not covered by existing skill | Duplicate of existing skill |

A pattern must pass all five criteria to be crystallized into a new skill. If it fails "Novel" but passes the rest, it should be incorporated into the existing skill as an update.
