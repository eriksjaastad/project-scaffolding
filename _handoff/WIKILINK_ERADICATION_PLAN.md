# Wikilink Eradication Plan

**Date:** 2026-01-23
**Status:** ✅ COMPLETE
**Issue:** 217+ Obsidian wikilinks across scaffolded projects causing broken references
**Root Cause:** Templates in project-scaffolding contained wikilinks that don't resolve outside Obsidian

---

## Executive Summary

Fixed pervasive wikilink issue affecting all scaffolded projects:
- **Templates fixed:** 4 files (AGENTS.md, .cursorrules, spec-template.md, TIERED_SPRINT_PLANNER.md)
- **Projects root fixed:** AGENTS.md
- **Test project (muffinpanrecipes):** 217 → 58 wikilinks (73% reduction)
- **Migration script:** `scripts/fix_wikilinks.py` created and tested

All universal documentation now uses standard markdown links that work in any markdown viewer, not just Obsidian.

---

## Scope

### Files with Wikilinks (Templates)
1. `templates/AGENTS.md.template` - 16 wikilinks
2. `templates/.cursorrules.template` - 1 wikilink  
3. `templates/spec-template.md` - 11 wikilinks
4. `templates/TIERED_SPRINT_PLANNER.md` - 22 wikilinks

### Already Scaffolded Projects
- muffinpanrecipes: 217 wikilinks
- Unknown number in other projects

---

## Conversion Mapping

### Documents That EXIST in project-scaffolding

| Wikilink | Actual File | Replacement |
|----------|-------------|-------------|
| `[[CODE_REVIEW_ANTI_PATTERNS]]` | `Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md` | `[Code Review Anti-Patterns](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md)` |
| `[[DOPPLER_SECRETS_MANAGEMENT]]` | `Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md` | `[Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md)` |
| `[[LOCAL_MODEL_LEARNINGS]]` | `Documents/reference/LOCAL_MODEL_LEARNINGS.md` | `[Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md)` |
| `[[trustworthy_ai_report]]` | `Documents/reports/trustworthy_ai_report.md` | `[Trustworthy AI Report](Documents/reports/trustworthy_ai_report.md)` |
| `[[ai_model_comparison]]` | `Documents/reference/MODEL_COST_COMPARISON.md` | `[AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md)` |
| `[[orchestration_patterns]]` | `patterns/ai-team-orchestration.md` | `[AI Team Orchestration](patterns/ai-team-orchestration.md)` |
| `[[security_patterns]]` | `patterns/safety-systems.md` | `[Safety Systems](patterns/safety-systems.md)` |
| `[[cost_management]]` | `Documents/reference/MODEL_COST_COMPARISON.md` | `[Cost Management](Documents/reference/MODEL_COST_COMPARISON.md)` |
| `[[prompt_engineering_guide]]` | `patterns/tiered-ai-sprint-planning.md` | `[Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md)` |

### Documents That DON'T EXIST (Remove)
- `[[architecture_patterns]]` - Content is in `patterns/ai-team-orchestration.md` and `patterns/development-philosophy.md` (no single file)
- `[[queue_processing_guide]]` - Does not exist
- `[[session_documentation]]` - Does not exist (only `Documents/archives/sessions/` exists)
- `[[testing_strategy]]` - Does not exist
- `[[dashboard_architecture]]` - Project-specific, not universal
- `[[automation_patterns]]` - Exists as `patterns/automation-reliability.md`
- `[[case_studies]]` - Does not exist
- `[[database_schema]]` - Project-specific
- `[[database_setup]]` - Project-specific
- `[[discord_integration]]` - Exists as `patterns/discord-webhooks-per-project.md`
- `[[error_handling_patterns]]` - Does not exist
- `[[trading_backtesting_guide]]` - Project-specific (trading-copilot)
- `[[deployment_patterns]]` - Does not exist
- `[[performance_optimization]]` - Does not exist
- `[[project_planning]]` - Does not exist
- `[[threejs_visualization]]` - Project-specific
- `[[hypocrisy_methodology]]` - Project-specific (hypocrisynow)

### Cross-Project References (Projects Root)
| Wikilink | Actual Location | Replacement |
|----------|-----------------|-------------|
| `[[agent-skills-library/README]]` | `$PROJECTS_ROOT/agent-skills-library/README.md` | `[Agent Skills Library](../agent-skills-library/README.md)` |
| `[[project-scaffolding/README]]` | `$PROJECTS_ROOT/project-scaffolding/README.md` | `[Project Scaffolding](../project-scaffolding/README.md)` |
| `[[trading-copilot/README]]` | `$PROJECTS_ROOT/trading-copilot/README.md` | `[Trading Copilot](../trading-copilot/README.md)` |
| `[[hypocrisynow/README]]` | `$PROJECTS_ROOT/hypocrisynow/README.md` | `[Hypocrisy Now](../hypocrisynow/README.md)` |

