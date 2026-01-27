# Pattern Management System

**Purpose:** Keep patterns useful, current, and free of fluff
**Last Updated:** January 9, 2026

---

## The Problem

Patterns were getting created with "hand-wavy" instructions, agents had free reign, and nobody knew:
- What patterns actually exist
- Which are documented vs. just ideas
- When to review or update them
- Whether they're still useful or just fluff

**Result:** PATTERN_ANALYSIS.md got 3 weeks out of date, patterns/ directory had inconsistent status tags, and no process for keeping things current.

---

## The System

### Pattern Registry (Single Source of Truth)

**Location:** This document, section below

**What it tracks:**
- ✅ Pattern name & file path
- ✅ Status (🟢 Proven / 🟡 Emerging / 🔵 Candidate)
- ✅ Last reviewed date
- ✅ Evidence (which projects use it)
- ✅ Notes (issues, planned updates)

### Pattern Lifecycle

```
🔵 CANDIDATE (1 project)
  ↓ Applied in 2nd project
🟡 EMERGING (2 projects)
  ↓ Applied in 3rd project + battle-tested
🟢 PROVEN (3+ projects, stable)
  ↓ No changes needed for 6+ months
🏆 MATURE (battle-tested, reference quality)
```

**Promotion rules:**
- 🔵 → 🟡: After 2nd project uses it successfully
- 🟡 → 🟢: After 3rd project + 3 months stable
- 🟢 → 🏆: After 6 months with no updates needed

**Demotion rules:**
- If pattern causes problems in new project → investigate
- If pattern isn't being used → mark for deletion
- If pattern is obsolete → archive it

### Review Schedule

**Monthly (10 minutes):**
- [ ] Check new projects: Did they apply any patterns? Add evidence.
- [ ] Check 🟡 patterns: Any hit 3 projects? Promote to 🟢.
- [ ] Check registry: Any patterns need review?

**Quarterly (30 minutes):**
- [ ] Review all 🟢 patterns: Still accurate? Any updates needed?
- [ ] Audit fluff: Are patterns getting too long? Trim them.
- [ ] Check TODO.md: Any pattern work completed? Update registry.

**After Each New Project (5 minutes):**
- [ ] Which patterns did you apply? Mark in registry.
- [ ] Did any patterns fail or cause problems? Document.
- [ ] Did you discover new patterns? Add as 🔵 Candidate.

---

## Pattern Quality Standards

### Keep Patterns Lean

**Good pattern doc:**
- Problem statement (1-2 paragraphs)
- The solution (1-2 paragraphs)
- When to apply (bulleted list)
- How to apply (checklist or code snippet)
- Evidence (which projects use it)
- Status (🟢 🟡 🔵)

**Bad pattern doc:**
- Long philosophical essays
- Hypothetical examples that never happened
- Extensive "what if" scenarios
- More than 300 lines unless it's a comprehensive guide

**Rule:** If a pattern doc is >300 lines, it should either be:
1. Split into multiple patterns
2. Moved to Documents/guides/
3. Trimmed aggressively

### Required Sections

Every pattern MUST have:
1. **Status line** at top (Pattern Type: 🟢 Proven)
2. **The Problem** - Why does this exist?
3. **The Pattern** - What's the solution?
4. **Evidence** - Which projects use it?
5. **Date** - When was it created/updated?

Optional but recommended:
- When to apply / When NOT to apply
- Implementation checklist
- Code snippets
- Related patterns

---

## Current Pattern Registry

**Last Updated:** January 9, 2026

| Pattern | File | Status | Projects | Last Review | Notes |
|---------|------|--------|----------|-------------|-------|
| API Key Management | `api-key-management.md` | 🟢 Proven | 3+ projects | Jan 2026 | ✅ Good |
| Code Review Standard | `code-review-standard.md` | 🟢 Proven | project-scaffolding | Jan 2026 | ✅ Good |
| Cursor Configuration | `cursor-configuration.md` | 🟢 Proven | All workspace | Jan 2026 | ✅ Good |
| Development Philosophy | `development-philosophy.md` | 🟢 Proven | 3+ projects | Jan 2026 | ⚠️ LONG (800+ lines) - Review for fluff |
| Discord Webhooks | `discord-webhooks-per-project.md` | 🟢 Proven | Trading Co-Pilot | Dec 2024 | ✅ Good |
| Foundation Docs First | `foundation-documents-first.md` | 🟢 Proven | project-scaffolding | Jan 2026 | ✅ Good |
| Local AI Integration | `local-ai-integration.md` | 🟡 Emerging | 2 projects | Jan 2026 | ✅ Good |
| Safety Systems | `safety-systems.md` | 🟢 Proven | image-workflow, Cortana, Trading | Dec 2025 | ✅ Good |
| SSOT via YAML | `ssot-via-yaml.md` | 🟢 Proven | 3+ projects | Dec 2025 | ✅ Good |
| Tiered AI Sprint Planning | `tiered-ai-sprint-planning.md` | 🟡 Emerging | 2 projects | Jan 2026 | ⚠️ Needs validation in 3rd project |

