#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///

"""
Rules Config Sync

Generates IDE-specific rule files from .agentsync/rules/*.md files.

Source: project/.agentsync/rules/*.md
Targets:
  - Claude Code: CLAUDE.md
  - Cursor: .cursorrules
  - Antigravity: .agent/rules/instructions.md (with trigger: always_on frontmatter)

Features:
  - Concatenates rules in filename order (00-*, 01-*, etc.)
  - Supports YAML frontmatter for tool targeting
  - Adds tool-specific headers to generated files
  - PRESERVES custom content outside AGENTSYNC markers
  - Can stage changes for git (--stage flag)

Usage:
  uv run sync_rules.py project-name           # Sync specific project
  uv run sync_rules.py --all                  # Sync all projects
  uv run sync_rules.py project-name --stage   # Sync and git add
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


# Self-locate
# Script is at: project-scaffolding/agentsync/sync_rules.py
# Projects root is two levels up
SCRIPT_DIR = Path(__file__).resolve().parent
SCAFFOLDING_ROOT = SCRIPT_DIR.parent
PROJECTS_ROOT = SCAFFOLDING_ROOT.parent


def get_rules_version() -> str:
    """Read rules version from templates/.agentsync/RULES_VERSION."""
    try:
        rules_version_path = SCAFFOLDING_ROOT / "templates" / ".agentsync" / "RULES_VERSION"
        if rules_version_path.exists():
            return rules_version_path.read_text().strip()
    except Exception:
        pass
    return "0.0.0"


def get_project_rules_version(project_path: Path) -> str:
    """Read project's current rules_version from .scaffolding-version."""
    version_file = project_path / ".scaffolding-version"
    if version_file.exists():
        try:
            data = json.loads(version_file.read_text())
            return data.get("rules_version", "0.0.0")
        except Exception:
            pass
    return "0.0.0"


def update_rules_version(project_path: Path, new_version: str):
    """Update rules_version in .scaffolding-version after successful sync."""
    version_file = project_path / ".scaffolding-version"
    try:
        if version_file.exists():
            data = json.loads(version_file.read_text())
        else:
            data = {}
        
        data["rules_version"] = new_version
        data["rules_synced_at"] = datetime.now().isoformat()
        
        version_file.write_text(json.dumps(data, indent=2))
        print(f"  ✅ Updated rules_version to {new_version} in .scaffolding-version")
    except Exception as e:
        print(f"  ⚠️  Failed to update .scaffolding-version: {e}")


# Markers for auto-generated sections (content outside these is preserved)
MARKERS = {
    "markdown": {
        "start": "<!-- AGENTSYNC:START - Do not edit between markers -->",
        "end": "<!-- AGENTSYNC:END - Custom rules below this line are preserved -->",
    },
    "comment": {
        "start": "# AGENTSYNC:START - Do not edit between markers",
        "end": "# AGENTSYNC:END - Custom rules below this line are preserved",
    },
}

# Tool configurations
TOOLS = {
    "claude": {
        "output": "CLAUDE.md",
        "marker_style": "markdown",
        "file_header": "# CLAUDE.md - {project_name}\n\n",
        "section_header": "<!-- To modify synced rules: Edit .agentsync/rules/*.md, then run: -->\n<!-- uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py {project_name} -->\n\n",
        "section_footer": "\n\n<!-- Source: .agentsync/rules/*.md -->\n",
    },
    "cursor": {
        "output": ".cursorrules",
        "marker_style": "comment",
        "file_header": "# Cursor Rules for {project_name}\n\n",
        "section_header": "# To modify synced rules: Edit .agentsync/rules/*.md, then run:\n# uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py {project_name}\n\n",
        "section_footer": "\n\n# Source: .agentsync/rules/*.md\n",
    },
    "antigravity": {
        "output": ".agent/rules/instructions.md",
        "marker_style": "markdown",
        "file_header": "---\ntrigger: always_on\n---\n\n# Antigravity Rules for {project_name}\n\n",
        "section_header": "<!-- To modify synced rules: Edit .agentsync/rules/*.md, then run: -->\n<!-- uv run $PROJECTS_ROOT/project-scaffolding/agentsync/sync_rules.py {project_name} -->\n\n",
        "section_footer": "\n\n<!-- Source: .agentsync/rules/*.md -->\n",
    },
}


