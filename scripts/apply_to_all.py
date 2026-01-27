#!/usr/bin/env python3
"""
Run 'scaffold apply' on all projects to fix missing files and placeholders.
"""
import os
import subprocess
from pathlib import Path
from scaffold.constants import PROTECTED_PROJECTS

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def apply_scaffolding_to_all() -> None:
    projects_root = get_projects_root()
    scaffolding_root = Path(__file__).parent.parent
    cli_script = scaffolding_root / "scaffold_cli.py"
    
    print(f"Applying scaffolding to all projects in {projects_root}...\n")
    
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
            
        if project_dir.name in PROTECTED_PROJECTS:
            print(f"⏭️  Skipping protected/scaffolding project: {project_dir.name}")
            continue
            
        print(f"🚀 Applying to {project_dir.name}...")
        try:
            # Use uv run for consistent Python environment
            subprocess.run(
                ["uv", "run", str(cli_script), "apply", project_dir.name],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✅ Success: {project_dir.name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {project_dir.name}")
            print(f"   Error: {e.stderr}")

if __name__ == "__main__":
    apply_scaffolding_to_all()
