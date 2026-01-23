#!/usr/bin/env python3
"""
Audit all projects for unfilled template placeholders.
"""
import os
import re
from pathlib import Path
from typing import List, Dict

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        # Fallback to standard layout if env var not set
        return Path(__file__).parent.parent.parent
    return Path(root)

def audit_projects() -> Dict[str, List[str]]:
    projects_root = get_projects_root()
    placeholder_pattern = re.compile(r"\{\{[A-Z0-9_]+\}\}|\{[a-z0-9_]+\}")
    damage_report = {}

    skip_dirs = {".git", "venv", ".venv", "__pycache__", "node_modules", "_trash", "archives"}

    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
        
        project_issues = []
        for root, dirs, files in os.walk(project_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
            
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
