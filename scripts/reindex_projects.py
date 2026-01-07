#!/usr/bin/env python3
"""
Re-index projects by creating or updating index files.

Usage:
    ./scripts/reindex_projects.py                     # Interactive mode
    ./scripts/reindex_projects.py --missing           # Create missing indexes only
    ./scripts/reindex_projects.py --stale             # Update stale indexes (>6 months)
    ./scripts/reindex_projects.py --all               # Recreate all indexes
    ./scripts/reindex_projects.py [project_name]      # Re-index specific project

This script:
- Scans project structure to detect key components
- Determines primary technology from file extensions
- Calculates status based on last modification (>6 months = archived)
- Generates index file using template structure
"""

import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import Counter
import subprocess
import logging

# Configuration
SCAFFOLDING_ROOT = Path(__file__).parent.parent
PROJECTS_ROOT = Path(os.getenv("PROJECTS_ROOT", Path.home() / "projects"))
TEMPLATE_PATH = SCAFFOLDING_ROOT / "templates" / "00_Index_Template.md"
SKIP_DIRS = {"__Knowledge", "_collaboration", "_inbox", "_obsidian", "_tools"}
ARCHIVE_THRESHOLD_DAYS = 180  # 6 months

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Technology detection
TECH_EXTENSIONS = {
    ".py": "python",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".go": "go",
    ".rs": "rust",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
}


def find_projects(root: Path) -> List[Path]:
    """Find all project directories."""
    projects = []
    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            if item.name in SKIP_DIRS:
                continue
            projects.append(item)
    return sorted(projects)


def get_last_modified(project_path: Path) -> datetime:
    """Get most recent file modification in project (excluding .git)."""
    try:
        # Use git if available (more accurate)
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        if result.stdout.strip():
            timestamp = int(result.stdout.strip())
            return datetime.fromtimestamp(timestamp)
    except FileNotFoundError:
        logger.debug(f"Git not found or not a repo: {project_path}")
    except subprocess.CalledProcessError as e:
        logger.warning(f"Git log failed for {project_path}: {e}")
    except subprocess.TimeoutExpired:
        logger.warning(f"Git log timed out for {project_path}")
    except ValueError as e:
        logger.error(f"Invalid git timestamp for {project_path}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in get_last_modified: {e}")
    
    # Fallback: scan filesystem
    latest = datetime.fromtimestamp(0)
    for file in project_path.rglob("*"):
        if file.is_file() and not any(part.startswith(".") for part in file.parts):
            mtime = datetime.fromtimestamp(file.stat().st_mtime)
            if mtime > latest:
                latest = mtime
    
    return latest


def detect_primary_tech(project_path: Path) -> str:
    """Detect primary technology based on file extensions."""
    extensions = Counter()
    
    for file in project_path.rglob("*"):
        if file.is_file() and not any(part.startswith(".") for part in file.parts):
            ext = file.suffix.lower()
            if ext in TECH_EXTENSIONS:
                extensions[ext] += 1
    
    if not extensions:
        return "unknown"
    
    # Most common extension
    most_common_ext = extensions.most_common(1)[0][0]
    return TECH_EXTENSIONS[most_common_ext]


def detect_status(project_path: Path) -> str:
    """Detect project status based on activity."""
    last_modified = get_last_modified(project_path)
    age_days = (datetime.now() - last_modified).days
    
    if age_days > ARCHIVE_THRESHOLD_DAYS:
        return "archived"
    else:
        return "active"


def scan_components(project_path: Path) -> List[Tuple[str, int]]:
    """Scan major directories and count files."""
    components = []
    
    for item in project_path.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Count files (not recursive for top-level overview)
            file_count = sum(1 for _ in item.iterdir() if _.is_file())
            if file_count > 0 or any(item.iterdir()):  # Has files or subdirs
                components.append((item.name, file_count))
    
    return sorted(components, key=lambda x: x[1], reverse=True)[:6]  # Top 6


def generate_index_content(project_path: Path, template_content: str) -> str:
    """Generate index file content for project."""
    project_name = project_path.name
    
    # Detect attributes
    primary_tech = detect_primary_tech(project_path)
    status = detect_status(project_path)
    components = scan_components(project_path)
    last_modified = get_last_modified(project_path)
    
    # Replace template placeholders
    content = template_content
    content = content.replace("[PROJECT_NAME]", project_name)
    content = content.replace("p/[project-name]", f"p/{project_name.lower().replace(' ', '-')}")
    content = content.replace("tech/[primary-tech]", f"tech/{primary_tech}")
    content = content.replace("status/[active|archived|production]", f"status/{status}")
    content = content.replace("created: YYYY-MM-DD", f"created: {datetime.now().strftime('%Y-%m-%d')}")
    
    # Generate component list
    component_lines = []
    for dir_name, file_count in components:
        component_lines.append(f"- `{dir_name}/` - ({file_count} files)")
    
    if component_lines:
        components_text = "\n".join(component_lines)
    else:
        components_text = "- No major components detected yet"
    
    # Replace component placeholder (if exists in template)
    if "[COMPONENTS]" in content:
        content = content.replace("[COMPONENTS]", components_text)
    
    # Update status line
    status_line = f"**Status:** #status/{status}"
    if "**Status:**" in content:
        # Find and replace status line
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("**Status:**"):
                lines[i] = status_line
                break
        content = "\n".join(lines)
    
    # Update last modified
    last_update = last_modified.strftime("%B %Y")
    if "**Last Major Update:**" in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("**Last Major Update:**"):
                lines[i] = f"**Last Major Update:** {last_update}"
                break
        content = "\n".join(lines)
    
    return content


