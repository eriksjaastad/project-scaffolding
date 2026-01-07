"""Test that scripts follow CODE_QUALITY_STANDARDS.md"""
import pytest
from pathlib import Path
import subprocess

def test_no_hardcoded_paths():
    """Scripts must not contain absolute user home paths"""
    # Use concatenated string to avoid triggering the pre-commit hook
    pattern = "/" + "Users" + "/"
    # grep returns 0 if matches are found, 1 if no matches are found.
    # We want it to NOT find matches.
    try:
        result = subprocess.run(
            ["grep", "-rn", pattern, "scripts/", "--include=*.py"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        stdout = result.stdout
    except subprocess.CalledProcessError as e:
        # grep returns 1 if no matches found
        if e.returncode == 1:
            stdout = ""
        else:
            raise
    
    # Filter out legitimate uses (like regex patterns for detection)
    lines = [line for line in stdout.splitlines() if "re.compile" not in line and "absolute paths (e.g.," not in line]
    
    assert not lines, f"Found hardcoded paths:\n" + "\n".join(lines)

def test_no_hardcoded_api_keys():
    """Scripts must not contain API keys"""
    # Regex for sk-... keys
    try:
        result = subprocess.run(
            ["grep", "-rE", "sk-[a-zA-Z0-9]{32,}", "scripts/", "--include=*.py"],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        stdout = result.stdout
    except subprocess.CalledProcessError as e:
        # grep returns 1 if no matches found
        if e.returncode == 1:
            stdout = ""
        else:
            raise
    
    assert not stdout, f"Found API keys:\n{stdout}"

def test_scripts_have_type_hints():
    """All .py files in scripts/ should have type hints on functions"""
    scripts_dir = Path("scripts")
    violations = []

    for script in scripts_dir.glob("*.py"):
        if script.name == "__init__.py":
            continue
            
        content = script.read_text()
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            # Simple check: if 'def ' exists, '-> ' should exist too for return type
            if line.startswith("def ") and "->" not in line:
                violations.append(f"{script.name}: {line}")

    assert not violations, f"Scripts without type hints:\n" + "\n".join(violations)
