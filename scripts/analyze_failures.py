#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

def get_projects_root() -> Path:
    root = os.getenv("PROJECTS_ROOT")
    if not root:
        return Path(__file__).parent.parent.parent
    return Path(root)

def analyze_failures() -> None:
    projects_root = get_projects_root()
    validator = Path(__file__).parent.parent / "scripts" / "validate_project.py"
    
    print(f"Analyzing validation failures across {projects_root}...\n")
    
    placeholder_failures = 0
    safety_failures = 0
    dna_failures = 0
    missing_file_failures = 0
    fully_compliant = 0
    
    for project_dir in projects_root.iterdir():
        if not project_dir.is_dir() or project_dir.name.startswith((".", "_")):
            continue
            
        if project_dir.name in {"ai-journal", "writing", "plugin-duplicate-detection", "plugin-find-names-chrome"}:
            continue
            
        try:
            result = subprocess.run(
                ["python3", str(validator), project_dir.name],
                capture_output=True,
                text=True,
                check=False
            )
            
            output = result.stdout + result.stderr
            
            if "Fully Compliant" in output:
                fully_compliant += 1
                continue
                
            has_placeholder = "Placeholder Defect" in output
            has_safety = "Safety Defect" in output
            has_dna = "DNA Defect" in output
            has_missing = "Missing mandatory" in output or "Missing index" in output
            
            if has_placeholder: placeholder_failures += 1
            if has_safety: safety_failures += 1
            if has_dna: dna_failures += 1
            if has_missing: missing_file_failures += 1
            
        except Exception as e:
            print(f"Error analyzing {project_dir.name}: {e}")

    print("=== Validation Failure Analysis ===")
    print(f"✅ Fully Compliant: {fully_compliant}")
    print(f"🧩 Placeholder Defects: {placeholder_failures}")
    print(f"🛡️  Safety Defects: {safety_failures}")
    print(f"🧬 DNA Defects: {dna_failures}")
    print(f"📁 Missing Files/Indexes: {missing_file_failures}")
    print(f"Total projects analyzed: {fully_compliant + max(placeholder_failures, safety_failures, dna_failures, missing_file_failures)}")

if __name__ == "__main__":
    analyze_failures()
