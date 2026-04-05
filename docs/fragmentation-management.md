# Fragmentation Management

## 1. The Fragmentation Problem

As an agent learns, it accumulates many small, specific skills: bug fixes, workarounds, domain snippets, configuration tips, and workflow shortcuts. Each skill is individually valuable, but over time they create **semantic noise**. When the skill matcher evaluates a new task, it surfaces multiple similar skills, making it harder to identify the most relevant one. The retrieval signal degrades, the agent spends more time evaluating candidates, and the user sees diminishing returns from the knowledge base.

This is not a failure of the learning process. Fragmentation is the natural consequence of incremental knowledge acquisition. The solution is not to learn less, but to **consolidate deliberately**.

### Symptoms of Fragmentation

- A semantic search for a problem returns five or more partially overlapping skills.
- The agent applies the wrong variant of a solution because two skills cover similar ground.
- The skill count grows steadily while the per-skill value declines.
- Crystallization sessions produce skills that duplicate existing ones under different names.
- The user must manually specify which skill to apply because automatic matching is ambiguous.

### Root Cause

Each learning event creates a new, narrow skill optimized for the immediate context. Without periodic consolidation, these micro-skills never merge into coherent, high-value knowledge units. The knowledge base resembles a library where every page is its own book.

---

## 2. Decision Framework: Keep Separate vs. Merge

Not every cluster of similar skills should be merged. The decision depends on whether the skills serve distinct purposes or merely fragment a single purpose.

### Keep Separate When

- **Different trigger conditions.** The skills activate in response to different error messages, symptoms, or contexts. For example, "connection refused" and "connection timeout" may look similar but have distinct root causes and solutions.
- **Skills from different domains.** A debugging pattern in web development and a debugging pattern in data engineering may share structure but serve different audiences and contexts.
- **The skill is the canonical reference for a specific problem.** If a skill is the definitive, well-tested answer to a narrowly defined problem, merging it with adjacent skills risks diluting its precision.
- **Trigger conditions are highly specific and distinct.** When the conditions that activate each skill are unambiguous and non-overlapping, separate skills improve matching accuracy.

### Merge When

- **Same domain prefix with more than five skills.** When more than five skills share a directory prefix (e.g., `api-integration/`), the domain is likely over-fragmented and would benefit from consolidation.
- **Trigger conditions overlap by more than 50%.** If most of the scenarios that activate Skill A also activate Skill B, the skills are competing for the same retrieval slot and should be unified.
- **No skill has been auto-triggered in 30 or more days.** A skill that never fires is either stale or redundant with another skill that captures the same knowledge more effectively.
- **Skills share more than 50% of their solution content.** When the actionable steps in two skills are largely identical, maintaining them separately creates a synchronization burden. Any update to one must be replicated in the other.

### Decision Flowchart

```
Are trigger conditions distinct?
  YES → Keep separate
  NO  → Do solutions differ significantly?
          YES → Keep separate, add cross-reference
          NO  → Merge into single skill
```

---

## 3. Three-Phase Consolidation Strategy

Consolidation is a deliberate, repeatable process. It should be performed regularly as part of the agent's knowledge maintenance cycle.

### Phase 1: Audit (Weekly)

The audit phase identifies fragmentation without attempting to fix it. Its purpose is to surface clusters and candidates for consolidation.

**Steps:**

1. **Count skills by prefix or category.** List all skill directories and count the number of skills in each. Categories with more than five skills are consolidation candidates.

2. **Identify clusters.** Within large categories, group skills by trigger condition similarity. Skills that address related problems form natural clusters.

3. **Flag stale skills.** Query the trigger log for skills not activated in the past 30 days. Stale skills may be obsolete, redundant, or poorly indexed.

4. **Calculate overlap metrics.** For each cluster, compute pairwise similarity between skill descriptions and solution content using Jaccard similarity. Pairs above 0.3 warrant review; pairs above 0.5 are strong merge candidates.

5. **Produce an audit report.** Summarize findings in the consolidation audit template (see `templates/consolidation-audit-template.md`).

**Output:** A prioritized list of clusters to consolidate, with specific merge recommendations.

### Phase 2: Merge (Per Cluster)

For each cluster identified in the audit, perform a structured merge.

**Steps:**

1. **Group related skills.** Lay out all skills in the cluster side by side. Map their trigger conditions, solutions, and edge cases.

2. **Identify the primary skill.** The primary skill is the one that is most comprehensive, most frequently triggered, or most recently updated. It becomes the foundation for the merged skill.

3. **Absorb secondary skills.** For each secondary skill:
   - Merge its trigger conditions into the primary skill's trigger section.
   - Incorporate any unique solution steps not already present.
   - Preserve edge cases and caveats as subsections.
   - Add the secondary skill's tags to the primary skill.

4. **Add cross-references.** For any edge case that is too specialized to include in the primary skill, add a cross-reference to a separate, dedicated skill.

5. **Delete merged skills.** Once the primary skill incorporates all knowledge from the secondary skills, remove the secondary skill files. Update any references to them.

**Output:** A single, consolidated skill that covers the full scope of the original cluster.

### Phase 3: Validate

Validation ensures the merge did not lose critical knowledge.

**Steps:**

1. **Verify trigger coverage.** Walk through every trigger condition from the original skills and confirm the merged skill would activate for each one.