**Summary:**
- Total patterns: 10
- 🟢 Proven: 8
- 🟡 Emerging: 2
- 🔵 Candidate: 0

**Action items:**
- [ ] Review `development-philosophy.md` for fluff (800+ lines is long)
- [ ] Apply `tiered-ai-sprint-planning.md` to 3rd project to promote to 🟢
- [ ] Apply `local-ai-integration.md` to 3rd project to promote to 🟢

---

## Monthly Checklist Template

**Pattern Registry Review - [Month Year]**

**Quick checks (5 min):**
- [ ] Any new projects launched? → Note which patterns were applied
- [ ] Any patterns cause problems? → Document in registry
- [ ] Any 🟡 patterns hit 3 projects? → Promote to 🟢

**Registry updates (5 min):**
- [ ] Update "Last Review" dates for any checked patterns
- [ ] Update "Projects" column with new evidence
- [ ] Add any new 🔵 Candidate patterns discovered

**Issues found:**
- [List any issues]

**Promotions:**
- [List any patterns promoted]

**Next month focus:**
- [What to watch for]

---

## Fluff Detection Checklist

When reviewing a pattern, ask:

1. **Is every section necessary?**
   - ❌ Remove: Philosophical tangents
   - ❌ Remove: Hypothetical "what if" scenarios not based on real experience
   - ❌ Remove: Extensive background that doesn't help implementation

2. **Are examples real or theoretical?**
   - ✅ Keep: "In project X, we did Y and it worked"
   - ❌ Remove: "You could imagine a scenario where..."

3. **Is the pattern actionable?**
   - ✅ Keep: Checklists, code snippets, specific steps
   - ❌ Remove: Vague advice like "use best judgment"

4. **Is it under 300 lines?**
   - ✅ Yes → Probably fine
   - ❌ No → Split, move, or trim aggressively

---

## Anti-Patterns to Avoid

### ❌ Pattern Explosion
**Problem:** Creating a pattern for every tiny thing
**Fix:** Only document after 3rd instance (Consolidate on 3rd Duplicate principle)

### ❌ Premature Documentation
**Problem:** Documenting patterns before they're proven
**Fix:** Start as 🔵 Candidate, promote only with evidence

### ❌ Stale Registry
**Problem:** Registry gets out of date, nobody trusts it
**Fix:** Monthly 10-minute review is mandatory

### ❌ Fluff Accumulation
**Problem:** Patterns get longer over time with "helpful" additions
**Fix:** Quarterly trim, enforce 300-line soft limit

### ❌ No Accountability
**Problem:** "Someone should review patterns" but nobody does
**Fix:** Add to TODO.md with owner (Erik or delegated agent)

---

## Integration with TODO.md

**Pattern work should always be in TODO.md:**

```markdown
## 📚 Pattern Management

**Monthly Review:** Due [Date]
- [ ] Check registry for promotions (🟡 → 🟢)
- [ ] Update evidence from new projects
- [ ] Mark patterns reviewed in registry

**Quarterly Audit:** Due [Date]
- [ ] Review all 🟢 patterns for accuracy
- [ ] Check for fluff (enforce 300-line guideline)
- [ ] Update PATTERN_ANALYSIS.md to match registry

**Ad-hoc:**
- [ ] [Specific pattern work as needed]
```

---

## Success Metrics

**This system is working if:**
- ✅ Registry is updated monthly
- ✅ No pattern is >300 lines without good reason
- ✅ New projects reference patterns (they're useful)
- ✅ Patterns are promoted based on evidence, not gut feeling
- ✅ PATTERN_ANALYSIS.md stays current (within 1 month)

**This system is failing if:**
- ❌ Registry is >2 months out of date
- ❌ Patterns are growing without pruning
- ❌ New projects don't use patterns (they're not useful)
- ❌ Can't find information (too much fluff)

---

## Related Files

- `PATTERN_ANALYSIS.md` - Detailed extraction analysis (gets updated quarterly)
- `TODO.md` - Pattern work tracking
- `patterns/` - Actual pattern files
- `templates/` - Reusable templates (not the same as patterns)

---

*Keep patterns lean. Keep registry current. No fluff.*

## Related Documentation

- [Code Review Anti-Patterns](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md) - code review
- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [PATTERN_MANAGEMENT](PATTERN_MANAGEMENT.md) - patterns
- [PROJECT_KICKOFF_GUIDE](../PROJECT_KICKOFF_GUIDE.md) - project setup
- [Discord Webhooks Per Project](patterns/discord-webhooks-per-project.md) - Discord
- [cortana-personal-ai/README](../../../ai-model-scratch-build/README.md) - Cortana AI
- [image-workflow/README](../../../ai-model-scratch-build/README.md) - Image Workflow
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
