# Worker Task: Canary + Create Flags

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 20 minutes
**Objective:** Add --projects flag (canary deployment) and --create flag (create missing .cursorrules)

---

## Context

Tasks 1-3 created the core script with dry-run, execute, and rollback. Now we need precision targeting:
- `--projects` for canary deployment (update only specific projects)
- `--create` for projects that don't have .cursorrules yet

**File to modify:** `scripts/update_cursorrules.py`

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **Argument:** Add `--projects` flag (comma-separated list of project names)
- [ ] **Argument:** Add `--create` flag (create .cursorrules from template if missing)
- [ ] **Filter:** When --projects specified, only process those projects
- [ ] **Create Logic:** Uses template from `templates/.cursorrules-template`
- [ ] **Create Logic:** Only creates if --create AND --execute both set
- [ ] **Output:** Shows which projects were filtered/skipped
- [ ] **Validation:** Errors gracefully if specified project doesn't exist

---

## Implementation Details

### 1. Add Arguments

```python
parser.add_argument(
    "--projects",
    type=str,
    help="Comma-separated list of project names to update (canary mode)"
)
parser.add_argument(
    "--create",
    action="store_true",
    help="Create .cursorrules from template for projects that don't have one"
)
```

### 2. Parse Projects List

```python
def parse_projects_filter(projects_arg: str | None) -> set | None:
    """Parse comma-separated project names into a set."""
    if not projects_arg:
        return None  # None means "all projects"

    # Split and clean up whitespace
    projects = {p.strip() for p in projects_arg.split(',')}
    return projects
```

### 3. Update find_cursorrules_files for Filtering

```python
def find_cursorrules_files(
    projects_root: pathlib.Path,
    projects_filter: set | None = None,
    include_missing: bool = False
) -> tuple[list[pathlib.Path], list[pathlib.Path]]:
    """Find .cursorrules files, optionally filtered by project name.

    Returns: (existing_files, missing_projects)
    """
    existing = []
    missing = []

    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir():
            continue
        if project_dir.name.startswith('.') or project_dir.name.startswith('_'):
            continue

        # Apply filter if specified
        if projects_filter and project_dir.name not in projects_filter:
            continue

        cursorrules = project_dir / ".cursorrules"
        if cursorrules.exists():
            existing.append(cursorrules)
        elif include_missing:
            missing.append(project_dir)

    return sorted(existing), sorted(missing)
```

### 4. Create from Template Function

```python
def create_from_template(
    project_dir: pathlib.Path,
    template_path: pathlib.Path,
    backup_dir: pathlib.Path,
    manifest_entries: list
) -> bool:
    """Create .cursorrules from template for a project."""
    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        return False

    cursorrules_path = project_dir / ".cursorrules"

    # Read template and customize
    template_content = template_path.read_text()

    # Replace placeholder project name if present
    content = template_content.replace("[project-name]", project_dir.name)

    # Write the new file
    cursorrules_path.write_text(content)

    # Track in manifest (no backup since file is new)
    manifest_entries.append({
        'project': project_dir.name,
        'original': str(cursorrules_path),
        'backup': None,  # No backup for newly created files
        'action': 'created'
    })

    logger.info(f"CREATED: {project_dir.name}/.cursorrules")
    return True
```

### 5. Update run_update Function

```python
def run_update(
    projects_root: pathlib.Path,
    backup_dir: pathlib.Path,
    execute: bool = False,
    projects_filter: set | None = None,
    create_missing: bool = False,
    template_path: pathlib.Path | None = None
) -> bool:
    """Scan and update all .cursorrules files."""
    mode = "EXECUTE" if execute else "DRY-RUN"
    logger.info(f"Mode: {mode}")
    if projects_filter:
        logger.info(f"Filter: {', '.join(sorted(projects_filter))}")
    logger.info(f"Scanning: {projects_root}")
    logger.info("-" * 60)

    existing, missing = find_cursorrules_files(
        projects_root,
        projects_filter,
        include_missing=create_missing
    )

    if not existing and not missing:
        if projects_filter:
            logger.warning(f"No matching projects found for filter: {projects_filter}")
        else:
            logger.warning("No .cursorrules files found")
        return True

    stats = {'ok': 0, 'updated': 0, 'created': 0, 'skipped': 0}
    manifest_entries = []

    # Process existing files
    for cr_path in existing:
        result = update_cursorrules(cr_path, backup_dir, execute, manifest_entries)
        stats[result] += 1

    # Create missing files if requested
    if create_missing and missing:
        if not execute:
            for project_dir in missing:
                logger.info(f"WOULD CREATE: {project_dir.name}/.cursorrules")
                stats['created'] += 1
        else:
            for project_dir in missing:
                if create_from_template(project_dir, template_path, backup_dir, manifest_entries):
                    stats['created'] += 1

    # Write manifest after all updates
    if execute and manifest_entries:
        write_manifest(backup_dir, projects_root, manifest_entries)

    logger.info("-" * 60)
    summary_parts = [f"{stats['ok']} OK"]
    if stats['updated']:
        summary_parts.append(f"{stats['updated']} {'updated' if execute else 'would update'}")
    if stats['created']:
        summary_parts.append(f"{stats['created']} {'created' if execute else 'would create'}")
    logger.info(f"Summary: {', '.join(summary_parts)}")

    if execute:
        logger.info(f"Backups saved to: {backup_dir}")

    return True
```

### 6. Update main() Function

```python
def main():
    parser = argparse.ArgumentParser(
        description="Push safety rules to all project .cursorrules files"
    )
    # ... existing args ...

    args = parser.parse_args()

    backup_dir = args.backup_dir.resolve()
    projects_filter = parse_projects_filter(args.projects)

    # Template path for --create
    script_dir = pathlib.Path(__file__).parent.parent
    template_path = script_dir / "templates" / ".cursorrules-template"

    if args.rollback:
        success = run_rollback(backup_dir)
    else:
        success = run_update(
            args.root,
            backup_dir,
            execute=args.execute,
            projects_filter=projects_filter,
            create_missing=args.create,
            template_path=template_path
        )

    sys.exit(0 if success else 1)
```

---

## Verification Steps

1. **Test --projects filter (dry-run):**
   ```bash
   python scripts/update_cursorrules.py --dry-run --projects "project-tracker,AI-journal"
   # Should only show 2 projects, not all 16
   ```

2. **Test --projects with non-existent project:**
   ```bash
   python scripts/update_cursorrules.py --dry-run --projects "fake-project-xyz"
   # Should show warning: "No matching projects found"
   ```

3. **Test --create dry-run:**
   ```bash
   # Find a project without .cursorrules
   ls /Users/eriksjaastad/projects/*/. | head -20

   # Test create flag
   python scripts/update_cursorrules.py --dry-run --create --projects "some-project-without-cursorrules"
   # Should show: "WOULD CREATE: project-name/.cursorrules"
   ```

4. **Test canary deployment simulation:**
   ```bash
   python scripts/update_cursorrules.py --dry-run --projects "project-tracker,Tax processing,analyze-youtube-videos"
   # Should show exactly 3 projects
   ```

---

## Files to Read First

- `scripts/update_cursorrules.py` (current state from Tasks 1-3)
- `templates/.cursorrules-template` (template for --create)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 7 acceptance criteria checked
- [ ] Verification steps 1-4 completed successfully
- [ ] --projects correctly filters to specified projects only
- [ ] --create shows correct output in dry-run mode

**Max 3 attempts.** If Worker fails 3x, halt and alert Conductor.