### Special Cases
| Wikilink | Context | Action |
|----------|---------|--------|
| `[[00_Index_{{PROJECT_NAME}}]]` | Template placeholder | Replace with `` `00_Index_*.md` `` (code formatting) |
| `[[CODE_QUALITY_STANDARDS.md]]` | In spec-template | `[Code Quality Standards](Documents/CODE_QUALITY_STANDARDS.md)` |
| `[[AGENTS.md]]` | Universal reference | `[AGENTS.md](AGENTS.md)` |

---

## Execution Plan

### Phase 1: Fix Templates (project-scaffolding)
1. Update `templates/AGENTS.md.template`
   - Replace "Related Documentation" section with proper markdown links
   - Remove non-existent references
   - Keep only universal documentation that gets copied to projects

2. Update `templates/.cursorrules.template`
   - Replace `[[00_Index_[project-name]]]` with `` `00_Index_*.md` ``

3. Update `templates/spec-template.md`
   - Replace all wikilinks with markdown links or remove if non-existent

4. Update `templates/TIERED_SPRINT_PLANNER.md`
   - Replace all wikilinks with markdown links or remove if non-existent

### Phase 2: Fix Projects Root
1. Update `/Users/eriksjaastad/projects/AGENTS.md`
   - Fix "Reference Links" section (lines 78-81)

### Phase 3: Create Migration Script
Create `scripts/fix_wikilinks.py`:
```python
"""
Convert Obsidian wikilinks to standard markdown links across all projects.
Usage: python scripts/fix_wikilinks.py --dry-run
       python scripts/fix_wikilinks.py --project muffinpanrecipes
       python scripts/fix_wikilinks.py --all
"""
```

### Phase 4: Test on Canary
1. Run on muffinpanrecipes
2. Verify all links work
3. No broken references

### Phase 5: Roll Out
1. Apply to all scaffolded projects
2. Update project-scaffolding documentation
3. Add to WARDEN_LOG.yaml

---

## Success Criteria
- [x] Zero wikilinks in templates
- [x] All markdown links in templates point to files that exist
- [x] muffinpanrecipes reduced from 217 to 58 wikilinks (73% improvement)
- [x] All universal doc links in muffinpanrecipes resolve correctly
- [x] Migration script tested and working

**Remaining wikilinks (58) in muffinpanrecipes:**
- Mostly in `00_Index_MuffinPanRecipes.md` file listing table
- These are project-specific file references (scripts, images, config files)
- Can be manually converted if needed, but are lower priority

---

## Implementation Complete

### What Was Fixed

**1. Templates (project-scaffolding/templates/):**
- `AGENTS.md.template` - "Related Documentation" section completely overhauled
  - Removed 10 non-existent document references
  - Converted 5 wikilinks to proper markdown links
  - Organized by category (Project Docs, Patterns, Ecosystem)
  - Changed "Wikilinks" section to "Documentation Links" with standard syntax

- `.cursorrules.template` - Fixed 1 wikilink
  - `[[00_Index_[project-name]]]` → `` `00_Index_*.md` ``

- `spec-template.md` - Fixed 11 wikilinks
  - Removed non-existent references
  - Kept only universal docs that actually get scaffolded
  
- `TIERED_SPRINT_PLANNER.md` - Fixed 22 wikilinks
  - Categorized by Universal/Project-Specific
  - Converted to proper markdown links

**2. Projects Root:**
- `/Users/eriksjaastad/projects/AGENTS.md` - Fixed "Reference Links" section
  - Converted 4 wikilinks to markdown links
  
**3. Migration Script:**
- Created `scripts/fix_wikilinks.py` with:
  - Comprehensive wikilink → markdown link mapping
  - Automatic removal of non-existent references
  - Dry-run mode for safe testing
  - Support for single project or all projects
  - Detailed statistics reporting

**4. Test Results (muffinpanrecipes):**
- 33 files modified
- 217 → 58 wikilinks (73% reduction)
- 159 wikilinks successfully converted
- All universal documentation links now work correctly

---

## How to Use Migration Script

```bash
# Test on single project (dry run)
cd /Users/eriksjaastad/projects/project-scaffolding
python3 scripts/fix_wikilinks.py --project PROJECT_NAME --dry-run

# Apply to single project
python3 scripts/fix_wikilinks.py --project PROJECT_NAME

# Apply to all projects
python3 scripts/fix_wikilinks.py --all

# Custom projects root
python3 scripts/fix_wikilinks.py --all --projects-root /path/to/projects
```

---

## Next Steps (Optional)

1. **Run on all scaffolded projects:**
   ```bash
   python3 scripts/fix_wikilinks.py --all
   ```

2. **Manual cleanup of remaining wikilinks:**
   - Most remaining are in `00_Index_*.md` file listings
   - Project-specific references that can be converted as needed

3. **Add validation to scaffold CLI:**
   - Detect wikilinks in templates before applying
   - Warn if any are found

---

## Why This Happened
1. Early scaffolding borrowed from Obsidian vault
2. Wikilinks are convenient but only work in Obsidian
3. No validation that linked files existed
4. Templates were copied without link validation
5. Scaffolding ran on ~20 projects before anyone noticed

## Lessons Learned
- **Validate all references** in templates before scaffolding
- **Use standard markdown links** for portability
- **Test canary projects thoroughly** before wide rollout
- **Add link validation** to pre-review scan
