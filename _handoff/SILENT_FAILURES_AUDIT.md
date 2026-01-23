# Silent Failures Audit

**Created:** 2026-01-23
**Created By:** Claude (Super Manager)
**Status:** NEEDS FLOOR MANAGER
**Priority:** HIGH - Systemic trust issue

---

## The Pattern

Things are marked "done" or "working" but were never actually implemented. We discover failures days later by accident. This has happened repeatedly over the last 2-3 days.

**Core Problem:** "No silent errors" is a principle in documents, but there's no enforcement mechanism. Success is self-reported by the system doing the work, with no independent verification.

---

## Problems Discovered Today (2026-01-23)

### Problem 1: scaffold CLI Never Substitutes Variables

**Location:** `project-scaffolding/scaffold/cli.py`

**What it claims:** Scaffolds projects from templates
**What it actually does:** Copies raw templates without substituting `{variable}` or `{{VARIABLE}}` placeholders

**Evidence:**
- `muffinpanrecipes/.agentsync/rules/00-full-content.md` has unfilled `{project_description}`, `{language}` placeholders
- `trading-copilot/TODO.md` has unfilled `{{AI_NAME}}`, `{{PHASE}}` placeholders
- CLI prints "✅ success" even though substitution never happened

**Root Cause:** Lines 310-313 and 323-327 in cli.py append/create from templates without any substitution logic. The `_update_file_references()` function only replaces `$SCAFFOLDING/` paths, not variable placeholders.

---

### Problem 2: Two Incompatible Placeholder Syntaxes

**Locations:** Various templates in `project-scaffolding/templates/`

**Issue:** Some templates use `{single_brace}`, others use `{{double_brace}}`. Neither are substituted.

| Template | Syntax | Example |
|----------|--------|---------|
| `AGENTS.md.template` | `{var}` | `{project_description}` |
| `00-overview.md.template` | `{var}` | `{project_name}` |
| `TODO.md.template` | `{{VAR}}` | `{{PROJECT_NAME}}` |

**Impact:** Even if we add substitution, we need to handle both syntaxes or standardize.

---

### Problem 3: REVIEWS_AND_GOVERNANCE_PROTOCOL.md Disconnected

**Location:** `project-scaffolding/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`

**Issues:**
1. Doesn't reference `Project-workflow.md` (the master workflow at projects root)
2. Doesn't acknowledge its role as the Industrial Hardening checklist for Phase 5 Judge
3. Says "Protocol Authorized by: The Super Manager (Gemini 3 Flash)" - stale
4. Gets copied to all projects' `Documents/` folder in this broken state

---

### Problem 4: Wrong Path in agentsync Rules

**Location:** Template content that ends up in `.agentsync/rules/` files

**Issue:** Line 70 of the template says:
```
See `./REVIEWS_AND_GOVERNANCE_PROTOCOL.md` for full review process.
```

**Should be:**
```
See `Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md` for full review process.
```

---

### Problem 5: project-tracker Dashboard Shows Garbage

**Location:** project-tracker dashboard

**Issue:** Parses TODO.md files and displays unfilled `{{PLACEHOLDER}}` values as if they were real data. No alert is generated.

**What should happen:** If the parser sees `{{` patterns, it should:
1. Log a warning
2. Send Discord alert
3. Not display garbage in the UI

---

### Problem 6: Discord Alerts Not Connected

**Belief:** Errors and warnings go to Discord
**Reality:** Unknown - need to audit what's actually hooked up

**Questions to answer:**
- What Discord webhooks exist?
- What events trigger them?
- Are scaffold failures connected? (Probably not)
- Are project-tracker parse errors connected? (Probably not)

---

### Problem 7: No Validation After Scaffolding

**Issue:** scaffold CLI marks success without verifying:
- All placeholders were substituted
- Required files were created correctly
- References point to existing files

**What should exist:** A post-scaffold validator that:
1. Greps for `{` and `{{` patterns in output files
2. Fails loudly if placeholders remain
3. Sends Discord alert on failure

---

## How to Surface More Problems

### Immediate Audit Commands

Run from `$PROJECTS_ROOT`:

