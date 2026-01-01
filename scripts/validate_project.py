#!/usr/bin/env python3
"""
Validate project structure and requirements.

Usage:
    ./scripts/validate_project.py [project_name]      # Check specific project
    ./scripts/validate_project.py --all               # Check all projects
    ./scripts/validate_project.py --missing           # List projects without indexes

This script enforces:
- Critical Rule #0: Every project must have an index file
- Index file naming: 00_Index_[ProjectName].md
- Index file location: project root
- Index file structure: Valid YAML frontmatter + required sections
"""

import sys
from pathlib import Path
from typing import List, Tuple
import re

# Configuration
PROJECTS_ROOT = Path("/Users/eriksjaastad/projects")
REQUIRED_INDEX_PATTERN = r"00_Index_.+\.md"
SKIP_DIRS = {"__Knowledge", "_collaboration", "_inbox", "_obsidian", "_tools"}

# YAML frontmatter requirements
REQUIRED_TAGS = ["map/project", "p/"]  # p/ is a prefix that must exist
REQUIRED_SECTIONS = ["# ", "## Key Components", "## Status"]


class ValidationError(Exception):
    """Raised when project fails validation."""
    pass


def find_projects(root: Path) -> List[Path]:
    """Find all project directories (top-level folders)."""
    projects = []
    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            # Skip special directories
            if item.name in SKIP_DIRS:
                continue
            projects.append(item)
    return sorted(projects)


def has_index_file(project_path: Path) -> Tuple[bool, Path | None]:
    """Check if project has index file matching pattern."""
    for file in project_path.glob("00_Index_*.md"):
        return True, file
    return False, None


def validate_index_content(index_path: Path) -> List[str]:
    """Validate index file content. Returns list of errors."""
    errors = []
    content = index_path.read_text()
    
    # Check for YAML frontmatter
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter (must start with '---')")
        return errors  # Can't continue without frontmatter
    
    # Extract frontmatter
    try:
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append("Invalid YAML frontmatter (must have closing '---')")
            return errors
        
        frontmatter = parts[1]
        body = parts[2]
    except Exception as e:
        errors.append(f"Failed to parse frontmatter: {e}")
        return errors
    
    # Check required tags
    for required_tag in REQUIRED_TAGS:
        if required_tag not in frontmatter:
            errors.append(f"Missing required tag: {required_tag}")
    
    # Check required sections
    for required_section in REQUIRED_SECTIONS:
        if required_section not in body:
            errors.append(f"Missing required section: {required_section}")
    
    # Check for 3-sentence summary (heuristic: body should have substance before first ##)
    if "## Key Components" in body:
        summary_section = body.split("## Key Components")[0]
        # Should have H1 title and some content
        if summary_section.count("\n") < 5:
            errors.append("Summary section appears too short (need 3-sentence description)")
    
    return errors


def validate_project(project_path: Path, verbose: bool = True) -> bool:
    """
    Validate a single project.
    
    Returns:
        True if valid, False otherwise
    """
    project_name = project_path.name
    
    # Check for index file
    has_index, index_path = has_index_file(project_path)
    
    if not has_index:
        if verbose:
            print(f"❌ {project_name}")
            print(f"   ERROR: Missing index file (00_Index_*.md)")
            print(f"   Create one: cp templates/00_Index_Template.md \"{project_path}/00_Index_{project_name}.md\"")
        return False
    
    # Validate index content
    errors = validate_index_content(index_path)
    
    if errors:
        if verbose:
            print(f"⚠️  {project_name}")
            print(f"   Index exists: {index_path.name}")
            for error in errors:
                print(f"   - {error}")
        return False
    
    # All good!
    if verbose:
        print(f"✅ {project_name}")
        print(f"   Index: {index_path.name}")
    return True


def main():
    """Main validation logic."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./scripts/validate_project.py [project_name]  # Check specific project")
        print("  ./scripts/validate_project.py --all           # Check all projects")
        print("  ./scripts/validate_project.py --missing       # List missing indexes")
        sys.exit(1)
    
    arg = sys.argv[1]
    
    if arg == "--all":
        # Validate all projects
        print("Validating all projects...\n")
        projects = find_projects(PROJECTS_ROOT)
        
        valid_count = 0
        invalid_count = 0
        
        for project in projects:
            is_valid = validate_project(project, verbose=True)
            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
            print()  # Blank line between projects
        
        # Summary
        total = valid_count + invalid_count
        print(f"{'='*60}")
        print(f"Summary: {valid_count}/{total} projects valid ({invalid_count} need attention)")
        
        if invalid_count > 0:
            print(f"\n⚠️  {invalid_count} projects need index files or fixes")
            print("Run with --missing to see which projects need indexes")
            sys.exit(1)
        else:
            print("\n✅ All projects have valid index files!")
            sys.exit(0)
    
    elif arg == "--missing":
        # List projects without indexes
        print("Projects missing index files:\n")
        projects = find_projects(PROJECTS_ROOT)
        
        missing = []
        for project in projects:
            has_index, _ = has_index_file(project)
            if not has_index:
                missing.append(project.name)
        
        if missing:
            for name in missing:
                print(f"  - {name}")
            
            print(f"\n{len(missing)} projects need index files")
            print("\nTo create indexes:")
            print("  ./scripts/reindex_projects.py --missing")
        else:
            print("✅ All projects have index files!")
        
        sys.exit(len(missing))  # Exit code = number of missing
    
    else:
        # Validate specific project
        project_name = arg
        project_path = PROJECTS_ROOT / project_name
        
        if not project_path.exists():
            print(f"❌ Project not found: {project_name}")
            print(f"   Expected: {project_path}")
            sys.exit(1)
        
        if not project_path.is_dir():
            print(f"❌ Not a directory: {project_name}")
            sys.exit(1)
        
        print(f"Validating: {project_name}\n")
        is_valid = validate_project(project_path, verbose=True)
        
        if not is_valid:
            print(f"\n❌ Validation failed for {project_name}")
            sys.exit(1)
        else:
            print(f"\n✅ {project_name} is valid!")
            sys.exit(0)


if __name__ == "__main__":
    main()

