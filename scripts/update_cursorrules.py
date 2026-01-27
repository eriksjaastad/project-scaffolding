"""
Update .cursorrules files with safety rules section.

Reads configuration from scan_config.yaml (single source of truth).
"""
import argparse
import logging
import pathlib
import sys
import shutil
import json
from datetime import datetime

from scaffold.constants import PROTECTED_PROJECTS

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

SAFETY_RULES_SECTION = '''
---

## 🛡️ Safety Rules

### File Operations
- **Trash, Don't Delete:** NEVER use `rm`, `os.` + `remove`, `os.` + `unlink`, or `shutil.` + `rmtree` for permanent deletion.
- ALWAYS use `send2trash` (Python) to move files to the system Trash.

### Error Handling
- **No Silent Failures:** NEVER swallow exceptions without logging.
- ALWAYS log errors with context (file path, operation attempted, error message).
'''

# Use PROTECTED_PROJECTS from constants (reads from scan_config.yaml)
SKIP_DIRS = PROTECTED_PROJECTS

def parse_projects_filter(projects_arg: str | None) -> set | None:
    """Parse comma-separated project names into a set."""
    if not projects_arg:
        return None
    return {p.strip() for p in projects_arg.split(',')}

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
        if project_dir.name in SKIP_DIRS:
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

def check_compliance(cursorrules_path: pathlib.Path) -> dict:
    """Check if a .cursorrules file has the required safety rules."""
    content = cursorrules_path.read_text()
    return {
        'path': cursorrules_path,
        'project': cursorrules_path.parent.name,
        'has_trash_rule': "Trash, Don't Delete" in content,
        'has_silent_rule': "No Silent Failures" in content,
    }

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
        'backup': str(backup_path),
        'action': 'updated'
    })

    logger.info(f"  Backed up to: {backup_path}")
    return backup_path

def create_from_template(
    project_dir: pathlib.Path,
    template_path: pathlib.Path,
    manifest_entries: list
) -> bool:
    """Create .cursorrules from template for a project."""
    if not template_path.exists():
        logger.error(f"Template not found: {template_path}")
        return False

    cursorrules_path = project_dir / ".cursorrules"
    template_content = template_path.read_text()
    content = template_content.replace("[project-name]", project_dir.name)
    
    cursorrules_path.write_text(content)

    manifest_entries.append({
        'project': project_dir.name,
        'original': str(cursorrules_path),
        'backup': None,
        'action': 'created'
    })

    logger.info(f"CREATED: {project_dir.name}/.cursorrules")
    return True

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

    if manifest_path.exists():
        try:
            existing = json.loads(manifest_path.read_text())
            if isinstance(existing, list):
                existing.append(manifest)
            else:
                existing = [existing, manifest]
            manifest_data = existing
        except json.JSONDecodeError:
            manifest_data = [manifest]
    else:
        manifest_data = [manifest]

    manifest_path.write_text(json.dumps(manifest_data, indent=2))
    logger.info(f"Manifest written to: {manifest_path}")

def inject_safety_rules(content: str, has_trash: bool, has_silent: bool) -> str:
    """Inject missing safety rules into .cursorrules content."""
    if has_trash and has_silent:
        return content

    if not content.endswith('\n'):
        content += '\n'

    content += SAFETY_RULES_SECTION
    return content

def update_cursorrules(
    cursorrules_path: pathlib.Path,
    backup_dir: pathlib.Path,
    execute: bool = False,
    manifest_entries: list = None
) -> str:
    """Update a single .cursorrules file with safety rules."""
    compliance = check_compliance(cursorrules_path)
    project = compliance['project']

    if compliance['has_trash_rule'] and compliance['has_silent_rule']:
        logger.info(f"OK: {project} - already has safety rules")
        return 'ok'

    content = cursorrules_path.read_text()
    new_content = inject_safety_rules(
        content,
        compliance['has_trash_rule'],
        compliance['has_silent_rule']
    )

    if execute:
        create_backup(cursorrules_path, backup_dir, manifest_entries if manifest_entries is not None else [])
        cursorrules_path.write_text(new_content)
        logger.info(f"UPDATED: {project}")
    else:
        logger.info(f"WOULD UPDATE: {project}")
        logger.info(f"  + Safety Rules section ({len(SAFETY_RULES_SECTION)} chars)")

    return 'updated'

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

    for cr_path in existing:
        result = update_cursorrules(cr_path, backup_dir, execute, manifest_entries)
        stats[result] += 1

    if create_missing and missing:
        if not execute:
            for project_dir in missing:
                logger.info(f"WOULD CREATE: {project_dir.name}/.cursorrules")
                stats['created'] += 1
        else:
            for project_dir in missing:
                if create_from_template(project_dir, template_path, manifest_entries):
                    stats['created'] += 1

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

def run_rollback(backup_dir: pathlib.Path) -> bool:
    """Restore .cursorrules files from most recent backup."""
    manifest_path = backup_dir / 'manifest.json'

    if not manifest_path.exists():
        logger.error(f"No manifest found at: {manifest_path}")
        return False

    try:
        manifest_data = json.loads(manifest_path.read_text())
    except json.JSONDecodeError:
        logger.error(f"Failed to parse manifest: {manifest_path}")
        return False

    if not manifest_data:
        logger.error("Manifest is empty")
        return False
    
    latest = manifest_data[-1] if isinstance(manifest_data, list) else manifest_data

    logger.info(f"Rolling back to: {latest['timestamp']}")
    logger.info("-" * 60)

    restored = 0
    for entry in latest['files_modified']:
        if entry.get('action') == 'created':
            logger.info(f"SKIP: {entry['project']} was created, not updated (manual cleanup required if needed)")
            continue
            
        backup_path = pathlib.Path(entry['backup'])
        original_path = pathlib.Path(entry['original'])

        if not backup_path.exists():
            logger.warning(f"SKIP: Backup not found: {backup_path}")
            continue

        shutil.copy2(backup_path, original_path)
        logger.info(f"RESTORED: {entry['project']}")
        restored += 1

    logger.info("-" * 60)
    logger.info(f"Restored {restored} files")
    return True

def main():
    parser = argparse.ArgumentParser(description="Push safety rules to all project .cursorrules files")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Show what would change (default)")
    parser.add_argument("--execute", action="store_true", help="Actually modify files")
    parser.add_argument("--rollback", action="store_true", help="Restore files from most recent backup")
    parser.add_argument("--projects", type=str, help="Comma-separated project names to update")
    parser.add_argument("--create", action="store_true", help="Create missing .cursorrules from template")
    parser.add_argument("--backup-dir", type=pathlib.Path, default=pathlib.Path("_cursorrules_backups"), help="Backup directory")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path.home() / "projects", help="Projects root")
    args = parser.parse_args()
    
    if not args.root.exists():
        logger.error(f"Projects root not found: {args.root}")
        sys.exit(1)
    
    backup_dir = args.backup_dir.resolve()
    projects_filter = parse_projects_filter(args.projects)
    
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

if __name__ == "__main__":
    main()
