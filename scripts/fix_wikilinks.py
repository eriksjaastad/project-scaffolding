#!/usr/bin/env python3
"""
Convert Obsidian wikilinks to standard markdown links across all projects.

This script fixes the pervasive wikilink issue caused by early Obsidian usage.
Wikilinks ([[document]]) only work in Obsidian; standard markdown links work everywhere.

Usage:
    # Dry run on single project
    python scripts/fix_wikilinks.py --project muffinpanrecipes --dry-run
    
    # Fix single project
    python scripts/fix_wikilinks.py --project muffinpanrecipes
    
    # Fix all projects
    python scripts/fix_wikilinks.py --all
    
    # Custom projects root
    python scripts/fix_wikilinks.py --all --projects-root /path/to/projects
"""

import argparse
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple
import sys

# Wikilink → Markdown Link conversion mapping
UNIVERSAL_REPLACEMENTS = [
    # Universal documents that exist in scaffolded projects
    (r'\[\[CODE_REVIEW_ANTI_PATTERNS\]\]', '[Code Review Anti-Patterns](Documents/reference/CODE_REVIEW_ANTI_PATTERNS.md)'),
    (r'\[\[DOPPLER_SECRETS_MANAGEMENT\]\]', '[Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md)'),
    (r'\[\[LOCAL_MODEL_LEARNINGS\]\]', '[Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md)'),
    (r'\[\[trustworthy_ai_report\]\]', '[Trustworthy AI Report](Documents/reports/trustworthy_ai_report.md)'),
    
    # Pattern mappings (actual file names)
    (r'\[\[ai_model_comparison\]\]', '[AI Model Cost Comparison](Documents/reference/MODEL_COST_COMPARISON.md)'),
    (r'\[\[cost_management\]\]', '[Cost Management](Documents/reference/MODEL_COST_COMPARISON.md)'),
    (r'\[\[orchestration_patterns\]\]', '[AI Team Orchestration](patterns/ai-team-orchestration.md)'),
    (r'\[\[security_patterns\]\]', '[Safety Systems](patterns/safety-systems.md)'),
    (r'\[\[prompt_engineering_guide\]\]', '[Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md)'),
    (r'\[\[automation_patterns\]\]', '[Automation Reliability](patterns/automation-reliability.md)'),
    (r'\[\[discord_integration\]\]', '[Discord Webhooks Per Project](patterns/discord-webhooks-per-project.md)'),
    
    # Cross-project references (relative to projects root)
    (r'\[\[agent-skills-library/README\]\]', '[Agent Skills Library](../agent-skills-library/README.md)'),
    (r'\[\[project-scaffolding/README\]\]', '[Project Scaffolding](../project-scaffolding/README.md)'),
    
    # Projects root references (when in project, link up to root)
    (r'\[\[Project-workflow\]\]', '[Project Workflow](../Project-workflow.md)'),
    (r'\[\[AGENT_QUICK_REFERENCE\]\]', '[Agent Quick Reference](../AGENT_QUICK_REFERENCE.md)'),
    (r'\[\[TODO\]\]', '[Root TODO](../TODO.md)'),
    (r'\[\[AGENTS\.md\]\]', '[AGENTS.md](AGENTS.md)'),
    (r'\[\[CLAUDE\.md\]\]', '[CLAUDE.md](CLAUDE.md)'),
    (r'\[\[README\.md\]\]', '[README.md](README.md)'),
    
    # Project-level documents (generic patterns)
    (r'\[\[ARCHITECTURAL_DECISIONS\]\]', '[Architectural Decisions](Documents/ARCHITECTURAL_DECISIONS.md)'),
    (r'\[\[RECIPE_SCHEMA\]\]', '[Recipe Schema](Documents/RECIPE_SCHEMA.md)'),
    (r'\[\[IMAGE_STYLE_GUIDE\]\]', '[Image Style Guide](Documents/IMAGE_STYLE_GUIDE.md)'),
    
    # Index file references - convert to plain text (can't predict project name)
    (r'\[\[00_Index_[^\]]+\]\]', '`00_Index_*.md`'),
]

# Wikilinks to REMOVE (documents that don't exist universally)
REMOVE_PATTERNS = [
    r'- \[\[architecture_patterns\]\] - architecture\n',
    r'- \[\[queue_processing_guide\]\] - queue/workflow\n',
    r'- \[\[session_documentation\]\] - session notes\n',
    r'- \[\[testing_strategy\]\] - testing/QA\n',
    r'- \[\[dashboard_architecture\]\] - dashboard/UI\n',
    r'- \[\[case_studies\]\] - examples\n',
    r'- \[\[database_schema\]\] - database design\n',
    r'- \[\[database_setup\]\] - database\n',
    r'- \[\[error_handling_patterns\]\] - error handling\n',
    r'- \[\[trading_backtesting_guide\]\] - backtesting\n',
    r'- \[\[deployment_patterns\]\] - deployment\n',
    r'- \[\[performance_optimization\]\] - performance\n',
    r'- \[\[project_planning\]\] - planning/roadmap\n',
    r'- \[\[threejs_visualization\]\] - 3D visualization\n',
    r'- \[\[hypocrisy_methodology\]\] - bias detection\n',
    r'- \[\[cloud_gpu_setup\]\] - cloud GPU\n',
    r'- \[\[recipe_system\]\] - recipe generation\n',
]


