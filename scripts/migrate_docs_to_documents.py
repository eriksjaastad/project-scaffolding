#!/usr/bin/env python3
"""
Migrate all 'docs/' references to 'Documents/' throughout the codebase.

This script was created during the January 2026 cleanup to fix outdated
references after the docs/ → Documents/ directory rename.

Usage:
    python scripts/migrate_docs_to_documents.py --dry-run   # Preview changes
    python scripts/migrate_docs_to_documents.py             # Apply changes
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def find_markdown_files(root: Path) -> List[Path]:
    """Find all markdown files in the project."""
    exclude_dirs = {'.git', 'venv', 'node_modules', '__pycache__', '.pytest_cache', '.mypy_cache'}

    markdown_files = []
    for md_file in root.rglob('*.md'):
        # Check if any parent directory is excluded
        if any(part in exclude_dirs for part in md_file.parts):
            continue
        markdown_files.append(md_file)

    return sorted(markdown_files)


def find_docs_references(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Find lines with 'docs/' references and their proposed replacements.

    Returns:
        List of (line_number, original_line, proposed_line) tuples
    """
    changes = []

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        for line_num, line in enumerate(lines, start=1):
            # Look for 'docs/' pattern (case-sensitive)
            if 'docs/' in line:
                # Replace docs/ with Documents/
                new_line = line.replace('docs/', 'Documents/')
                changes.append((line_num, line, new_line))

    except Exception as e:
        logger.warning(f"Could not read {file_path}: {e}")

    return changes


def apply_changes(file_path: Path, dry_run: bool = True) -> int:
    """
    Apply docs/ → Documents/ changes to a file.

    Returns:
        Number of changes made
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        original_content = content

        # Simple replacement
        new_content = content.replace('docs/', 'Documents/')

        if new_content == original_content:
            return 0

        changes_count = original_content.count('docs/')

        if not dry_run:
            # Write the file with changes
            file_path.write_text(new_content, encoding='utf-8')
            logger.info(f"✓ Updated: {file_path} ({changes_count} changes)")
        else:
            logger.info(f"[DRY RUN] Would update: {file_path} ({changes_count} changes)")

        return changes_count

    except Exception as e:
        logger.error(f"Failed to update {file_path}: {e}")
        return 0


def main() -> None:
    """Main migration logic."""
    parser = argparse.ArgumentParser(description="Migrate docs/ references to Documents/")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root directory to scan (default: current directory)"
    )
    args = parser.parse_args()

    root = args.root.resolve()

    logger.info(f"Scanning for 'docs/' references in: {root}")
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be modified")

    # Find all markdown files
    markdown_files = find_markdown_files(root)
    logger.info(f"Found {len(markdown_files)} markdown files to scan")

    # Track statistics
    files_with_changes = 0
    total_changes = 0

    # Process each file
    for md_file in markdown_files:
        changes = find_docs_references(md_file)

        if changes:
            files_with_changes += 1

            if args.dry_run:
                # Show preview of changes
                rel_path = md_file.relative_to(root)
                logger.info(f"\n{rel_path}:")
                for line_num, old_line, new_line in changes[:3]:  # Show first 3 changes
                    logger.info(f"  Line {line_num}:")
                    logger.info(f"    - {old_line.strip()}")
                    logger.info(f"    + {new_line.strip()}")
                if len(changes) > 3:
                    logger.info(f"  ... and {len(changes) - 3} more changes")

            # Apply changes (or dry-run)
            changes_made = apply_changes(md_file, dry_run=args.dry_run)
            total_changes += changes_made

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info(f"Summary:")
    logger.info(f"  Files scanned: {len(markdown_files)}")
    logger.info(f"  Files with changes: {files_with_changes}")
    logger.info(f"  Total replacements: {total_changes}")

    if args.dry_run:
        logger.info("\nTo apply these changes, run without --dry-run:")
        logger.info("  python scripts/migrate_docs_to_documents.py")
    else:
        logger.info("\n✅ Migration complete!")

    sys.exit(0)


if __name__ == "__main__":
    main()