2. **Test semantic matching.** Run the skill's description against the matcher with representative queries from the original skills' trigger conditions. Confirm the merged skill surfaces appropriately.

3. **Run quality assessment.** Apply the standard skill quality rubric: specificity, reusability, non-triviality, actionability. The merged skill should score at least as well as the best original skill.

4. **Check for gaps.** Review the merge diff to identify any content that was present in the originals but missing from the merged skill.

**Output:** A validated, consolidated skill ready for production use.

---

## 4. Quantitative Merge Thresholds

The following thresholds provide objective criteria for flagging and recommending consolidation actions.

| Metric | Threshold | Action |
|--------|-----------|--------|
| Jaccard similarity (descriptions) | > 0.3 | Flag for manual review |
| Jaccard similarity (descriptions) | > 0.5 | Recommend merge |
| Jaccard similarity (solutions) | > 0.5 | Strong merge candidate |
| Shared domain prefix skill count | > 5 | Trigger consolidation audit |
| Days since last auto-trigger | > 30 | Flag as potentially stale |
| Days since last auto-trigger | > 60 | Recommend archive or merge |
| Skills in a single domain | > 10 | Mandatory consolidation |

### Jaccard Similarity Calculation

For two skill descriptions A and B, treated as sets of tokens:

```
Jaccard(A, B) = |A intersection B| / |A union B|
```

A value of 0 means no overlap. A value of 1 means identical content. In practice, descriptions with Jaccard > 0.3 share significant terminology and likely address overlapping problems.

### Application Notes

- These thresholds are starting points. Adjust based on your domain's specificity. A highly specialized domain with many similar-but-distinct problems may require tighter thresholds (e.g., Jaccard > 0.6 for merge).
- Always validate merges manually. Automated recommendations are a triage tool, not a decision maker.
- After adjusting thresholds, re-audit to ensure the new criteria produce sensible results.

---

## 5. Consolidation Example

This section demonstrates a complete consolidation cycle for a generic domain.

### Before: 8 Fragmented Skills in `api-integration/`

```
skills/api-integration/
  rest-auth-basic.md          — Basic HTTP auth setup
  rest-auth-bearer.md         — Bearer token auth setup
  rest-auth-oauth.md          — OAuth2 flow implementation
  rest-error-handling.md      — HTTP error code handling
  rest-retry-logic.md         — Retry strategies for failed requests
  rest-rate-limiting.md       — Client-side rate limit handling
  rest-pagination.md          — Paginated API response handling
  rest-connection-debug.md    — Debugging connection failures
```

**Problems with this structure:**
- Three separate authentication skills (basic, bearer, OAuth) overlap significantly in setup code and error handling.
- Error handling and retry logic are tightly coupled but split across two files.
- Rate limiting and retry logic share the backoff calculation code.
- Searching for "API authentication" surfaces three skills with no clear ranking.

### Audit Phase Results

| Cluster | Skills | Avg. Jaccard | Recommendation |
|---------|--------|-------------|----------------|
| Authentication | basic, bearer, oauth | 0.42 | Merge into `api-authentication.md` |
| Error handling | error-handling, retry-logic, rate-limiting | 0.38 | Merge into `api-error-resilience.md` |
| Standalone | pagination, connection-debug | N/A | Keep separate |

### Merge Process: Authentication Cluster

**Step 1: Identify primary skill.** `rest-auth-oauth.md` is the most comprehensive (covers flows, token management, refresh logic). It becomes the primary.

**Step 2: Absorb `rest-auth-basic.md`.**
- Add trigger condition: "Connecting to API with Basic HTTP authentication."
- Add solution section: "For Basic Auth, include the `Authorization: Basic <encoded>` header. No token refresh is needed."
- Add note about when to prefer Basic Auth over Bearer/OAuth.

**Step 3: Absorb `rest-auth-bearer.md`.**
- Add trigger condition: "Connecting to API with Bearer token authentication."
- Add solution section: "For Bearer Auth, include the `Authorization: Bearer <token>` header. Implement token refresh if the API supports it."
- Merge the token storage and refresh logic into the existing OAuth token management section.

**Step 4: Consolidate.**
- Rename to `api-authentication.md`.
- Structure as a decision tree: determine auth type, then follow the appropriate sub-section.
- Preserve all edge cases (expired tokens, invalid credentials, scope issues).

### After: 4 Consolidated Skills in `api-integration/`

```
skills/api-integration/
  api-authentication.md       — All authentication methods (Basic, Bearer, OAuth2)
  api-error-resilience.md     — Error handling, retries, and rate limiting
  api-pagination.md           — Paginated response handling (kept separate)
  api-connection-debug.md     — Connection failure debugging (kept separate)
```

**Improvements:**
- Searching for "authentication" returns one comprehensive skill instead of three competing ones.
- Error handling, retry logic, and rate limiting are unified since they share the same resilience patterns.
- Pagination and connection debugging remain separate because their trigger conditions are distinct and non-overlapping.
- The total skill count dropped from 8 to 4, reducing semantic noise by 50%.

### Validation Checklist

- [x] `api-authentication.md` triggers for "Basic Auth", "Bearer token", and "OAuth" queries.
- [x] `api-error-resilience.md` triggers for "retry", "rate limit exceeded", and "HTTP error" queries.
- [x] All original trigger conditions are preserved in the consolidated skills.
- [x] No solution content was lost during the merge.
- [x] Quality scores of consolidated skills meet or exceed the originals.