def find_markdown_files(project_root: Path) -> List[Path]:
    """Find all markdown files in project, excluding node_modules and venv."""
    md_files = []
    for pattern in ['**/*.md', '**/*.MD']:
        for f in project_root.glob(pattern):
            # Skip common non-documentation directories
            if any(part in f.parts for part in ['node_modules', 'venv', '.venv', '__pycache__', '.git']):
                continue
            md_files.append(f)
    return md_files


def count_wikilinks(content: str) -> int:
    """Count wikilinks in content."""
    return len(re.findall(r'\[\[.*?\]\]', content))


def fix_wikilinks_in_content(content: str, project_name: str) -> Tuple[str, int]:
    """
    Replace wikilinks with markdown links.
    Returns (fixed_content, changes_made).
    """
    original = content
    changes = 0
    
    # First, remove non-existent document references
    for pattern in REMOVE_PATTERNS:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content)
            changes += 1
    
    # Then apply replacements
    for wikilink_pattern, markdown_link in UNIVERSAL_REPLACEMENTS:
        if re.search(wikilink_pattern, content):
            content = re.sub(wikilink_pattern, markdown_link, content)
            changes += 1
    
    # Project-specific index file patterns
    # [[muffinpanrecipes/README]] → [README.md](README.md)
    content = re.sub(
        rf'\[\[{re.escape(project_name)}/([^\]]+)\]\]',
        r'[\1](\1)',
        content
    )
    
    # Remaining generic wikilinks in tables or lists (best effort)
    # [[some-file.md]] → [some-file.md](some-file.md)
    content = re.sub(
        r'\[\[([^/\]]+\.md)\]\]',
        r'[\1](\1)',
        content
    )
    
    if content != original:
        changes = 1
        
    return content, changes


def fix_project(project_root: Path, dry_run: bool = False) -> Dict[str, int]:
    """Fix all markdown files in a project. Returns stats."""
    stats = {
        'files_scanned': 0,
        'files_changed': 0,
        'wikilinks_before': 0,
        'wikilinks_after': 0,
        'changes_made': 0,
    }
    
    project_name = project_root.name
    md_files = find_markdown_files(project_root)
    stats['files_scanned'] = len(md_files)
    
    print(f"\n📁 Processing: {project_name}")
    print(f"   Found {len(md_files)} markdown files")
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"   ⚠️  Error reading {md_file}: {e}")
            continue
        
        wikilinks_before = count_wikilinks(content)
        stats['wikilinks_before'] += wikilinks_before
        
        if wikilinks_before == 0:
            continue
        
        fixed_content, changes = fix_wikilinks_in_content(content, project_name)
        wikilinks_after = count_wikilinks(fixed_content)
        stats['wikilinks_after'] += wikilinks_after
        
        if changes > 0:
            stats['files_changed'] += 1
            stats['changes_made'] += changes
            rel_path = md_file.relative_to(project_root)
            
            if dry_run:
                print(f"   🔍 Would fix: {rel_path} ({wikilinks_before} → {wikilinks_after} wikilinks)")
            else:
                md_file.write_text(fixed_content, encoding='utf-8')
                print(f"   ✅ Fixed: {rel_path} ({wikilinks_before} → {wikilinks_after} wikilinks)")
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Convert Obsidian wikilinks to standard markdown links',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--project', help='Project name to fix (e.g., muffinpanrecipes)')
    parser.add_argument('--all', action='store_true', help='Fix all projects in projects root')
    parser.add_argument('--projects-root', 
                       default=os.getenv('PROJECTS_ROOT', os.path.expanduser('~/projects')),
                       help='Path to projects root (default: $PROJECTS_ROOT or ~/projects)')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be changed without modifying files')
    
    args = parser.parse_args()
    
    if not args.project and not args.all:
        parser.error('Must specify --project NAME or --all')
    
    projects_root = Path(args.projects_root)
    if not projects_root.exists():
        print(f"❌ Projects root not found: {projects_root}")
        sys.exit(1)
    
    # Determine which projects to process
    if args.project:
        project_dirs = [projects_root / args.project]
        if not project_dirs[0].exists():
            print(f"❌ Project not found: {args.project}")
            sys.exit(1)
    else:
        # Process all directories that look like projects (have .git or README.md)
        project_dirs = [
            d for d in projects_root.iterdir()
            if d.is_dir() 
            and not d.name.startswith('.')
            and not d.name.startswith('_')
            and (d / '.git').exists()  # Has git repo
        ]
    
    print(f"{'🔍 DRY RUN MODE' if args.dry_run else '🔧 FIX MODE'}")
    print(f"Projects root: {projects_root}")
    print(f"Projects to process: {len(project_dirs)}")
    
    total_stats = {
        'files_scanned': 0,
        'files_changed': 0,
        'wikilinks_before': 0,
        'wikilinks_after': 0,
        'changes_made': 0,
    }
    
    for project_dir in sorted(project_dirs):
        stats = fix_project(project_dir, dry_run=args.dry_run)
        for key in total_stats:
            total_stats[key] += stats[key]
    
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    print(f"Files scanned:    {total_stats['files_scanned']}")
    print(f"Files changed:    {total_stats['files_changed']}")
    print(f"Wikilinks before: {total_stats['wikilinks_before']}")
    print(f"Wikilinks after:  {total_stats['wikilinks_after']}")
    print(f"Wikilinks fixed:  {total_stats['wikilinks_before'] - total_stats['wikilinks_after']}")
    print(f"Changes made:     {total_stats['changes_made']}")
    
    if args.dry_run:
        print("\n💡 This was a dry run. Run without --dry-run to apply changes.")


if __name__ == '__main__':
    main()
