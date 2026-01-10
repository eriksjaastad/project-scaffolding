# Worker Task: Add Hardcoded Path Detection to Warden

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 15 minutes
**Objective:** Detect hardcoded absolute paths (/Users/, /home/, C:\) to prevent portability violations

---

## Context

Projects should use relative paths or environment variables. Hardcoded absolute paths like `/Users/erik/project` make code non-portable. This violates CODE_QUALITY_STANDARDS.md Rule #5.

**File to modify:** `scripts/warden_audit.py`

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **Patterns:** Add `/Users/`, `/home/`, `C:\\` to dangerous_patterns list
- [ ] **Severity:** Classify hardcoded paths as P1 (ERROR - block commit)
- [ ] **Exclusions:** Don't flag paths in comments or docstrings (basic check)
- [ ] **Test:** Create fixture with hardcoded path, confirm detection
- [ ] **Verification:** Run on project-scaffolding, should find zero (all paths are relative)

---

## Implementation Details

### 1. Expand dangerous_patterns (line 50)

Change from:
```python
dangerous_patterns = ['os.remove', 'os.unlink', 'shutil.rmtree']
```

To:
```python
dangerous_patterns = [
    'os.remove', 'os.unlink', 'shutil.rmtree',  # Dangerous functions
    '/Users/', '/home/',  # macOS/Linux absolute paths
    'C:\\\\', 'C:/'       # Windows absolute paths (escaped)
]
```

### 2. Update Severity Logic (in check_dangerous_functions)

After line ~67, update severity classification:

```python
# Determine severity based on file location and pattern type
is_test_file = 'test' in file_path.parts or file_path.name.startswith('test_')

# Classify pattern type
is_dangerous_function = pattern in ['os.remove', 'os.unlink', 'shutil.rmtree']
is_hardcoded_path = pattern in ['/Users/', '/home/', 'C:\\\\', 'C:/']

if is_hardcoded_path:
    # Hardcoded paths are always P1 (ERROR) - block commit
    severity = Severity.P1
elif is_dangerous_function:
    # Production code = P0, test code = P2
    severity = Severity.P2 if is_test_file else Severity.P0
else:
    severity = Severity.P3
```

### 3. Update Fast Mode (if implemented in Task 1)

If `check_dangerous_functions_fast()` exists, add the same patterns to it:

```python
dangerous_patterns = [
    'os.remove', 'os.unlink', 'shutil.rmtree',
    '/Users/', '/home/',
    'C:\\\\', 'C:/'
]
```

And apply the same severity logic.

---

## Verification Steps

1. **Create test file with hardcoded path:**
   ```bash
   cat > tests/test_hardcoded_path.py << 'EOF'
   from pathlib import Path

   # This should be flagged as P1
   BAD_PATH = Path("/Users/erik/my-project")

   # This is OK - relative path
   GOOD_PATH = Path("../my-project")
   EOF
   ```

2. **Run Warden:**
   ```bash
   python scripts/warden_audit.py --root .
   ```
   Expected output: `[P1-ERROR] project-scaffolding: '/Users/' found in tests/test_hardcoded_path.py`

3. **Verify exit code:**
   ```bash
   python scripts/warden_audit.py --root . && echo "PASSED" || echo "FAILED"
   ```
   Should show "FAILED" (P1 blocks commit)

4. **Clean up test file:**
   ```bash
   rm tests/test_hardcoded_path.py
   ```

5. **Verify project-scaffolding is clean:**
   ```bash
   python scripts/warden_audit.py --root . --fast
   ```
   Should find only the P0 issue in `scaffold/review.py` (os.unlink), no hardcoded paths

---

## Known Edge Cases

**False positives to ignore (for now):**
- Comments: `# Don't use /Users/ paths`
- Docstrings: `"""Avoid /home/ directories"""`
- String examples: `example = "/Users/example"`

**Why we flag comments:** Being explicit is better than silent. If a comment mentions `/Users/`, developer can acknowledge it's intentional.

**Future improvement:** Use AST parsing to only check string literals (not comments). For now, keep it simple.

---

## Files to Read First

- `scripts/warden_audit.py` (should have --fast flag and severity from Tasks 1-2)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 5 acceptance criteria checked
- [ ] Verification steps 1-5 completed successfully
- [ ] Hardcoded paths flagged as P1 (ERROR)
- [ ] Clean project shows no hardcoded path violations

If Worker fails 3 times, halt and alert Conductor.
