#!/usr/bin/env python3
import os
from pathlib import Path
import shutil

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def cleanup_backups() -> None:
    projects_root = get_projects_root()
    trash_dir = projects_root / ".trash"
    trash_dir.mkdir(exist_ok=True)
    
    print(f"Cleaning up .backup files in {projects_root}...\n")
    
    count = 0
    for root, dirs, files in os.walk(projects_root):
        # Skip the trash itself and hidden dirs
        if ".trash" in root or "/." in root:
            continue
            
        for file in files:
            if file.endswith(".backup"):
                file_path = Path(root) / file
                # Create a unique name in trash to avoid collisions
                rel_path_str = str(file_path.relative_to(projects_root)).replace("/", "_")
                target_path = trash_dir / rel_path_str
                
                print(f"🗑️  Moving to trash: {file_path.relative_to(projects_root)}")
                shutil.move(str(file_path), str(target_path))
                count += 1
                
    print(f"\nCleanup complete. Moved {count} files to .trash/")

if __name__ == "__main__":
    cleanup_backups()
