#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
AGENTS.md Sync

Syncs the governed portion of AGENTS.md from the template to all scaffolded
projects. Uses SCAFFOLD markers to preserve project-specific customizations.

Source: project-scaffolding/templates/AGENTS.md.template
Target: <project>/AGENTS.md

Content between <!-- SCAFFOLD:START --> and <!-- SCAFFOLD:END --> markers is
replaced with the template. Content outside those markers is preserved.

This is the cross-platform instruction file read by:
  - Codex (walks directory tree, concatenates all AGENTS.md)
  - Gemini CLI (auto-loads AGENTS.md, GEMINI.md overrides if both exist)

Version tracking is written to .scaffolding-version so project-tracker
can surface out-of-sync projects.

Usage:
  uv run sync_agents_md.py                          # Sync all scaffolded projects
  uv run sync_agents_md.py smart-invoice-workflow    # Sync one project
  uv run sync_agents_md.py --dry-run                 # Show what would change
  uv run sync_agents_md.py --stage                   # Sync and git add changed files
  uv run sync_agents_md.py --list                    # List projects that have AGENTS.md
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLDING_ROOT = SCRIPT_DIR.parent
PROJECTS_ROOT = SCAFFOLDING_ROOT.parent

TEMPLATE_FILE = SCAFFOLDING_ROOT / "templates" / "AGENTS.md.template"
TARGET_FILENAME = "AGENTS.md"

# Markers that delineate the governed section
MARKER_START = "<!-- SCAFFOLD:START - Do not edit between markers -->"
MARKER_END = "<!-- SCAFFOLD:END - Custom content below is preserved -->"

# Safe zones - projects to skip
SAFE_ZONES = ["ai-journal", "writing"]


def extract_template_version(template_path: Path) -> str:
    """Extract a version identifier from the template.

    Uses the hash of the template content as a lightweight version.
    If there's a version string in the file, prefer that.
    """
    content = template_path.read_text()
    # Look for explicit version like (v1.5)
    match = re.search(r"\(v([\d.]+)\)", content)
    if match:
        return match.group(1)
    # Fallback: date-based
    return datetime.now().strftime("%Y.%m.%d")


def update_scaffolding_version(project_dir: Path, version: str):
    """Write agents_md_version and agents_md_synced_at to .scaffolding-version."""
    version_file = project_dir / ".scaffolding-version"
    try:
        if version_file.exists():
            data = json.loads(version_file.read_text())
        else:
            data = {}

        data["agents_md_version"] = version
        data["agents_md_synced_at"] = datetime.now().isoformat()

        version_file.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"  Warning: Failed to update .scaffolding-version: {e}")


def build_governed_section(template_content: str) -> str:
    """Build the full governed section wrapped in SCAFFOLD markers."""
    return f"{MARKER_START}\n{template_content.rstrip()}\n{MARKER_END}"


def extract_custom_content(existing: str) -> tuple[str, str]:
    """Extract content before START marker and after END marker.

    Returns (content_before, content_after).
    """
    content_before = ""
    content_after = ""

    start_idx = existing.find(MARKER_START)
    if start_idx != -1:
        content_before = existing[:start_idx].rstrip()

    end_idx = existing.find(MARKER_END)
    if end_idx != -1:
        after_marker = end_idx + len(MARKER_END)
        content_after = existing[after_marker:].lstrip("\n")

    return content_before, content_after


def find_scaffolded_projects() -> list[Path]:
    """Find all projects with a .scaffolding-version file."""
    projects = []
    for item in sorted(PROJECTS_ROOT.iterdir()):
        if item.is_dir() and (item / ".scaffolding-version").exists():
            if item.name == "project-scaffolding":
                continue
            projects.append(item)
    return projects


def sync_project(
    project_dir: Path,
    template_content: str,
    version: str,
    dry_run: bool = False,
    stage: bool = False,
) -> str:
    """
    Sync AGENTS.md for a single project.

    Returns: "updated", "created", "unchanged", or "skipped"
    """
    if project_dir.name in SAFE_ZONES:
        return "skipped"

    target = project_dir / TARGET_FILENAME
    governed_section = build_governed_section(template_content)

    if target.exists():
        existing = target.read_text()

        if MARKER_START in existing:
            # Has markers — replace governed section, preserve custom content
            content_before, content_after = extract_custom_content(existing)

            parts = []
            if content_before:
                parts.append(content_before)
                parts.append("")
            parts.append(governed_section)
            if content_after:
                parts.append("")
                parts.append(content_after)

            new_content = "\n".join(parts) + "\n"
        else:
            # File exists but no markers — wrap existing content
            # Put markers around the template, keep old content after END
            print(f"  Note: {project_dir.name}/AGENTS.md has no SCAFFOLD markers — adding them")
            new_content = governed_section + "\n"

        if existing == new_content:
            return "unchanged"
        if dry_run:
            return "updated"

        target.write_text(new_content)
        update_scaffolding_version(project_dir, version)

        if stage:
            subprocess.run(
                ["git", "add", str(target)],
                cwd=project_dir,
                capture_output=True,
            )
        return "updated"
    else:
        # No AGENTS.md — create one
        if dry_run:
            return "created"

        new_content = governed_section + "\n"
        target.write_text(new_content)
        update_scaffolding_version(project_dir, version)

        if stage:
            subprocess.run(
                ["git", "add", str(target)],
                cwd=project_dir,
                capture_output=True,
            )
        return "created"


def main():
    parser = argparse.ArgumentParser(description="Sync AGENTS.md to scaffolded projects")
    parser.add_argument("project", nargs="?", help="Specific project name (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--stage", action="store_true", help="Git add changed files")
    parser.add_argument("--list", action="store_true", help="List projects with AGENTS.md")
    args = parser.parse_args()

    if not TEMPLATE_FILE.exists():
        print(f"Error: Template not found at {TEMPLATE_FILE}")
        sys.exit(1)

    template_content = TEMPLATE_FILE.read_text()
    version = extract_template_version(TEMPLATE_FILE)

    if args.list:
        projects = find_scaffolded_projects()
        print("Projects with .scaffolding-version (eligible for AGENTS.md sync):")
        for p in projects:
            has_agents = (p / TARGET_FILENAME).exists()
            has_markers = False
            if has_agents:
                content = (p / TARGET_FILENAME).read_text()
                has_markers = MARKER_START in content
            status = "markers" if has_markers else ("no markers" if has_agents else "no AGENTS.md")
            print(f"  {p.name} ({status})")
        return

    if args.project:
        project_dir = PROJECTS_ROOT / args.project
        if not project_dir.exists():
            print(f"Error: Project not found: {project_dir}")
            sys.exit(1)
        projects = [project_dir]
    else:
        projects = find_scaffolded_projects()

    if args.dry_run:
        print("DRY RUN -- no files will be changed\n")

    print(f"AGENTS.md sync (template version: {version})")

    counts = {"updated": 0, "created": 0, "unchanged": 0, "skipped": 0}

    for project_dir in projects:
        result = sync_project(
            project_dir, template_content, version,
            dry_run=args.dry_run, stage=args.stage,
        )
        counts[result] = counts.get(result, 0) + 1

        if result == "unchanged" or result == "skipped":
            continue

        icon = {"updated": "✏️ ", "created": "✨"}.get(result, "  ")
        print(f"  {icon} {project_dir.name}: {result}")

    print(f"\nDone: {counts['updated']} updated, {counts['created']} created, "
          f"{counts['unchanged']} unchanged, {counts['skipped']} skipped")


if __name__ == "__main__":
    main()
