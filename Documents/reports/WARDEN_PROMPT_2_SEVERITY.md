# Worker Task: Add Severity Classification to Warden

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 25 minutes
**Objective:** Classify findings by severity (P0/P1/P2) so pre-commit hook knows what to block vs. warn

---

## Context

Pre-commit hooks need to distinguish between critical violations (block commit) and warnings (show but allow). We use P0 (critical), P1 (error), P2 (warning) severity levels.

**File to modify:** `scripts/warden_audit.py`

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **Enum:** Define Severity levels (P0, P1, P2)
- [ ] **Logic:** Dangerous functions in production code = P0
- [ ] **Logic:** Dangerous functions in test files = P2
- [ ] **Logic:** Missing dependency manifest = P2 (warning only)
- [ ] **Output:** Log messages show severity: `[P0-CRITICAL]`, `[P1-ERROR]`, `[P2-WARNING]`
- [ ] **Exit code:** Exit 1 only if P0 or P1 found; exit 0 if only P2 warnings

---

## Implementation Details

### 1. Add Severity Enum (after imports, around line 7)

```python
from enum import Enum

class Severity(Enum):
    P0 = "CRITICAL"  # Block commit - dangerous functions in production
    P1 = "ERROR"     # Block commit - hardcoded paths (future)
    P2 = "WARNING"   # Allow commit - acceptable with context
    P3 = "INFO"      # Allow commit - informational only
```

### 2. Update check_dangerous_functions() Return Type (line 48)

Change from returning `list` to returning `list[tuple]` with severity:

```python
def check_dangerous_functions(project_root: pathlib.Path) -> list:
    """Greps for dangerous file removal functions.

    Returns: List of (file_path, pattern, severity) tuples
    """
    dangerous_patterns = ['os.remove', 'os.unlink', 'shutil.rmtree']
    found_issues = []

    for file_path in project_root.rglob('*.py'):
        # Skip certain directories
        if any(part in file_path.parts for part in ['venv', 'node_modules', '.git', '__pycache__']):
            continue

        if file_path.name == 'warden_audit.py':
            continue

        # Determine severity based on file location
        is_test_file = 'test' in file_path.parts or file_path.name.startswith('test_')

        try:
            with file_path.open('r') as f:
                content = f.read()
                for pattern in dangerous_patterns:
                    if pattern in content:
                        # Production code = P0, test code = P2
                        severity = Severity.P2 if is_test_file else Severity.P0
                        found_issues.append((file_path, pattern, severity))
        except Exception as e:
            logger.warning(f"Could not read file {file_path}: {e}")
            # Read errors are informational
            found_issues.append((file_path, f"READ_ERROR: {e}", Severity.P3))

    return found_issues
```

### 3. Update check_dangerous_functions_fast() Similarly

If Worker completed Task 1 (--fast flag), update that function too:

```python
# In check_dangerous_functions_fast(), change append to:
severity = Severity.P2 if 'test' in file_path else Severity.P0
found_issues.append((pathlib.Path(file_path), pattern, severity))
```

### 4. Update run_audit() to Track Severity (line 74)

```python
def run_audit(root_dir: pathlib.Path, use_fast: bool = False) -> bool:
    """Crawls the ecosystem and performs the audit."""
    logger.info(f"Starting Warden Audit in: {root_dir}")

    projects_found = 0
    p0_issues = 0  # Critical
    p1_issues = 0  # Error
    p2_issues = 0  # Warning

    # ... existing project scanning logic ...

    # Tier 1 Dependency Check (change to P2)
    if is_tier_1:
        if not check_dependencies(project_root):
            logger.warning(f"[P2-WARNING] {project_name}: Missing dependency manifest")
            p2_issues += 1

    # Safety Check (All Tiers)
    dangerous_usage = check_dangerous_functions_fast(project_root) if use_fast else check_dangerous_functions(project_root)
    for file_path, pattern, severity in dangerous_usage:
        try:
            rel_path = file_path.relative_to(root_dir)
        except ValueError:
            rel_path = file_path

        # Log with severity prefix
        severity_label = f"[{severity.name}-{severity.value}]"
        if severity == Severity.P0:
            logger.error(f"{severity_label} {project_name}: '{pattern}' found in {rel_path}")
            p0_issues += 1
        elif severity == Severity.P1:
            logger.error(f"{severity_label} {project_name}: '{pattern}' found in {rel_path}")
            p1_issues += 1
        elif severity == Severity.P2:
            logger.warning(f"{severity_label} {project_name}: '{pattern}' found in {rel_path}")
            p2_issues += 1
        else:
            logger.info(f"{severity_label} {project_name}: '{pattern}' in {rel_path}")

    logger.info("--- Audit Summary ---")
    logger.info(f"Projects scanned: {projects_found}")
    logger.info(f"P0 (Critical): {p0_issues}")
    logger.info(f"P1 (Error): {p1_issues}")
    logger.info(f"P2 (Warning): {p2_issues}")

    # Exit clean only if no P0 or P1 issues
    return (p0_issues == 0 and p1_issues == 0)
```

---

## Verification Steps

1. **Test severity classification on known file:**
   ```bash
   python scripts/warden_audit.py --root .
   ```
   Expected: `[P0-CRITICAL]` for `scaffold/review.py` (production code)

2. **Create test file with os.remove:**
   ```bash
   echo "import os; os.remove('test.txt')" > tests/test_temp.py
   python scripts/warden_audit.py --root .
   ```
   Expected: `[P2-WARNING]` for `tests/test_temp.py` (test code)
   Expected: Exit code 0 (warnings don't fail)

3. **Verify exit codes:**
   ```bash
   python scripts/warden_audit.py --root . && echo "PASSED" || echo "FAILED"
   ```
   Should show "FAILED" because scaffold/review.py has P0 issue

4. **Clean up test file:**
   ```bash
   rm tests/test_temp.py
   ```

---

## Files to Read First

- `scripts/warden_audit.py` (should already have --fast flag from Task 1)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 6 acceptance criteria checked
- [ ] Verification steps 1-4 completed successfully
- [ ] Output clearly shows severity levels
- [ ] Exit code 0 for P2-only, exit code 1 for P0/P1

If Worker fails 3 times, halt and alert Conductor.
