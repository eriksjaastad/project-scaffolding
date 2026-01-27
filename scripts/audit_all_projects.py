#!/usr/bin/env python3
"""
Audit all projects for unfilled template placeholders.

Reads configuration from scan_config.yaml (single source of truth).
"""
import os
import re
from pathlib import Path
from typing import List, Dict

import yaml

from scaffold.constants import PROTECTED_PROJECTS

# Load config from shared YAML file
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", Path.home() / "projects"))
CONFIG_PATH = PROJECTS_ROOT / "project-scaffolding" / "config" / "scan_config.yaml"


def _load_config() -> dict:
    """Load scan configuration from YAML file."""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f)
    return {}


_config = _load_config()
SKIP_DIRS = set(_config.get("skip_dirs", []))


def get_projects_root() -> Path:
    return PROJECTS_ROOT


def audit_projects() -> Dict[str, List[str]]:
    projects_root = get_projects_root()
    placeholder_pattern = re.compile(r"\{\{[A-Z0-9_]+\}\}|\{[a-z0-9_]+\}")
    damage_report = {}

    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
        
        if project_dir.name in PROTECTED_PROJECTS:
            continue
        
        project_issues = []
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            
            for file in files:
                if not file.endswith((".md", ".py", ".sh", ".js", ".ts")):
                    continue
                
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    lines = content.splitlines()
                    for i, line in enumerate(lines):
                        matches = placeholder_pattern.findall(line)
                        if matches:
                            # Heuristic: ignore f-strings in python
                            if file.endswith(".py") and ("f\"" in line or "f'" in line):
                                continue
                            for match in matches:
                                project_issues.append(f"{file_path.relative_to(project_dir)}:{i+1} - {match}")
                except Exception:
                    pass
        
        if project_issues:
            damage_report[project_dir.name] = project_issues
            
    return damage_report

def main() -> None:
    print("=== Ecosystem Damage Report: Unfilled Placeholders ===\n")
    report = audit_projects()
    
    total_files = 0
    if not report:
        print("✅ No unfilled placeholders found across any projects!")
        return

    for project, issues in report.items():
        print(f"📁 {project} ({len(issues)} issues)")
        for issue in issues:
            print(f"   - {issue}")
        total_files += len(issues)
        print()

    print(f"Summary: Found {total_files} issues across {len(report)} projects.")

if __name__ == "__main__":
    main()
