#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["send2trash"]
# ///

"""
Migrate AGENTS.md to .agentsync/rules/ Structure

Converts a single AGENTS.md file into the new modular .agentsync/rules/ structure.

Usage:
  uv run migrate_agents_md.py project-name           # Migrate specific project
  uv run migrate_agents_md.py --all                  # Migrate all projects
  uv run migrate_agents_md.py project-name --dry-run # Preview migration
  uv run migrate_agents_md.py project-name --cleanup # Cleanup migration artifacts
"""

import argparse
import os
import re
import sys
from pathlib import Path

import send2trash


# Self-locate
# Script is at: project-scaffolding/agentsync/migrate_agents_md.py
SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLDING_ROOT = SCRIPT_DIR.parent
PROJECTS_ROOT = SCAFFOLDING_ROOT.parent


# Safe zones - projects to skip
SAFE_ZONES = ["ai-journal", "writing"]


def get_projects_root():
    """Get projects root from env or self-location."""
    if "PROJECTS_ROOT" in os.environ:
        return Path(os.environ["PROJECTS_ROOT"])
    return PROJECTS_ROOT


def split_agents_md(content: str) -> dict[str, str]:
    """Split AGENTS.md content into logical sections.

    Returns a dict mapping section names to content.
    """
    sections = {}

    # Common section headers to look for
    section_patterns = [
        (r'^#\s*(?:AGENTS\.md\s*-\s*)?Ecosystem Constitution.*$', '00-overview'),
        (r'^##\s*.*SYSTEM ARCHITECTURE.*HIERARCHY.*$', '01-hierarchy'),
        (r'^##\s*.*THE WORKFLOW.*$', '02-workflow'),
        (r'^##\s*.*SANDBOX DRAFT PATTERN.*$', '03-sandbox-draft'),
        (r'^##\s*.*MCP SERVER INFRASTRUCTURE.*$', '04-mcp-infrastructure'),
        (r'^##\s*.*STANDARDIZED PROMPT TEMPLATE.*$', '05-prompt-template'),
        (r'^##\s*.*UNIVERSAL CONSTRAINTS.*$', '06-constraints'),
        (r'^##\s*.*Safety.*File Operations.*$', '07-safety'),
        (r'^##\s*.*JOURNAL ENTRY PROTOCOL.*$', '08-journal'),
        (r'^##\s*.*CARETAKER ROLE.*$', '09-caretaker'),
        (r'^##\s*.*OBSIDIAN INTEGRATION.*$', '10-obsidian'),
        (r'^##\s*.*RELATED DOCUMENTS.*$', '99-related'),
    ]

    # For now, we'll put everything in a single file
    # A more sophisticated version would split by headers
    sections['00-full-content'] = content

    return sections


def migrate_project(project_name: str, dry_run: bool = False) -> bool:
    """Migrate a single project from AGENTS.md to .agentsync/rules/."""
    projects_root = get_projects_root()
    project_path = projects_root / project_name

    if not project_path.exists():
        print(f"  Error: Project not found: {project_path}", file=sys.stderr)
        return False

    # Check safe zones
    if project_name in SAFE_ZONES:
        print(f"  Skipping {project_name}: Protected safe zone")
        return True

    agents_md = project_path / "AGENTS.md"
    if not agents_md.exists():
        print(f"  Skipping {project_name}: No AGENTS.md found")
        return True

    # Check if already migrated
    agentsync_dir = project_path / ".agentsync" / "rules"
    if agentsync_dir.exists() and any(agentsync_dir.glob("*.md")):
        print(f"  Skipping {project_name}: Already has .agentsync/rules/")
        return True

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Migrating {project_name}...")

    # Read AGENTS.md
    content = agents_md.read_text()

    # Check if it's an auto-generated file (from old sync)
    if "AUTO-GENERATED from AGENTS.md" in content or "Source of truth: AGENTS.md" in content:
        print(f"  Note: This appears to be an auto-generated file, looking for source...")
        # This might be CLAUDE.md or .cursorrules, not the actual AGENTS.md
        # Skip these

    # Create .agentsync/rules/ directory
    rules_dir = project_path / ".agentsync" / "rules"

    if dry_run:
        print(f"  Would create: {rules_dir}")
        print(f"  Would write: {rules_dir / '00-full-content.md'}")
        print(f"  Content length: {len(content)} chars")
        return True

    # Create directory
    rules_dir.mkdir(parents=True, exist_ok=True)

    # Write the content as a single file (can be split later)
    # Add frontmatter
    output_content = f"""---
targets: ["*"]
---

{content}
"""

    output_file = rules_dir / "00-full-content.md"
    output_file.write_text(output_content)
    print(f"  Created: {output_file.relative_to(project_path)}")

    # Create README
    readme = project_path / ".agentsync" / "README.md"
    if not readme.exists():
        readme_content = """# .agentsync Directory

This directory contains the source of truth for agent configurations.

## Structure

Edit files in `rules/` - they will be synced to CLAUDE.md, .cursorrules, and .agent/rules/agents.md.

## Manual Sync

```bash
uv run $PROJECT_ROOT/project-scaffolding/agentsync/sync_rules.py {project_name}
```
""".format(project_name=project_name)
        readme.write_text(readme_content)
        print(f"  Created: {readme.relative_to(project_path)}")

    return True


