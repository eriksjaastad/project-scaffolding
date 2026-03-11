#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Unified AgentSync

Canonical project-scoped sync command for AgentSync.

By default this orchestrates the project-scoped sync components:
  - rules      -> CLAUDE.md and .agent/rules/instructions.md
  - agents     -> AGENTS.md governed section
  - governance -> .agent/rules/governance.md

MCP sync is intentionally excluded from the default flow because it manages
workstation-level configuration, not per-project files.

Usage:
  uv run sync.py project-name
  uv run sync.py --all
  uv run sync.py project-name --components rules
  uv run sync.py --list
"""

import argparse
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLDING_ROOT = SCRIPT_DIR.parent

# Ensure direct script execution imports the local agentsync modules, not an
# unrelated installed package with the same top-level name.
if str(SCAFFOLDING_ROOT) not in sys.path:
    sys.path.insert(0, str(SCAFFOLDING_ROOT))

from agentsync import sync_agents_md, sync_governance, sync_rules  # noqa: E402


AVAILABLE_COMPONENTS = ("rules", "agents", "governance")
SAFE_ZONES = set(getattr(sync_rules, "SAFE_ZONES", []))


def parse_components(raw: str | None) -> list[str]:
    """Parse a comma-separated component list in canonical order."""
    if not raw:
        return list(AVAILABLE_COMPONENTS)

    requested = {part.strip().lower() for part in raw.split(",") if part.strip()}
    invalid = sorted(requested.difference(AVAILABLE_COMPONENTS))
    if invalid:
        valid = ", ".join(AVAILABLE_COMPONENTS)
        raise ValueError(f"Unknown component(s): {', '.join(invalid)}. Valid components: {valid}")

    return [component for component in AVAILABLE_COMPONENTS if component in requested]


def get_projects_root() -> Path:
    """Resolve the projects root using the existing rules sync logic."""
    return Path(sync_rules.get_projects_root())


def is_safe_zone(project_name: str) -> bool:
    """Return True when the project is a protected safe zone."""
    return project_name in SAFE_ZONES


def list_projects(component: str) -> list[str]:
    """List projects eligible for a given sync component."""
    if component == "rules":
        return sync_rules.find_agentsync_projects()
    if component == "agents":
        return [project.name for project in sync_agents_md.find_scaffolded_projects()]
    if component == "governance":
        return [project.name for project in sync_governance.find_scaffolded_projects()]
    raise ValueError(f"Unsupported component: {component}")


def print_project_list(components: list[str]) -> None:
    """Print eligible projects for each selected component."""
    for component in components:
        projects = list_projects(component)
        print(f"{component}:")
        if projects:
            for project in projects:
                print(f"  {project}")
        else:
            print("  (none found)")


def resolve_project(project_name: str) -> Path | None:
    """Resolve an explicit project path, returning None if it does not exist."""
    project_dir = get_projects_root() / project_name
    if not project_dir.exists():
        print(f"Error: Project not found: {project_dir}", file=sys.stderr)
        return None
    return project_dir


def run_rules_component(project_name: str | None, all_projects: bool, dry_run: bool, stage: bool) -> bool:
    """Run the rules sync component."""
    if project_name:
        return sync_rules.sync_project(project_name, stage_changes=stage, dry_run=dry_run)

    if not all_projects:
        return True

    projects = sync_rules.find_agentsync_projects()
    if not projects:
        print("No projects with .agentsync/rules/ found")
        return True

    print(f"Syncing rules for {len(projects)} project(s)...")
    success = True
    for project in projects:
        if not sync_rules.sync_project(project, stage_changes=stage, dry_run=dry_run):
            success = False
    return success


def run_agents_component(project_name: str | None, all_projects: bool, dry_run: bool, stage: bool) -> bool:
    """Run the AGENTS.md sync component."""
    if not sync_agents_md.TEMPLATE_FILE.exists():
        print(f"Error: Template not found at {sync_agents_md.TEMPLATE_FILE}", file=sys.stderr)
        return False

    template_content = sync_agents_md.TEMPLATE_FILE.read_text()
    version = sync_agents_md.extract_template_version(sync_agents_md.TEMPLATE_FILE)

    if project_name:
        project_dir = resolve_project(project_name)
        if project_dir is None:
            return False
        projects = [project_dir]
    elif all_projects:
        projects = sync_agents_md.find_scaffolded_projects()
    else:
        return True

    if dry_run:
        print("DRY RUN -- no AGENTS.md files will be changed\n")

    print(f"AGENTS.md sync (template version: {version})")
    counts = {"updated": 0, "created": 0, "unchanged": 0, "skipped": 0}

    for project_dir in projects:
        result = sync_agents_md.sync_project(
            project_dir,
            template_content,
            version,
            dry_run=dry_run,
            stage=stage,
        )
        counts[result] = counts.get(result, 0) + 1
        if result in {"updated", "created"}:
            icon = {"updated": "✏️ ", "created": "✨"}[result]
            print(f"  {icon} {project_dir.name}: {result}")

    print(
        f"\nDone: {counts['updated']} updated, {counts['created']} created, "
        f"{counts['unchanged']} unchanged, {counts['skipped']} skipped"
    )
    return True


def run_governance_component(project_name: str | None, all_projects: bool, dry_run: bool, stage: bool) -> bool:
    """Run the governance sync component."""
    if not sync_governance.SOURCE_FILE.exists():
        print(f"Error: Source not found at {sync_governance.SOURCE_FILE}", file=sys.stderr)
        return False

    version = sync_governance.extract_version(sync_governance.SOURCE_FILE)
    synced_content = sync_governance.build_synced_content(sync_governance.SOURCE_FILE)

    if project_name:
        project_dir = resolve_project(project_name)
        if project_dir is None:
            return False
        projects = [project_dir]
    elif all_projects:
        projects = sync_governance.find_scaffolded_projects()
    else:
        return True

    if dry_run:
        print("DRY RUN — no governance files will be changed\n")

    print(f"Governance Protocol v{version}")
    counts: dict[str, int] = {"updated": 0, "created": 0, "unchanged": 0}

    for project_dir in projects:
        if is_safe_zone(project_dir.name):
            print(f"  Skipping {project_dir.name}: Protected safe zone")
            continue
        result = sync_governance.sync_project(
            project_dir,
            version,
            synced_content,
            dry_run=dry_run,
            stage=stage,
        )
        counts[result] = counts.get(result, 0) + 1
        if result != "unchanged":
            icon = {"updated": "✏️ ", "created": "✨"}.get(result, "  ")
            print(f"  {icon} {project_dir.name}: {result}")

    print(
        f"\nDone: {counts['updated']} updated, {counts['created']} created, "
        f"{counts['unchanged']} unchanged"
    )
    return True


def run_component(component: str, project_name: str | None, all_projects: bool, dry_run: bool, stage: bool) -> bool:
    """Dispatch to the selected sync component."""
    if project_name and is_safe_zone(project_name):
        print(f"Skipping {project_name}: Protected safe zone")
        return True

    if component == "rules":
        return run_rules_component(project_name, all_projects, dry_run, stage)
    if component == "agents":
        return run_agents_component(project_name, all_projects, dry_run, stage)
    if component == "governance":
        return run_governance_component(project_name, all_projects, dry_run, stage)
    raise ValueError(f"Unsupported component: {component}")


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and run the selected AgentSync components."""
    parser = argparse.ArgumentParser(description="Unified AgentSync command")
    parser.add_argument("project", nargs="?", help="Project name to sync")
    parser.add_argument("--all", action="store_true", help="Sync all eligible projects")
    parser.add_argument("--components", help="Comma-separated components: rules,agents,governance")
    parser.add_argument("--stage", action="store_true", help="Git add changed files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--list", action="store_true", help="List eligible projects for the selected components")
    args = parser.parse_args(argv)

    if args.project and args.all:
        parser.error("Choose either a specific project or --all, not both")

    try:
        components = parse_components(args.components)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.list:
        print_project_list(components)
        return 0

    if not args.project and not args.all:
        parser.print_help()
        return 0

    success = True
    for component in components:
        if not run_component(component, args.project, args.all, args.dry_run, args.stage):
            success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())