# Global Rules Injection - Design Document

> **Purpose:** Design for safely pushing safety rules to all project .cursorrules files
> **Created:** January 10, 2026
> **Status:** DESIGN ONLY - Awaiting Erik approval before execution
> **Blast Radius:** 16 projects with .cursorrules files

---

## Executive Summary

We need to ensure all projects have consistent safety rules in their `.cursorrules` files. Some projects (like `hypocrisynow`) already have them, others don't. This script will:

1. Scan all projects for `.cursorrules` files
2. Check if safety rules exist
3. Inject them if missing (or update if outdated)
4. Backup everything first
5. Support dry-run and canary deployment

---

## The Rules to Inject

### Rule 1: Trash, Don't Delete
```markdown
## 🛡️ Safety Rules

### File Operations
- **Trash, Don't Delete:** NEVER use `rm`, `os.remove`, `os.unlink`, or `shutil.rmtree` for permanent deletion.
- ALWAYS use `send2trash` (Python) to move files to the system Trash.
- For critical data, verify existence and permissions before modifying.
```

### Rule 2: No Silent Failures
```markdown
### Error Handling
- **No Silent Failures:** NEVER swallow exceptions without logging.
- ALWAYS log errors with context (file path, operation attempted, error message).
- Use `logging` module, not `print()`, for error output.
```

---

## Script Design: `update_cursorrules.py`

### Location
`scripts/update_cursorrules.py`

### Command Line Interface

```bash
# Dry run - show what would change, change nothing
python scripts/update_cursorrules.py --dry-run

# Canary deployment - only update specific projects
python scripts/update_cursorrules.py --projects "hypocrisynow,project-tracker,AI-journal"

# Full deployment (after canary success)
python scripts/update_cursorrules.py --execute

# Rollback from backups
python scripts/update_cursorrules.py --rollback
```

### Arguments

| Flag | Description |
|------|-------------|
| `--dry-run` | Show what would change without modifying files (DEFAULT) |
| `--execute` | Actually perform the modifications |
| `--projects` | Comma-separated list of project names to update (canary mode) |
| `--rollback` | Restore all .cursorrules from backups |
| `--create` | Create .cursorrules from template for projects that don't have one |
| `--backup-dir` | Where to store backups (default: `_cursorrules_backups/`) |
| `--root` | Projects root directory (default: `/Users/eriksjaastad/projects`) |

### Core Logic

```python
def update_cursorrules(project_path, dry_run=True):
    """
    1. Read existing .cursorrules
    2. Check if safety rules section exists
    3. If missing: inject at end (before closing comments)
    4. If outdated: update to latest version
    5. If current: skip (no changes needed)
    """

    cursorrules_path = project_path / ".cursorrules"

    if not cursorrules_path.exists():
        log(f"SKIP: {project_path.name} - no .cursorrules file")
        return "skip"

    content = cursorrules_path.read_text()

    # Check for existing safety rules
    has_trash_rule = "Trash, Don't Delete" in content
    has_silent_rule = "Silent Failures" in content

    if has_trash_rule and has_silent_rule:
        log(f"OK: {project_path.name} - already has safety rules")
        return "ok"

    # Backup before modifying
    if not dry_run:
        backup(cursorrules_path)

    # Inject missing rules
    new_content = inject_safety_rules(content, has_trash_rule, has_silent_rule)

    if dry_run:
        log(f"WOULD UPDATE: {project_path.name}")
        show_diff(content, new_content)
    else:
        cursorrules_path.write_text(new_content)
        log(f"UPDATED: {project_path.name}")

    return "updated"
```

### Backup Strategy

```
_cursorrules_backups/
├── 2026-01-10T12-00-00/
│   ├── project-tracker/.cursorrules
│   ├── AI-journal/.cursorrules
│   └── ... (all modified files)
└── manifest.json  # What was backed up, when, by whom
```

**Rollback command:**
```bash
python scripts/update_cursorrules.py --rollback --backup-dir _cursorrules_backups/2026-01-10T12-00-00
```

---

## Safety Mechanisms

### 1. Dry-Run by Default
The script does NOTHING unless `--execute` is explicitly passed. This prevents accidental modifications.

### 2. Automatic Backups
Before any modification, the original file is copied to a timestamped backup directory.

### 3. Canary Deployment
Use `--projects` to update a small subset first, verify for 24-48 hours, then proceed.

### 4. Idempotent
Running the script multiple times is safe. It skips projects that already have the rules.

### 5. Diff Output
In dry-run mode, shows exactly what would change using a unified diff format.

### 6. Manifest Logging
All operations are logged to a manifest file with timestamps and file hashes.

---

## Test Strategy

