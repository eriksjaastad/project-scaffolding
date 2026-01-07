import os
import pathlib
import logging
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def is_tier_1_project(index_path: str) -> bool:
    """
    Determines if the given markdown index file represents a Tier 1 (Full Stack/Code) project.
    Drafted by Ollama (deepseek-r1:14b).
    """
    if not pathlib.Path(index_path).exists():
        return False
    
    tech_languages = {'python', 'javascript', 'java', 'c++', 'ruby', 'php', 'typescript', 'rust', 'go'}
    
    try:
        with pathlib.Path(index_path).open('r') as f:
            content = f.read()
            
        # Check for the specific tag
        if '#type/code' in content or '#type/project' in content:
            # We add #type/project as it's often used for coding projects in this ecosystem
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
        logging.error(f"Error reading file {index_path}: {e}")
        return False

def check_dependencies(project_root: str) -> bool:
    """Checks if a Tier 1 project has a dependency manifest."""
    manifests = ['requirements.txt', 'package.json', 'pyproject.toml', 'setup.py']
    for manifest in manifests:
        if os.path.exists(os.path.join(project_root, manifest)):
            return True
    return False

def check_dangerous_functions(project_root: str) -> list:
    """Greps for dangerous file removal functions."""
    dangerous_patterns = ['os.remove', 'os.unlink', 'shutil.rmtree']
    # Use grep -r to find patterns in .py files
    found_issues = []
    
    # Simple walk and check to avoid external dependency for basic audit
    for dirpath, _, filenames in os.walk(project_root):
        if any(d in dirpath for d in ['venv', 'node_modules', '.git', '__pycache__']):
            continue
            
        for filename in filenames:
            if filename.endswith('.py') and filename != 'warden_audit.py': # Exclude self
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        for pattern in dangerous_patterns:
                            if pattern in content:
                                found_issues.append((file_path, pattern))
                except Exception:
                    pass
    return found_issues

def run_audit(root_dir: str) -> bool:
    """Crawls the ecosystem and performs the audit."""
    logging.info(f"Starting Warden Audit in: {root_dir}")
    
    projects_found = 0
    issues_found = 0
    
    for dirpath, _, filenames in os.walk(root_dir):
        # Identify project roots by 00_Index_*.md
        index_files = [f for f in filenames if f.startswith('00_Index_') and f.endswith('.md')]
        
        if index_files:
            projects_found += 1
            project_root = dirpath
            index_path = os.path.join(project_root, index_files[0])
            project_name = os.path.basename(project_root)
            
            is_tier_1 = is_tier_1_project(index_path)
            tier_label = "Tier 1 (Code)" if is_tier_1 else "Tier 2 (Other)"
            
            logging.info(f"Auditing Project: {project_name} [{tier_label}]")
            
            # Tier 1 Dependency Check
            if is_tier_1:
                if not check_dependencies(project_root):
                    logging.error(f"[CRITICAL] {project_name}: Missing dependency manifest (requirements.txt/package.json)")
                    issues_found += 1
            
            # Safety Check (All Tiers)
            dangerous_usage = check_dangerous_functions(project_root)
            for file_path, pattern in dangerous_usage:
                logging.warning(f"[DANGEROUS] {project_name}: Raw '{pattern}' found in {os.path.relpath(file_path, root_dir)}")
                issues_found += 1
                
    logging.info("--- Audit Summary ---")
    logging.info(f"Projects scanned: {projects_found}")
    logging.info(f"Issues found: {issues_found}")
    
    if issues_found > 0:
        return False
    return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Warden Audit Agent - Phase 1")
    parser.add_argument("--root", default=".", help="Root directory to scan (default: .)")
    args = parser.parse_args()
    
    success = run_audit(os.path.abspath(args.root))
    if not success:
        exit(1)
    exit(0)

