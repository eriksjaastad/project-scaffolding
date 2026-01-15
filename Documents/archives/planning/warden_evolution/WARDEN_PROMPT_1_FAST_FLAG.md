# Worker Task: Add --fast Flag to Warden

**Worker Model:** DeepSeek-R1 or Qwen-2.5-Coder
**Estimated Time:** 20 minutes
**Objective:** Add grep-based fast scanning mode for pre-commit hook use (target <1 second)

---

## Context

The current Warden uses Python's `.rglob()` to scan files, which takes 10+ seconds. For pre-commit hooks, we need <1 second performance using grep/ripgrep.

**File to modify:** `scripts/warden_audit.py`

---

## 🎯 [ACCEPTANCE CRITERIA]

- [x] **Argument:** Add `--fast` flag to argparse (line ~121)
- [x] **Function:** Create `check_dangerous_functions_fast()` using subprocess + grep
- [x] **Fallback:** If grep/ripgrep not available, fall back to regular scan
- [x] **Performance:** Benchmark confirms <1 second on current directory
- [x] **Correctness:** Fast mode finds same dangerous patterns as regular scan
- [x] **Integration:** Update `run_audit()` to use fast function when flag set

---

## Implementation Details

### 1. Add Argument (around line 121)

```bash
parser.add_argument("--fast", action="store_true",
                   help="Fast scan mode for pre-commit hooks (<1s target)")
```

### 2. Create Fast Function (after line 72)

```bash
def check_dangerous_functions_fast(project_root: pathlib.Path) -> list:
    """Fast grep-based scanner for pre-commit hooks.

    Uses ripgrep (rg) or grep for sub-second performance.
    Falls back to regular scan if grep not available.
    """
    import subprocess
    import shutil

    # Check if ripgrep or grep available
    grep_cmd = 'rg' if shutil.which('rg') else 'grep' if shutil.which('grep') else None

    if grep_cmd is None:
        logger.warning("grep/ripgrep not found, falling back to regular scan")
        return check_dangerous_functions(project_root)

    dangerous_patterns = ['os.remove', 'os.unlink', 'shutil.rmtree']
    found_issues = []

    for pattern in dangerous_patterns:
        try:
            if grep_cmd == 'rg':
                # ripgrep: --type py, -l (files with matches)
                cmd = ['rg', '--type', 'py', '-l', pattern, str(project_root)]
            else:
                # grep: -r (recursive), -l (files), --include (Python files)
                cmd = ['grep', '-r', '-l', '--include=*.py', pattern, str(project_root)]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=2, check=False)

            if result.returncode == 0:  # Matches found
                for file_path in result.stdout.strip().split('\n'):
                    if file_path:  # Skip empty lines
                        found_issues.append((pathlib.Path(file_path), pattern))

        except subprocess.TimeoutExpired:
            logger.warning(f"Fast scan timeout for pattern: {pattern}")
        except Exception as e:
            logger.warning(f"Fast scan error: {e}")

    return found_issues
```

### 3. Update run_audit() (around line 103)

Change line 103 from:
```bash
dangerous_usage = check_dangerous_functions(project_root)
```

To:
```bash
dangerous_usage = check_dangerous_functions_fast(project_root) if use_fast else check_dangerous_functions(project_root)
```

Add parameter to `run_audit()` function signature (line 74):
```bash
def run_audit(root_dir: pathlib.Path, use_fast: bool = False) -> bool:
```

And in `__main__` section (line 131):
```bash
success = run_audit(root_path, use_fast=args.fast)
```

---

## Verification Steps

1. **Test regular mode still works:**
   ```bash
   doppler run -- python scripts/warden_audit.py --root .
   # Should complete (even if slow)
   ```

2. **Test fast mode:**
   ```bash
   time python scripts/warden_audit.py --root . --fast
   # Should complete in <1 second
   ```

3. **Compare outputs:**
   Both should find the same issue in `scaffold/review.py` (os.unlink)

4. **Test on project without issues:**
   Fast mode should exit with code 0 in <1 second

---

## Files to Read First

- `scripts/warden_audit.py` (full file, 133 lines)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [x] All 6 acceptance criteria checked
- [x] Verification steps 1-4 completed successfully
- [x] Performance benchmark shows <1 second execution

**STATUS: SIGNED OFF BY FLOOR MANAGER**
*Note: Due to worker timeouts and output repetition issues, the Floor Manager performed the final implementation and verification to ensure sub-second performance and correctness.*
