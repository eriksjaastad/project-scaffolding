import pathlib
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def is_tier_1_project(index_path: pathlib.Path) -> bool:
    """
    Determines if the given markdown index file represents a Tier 1 (Full Stack/Code) project.
    """
    if not index_path.exists():
        return False
    
    tech_languages = {'python', 'javascript', 'java', 'c++', 'ruby', 'php', 'typescript', 'rust', 'go'}
    
    try:
        with index_path.open('r') as f:
            content = f.read()
            
        # Check for the specific tag
        if '#type/code' in content or '#type/project' in content:
            return True
            
        # Check each header line for tech languages
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                header = line.strip().lower()
                if any(lang in header for lang in tech_languages):
                    return True
                    
        return False
        
    except Exception as e:
        logger.error(f"Error reading file {index_path}: {e}")
        return False

def check_dependencies(project_root: pathlib.Path) -> bool:
    """Checks if a Tier 1 project has a dependency manifest."""
    manifests = ['requirements.txt', 'package.json', 'pyproject.toml', 'setup.py']
    for manifest in manifests:
        if (project_root / manifest).exists():
            return True
    return False

def check_dangerous_functions(project_root: pathlib.Path) -> list:
    """Greps for dangerous file removal functions."""
    dangerous_patterns = ['os.remove', 'os.unlink', 'shutil.rmtree']
    found_issues = []
    
    # Simple walk and check to avoid external dependency for basic audit
    for file_path in project_root.rglob('*.py'):
        # Skip certain directories
        if any(part in file_path.parts for part in ['venv', 'node_modules', '.git', '__pycache__']):
            continue
            
        if file_path.name == 'warden_audit.py': # Exclude self
            continue

        try:
            with file_path.open('r') as f:
                content = f.read()
                for pattern in dangerous_patterns:
                    if pattern in content:
                        found_issues.append((file_path, pattern))
        except Exception as e:
            logger.warning(f"Could not read file {file_path}: {e}")
            found_issues.append((file_path, f"READ_ERROR: {e}"))
            
    return found_issues

def run_audit(root_dir: pathlib.Path) -> bool:
    """Crawls the ecosystem and performs the audit."""
    logger.info(f"Starting Warden Audit in: {root_dir}")
    
    projects_found = 0
    issues_found = 0
    
    # Find all project roots by looking for 00_Index_*.md files
    for index_path in root_dir.rglob('00_Index_*.md'):
        # Skip indices in templates or archives
        if any(part in index_path.parts for part in ['templates', 'archives', 'venv', '.git']):
            continue
            
        projects_found += 1
        project_root = index_path.parent
        project_name = project_root.name
        
        is_tier_1 = is_tier_1_project(index_path)
        tier_label = "Tier 1 (Code)" if is_tier_1 else "Tier 2 (Other)"
        
        logger.info(f"Auditing Project: {project_name} [{tier_label}]")
        
        # Tier 1 Dependency Check
        if is_tier_1:
            if not check_dependencies(project_root):
                logger.error(f"[CRITICAL] {project_name}: Missing dependency manifest (requirements.txt/package.json)")
                issues_found += 1
        
        # Safety Check (All Tiers)
        dangerous_usage = check_dangerous_functions(project_root)
        for file_path, pattern in dangerous_usage:
            try:
                rel_path = file_path.relative_to(root_dir)
            except ValueError:
                rel_path = file_path
            logger.warning(f"[DANGEROUS] {project_name}: Raw '{pattern}' found in {rel_path}")
            issues_found += 1
                
    logger.info("--- Audit Summary ---")
    logger.info(f"Projects scanned: {projects_found}")
    logger.info(f"Issues found: {issues_found}")
    
    return issues_found == 0

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Warden Audit Agent - Phase 1")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: .)")
    args = parser.parse_args()
    
    # Standardize to pathlib.Path and relative path if possible
    root_path = pathlib.Path(args.root).resolve()
    try:
        root_path = root_path.relative_to(pathlib.Path.cwd())
    except ValueError:
        pass # Keep absolute if not under CWD, but preference is relative
        
    success = run_audit(root_path)
    sys.exit(0 if success else 1)