# Safe zones - projects to skip
SAFE_ZONES = ["ai-journal", "writing"]


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content.

    Returns (frontmatter_dict, content_without_frontmatter)
    """
    if not content.startswith("---"):
        return {}, content

    # Find closing ---
    end_match = re.search(r'\n---\n', content[3:])
    if not end_match:
        return {}, content

    frontmatter_str = content[3:end_match.start() + 3]
    remaining_content = content[end_match.end() + 3 + 1:]

    # Parse YAML (simple key: value parsing to avoid heavy dependency)
    frontmatter = {}
    for line in frontmatter_str.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Handle lists like ["claude", "cursor"]
            if value.startswith('[') and value.endswith(']'):
                value = [v.strip().strip('"').strip("'") for v in value[1:-1].split(',')]
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            frontmatter[key] = value

    return frontmatter, remaining_content


def extract_custom_content(existing_content: str, marker_style: str) -> tuple[str, str]:
    """Extract content before START marker and after END marker.

    Returns (content_before, content_after)
    """
    markers = MARKERS[marker_style]
    start_marker = markers["start"]
    end_marker = markers["end"]

    content_before = ""
    content_after = ""

    # Find start marker
    start_idx = existing_content.find(start_marker)
    if start_idx != -1:
        content_before = existing_content[:start_idx].rstrip()

    # Find end marker
    end_idx = existing_content.find(end_marker)
    if end_idx != -1:
        after_marker = end_idx + len(end_marker)
        content_after = existing_content[after_marker:].lstrip('\n')

    return content_before, content_after


def get_projects_root():
    """Get projects root from env or self-location."""
    if "PROJECTS_ROOT" in os.environ:
        return Path(os.environ["PROJECTS_ROOT"])
    return PROJECTS_ROOT


def load_rules(project_path: Path) -> list[tuple[str, dict, str]]:
    """Load all rule files from .agentsync/rules/.

    Returns list of (filename, frontmatter, content) tuples, sorted by filename.
    """
    rules_dir = project_path / ".agentsync" / "rules"
    if not rules_dir.exists():
        return []

    rules = []
    for rule_file in sorted(rules_dir.glob("*.md")):
        content = rule_file.read_text()
        frontmatter, body = parse_frontmatter(content)
        rules.append((rule_file.name, frontmatter, body))

    return rules


def should_include_for_tool(frontmatter: dict, tool_name: str) -> bool:
    """Check if a rule should be included for a specific tool."""
    targets = frontmatter.get("targets", ["*"])
    if isinstance(targets, str):
        targets = [targets]
    return "*" in targets or tool_name in targets


def generate_rules_content(rules: list[tuple[str, dict, str]], tool_name: str) -> str:
    """Generate concatenated rules content for a specific tool."""
    parts = []
    for filename, frontmatter, body in rules:
        if should_include_for_tool(frontmatter, tool_name):
            parts.append(body.strip())
    return "\n\n".join(parts)


def sync_project(project_name: str, stage_changes: bool = False, dry_run: bool = False) -> bool:
    """Sync rules for a specific project."""
    projects_root = get_projects_root()
    project_path = projects_root / project_name

    if not project_path.exists():
        print(f"  Error: Project not found: {project_path}", file=sys.stderr)
        return False

    # Check safe zones
    if project_name in SAFE_ZONES:
        print(f"  Skipping {project_name}: Protected safe zone")
        return True

    # Check for .agentsync/rules/
    rules_dir = project_path / ".agentsync" / "rules"
    if not rules_dir.exists():
        print(f"  Skipping {project_name}: No .agentsync/rules/ directory")
        return True

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Syncing {project_name}...")

    # Version comparison
    current_rules_version = get_rules_version()
    project_rules_version = get_project_rules_version(project_path)

    if project_rules_version < current_rules_version:
        print(f"  ⚠️  Updating rules from {project_rules_version} to {current_rules_version}")
    elif project_rules_version > current_rules_version:
        print(f"  ⚠️  Warning: Project has newer rules version ({project_rules_version}) than this CLI ({current_rules_version})")
    else:
        print(f"  ℹ️  Rules already at version {current_rules_version}")

    # Load rules
    rules = load_rules(project_path)
    if not rules:
        print(f"  No rule files found in {rules_dir}")
        return True

    print(f"  Found {len(rules)} rule file(s): {', '.join(r[0] for r in rules)}")

    updated_files = []

    # Generate for each tool
    for tool_name, tool_config in TOOLS.items():
        content = generate_rules_content(rules, tool_name)
        if not content:
            continue

        marker_style = tool_config["marker_style"]
        markers = MARKERS[marker_style]

        # Build the auto-generated section
        file_header = tool_config["file_header"].format(project_name=project_name)
        section_header = tool_config["section_header"].format(project_name=project_name)
        section_footer = tool_config["section_footer"]

        auto_section = (
            markers["start"] + "\n" +
            section_header +
            content +
            section_footer +
            markers["end"]
        )

        # Determine output path
        output_path = project_path / tool_config["output"]

        # Check for existing content to preserve
        content_before = file_header.rstrip()
        content_after = ""

        if output_path.exists():
            existing = output_path.read_text()

            # Check if file has our markers
            if markers["start"] in existing:
                preserved_before, preserved_after = extract_custom_content(existing, marker_style)
                # Only use preserved_before if it's not just our standard header
                # (to avoid duplicating headers on migration)
                if preserved_before and not preserved_before.endswith(file_header.strip()):
                    content_before = preserved_before
                content_after = preserved_after
            else:
                # File exists but has NO markers (first-time sync)
                # Preserve ALL existing content below the new AGENTSYNC:END marker
                content_after = existing.strip()
                print(f"  Note: {output_path.name} exists without markers — preserving existing content below AGENTSYNC:END")

        # Build full content
        parts = [content_before, "", auto_section]
        if content_after:
            parts.append("")
            parts.append(content_after)

        full_content = "\n".join(parts)

        if dry_run:
            print(f"  Would write: {output_path.relative_to(project_path)}")
            if content_after:
                print(f"    (preserving custom content after END marker)")
            continue

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if content changed
        if output_path.exists():
            existing = output_path.read_text()
            if existing == full_content:
                continue

        # Write output
        output_path.write_text(full_content)
        updated_files.append(output_path)
        print(f"  Wrote: {output_path.relative_to(project_path)}")
        if content_after:
            print(f"    (preserved custom content)")

    # Stage changes if requested
    if stage_changes and updated_files and not dry_run:
        for f in updated_files:
            subprocess.run(["git", "add", str(f)], cwd=project_path, check=False)
        print(f"  Staged {len(updated_files)} file(s)")

    if not updated_files and not dry_run:
        print(f"  All files already up to date")

    # Update version metadata
    if not dry_run:
        update_rules_version(project_path, current_rules_version)

    return True


def find_agentsync_projects() -> list[str]:
    """Find all projects with .agentsync/rules/ directories."""
    projects_root = get_projects_root()
    projects = []

    for item in projects_root.iterdir():
        if item.is_dir() and not item.name.startswith(".") and not item.name.startswith("_"):
            agentsync_dir = item / ".agentsync" / "rules"
            if agentsync_dir.exists():
                projects.append(item.name)

    return sorted(projects)


def main():
    parser = argparse.ArgumentParser(description="Sync .agentsync/rules/ to IDE-specific config files")
    parser.add_argument("project", nargs="?", help="Project name to sync")
    parser.add_argument("--all", action="store_true", help="Sync all projects with .agentsync/")
    parser.add_argument("--stage", action="store_true", help="Git add changed files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--list", action="store_true", help="List projects with .agentsync/")
    parser.add_argument("--version", action="store_true", help="Show current rules version")

    args = parser.parse_args()

    if args.version:
        print(f"Agentsync Rules Version: {get_rules_version()}")
        return

    if args.list:
        projects = find_agentsync_projects()
        print(f"Projects with .agentsync/rules/:")
        for p in projects:
            print(f"  {p}")
        if not projects:
            print("  (none found)")
        return

    if args.all:
        projects = find_agentsync_projects()
        if not projects:
            print("No projects with .agentsync/rules/ found")
            return
        print(f"Syncing {len(projects)} project(s)...")
        success = True
        for project in projects:
            if not sync_project(project, stage_changes=args.stage, dry_run=args.dry_run):
                success = False
        if not success:
            sys.exit(1)
    elif args.project:
        if not sync_project(args.project, stage_changes=args.stage, dry_run=args.dry_run):
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