def create_index(project_path: Path, force: bool = False) -> bool:
    """Create index file for project."""
    project_name = project_path.name
    index_path = project_path / f"00_Index_{project_name.replace(' ', '')}.md"
    
    # Check if exists
    if index_path.exists() and not force:
        print(f"  ⏩ Index already exists: {index_path.name}")
        return False
    
    # Load template
    if not TEMPLATE_PATH.exists():
        logger.error(f"Template not found: {TEMPLATE_PATH}")
        return False
    
    try:
        template_content = TEMPLATE_PATH.read_text()
        content = generate_index_content(project_path, template_content)
    except Exception as e:
        logger.error(f"Failed to generate index content for {project_name}: {e}")
        return False
    
    # Atomic write
    temp_file = None
    try:
        # Create temp file in same directory as target
        fd, temp_path = tempfile.mkstemp(dir=project_path, suffix=".tmp")
        temp_file = Path(temp_path)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        
        # Atomic rename
        os.replace(temp_path, index_path)
        print(f"  ✅ Created: {index_path.name}")
        return True
    except Exception as e:
        logger.error(f"Failed to write index atomically for {project_name}: {e}")
        if temp_file and temp_file.exists():
            try:
                temp_file.unlink()
            except Exception:
                pass
        return False


def main() -> None:
    """Main re-indexing logic."""
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h"]:
        print("Re-index Projects")
        print("\nUsage:")
        print("  ./scripts/reindex_projects.py --missing      # Create missing indexes")
        print("  ./scripts/reindex_projects.py --stale        # Update stale indexes")
        print("  ./scripts/reindex_projects.py --all          # Recreate all")
        print("  ./scripts/reindex_projects.py [project]      # Specific project")
        sys.exit(0 if len(sys.argv) > 1 else 1)
    
    arg = sys.argv[1]
    
    if arg == "--missing":
        print("Creating missing index files...\n")
        projects = find_projects(PROJECTS_ROOT)
        
        created = 0
        for project in projects:
            # Check if has index
            has_index = any(project.glob("00_Index_*.md"))
            if not has_index:
                print(f"{project.name}:")
                if create_index(project):
                    created += 1
                print()
        
        print(f"{'='*60}")
        print(f"Created {created} new index files")
        sys.exit(0)
    
    elif arg == "--stale":
        print("Updating stale index files (>6 months)...\n")
        projects = find_projects(PROJECTS_ROOT)
        
        updated = 0
        for project in projects:
            # Find index file
            index_files = list(project.glob("00_Index_*.md"))
            if not index_files:
                continue
            
            index_path = index_files[0]
            index_age = (datetime.now() - datetime.fromtimestamp(index_path.stat().st_mtime)).days
            
            if index_age > 180:  # 6 months
                print(f"{project.name} (index is {index_age} days old):")
                if create_index(project, force=True):
                    updated += 1
                print()
        
        print(f"{'='*60}")
        print(f"Updated {updated} stale index files")
        sys.exit(0)
    
    elif arg == "--all":
        print("⚠️  Recreating ALL index files...\n")
        response = input("This will overwrite existing indexes. Continue? (yes/no): ")
        if response.lower() != "yes":
            print("Aborted.")
            sys.exit(0)
        
        projects = find_projects(PROJECTS_ROOT)
        
        created = 0
        for project in projects:
            print(f"{project.name}:")
            if create_index(project, force=True):
                created += 1
            print()
        
        print(f"{'='*60}")
        print(f"Recreated {created} index files")
        sys.exit(0)
    
    else:
        # Specific project
        project_name = arg
        project_path = PROJECTS_ROOT / project_name
        
        if not project_path.exists():
            print(f"❌ Project not found: {project_name}")
            sys.exit(1)
        
        print(f"Re-indexing: {project_name}\n")
        
        if create_index(project_path, force=True):
            print(f"\n✅ Index updated for {project_name}")
        else:
            print(f"\n❌ Failed to update index for {project_name}")
            sys.exit(1)


if __name__ == "__main__":
    main()

