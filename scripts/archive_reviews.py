import os
import re
import shutil
import argparse
import logging
import sys
from glob import glob
from typing import List, Optional, Tuple
from send2trash import send2trash

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def find_project_root(file_path: str, max_depth: int = 10) -> Optional[str]:
    """
    Finds the nearest parent directory containing '00_Index_*.md'.
    This ensures Project Autonomy by defining clear boundaries.
    """
    current_path = os.path.abspath(file_path)
    if os.path.isfile(current_path):
        current_path = os.path.dirname(current_path)
    
    depth = 0
    while depth < max_depth:
        # Search for '00_Index_*.md' in the current directory
        index_files = glob(os.path.join(current_path, '00_Index_*.md'))
        if index_files:
            return current_path
        
        # Move up to the parent directory
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break  # Reached root
        
        current_path = parent_path
        depth += 1
        
    return None

def find_review_files(root_dir: str) -> List[str]:
    """
    Recursively finds review-related markdown files within the given root directory,
    excluding specified directories and Python scripts.
    """
    excluded_dirs = {'data', 'venv', 'node_modules', '.git', '__pycache__'}
    # Regex to match 'REVIEW.md', 'CODE_REVIEW_*.md', or '*review*.md' (case-insensitive)
    review_pattern = re.compile(r'^(?:REVIEW\.md|CODE_REVIEW_.*\.md|.*review.*\.md)$', re.IGNORECASE)
    
    review_files: List[str] = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter directories in-place
        dirnames[:] = [d for d in dirnames if d.lower() not in excluded_dirs]
        
        for filename in filenames:
            # Skip python files explicitly
            if filename.lower().endswith('.py'):
                continue
            
            if review_pattern.match(filename):
                full_path = os.path.join(dirpath, filename)
                review_files.append(full_path)
    
    return review_files

def archive_reviews(files: List[str], dry_run: bool = True) -> Tuple[int, int]:
    """
    Moves identified review files to their respective Project Root's Documents/archives/reviews/
    Returns (success_count, failure_count).
    """
    if not files:
        logging.info("No review files found.")
        return 0, 0

    success_count = 0
    failure_count = 0

    for src in files:
        project_root = find_project_root(src)
        if not project_root:
            logging.warning(f"Could not find project root for: {src}. Skipping.")
            failure_count += 1
            continue
            
        dest_dir = os.path.join(project_root, 'Documents', 'archives', 'reviews')
        filename = os.path.basename(src)
        dst = os.path.join(dest_dir, filename)
        
        # Avoid moving files that are already in the correct destination
        if os.path.abspath(src) == os.path.abspath(dst):
            continue
            
        if dry_run:
            logging.info(f"[DRY RUN] Project: {os.path.basename(project_root)} | Would move: {src} -> {dst}")
            success_count += 1
        else:
            try:
                os.makedirs(dest_dir, exist_ok=True)
                # Safety Protocol: Use send2trash if the destination already exists
                if os.path.exists(dst):
                    logging.info(f"Conflict: {dst} exists. Sending old version to trash.")
                    send2trash(dst)
                
                shutil.move(src, dst)
                logging.info(f"Moved: {src} -> {dst}")
                success_count += 1
            except Exception as e:
                logging.error(f"Failed to move {src}: {e}")
                failure_count += 1
                
    return success_count, failure_count

def main() -> None:
    """Entry point for the review archiver."""
    parser = argparse.ArgumentParser(description="Archive loose review markdown files into project-specific folders.")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: .)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be moved without moving.")
    args = parser.parse_args()

    scan_dir = os.path.abspath(args.root)
    logging.info(f"Scanning for reviews in: {scan_dir}")
    if args.dry_run:
        logging.info("DRY RUN MODE ENABLED")

    review_files = find_review_files(scan_dir)
    successes, failures = archive_reviews(review_files, dry_run=args.dry_run)
    
    logging.info(f"Archive complete: {successes} succeeded, {failures} failed.")
    
    if failures > 0:
        logging.error(f"Failing due to {failures} errors.")
        sys.exit(1)

if __name__ == "__main__":
    main()
