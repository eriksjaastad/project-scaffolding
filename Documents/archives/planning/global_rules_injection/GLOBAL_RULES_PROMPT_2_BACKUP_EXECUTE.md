# Worker Task: Backup + Execute Mode

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 25 minutes
**Objective:** Add backup functionality and --execute flag to update_cursorrules.py

---

## Context

Task 1 created the script with dry-run scanning. Now we need to add the ability to actually modify files, but ONLY after creating backups. Safety is paramount.

**File to modify:** `scripts/update_cursorrules.py`

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **Argument:** Add `--execute` flag to argparse
- [ ] **Argument:** Add `--backup-dir` flag (default: `_cursorrules_backups/`)
- [ ] **Backup Function:** Creates timestamped backup directory
- [ ] **Backup Function:** Copies original file before any modification
- [ ] **Inject Function:** Appends safety rules section to .cursorrules
- [ ] **Idempotent:** Skips files that already have both rules
- [ ] **Dry-run Default:** Without --execute, script only shows what would change
- [ ] **Output:** Shows diff of what changed (or would change)

---

## The Safety Rules to Inject

```markdown
---

## Safety Rules

### File Operations
- **Trash, Don't Delete:** NEVER use `rm`, `os.remove`, `os.unlink`, or `shutil.rmtree` for permanent deletion.
- ALWAYS use `send2trash` (Python) or move files to a `_trash/` directory.

### Error Handling
- **No Silent Failures:** NEVER swallow exceptions without logging.
- ALWAYS log errors with context (file path, operation attempted, error message).
```

---

## Implementation Details

### 1. Add Arguments

```python
parser.add_argument(
    "--execute",
    action="store_true",
    help="Actually modify files (default is dry-run)"
)
parser.add_argument(
    "--backup-dir",
    type=pathlib.Path,
    default=pathlib.Path("_cursorrules_backups"),
    help="Directory for backups (default: _cursorrules_backups/)"
)
```

### 2. Safety Rules Content

```python
SAFETY_RULES_SECTION = '''
---

## Safety Rules

### File Operations
- **Trash, Don't Delete:** NEVER use `rm`, `os.remove`, `os.unlink`, or `shutil.rmtree` for permanent deletion.
- ALWAYS use `send2trash` (Python) or move files to a `_trash/` directory.

### Error Handling
- **No Silent Failures:** NEVER swallow exceptions without logging.
- ALWAYS log errors with context (file path, operation attempted, error message).
'''
```

### 3. Backup Function

```python
import shutil
from datetime import datetime

def create_backup(cursorrules_path: pathlib.Path, backup_dir: pathlib.Path) -> pathlib.Path:
    """Create a timestamped backup of a .cursorrules file."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    backup_subdir = backup_dir / timestamp / cursorrules_path.parent.name
    backup_subdir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_subdir / ".cursorrules"
    shutil.copy2(cursorrules_path, backup_path)

    logger.info(f"  Backed up to: {backup_path}")
    return backup_path
```

### 4. Inject Function

```python
def inject_safety_rules(content: str, has_trash: bool, has_silent: bool) -> str:
    """Inject missing safety rules into .cursorrules content."""
    if has_trash and has_silent:
        return content  # Nothing to inject

    # If file doesn't end with newline, add one
    if not content.endswith('\n'):
        content += '\n'

    # Append the full safety rules section
    # (Even if one rule exists, we add the full section for consistency)
    content += SAFETY_RULES_SECTION

    return content
```

### 5. Update Single File

```python
def update_cursorrules(
    cursorrules_path: pathlib.Path,
    backup_dir: pathlib.Path,
    execute: bool = False
) -> str:
    """Update a single .cursorrules file with safety rules.

    Returns: 'ok', 'updated', or 'skipped'
    """
    compliance = check_compliance(cursorrules_path)
    project = compliance['project']

    # Already compliant
    if compliance['has_trash_rule'] and compliance['has_silent_rule']:
        logger.info(f"OK: {project} - already has safety rules")
        return 'ok'

    # Needs update
    content = cursorrules_path.read_text()
    new_content = inject_safety_rules(
        content,
        compliance['has_trash_rule'],
        compliance['has_silent_rule']
    )

    if execute:
        # Create backup first!
        create_backup(cursorrules_path, backup_dir)

        # Write updated content
        cursorrules_path.write_text(new_content)
        logger.info(f"UPDATED: {project}")
    else:
        logger.info(f"WOULD UPDATE: {project}")
        # Show what would be added
        logger.info(f"  + Safety Rules section ({len(SAFETY_RULES_SECTION)} chars)")

    return 'updated'
```

### 6. Update Main Function

```python
def run_update(
    projects_root: pathlib.Path,
    backup_dir: pathlib.Path,
    execute: bool = False
) -> bool:
    """Scan and update all .cursorrules files."""
    mode = "EXECUTE" if execute else "DRY-RUN"
    logger.info(f"Mode: {mode}")
    logger.info(f"Scanning: {projects_root}")
    logger.info("-" * 60)

    cursorrules_files = find_cursorrules_files(projects_root)

    if not cursorrules_files:
        logger.warning("No .cursorrules files found")
        return True

    stats = {'ok': 0, 'updated': 0, 'skipped': 0}

    for cr_path in cursorrules_files:
        result = update_cursorrules(cr_path, backup_dir, execute)
        stats[result] += 1

    logger.info("-" * 60)
    logger.info(f"Summary: {stats['ok']} OK, {stats['updated']} {'updated' if execute else 'would update'}")

    if execute:
        logger.info(f"Backups saved to: {backup_dir}")

    return True
```

### 7. Update CLI

```python
def main():
    # ... existing args ...

    args = parser.parse_args()

    # Resolve backup dir relative to current directory
    backup_dir = args.backup_dir.resolve()

    success = run_update(args.root, backup_dir, execute=args.execute)
    sys.exit(0 if success else 1)
```

---

## Verification Steps

1. **Test dry-run still works:**
   ```bash
   python scripts/update_cursorrules.py --dry-run
   # Should show WOULD UPDATE for non-compliant projects
   ```

2. **Test execute on single test file:**
   ```bash
   # First, create a test .cursorrules without rules
   mkdir -p /tmp/test-project
   echo "# Test cursorrules" > /tmp/test-project/.cursorrules

   # Run execute
   python scripts/update_cursorrules.py --execute --root /tmp

   # Verify backup was created
   ls _cursorrules_backups/

   # Verify file was modified
   cat /tmp/test-project/.cursorrules | grep "Trash"
   ```

3. **Test idempotency:**
   ```bash
   # Run again - should show OK, not update again
   python scripts/update_cursorrules.py --execute --root /tmp
   # Should show: OK: test-project - already has safety rules
   ```

4. **Cleanup test:**
   ```bash
   rm -rf /tmp/test-project
   ```

---

## Files to Read First

- `scripts/update_cursorrules.py` (current state from Task 1)
- `Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md` (backup strategy section)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 8 acceptance criteria checked
- [ ] Verification steps 1-4 completed successfully
- [ ] Backup directory created with timestamped subfolder
- [ ] Idempotency verified (running twice doesn't duplicate rules)

**Max 3 attempts.** If Worker fails 3x, halt and alert Conductor.


## Related Documentation

- [[LOCAL_MODEL_LEARNINGS]] - local AI

