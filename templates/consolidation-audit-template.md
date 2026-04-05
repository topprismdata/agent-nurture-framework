# Skill Consolidation Audit

Date: [YYYY-MM-DD]
Auditor: [Name]
Audit Period: [Start Date] to [End Date]

---

## Overview

- **Total Skills:** [N]
- **Active Skills (triggered in last 30 days):** [N]
- **Stale Skills (not triggered in 30+ days):** [N]
- **New Skills This Period:** [N]
- **Skills Consolidated This Period:** [N]

---

## Skill Inventory

List all skills with their current status. This provides the raw data for cluster analysis.

| # | Skill Name | Category | Last Triggered | Size (lines) | Quality Score | Status |
|---|-----------|----------|---------------|--------------|--------------|--------|
| 1 | | | | | | Active / Stale / Merge Candidate |
| 2 | | | | | | Active / Stale / Merge Candidate |
| 3 | | | | | | Active / Stale / Merge Candidate |
| 4 | | | | | | Active / Stale / Merge Candidate |
| 5 | | | | | | Active / Stale / Merge Candidate |

**Quality Score:** Rate each skill 1-5 based on specificity, reusability, non-triviality, and actionability.

**Status Definitions:**
- **Active:** Triggered in the last 30 days and performing well.
- **Stale:** Not triggered in the last 30 days. May be obsolete or redundant.
- **Merge Candidate:** Flagged for potential consolidation with one or more other skills.

---

## Cluster Analysis

Group skills by domain prefix or topic area. Categories with more than five skills are strong candidates for consolidation.

### Cluster 1: [Domain/Prefix Name]

- **Skills in cluster:** [List skill names]
- **Count:** [N]
- **Average Jaccard similarity:** [X.XX]
- **Overlap assessment:** [Description of how much these skills overlap in trigger conditions and solutions]
- **Recommendation:** Keep separate / Merge into [target skill name]
- **Merge priority:** High / Medium / Low
- **Rationale:** [Why this recommendation was made]

### Cluster 2: [Domain/Prefix Name]

- **Skills in cluster:** [List skill names]
- **Count:** [N]
- **Average Jaccard similarity:** [X.XX]
- **Overlap assessment:** [Description]
- **Recommendation:** Keep separate / Merge into [target skill name]
- **Merge priority:** High / Medium / Low
- **Rationale:** [Why this recommendation was made]

### Cluster 3: [Domain/Prefix Name]

- **Skills in cluster:** [List skill names]
- **Count:** [N]
- **Average Jaccard similarity:** [X.XX]
- **Overlap assessment:** [Description]
- **Recommendation:** Keep separate / Merge into [target skill name]
- **Merge priority:** High / Medium / Low
- **Rationale:** [Why this recommendation was made]

---

## Merge Recommendations

Specific merge actions derived from the cluster analysis.

| Source Skills | Target Skill | Overlap % | Trigger Compatibility | Action |
|--------------|-------------|-----------|----------------------|--------|
| [skill-a, skill-b, skill-c] | [merged-skill-name] | [X%] | [Compatible / Partial / Incompatible] | Merge / Keep / Delete |
| [skill-d, skill-e] | [merged-skill-name] | [X%] | [Compatible / Partial / Incompatible] | Merge / Keep / Delete |
| [skill-f] | N/A | N/A | N/A | Archive |

**Trigger Compatibility Definitions:**
- **Compatible:** Trigger conditions can be combined without ambiguity.
- **Partial:** Some trigger conditions overlap, others are distinct. Requires careful merge.
- **Incompatible:** Trigger conditions serve different purposes. Should remain separate.

---

## Stale Skills (>30 Days Without Trigger)

Skills that have not been auto-triggered in the past 30 days.

| Skill Name | Last Used | Days Since Trigger | Possible Reason | Recommendation |
|------------|-----------|-------------------|-----------------|----------------|
| | | | Obsolete / Redundant / Poor indexing / Low relevance | Archive / Keep / Investigate / Improve description |

**Possible Reasons for Staleness:**
- **Obsolete:** The problem this skill addresses no longer occurs (e.g., a dependency was updated).
- **Redundant:** Another skill covers the same problem more effectively.
- **Poor indexing:** The skill's description does not match the queries that should trigger it.
- **Low relevance:** The problem is genuine but rare in the current workflow.

---

## Action Items

Based on this audit, the following actions are recommended:

### High Priority (Complete within 1 week)

- [ ] Merge [Source Skills] into [Target Skill] -- [Rationale in one sentence]
- [ ] Archive stale skill [Skill Name] -- [Rationale]
- [ ] Improve description for [Skill Name] to fix poor indexing

### Medium Priority (Complete within 2 weeks)

- [ ] Merge [Source Skills] into [Target Skill]
- [ ] Investigate stale skill [Skill Name] to determine reason for non-triggering
- [ ] Create new consolidated skill for [Domain] covering [Scope]

### Low Priority (Complete by next audit)

- [ ] Review [Cluster] for potential future consolidation
- [ ] Update skill [Name] with additional trigger conditions

### Scheduling

- **Next audit scheduled for:** [YYYY-MM-DD]
- **Next crystallization session scheduled for:** [YYYY-MM-DD]
- **Next capability assessment scheduled for:** [YYYY-MM-DD]

---

## Metrics Summary

Track these metrics across audits to measure consolidation effectiveness.

| Metric | Previous Audit | Current Audit | Trend |
|--------|---------------|---------------|-------|
| Total skills | | | |
| Active skills | | | |
| Stale skills | | | |
| Avg. skills per category | | | |
| Avg. Jaccard similarity | | | |
| Crystallization efficiency (eta) | | | |
