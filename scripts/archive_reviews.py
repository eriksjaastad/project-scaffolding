import pathlib
import re
import shutil
import argparse
import logging
import sys
from typing import List, Optional, Tuple
from send2trash import send2trash

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def find_project_root(file_path: pathlib.Path, max_depth: int = 10) -> Optional[pathlib.Path]:
    """
    Finds the nearest parent directory containing '00_Index_*.md'.
    This ensures Project Autonomy by defining clear boundaries.

    Security: Validates found index is legitimate (not in templates/archives).
    Prevents path traversal and malicious index filenames.
    """
    excluded_dirs = {'templates', 'archives', 'venv', '.git', 'node_modules'}

    current_path = file_path.resolve()
    if current_path.is_file():
        current_path = current_path.parent

    for _ in range(max_depth):
        # Search for '00_Index_*.md' in the current directory
        index_files = list(current_path.glob('00_Index_*.md'))

        if index_files:
            # Security: Validate index is not in excluded directories
            index_path = index_files[0]

            # Check if current path contains any excluded directory
            if any(excluded in current_path.parts for excluded in excluded_dirs):
                logger.debug(f"Skipping index in excluded dir: {current_path}")
                # Continue searching upward instead of returning
                parent_path = current_path.parent
                if parent_path == current_path:
                    break
                current_path = parent_path
                continue

            # Security: Validate index filename doesn't contain path traversal
            if '..' in index_path.name or '/' in index_path.name or '\\' in index_path.name:
                logger.error(f"Security: Suspicious index filename: {index_path.name}")
                return None

            # Security: Warn if multiple indexes found (ambiguous)
            if len(index_files) > 1:
                logger.warning(f"Multiple index files in {current_path}: {[f.name for f in index_files]}")
                logger.warning(f"Using first match: {index_files[0].name}")

            return current_path

        # Move up to the parent directory
        parent_path = current_path.parent
        if parent_path == current_path:
            break  # Reached root

        current_path = parent_path

    return None

def find_review_files(root_dir: pathlib.Path) -> List[pathlib.Path]:
    """
    Recursively finds review-related markdown files within the given root directory,
    excluding specified directories and Python scripts.
    """
    excluded_dirs = {'data', 'venv', 'node_modules', '.git', '__pycache__'}
    # Regex to match 'REVIEW.md', 'CODE_REVIEW_*.md', or '*review*.md' (case-insensitive)
    review_pattern = re.compile(r'^(?:REVIEW\.md|CODE_REVIEW_.*\.md|.*review.*\.md)$', re.IGNORECASE)
    
    review_files: List[pathlib.Path] = []
    
    for file_path in root_dir.rglob('*.md'):
        # Check if any parent directory is excluded
        if any(part.lower() in excluded_dirs for part in file_path.parts):
            continue
            
        if review_pattern.match(file_path.name):
            review_files.append(file_path)
    
    return review_files

def archive_reviews(files: List[pathlib.Path], dry_run: bool = True) -> Tuple[int, int]:
    """
    Moves identified review files to their respective Project Root's Documents/archives/reviews/
    Returns (success_count, failure_count).
    """
    if not files:
        logger.info("No review files found.")
        return 0, 0

    success_count = 0
    failure_count = 0

    for src in files:
        project_root = find_project_root(src)
        if not project_root:
            logger.warning(f"Could not find project root for: {src}. Skipping.")
            failure_count += 1
            continue
            
        dest_dir = project_root / 'Documents' / 'archives' / 'reviews'
        dst = dest_dir / src.name
        
        # Avoid moving files that are already in the correct destination
        try:
            if src.resolve() == dst.resolve() if dst.exists() else False:
                continue
        except Exception:
            pass # Fallback if resolution fails
            
        if dry_run:
            logger.info(f"[DRY RUN] Project: {project_root.name} | Would move: {src} -> {dst}")
            success_count += 1
        else:
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                # Safety Protocol: Use send2trash if the destination already exists
                if dst.exists():
                    logger.info(f"Conflict: {dst} exists. Sending old version to trash.")
                    send2trash(str(dst))
                
                shutil.move(str(src), str(dst))
                logger.info(f"Moved: {src} -> {dst}")
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to move {src}: {e}")
                failure_count += 1
                
    return success_count, failure_count

def main() -> None:
    """Entry point for the review archiver."""
    parser = argparse.ArgumentParser(description="Archive loose review markdown files into project-specific folders.")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: .)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved without moving.")
    args = parser.parse_args()

    # Standardize to pathlib.Path and relative path if possible
    root_path = pathlib.Path(args.root).resolve()
    try:
        root_path = root_path.relative_to(pathlib.Path.cwd())
    except ValueError:
        pass
        
    logger.info(f"Scanning for reviews in: {root_path}")
    if args.dry_run:
        logger.info("DRY RUN MODE ENABLED")

    review_files = find_review_files(root_path)
    successes, failures = archive_reviews(review_files, dry_run=args.dry_run)
    
    logger.info(f"Archive complete: {successes} succeeded, {failures} failed.")
    
    if failures > 0:
        logger.error(f"Failing due to {failures} errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
