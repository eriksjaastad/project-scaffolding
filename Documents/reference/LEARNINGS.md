---
tags:
  - p/project-scaffolding
  - type/documentation
  - domain/learning
status: "#status/active"
created: 2026-02-01
---

# LEARNINGS.md

> **Purpose:** Captured knowledge from project work. Newest entries at top.
> **Format:** Date-stamped entries with task links, learnings, and action items.

---

## Entry Format Template

```markdown
## YYYY-MM-DD: Brief Title

**Task:** #XXXX (if applicable)
**Context:** What we were doing

### What We Learned
- Key insight or discovery

### What To Do Differently
- Concrete action or rule change

### Related Files
- `path/to/file.py` - why it's relevant
```

---

## 2026-02-01: Alert Detector False Positives

**Task:** #4689 (Fix false "Project blocked" alerts)
**Context:** Dashboard showing 30+ false "Project blocked" alerts

### What We Learned
- The `_get_clean_lines()` function was picking up HTML comments (`<!-- ... -->`) and scaffold template placeholder text as real content
- Template placeholders like "Clear description of the blocker" in TODO.md Blockers sections triggered false alerts
- Similarly, cron schedules with `{{CRON_EXPR...}}` placeholders were flagged as "invalid"

### What To Do Differently
- Filter HTML comments and known placeholder patterns before processing content
- Don't alert on template/scaffold placeholders - they're not real issues
- Prefer "signal over noise" - only alert on actionable problems, not compliance suggestions

### Related Files
- `project-tracker/scripts/discovery/alert_detector.py` - fixed `_get_clean_lines()` filtering
- `project-tracker/scripts/discovery/cron_monitor.py` - added `{{` template detection

---

## 2026-01-27: Database Safety Incident

**Task:** N/A (incident response)
**Context:** AI agent ran a migration that dropped the tasks table without backup

### What We Learned
- **94 tasks were destroyed** by an AI agent running `DROP TABLE` during a schema migration
- The agent assumed it could "fix" schema issues by recreating tables
- No backup was created before the destructive operation
- Stateful data (like tasks) cannot be recreated - it's accumulated work

### What To Do Differently
- **NEVER** run DROP TABLE, TRUNCATE, or DELETE without explicit user approval
- **ALWAYS** check row count before any schema change: `SELECT COUNT(*) FROM table_name`
- **ALWAYS** backup before migrations: `cp database.db database.db.backup`
- Added comprehensive "Database Safety Rules" section to AGENTS.md template

### Related Files
- `project-scaffolding/.agentsync/rules/07_database_safety.md` - new rule added
- `project-tracker/db/manager.py` - now creates auto-backups on destructive operations

---

## 2026-01-28: Scaffolding Version Sync

**Task:** N/A (research)
**Context:** Investigating `.scaffolding-version` files across projects

### What We Learned
- 28 projects have `.scaffolding-version` JSON files
- All were at v1.0.0 (in sync with template)
- Source of truth: `project-scaffolding/templates/.agentsync/RULES_VERSION`
- Version tracking managed by `scaffold/cli.py` and `agentsync/sync_rules.py`

### What To Do Differently
- Use scaffolding version for drift detection (implemented in alert_detector.py)
- When bumping template version, projects behind will show as warnings
- Include upgrade command in alert details for easy remediation

### Related Files
- `project-scaffolding/templates/.agentsync/RULES_VERSION` - source of truth
- `project-tracker/scripts/discovery/alert_detector.py` - `detect_scaffolding_drift()`

---

## Learning Debt Tracker

| Date | Learning | Compiled Into | Preventable? |
|------|----------|---------------|--------------|
| 2026-01-27 | DB safety incident | AGENTS.md rule, this file | Yes - needed guardrails |
| 2026-02-01 | Alert false positives | alert_detector.py fix | Yes - better filtering |

---

## How to Use This File

1. **After completing a task:** Add an entry if you learned something non-obvious
2. **After an incident:** Document what happened, why, and how to prevent it
3. **Link tasks:** Use `#XXXX` format for traceability
4. **Compile learnings:** Promote patterns to AGENTS.md rules or code changes
5. **Track debt:** Use the table to track learnings that need to be compiled
