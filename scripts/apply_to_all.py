#!/usr/bin/env python3
"""
Run 'scaffold apply' on all projects to fix missing files and placeholders.
"""
import os
import subprocess
from pathlib import Path

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def apply_scaffolding_to_all() -> None:
    projects_root = get_projects_root()
    scaffolding_root = Path(__file__).parent.parent
    cli_script = scaffolding_root / "scaffold_cli.py"
    
    skip_dirs = {"ai-journal", "writing", "plugin-duplicate-detection", "plugin-find-names-chrome", "project-scaffolding"}
    
    print(f"Applying scaffolding to all projects in {projects_root}...\n")
    
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
            
        if project_dir.name in skip_dirs:
            print(f"⏭️  Skipping protected/scaffolding project: {project_dir.name}")
            continue
            
        print(f"🚀 Applying to {project_dir.name}...")
        try:
            # We use the full path to the python executable and the script
            subprocess.run(
                ["python3", str(cli_script), "apply", project_dir.name, "--force"],
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
