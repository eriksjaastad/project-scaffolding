# Worker Task: Core Script + Dry-Run Mode

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 30 minutes
**Objective:** Create update_cursorrules.py with project scanning, rule detection, and --dry-run output

---

## Context

We need a script to push safety rules to all project .cursorrules files across the ecosystem. This task creates the foundation: scanning projects, detecting existing rules, and showing what would change.

**File to create:** `scripts/update_cursorrules.py`

**Reference for patterns:** `scripts/warden_audit.py` (argparse, logging, pathlib usage)

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **File Created:** `scripts/update_cursorrules.py` exists
- [ ] **Argparse:** Has `--dry-run`, `--root` arguments
- [ ] **Logging:** Uses Python logging module (not print)
- [ ] **Scanning:** Finds all .cursorrules files under projects root
- [ ] **Detection:** Correctly identifies if "Trash, Don't Delete" rule exists
- [ ] **Detection:** Correctly identifies if "Silent Failures" rule exists
- [ ] **Output:** Dry-run shows each project with status (OK/NEEDS UPDATE/SKIP)
- [ ] **Exit Code:** Returns 0 on success

---

## The Safety Rules to Detect

The script must detect these two rules in .cursorrules files:

**Rule 1 marker:** `"Trash, Don't Delete"` (exact string)
**Rule 2 marker:** `"Silent Failures"` (exact string)

---

## Implementation Details

### 1. File Structure

```bash
#!/usr/bin/env python3
"""
update_cursorrules.py - Push safety rules to all project .cursorrules files.

Usage:
    doppler run -- python scripts/update_cursorrules.py --dry-run
    doppler run -- python scripts/update_cursorrules.py --dry-run --root /path/to/projects
"""

import argparse
import logging
import pathlib
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)
```

### 2. Project Scanner

```bash
def find_cursorrules_files(projects_root: pathlib.Path) -> list[pathlib.Path]:
    """Find all .cursorrules files in project directories (not nested)."""
    cursorrules_files = []

    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir():
            continue
        if project_dir.name.startswith('.') or project_dir.name.startswith('_'):
            continue  # Skip hidden and special directories

        cursorrules = project_dir / ".cursorrules"
        if cursorrules.exists():
            cursorrules_files.append(cursorrules)

    return sorted(cursorrules_files)
```

### 3. Rule Detection

```bash
def check_compliance(cursorrules_path: pathlib.Path) -> dict:
    """Check if a .cursorrules file has the required safety rules."""
    content = cursorrules_path.read_text()

    return {
        'path': cursorrules_path,
        'project': cursorrules_path.parent.name,
        'has_trash_rule': "Trash, Don't Delete" in content,
        'has_silent_rule': "Silent Failures" in content,
    }
```

### 4. Main Logic

```bash
def run_dry_run(projects_root: pathlib.Path) -> bool:
    """Show what would be updated without making changes."""
    logger.info(f"Scanning: {projects_root}")
    logger.info("-" * 60)

    cursorrules_files = find_cursorrules_files(projects_root)

    if not cursorrules_files:
        logger.warning("No .cursorrules files found")
        return True

    stats = {'ok': 0, 'needs_update': 0, 'skip': 0}

    for cr_path in cursorrules_files:
        compliance = check_compliance(cr_path)

        if compliance['has_trash_rule'] and compliance['has_silent_rule']:
            logger.info(f"OK: {compliance['project']} - has all safety rules")
            stats['ok'] += 1
        else:
            missing = []
            if not compliance['has_trash_rule']:
                missing.append("Trash rule")
            if not compliance['has_silent_rule']:
                missing.append("Silent Failures rule")
            logger.info(f"NEEDS UPDATE: {compliance['project']} - missing: {', '.join(missing)}")
            stats['needs_update'] += 1

    logger.info("-" * 60)
    logger.info(f"Summary: {stats['ok']} OK, {stats['needs_update']} need update, {len(cursorrules_files)} total")

    return True
```

### 5. CLI Entry Point

```bash
def main():
    parser = argparse.ArgumentParser(
        description="Push safety rules to all project .cursorrules files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would change without modifying files (default)"
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path("[USER_HOME]/projects"),
        help="Projects root directory"
    )

    args = parser.parse_args()

    if not args.root.exists():
        logger.error(f"Projects root not found: {args.root}")
        sys.exit(1)

    success = run_dry_run(args.root)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

---

## Verification Steps

1. **Test script runs:**
   ```bash
   doppler run -- python scripts/update_cursorrules.py --dry-run
   # Should show list of projects with OK/NEEDS UPDATE status
   ```

2. **Test with explicit root:**
   ```bash
   doppler run -- python scripts/update_cursorrules.py --dry-run --root [USER_HOME]/projects
   # Same output as above
   ```

3. **Verify count:**
   - Should find ~16 projects with .cursorrules files
   - hypocrisynow should show as "OK" (it has the rules)
   - Most others should show as "NEEDS UPDATE"

4. **Test exit code:**
   ```bash
   doppler run -- python scripts/update_cursorrules.py --dry-run && echo "Success"
   # Should print "Success"
   ```

---

## Files to Read First

- `scripts/warden_audit.py` (reference for argparse/logging patterns)
- `Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md` (full context)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 8 acceptance criteria checked
- [ ] Verification steps 1-4 completed successfully
- [ ] Script finds ~16 projects (not 0, not 100+)
- [ ] hypocrisynow shows as "OK"

**Max 3 attempts.** If Worker fails 3x, halt and alert Conductor.


## Related Documentation

- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[LOCAL_MODEL_LEARNINGS]] - local AI

