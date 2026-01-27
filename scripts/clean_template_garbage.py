#!/usr/bin/env python3
"""
Clean template garbage from files that have both real content and appended template sections.

Handles both old and new marker formats:
- OLD: <!-- project-scaffolding template appended -->
- NEW: <!-- SCAFFOLD:START --> ... <!-- SCAFFOLD:END -->
"""
import os
from pathlib import Path
from scaffold.constants import PROTECTED_PROJECTS

# Markers (old and new)
OLD_MARKER = "<!-- project-scaffolding template appended -->"
NEW_START = "<!-- SCAFFOLD:START - Do not edit between markers -->"
NEW_END = "<!-- SCAFFOLD:END - Custom content below is preserved -->"

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def clean_file_old_marker(content: str) -> tuple[str, bool]:
    """Remove old marker and everything after it. Returns (clean_content, was_cleaned)."""
    if OLD_MARKER in content:
        parts = content.split(OLD_MARKER)
        return parts[0].strip(), True
    return content, False

def clean_file_new_markers(content: str) -> tuple[str, bool]:
    """Remove content between NEW markers, keep content outside. Returns (clean_content, was_cleaned)."""
    if NEW_START in content and NEW_END in content:
        start_idx = content.find(NEW_START)
        end_idx = content.find(NEW_END) + len(NEW_END)

        before = content[:start_idx].rstrip()
        after = content[end_idx:].lstrip('\n')

        # Keep content outside markers
        if before or after:
            clean = before + ("\n\n" if before and after else "") + after
            return clean.strip(), True
    return content, False

def clean_projects() -> None:
    projects_root = get_projects_root()

    print(f"Starting cleanup in {projects_root}...\n")

    cleaned_old = 0
    cleaned_new = 0

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

                    # Try old marker first
                    clean_content, was_cleaned = clean_file_old_marker(content)
                    if was_cleaned and clean_content:
                        print(f"✨ Cleaning (old marker) {file_path.relative_to(projects_root)}")
                        file_path.write_text(clean_content + "\n")
                        cleaned_old += 1
                        continue

                    # Try new markers
                    clean_content, was_cleaned = clean_file_new_markers(content)
                    if was_cleaned and clean_content:
                        print(f"✨ Cleaning (new markers) {file_path.relative_to(projects_root)}")
                        file_path.write_text(clean_content + "\n")
                        cleaned_new += 1

                except Exception as e:
                    print(f"❌ Error cleaning {file_path}: {e}")

    print(f"\nCleanup complete. Cleaned {cleaned_old} files (old marker), {cleaned_new} files (new markers).")

if __name__ == "__main__":
    clean_projects()
