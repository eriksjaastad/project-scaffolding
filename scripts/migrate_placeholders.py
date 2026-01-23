#!/usr/bin/env python3
import os
import re
from pathlib import Path

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def migrate_placeholders() -> None:
    projects_root = get_projects_root()
    # Pattern for {var} where var is lowercase letters and underscores
    pattern = re.compile(r"\{([a-z0-9_]+)\}")
    
    files_to_migrate = {"CLAUDE.md", "AGENTS.md", "TODO.md", "README.md", ".cursorrules"}
    
    print(f"Migrating placeholders in {projects_root}...\n")
    
    migrated_count = 0
    
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
            
        for filename in files_to_migrate:
            file_path = project_dir / filename
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    def replace(match):
                        var_name = match.group(1).upper()
                        return f"{{{{{var_name}}}}}"
                    
                    new_content = pattern.sub(replace, content)
                    
                    if new_content != content:
                        print(f"🔄 Migrated {file_path.relative_to(projects_root)}")
                        file_path.write_text(new_content)
                        migrated_count += 1
                except Exception as e:
                    print(f"❌ Error migrating {file_path}: {e}")
                    
    print(f"\nMigration complete. Migrated {migrated_count} files.")

if __name__ == "__main__":
    migrate_placeholders()
