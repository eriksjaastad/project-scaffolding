import os
import sys
import argparse
import subprocess
from pathlib import Path

def get_projects_root():
    return Path(os.environ.get("PROJECTS_ROOT", Path.home() / "projects"))

def get_scaffolding_root():
    return Path(os.environ.get("SCAFFOLDING", Path.home() / "projects" / "project-scaffolding"))

def main():
    parser = argparse.ArgumentParser(description="One-time migration to sync all project agent configs")
    parser.add_argument("--apply", action="store_true", help="Actually apply the changes")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Show what would change (default)")
    
    args = parser.parse_args()
    
    if args.apply:
        args.dry_run = False

    projects_root = get_projects_root()
    scaffolding_root = get_scaffolding_root()
    sync_script = scaffolding_root / "scripts" / "sync_agent_configs.py"
    
    print(f"=== Agent Config Migration ({'APPLY' if args.apply else 'DRY-RUN'}) ===\n")
    
    for item in projects_root.iterdir():
        if item.is_dir() and not item.name.startswith(".") and item.name not in ["ai-journal", "writing"]:
            agents_md = item / "AGENTS.md"
            if agents_md.exists():
                if args.dry_run:
                    print(f"🔍 Would sync {item.name}")
                else:
                    try:
                        subprocess.check_call([sys.executable, str(sync_script), item.name])
                    except subprocess.CalledProcessError:
                        print(f"❌ Failed to sync {item.name}")
    
    if args.dry_run:
        print("\nTo apply these changes, run with --apply")

if __name__ == "__main__":
    main()
