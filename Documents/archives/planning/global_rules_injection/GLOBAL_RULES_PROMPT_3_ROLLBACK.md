# Worker Task: Rollback + Manifest

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 20 minutes
**Objective:** Add manifest.json logging and --rollback flag to update_cursorrules.py

---

## Context

Tasks 1-2 created the script with dry-run and execute modes. Now we need the safety net: the ability to rollback changes if something goes wrong. Every modification must be logged to a manifest file.

**File to modify:** `scripts/update_cursorrules.py`

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **Argument:** Add `--rollback` flag to argparse
- [ ] **Manifest:** Creates `manifest.json` in backup directory after each run
- [ ] **Manifest Content:** Records timestamp, files modified, source paths, backup paths
- [ ] **Rollback Function:** Restores files from most recent backup
- [ ] **Rollback Output:** Shows which files were restored
- [ ] **Error Handling:** Graceful error if no backups exist
- [ ] **Verification:** After rollback, files match original content

---

## Implementation Details

### 1. Add Rollback Argument

```python
parser.add_argument(
    "--rollback",
    action="store_true",
    help="Restore .cursorrules files from most recent backup"
)
```

### 2. Manifest Structure

```python
import json

# Manifest format:
# {
#     "timestamp": "2026-01-10T12:00:00",
#     "projects_root": "/Users/eriksjaastad/projects",
#     "files_modified": [
#         {
#             "project": "project-tracker",
#             "original": "/Users/eriksjaastad/projects/project-tracker/.cursorrules",
#             "backup": "_cursorrules_backups/2026-01-10T12-00-00/project-tracker/.cursorrules"
#         }
#     ]
# }
```

### 3. Update create_backup to Track Files

```python
def create_backup(
    cursorrules_path: pathlib.Path,
    backup_dir: pathlib.Path,
    manifest_entries: list
) -> pathlib.Path:
    """Create a timestamped backup and track in manifest."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    backup_subdir = backup_dir / timestamp / cursorrules_path.parent.name
    backup_subdir.mkdir(parents=True, exist_ok=True)

    backup_path = backup_subdir / ".cursorrules"
    shutil.copy2(cursorrules_path, backup_path)

    # Track for manifest
    manifest_entries.append({
        'project': cursorrules_path.parent.name,
        'original': str(cursorrules_path),
        'backup': str(backup_path)
    })

    logger.info(f"  Backed up to: {backup_path}")
    return backup_path
```

### 4. Write Manifest Function

```python
def write_manifest(
    backup_dir: pathlib.Path,
    projects_root: pathlib.Path,
    manifest_entries: list
):
    """Write manifest.json with all backup information."""
    manifest = {
        'timestamp': datetime.now().isoformat(),
        'projects_root': str(projects_root),
        'files_modified': manifest_entries
    }

    manifest_path = backup_dir / 'manifest.json'

    # Read existing manifest if it exists (append to history)
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text())
        if isinstance(existing, list):
            existing.append(manifest)
        else:
            existing = [existing, manifest]
        manifest_data = existing
    else:
        manifest_data = [manifest]

    manifest_path.write_text(json.dumps(manifest_data, indent=2))
    logger.info(f"Manifest written to: {manifest_path}")
```

### 5. Rollback Function

```python
def run_rollback(backup_dir: pathlib.Path) -> bool:
    """Restore .cursorrules files from most recent backup."""
    manifest_path = backup_dir / 'manifest.json'

    if not manifest_path.exists():
        logger.error(f"No manifest found at: {manifest_path}")
        logger.error("Cannot rollback without manifest. Check backup directory.")
        return False

    manifest_data = json.loads(manifest_path.read_text())

    # Get most recent backup run
    if isinstance(manifest_data, list):
        if not manifest_data:
            logger.error("Manifest is empty")
            return False
        latest = manifest_data[-1]
    else:
        latest = manifest_data

    logger.info(f"Rolling back to: {latest['timestamp']}")
    logger.info("-" * 60)

    restored = 0
    for entry in latest['files_modified']:
        backup_path = pathlib.Path(entry['backup'])
        original_path = pathlib.Path(entry['original'])

        if not backup_path.exists():
            logger.warning(f"SKIP: Backup not found: {backup_path}")
            continue

        # Restore the file
        shutil.copy2(backup_path, original_path)
        logger.info(f"RESTORED: {entry['project']}")
        restored += 1

    logger.info("-" * 60)
    logger.info(f"Restored {restored} files")

    return True
```

### 6. Update run_update to Use Manifest

```python
def run_update(
    projects_root: pathlib.Path,
    backup_dir: pathlib.Path,
    execute: bool = False
) -> bool:
    """Scan and update all .cursorrules files."""
    # ... existing code ...

    manifest_entries = []  # Track all backups

    for cr_path in cursorrules_files:
        result = update_cursorrules(cr_path, backup_dir, execute, manifest_entries)
        stats[result] += 1

    # Write manifest after all updates
    if execute and manifest_entries:
        write_manifest(backup_dir, projects_root, manifest_entries)

    # ... rest of existing code ...
```

### 7. Update update_cursorrules Signature

```python
def update_cursorrules(
    cursorrules_path: pathlib.Path,
    backup_dir: pathlib.Path,
    execute: bool = False,
    manifest_entries: list = None  # Add this parameter
) -> str:
    # ... existing code ...

    if execute:
        # Create backup first!
        create_backup(cursorrules_path, backup_dir, manifest_entries or [])
        # ... rest ...
```

### 8. Update main() for Rollback

```python
def main():
    # ... existing args and parsing ...

    if args.rollback:
        success = run_rollback(backup_dir)
    else:
        success = run_update(args.root, backup_dir, execute=args.execute)

    sys.exit(0 if success else 1)
```

---

## Verification Steps

1. **Test manifest creation:**
   ```bash
   # Create test project
   mkdir -p /tmp/test-project
   echo "# Test" > /tmp/test-project/.cursorrules

   # Run execute
   python scripts/update_cursorrules.py --execute --root /tmp

   # Check manifest exists
   cat _cursorrules_backups/manifest.json
   # Should show JSON with files_modified array
   ```

2. **Test rollback:**
   ```bash
   # Verify file was modified
   grep "Trash" /tmp/test-project/.cursorrules
   # Should find the rule

   # Rollback
   python scripts/update_cursorrules.py --rollback

   # Verify file restored
   grep "Trash" /tmp/test-project/.cursorrules
   # Should NOT find the rule (back to original)
   ```

3. **Test rollback with no backups:**
   ```bash
   rm -rf _cursorrules_backups
   python scripts/update_cursorrules.py --rollback
   # Should show error: "No manifest found"
   ```

4. **Cleanup:**
   ```bash
   rm -rf /tmp/test-project _cursorrules_backups
   ```

---

## Files to Read First

- `scripts/update_cursorrules.py` (current state from Tasks 1-2)
- `Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md` (rollback procedure section)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 7 acceptance criteria checked
- [ ] Verification steps 1-4 completed successfully
- [ ] manifest.json contains valid JSON with correct structure
- [ ] Rollback actually restores original content

**Max 3 attempts.** If Worker fails 3x, halt and alert Conductor.