### Canary Projects (3 projects = ~20% of 16)

| Project | Type | Why Selected |
|---------|------|--------------|
| `project-tracker` | Tier 1 (Code) | Infrastructure project, well-tested |
| `Tax processing` | Tier 1 (Code) | Active project Erik should be working on |
| `analyze-youtube-videos` | Mixed | Has known DNA defects, good stress test |

**Erik's decision:** AI-journal dropped (it's writing, not code). Tax Processing added as active coding project.

### Success Criteria

**After canary deployment (24-48 hours):**
- [ ] Projects still build/run normally
- [ ] No developer complaints or workflow disruption
- [ ] Warden reports zero P0/P1 in canary projects
- [ ] Cursor still reads .cursorrules correctly
- [ ] No AI confusion from new rules

### Rollback Triggers

Immediately rollback if:
- Any project fails to build after update
- Cursor reports syntax errors in .cursorrules
- AI starts ignoring project-specific rules
- Erik requests rollback

---

## Current State Analysis

### Projects WITH .cursorrules (16 total)

```
1. 3D Pose Factory         - Unknown compliance
2. Trading Projects        - Unknown compliance
3. ollama-mcp              - Unknown compliance
4. Holoscape               - Unknown compliance
5. Cortana personal AI     - Unknown compliance
6. [ROOT]                  - Super Manager Protocol (different format)
7. AI usage-billing tracker - Unknown compliance
8. Tax processing          - Unknown compliance
9. muffinpanrecipes        - Unknown compliance
10. analyze-youtube-videos - Unknown compliance
11. project-tracker        - Unknown compliance
12. image-workflow         - Unknown compliance
13. project-scaffolding    - Template format, needs rules
14. AI-journal             - Unknown compliance
15. hypocrisynow           - HAS RULES ✅
16. audit-agent            - Unknown compliance
```

### Projects WITHOUT .cursorrules (~20+ projects)

These will need .cursorrules created from template. That's a separate task (not in scope for this injection).

---

## Execution Plan

### Phase 1: Dry Run (Tonight)
```bash
python scripts/update_cursorrules.py --dry-run
```
Review output, verify no surprises.

### Phase 2: Canary Deployment (After Erik Approval)
```bash
python scripts/update_cursorrules.py --execute --projects "project-tracker,AI-journal,analyze-youtube-videos"
```
Wait 24-48 hours. Monitor for issues.

### Phase 3: Full Rollout (After Canary Success)
```bash
python scripts/update_cursorrules.py --execute
```
Update all remaining projects.

### Phase 4: Template Update
Update `templates/.cursorrules-template` to include safety rules for all future projects.

---

## Rollback Procedure

```bash
# 1. List available backups
ls _cursorrules_backups/

# 2. Rollback to specific backup
python scripts/update_cursorrules.py --rollback --backup-dir _cursorrules_backups/2026-01-10T12-00-00

# 3. Verify rollback
git diff  # Should show reverted changes
```

---

## Acceptance Criteria

- [ ] Script exists at `scripts/update_cursorrules.py`
- [ ] `--dry-run` flag works (default behavior)
- [ ] `--execute` flag works (with explicit confirmation)
- [ ] `--projects` flag works (canary deployment)
- [ ] `--rollback` flag works (restore from backup)
- [ ] Backups created before any modification
- [ ] Idempotent (safe to run multiple times)
- [ ] 3 canary projects identified
- [ ] 24-48 hour monitoring plan defined
- [ ] **Erik approval received before Phase 2**

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Cursor can't parse modified .cursorrules | Low | Medium | Dry-run + canary first |
| AI ignores new rules | Low | Low | Rules are additive, not replacing |
| Rollback fails | Very Low | High | Backup manifest + git as fallback |
| Wrong projects modified | Low | Medium | `--projects` flag for precision |

---

## Erik's Decisions (Jan 10, 2026)

1. **Canary selection:** ✅ project-tracker, Tax Processing, analyze-youtube-videos

2. **Monitoring period:** ✅ 48 hours

3. **Root .cursorrules:** Leave separate. Super Manager rules are different - main rule is "no coding or touching files unless asked."

4. **Missing .cursorrules:** ✅ Add `--create` flag to generate .cursorrules from template for projects that don't have one.

---

## Philosophy Note

> "Safety is an evolution. Projects are never done - they're just at some point in their evolution. We should always be able to see what projects are checking all boxes, checking some boxes. A project doesn't grind to a halt if it hasn't been upgraded to the newest version, but we should know if it hasn't been upgraded."

**Future idea:** Version the scaffolding like npm modules - deployable, upgradeable, trackable.

---

**Design Complete. Erik approved canary projects and 48-hour monitoring. Ready for implementation.**
