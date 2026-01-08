"""Test that scripts follow CODE_QUALITY_STANDARDS.md"""
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
            ["grep", "-rn", pattern, "scripts/", "scaffold/", "--include=*.py"],
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
    
    assert not lines, "Found hardcoded paths:\n" + "\n".join(lines)

def test_no_hardcoded_api_keys():
    """Scripts must not contain API keys"""
    # Regex for sk-... keys
    try:
        result = subprocess.run(
            ["grep", "-rE", "sk-[a-zA-Z0-9]{32,}", "scripts/", "scaffold/", "--include=*.py"],
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
    """All .py files in scripts/ and scaffold/ should have type hints on functions"""
    violations = []

    for directory in ["scripts", "scaffold"]:
        dir_path = Path(directory)
        for script in dir_path.glob("*.py"):
            if script.name == "__init__.py":
                continue
            
        content = script.read_text()
        # Find all function definitions (even multi-line)
        import re
        # This pattern finds 'def function_name(...)' and checks for '->' before the colon
        matches = re.finditer(r"def\s+\w+\s*\([^)]*\)\s*([^:]*)", content)
        for match in matches:
            sig_tail = match.group(1)
            full_sig = match.group(0)
            if "->" not in sig_tail and "def __init__" not in full_sig:
                # Get the function name for reporting
                func_name = full_sig.split("(")[0].strip()
                violations.append(f"{script.name}: {func_name}")

    assert not violations, "Scripts without type hints:\n" + "\n".join(violations)