```bash
# Find all unfilled single-brace placeholders across projects
grep -r --include="*.md" '\{[a-z_]*\}' "$PROJECTS_ROOT"/*/

# Find all unfilled double-brace placeholders
grep -r --include="*.md" '\{\{[A-Z_]*\}\}' "$PROJECTS_ROOT"/*/

# Find CLAUDE.md files with template markers (indicates appended garbage)
grep -l "project-scaffolding template appended" "$PROJECTS_ROOT"/*/CLAUDE.md

# Find TODO.md files with unfilled placeholders
grep -l '\{\{' "$PROJECTS_ROOT"/*/TODO.md

# Check what Discord webhooks are configured
grep -r "DISCORD_WEBHOOK" "$PROJECTS_ROOT"/*/.env 2>/dev/null
grep -r "discord" "$PROJECTS_ROOT"/_tools/*/
```

### Systems to Audit

| System | Question | How to Check |
|--------|----------|--------------|
| scaffold CLI | What does it claim to do vs actually do? | Read cli.py, test on a project |
| agentsync | Does sync_rules.py validate output? | Read script, check for validation |
| project-tracker | What parsing errors are logged? | Check logs, dashboard code |
| Discord notifications | What's actually connected? | Grep for webhook usage |
| Agent Hub | Does it report failures to Discord? | Check watchdog.py, circuit breakers |

---

## Proposed Solutions

### Solution 1: Post-Action Validators

Every tool that claims "done" should have an independent validator:

```
scaffold CLI runs
    ↓
Post-scaffold validator runs
    ↓
Checks for unfilled placeholders
    ↓
If found → Discord alert + exit code 1
If clean → Actually done
```

### Solution 2: Centralized Alert Hub

One place where all systems report errors:

```
┌─────────────────────────────────────────┐
│           Alert Hub (Discord)           │
├─────────────────────────────────────────┤
│ scaffold CLI ──→ #alerts                │
│ agentsync ────→ #alerts                 │
│ project-tracker ──→ #alerts             │
│ Agent Hub ────→ #alerts                 │
│ Any new tool ──→ #alerts                │
└─────────────────────────────────────────┘
```

### Solution 3: Daily Health Check

A cron job that runs every morning:

1. Scans all projects for unfilled placeholders
2. Checks for common corruption patterns
3. Validates critical file references
4. Reports to Discord: "X projects healthy, Y have issues"

### Solution 4: "Trust But Verify" Principle

Update Project-workflow.md to include:

> **No tool self-reports success.** Every "done" claim must be independently verified by a validator or the Judge. If a validator doesn't exist, the task is not done.

---

## Definition of "Incrementally Better"

We are better when:

1. [ ] Running the audit commands above produces ZERO results (no unfilled placeholders)
2. [ ] scaffold CLI has a `--validate` flag that checks output
3. [ ] At least ONE Discord alert fires when scaffolding fails
4. [ ] project-tracker dashboard filters out `{{PLACEHOLDER}}` patterns
5. [ ] A daily health check runs and reports to Discord

---

## Immediate Next Steps (For Floor Manager)

### Step 1: Run the Audit
Execute the grep commands above. Document how many files are affected.

### Step 2: Inventory Discord Connections
Find every place that SHOULD send to Discord. Check if it actually does.

### Step 3: Fix scaffold CLI
Add placeholder validation. If `{` or `{{` patterns exist in output, fail with error.

### Step 4: Clean Existing Files
Write a script to strip template garbage from affected files. Run across all projects.

### Step 5: Add Health Check
Create a daily cron that scans for corruption patterns and reports to Discord.

---

## Questions for Erik (When Available)

1. Is there a single Discord channel for alerts, or multiple?
2. Should we standardize on `{var}` or `{{VAR}}` syntax?
3. Where should the daily health check live? (project-tracker? _tools?)
4. Who originally built the scaffold CLI? (Context for why substitution was never implemented)

---

## Files to Read for Context

- `project-scaffolding/scaffold/cli.py` - The broken scaffold logic
- `_tools/agentsync/sync_rules.py` - The agentsync system
- `project-tracker/` - Dashboard that shows the garbage
- `Project-workflow.md` - The workflow that should prevent this

---

**This is a trust issue.** Every time we find something marked "done" that wasn't, it erodes confidence in the entire system. The fix isn't just patching these specific bugs - it's adding verification layers so "done" actually means done.
