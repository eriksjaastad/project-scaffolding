#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Governance Document Sync

Copies REVIEWS_AND_GOVERNANCE_PROTOCOL.md from project-scaffolding (SSOT)
to all scaffolded projects. This is a direct replace — no per-project
customization. The source of truth always wins.

Source: project-scaffolding/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
Target: <project>/Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md

Usage:
  uv run sync_governance.py                     # Sync all scaffolded projects
  uv run sync_governance.py smart-invoice-workflow  # Sync one project
  uv run sync_governance.py --dry-run           # Show what would change
  uv run sync_governance.py --stage             # Sync and git add changed files
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLDING_ROOT = SCRIPT_DIR.parent
PROJECTS_ROOT = SCAFFOLDING_ROOT.parent

SOURCE_FILE = SCAFFOLDING_ROOT / "REVIEWS_AND_GOVERNANCE_PROTOCOL.md"
TARGET_REL = Path("Documents") / "REVIEWS_AND_GOVERNANCE_PROTOCOL.md"


def find_scaffolded_projects() -> list[Path]:
    """Find all projects with a .scaffolding-version file."""
    projects = []
    for item in sorted(PROJECTS_ROOT.iterdir()):
        if item.is_dir() and (item / ".scaffolding-version").exists():
            # Skip project-scaffolding itself — it has the source, not a copy
            if item.name == "project-scaffolding":
                continue
            projects.append(item)
    return projects


def sync_project(project_dir: Path, dry_run: bool = False, stage: bool = False) -> str:
    """
    Sync governance doc to a single project.

    Returns: "updated", "created", "unchanged", or "skipped"
    """
    target = project_dir / TARGET_REL

    if not target.parent.exists():
        if dry_run:
            return "created"
        target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists():
        if filecmp.cmp(SOURCE_FILE, target, shallow=False):
            return "unchanged"

    if dry_run:
        return "created" if not target.exists() else "updated"

    shutil.copy2(SOURCE_FILE, target)

    if stage:
        import subprocess
        subprocess.run(
            ["git", "add", str(target)],
            cwd=project_dir,
            capture_output=True,
        )

    return "created" if not target.exists() else "updated"


def main():
    parser = argparse.ArgumentParser(description="Sync governance doc to scaffolded projects")
    parser.add_argument("project", nargs="?", help="Specific project name (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--stage", action="store_true", help="Git add changed files")
    args = parser.parse_args()

    if not SOURCE_FILE.exists():
        print(f"Error: Source not found at {SOURCE_FILE}")
        sys.exit(1)

    if args.project:
        project_dir = PROJECTS_ROOT / args.project
        if not project_dir.exists():
            print(f"Error: Project not found: {project_dir}")
            sys.exit(1)
        projects = [project_dir]
    else:
        projects = find_scaffolded_projects()

    if args.dry_run:
        print("DRY RUN — no files will be changed\n")

    counts = {"updated": 0, "created": 0, "unchanged": 0}

    for project_dir in projects:
        result = sync_project(project_dir, dry_run=args.dry_run, stage=args.stage)
        counts[result] = counts.get(result, 0) + 1

        if result == "unchanged":
            continue

        icon = {"updated": "📝", "created": "✨"}.get(result, "  ")
        print(f"  {icon} {project_dir.name}: {result}")

    print(f"\nDone: {counts['updated']} updated, {counts['created']} created, {counts['unchanged']} unchanged")


if __name__ == "__main__":
    main()
