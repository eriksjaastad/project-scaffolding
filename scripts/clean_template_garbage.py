#!/usr/bin/env python3
"""
Clean template garbage from files that have both real content and appended template sections.
"""
import os
from pathlib import Path
from scaffold.constants import PROTECTED_PROJECTS

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def clean_projects() -> None:
    projects_root = get_projects_root()
    marker = "<!-- project-scaffolding template appended -->"
    
    print(f"Starting cleanup in {projects_root}...\n")
    
    cleaned_count = 0
    
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
            
        if project_dir.name in PROTECTED_PROJECTS:
            continue
            
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if not file.endswith(".md"):
                    continue
                    
                file_path = Path(root) / file
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    if marker in content:
                        # Split by marker and keep only the part before it
                        parts = content.split(marker)
                        clean_content = parts[0].strip()
                        
                        if clean_content:
                            print(f"✨ Cleaning {file_path.relative_to(projects_root)}")
                            file_path.write_text(clean_content + "\n")
                            cleaned_count += 1
                        else:
                            # If file ONLY has template garbage (no content before marker), 
                            # we might want to keep it but it will be fixed by future scaffolding.
                            # For now, we only strip if there's real content to preserve.
                            pass
                except Exception as e:
                    print(f"❌ Error cleaning {file_path}: {e}")
                    
    print(f"\nCleanup complete. Cleaned {cleaned_count} files.")

if __name__ == "__main__":
    clean_projects()