def cleanup_migration_artifacts(project_name: str, dry_run: bool = False) -> bool:
    """Remove migration artifact 00-full-content.md if real rule files exist.
    
    The 00-full-content.md file was created during initial migration as a temporary
    placeholder. Once sync_rules.py creates the real rule files (01-workflow.md, etc.),
    the artifact should be removed.
    
    Returns True if cleanup succeeded or was not needed, False on error.
    """
    projects_root = get_projects_root()
    project_path = projects_root / project_name
    
    if not project_path.exists():
        print(f"  Error: Project not found: {project_path}", file=sys.stderr)
        return False
    
    # Check safe zones
    if project_name in SAFE_ZONES:
        print(f"  Skipping {project_name}: Protected safe zone")
        return True
    
    rules_dir = project_path / ".agentsync" / "rules"
    if not rules_dir.exists():
        print(f"  Skipping {project_name}: No .agentsync/rules/ directory")
        return True
    
    # Check if 00-full-content.md exists
    artifact_file = rules_dir / "00-full-content.md"
    if not artifact_file.exists():
        print(f"  {project_name}: Already clean (no 00-full-content.md)")
        return True
    
    # Check if other real rule files exist (01-*, 02-*, etc.)
    other_rules = [f for f in rules_dir.glob("*.md") if f.name != "00-full-content.md"]
    
    if not other_rules:
        print(f"  {project_name}: Keeping 00-full-content.md (no synced rules yet)")
        return True
    
    # Migration is complete - safe to remove artifact
    if dry_run:
        print(f"  [DRY RUN] Would remove: {artifact_file.relative_to(project_path)}")
        return True
    
    try:
        send2trash.send2trash(str(artifact_file))
        print(f"  Cleaned up: {artifact_file.relative_to(project_path)} (migration artifact)")
        return True
    except Exception as e:
        print(f"  Error: Failed to clean up {artifact_file}: {e}", file=sys.stderr)
        return False
    """Find all projects with AGENTS.md files."""
    projects_root = get_projects_root()
    projects = []

    for item in projects_root.iterdir():
        if item.is_dir() and not item.name.startswith(".") and not item.name.startswith("_"):
            agents_md = item / "AGENTS.md"
            if agents_md.exists():
                projects.append(item.name)

    return sorted(projects)


def main():
    parser = argparse.ArgumentParser(description="Migrate AGENTS.md to .agentsync/rules/ structure")
    parser.add_argument("project", nargs="?", help="Project name to migrate")
    parser.add_argument("--all", action="store_true", help="Migrate all projects")
    parser.add_argument("--dry-run", action="store_true", help="Preview migration without changes")
    parser.add_argument("--list", action="store_true", help="List projects with AGENTS.md")
    parser.add_argument("--cleanup", action="store_true", help="Clean up migration artifacts without re-migrating")

    args = parser.parse_args()

    if args.list:
        projects = find_projects_with_agents_md()
        print(f"Projects with AGENTS.md ({len(projects)}):")
        for p in projects:
            agentsync = get_projects_root() / p / ".agentsync" / "rules"
            status = "already migrated" if agentsync.exists() else "needs migration"
            print(f"  {p}: {status}")
        return

    if args.cleanup:
        if args.all:
            projects = find_projects_with_agents_md()
            if not projects:
                print("No projects with AGENTS.md found")
                return
            print(f"Cleaning up migration artifacts in {len(projects)} project(s)...")
            success = True
            for project in projects:
                if not cleanup_migration_artifacts(project, dry_run=args.dry_run):
                    success = False
            if not success:
                sys.exit(1)
        elif args.project:
            if not cleanup_migration_artifacts(args.project, dry_run=args.dry_run):
                sys.exit(1)
        else:
            print("Cleanup requires either --all or a project name")
            sys.exit(1)
        return

    if args.all:
        projects = find_projects_with_agents_md()
        if not projects:
            print("No projects with AGENTS.md found")
            return
        print(f"Migrating {len(projects)} project(s)...")
        success = True
        for project in projects:
            if not migrate_project(project, dry_run=args.dry_run):
                success = False
        if not success:
            sys.exit(1)
    elif args.project:
        if not migrate_project(args.project, dry_run=args.dry_run):
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
