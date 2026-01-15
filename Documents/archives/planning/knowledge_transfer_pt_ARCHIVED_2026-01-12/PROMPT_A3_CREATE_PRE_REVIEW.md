# Prompt A3: Create pre_review_scan.sh

**Task:** Create a pre-review scan script that runs warden + validate locally
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b
**Dependencies:** A1 (warden_audit.py), A2 (validate_project.py)

---

## CONSTRAINTS (READ FIRST)

- DO NOT reference $SCAFFOLDING - use relative paths only
- Script must work when run from project root
- Use `./scripts/` paths (relative)
- Make script executable (chmod +x)

---

## [ACCEPTANCE CRITERIA]

- [x] File created at project-tracker/scripts/pre_review_scan.sh
- [x] Script is executable (has +x permission)
- [x] Script runs warden_audit.py with --fast flag
- [x] Script runs validate_project.py
- [x] Script exits with error code if either check fails
- [x] Script works from project-tracker root: `./scripts/pre_review_scan.sh`

---

## Task

Create this file at `[USER_HOME]/projects/project-tracker/scripts/pre_review_scan.sh`:

```bash
#!/bin/bash
# pre_review_scan.sh - Run before code reviews or commits
# Usage: ./scripts/pre_review_scan.sh

set -e  # Exit on first error

echo "=== Pre-Review Scan ==="
echo ""

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "1. Running Warden Security Audit (fast mode)..."
doppler run -- python ./scripts/warden_audit.py --root . --fast
WARDEN_EXIT=$?

echo ""
echo "2. Running Project Validation..."
doppler run -- python ./scripts/validate_project.py project-tracker
VALIDATE_EXIT=$?

echo ""
echo "=== Scan Complete ==="

if [ $WARDEN_EXIT -ne 0 ] || [ $VALIDATE_EXIT -ne 0 ]; then
    echo "FAILED: One or more checks failed"
    exit 1
else
    echo "PASSED: All checks passed"
    exit 0
fi
```

Then make it executable:
```bash
chmod +x [USER_HOME]/projects/project-tracker/scripts/pre_review_scan.sh
```

---

## Verification

```bash
cd [USER_HOME]/projects/project-tracker

# 1. File exists and is executable
ls -la scripts/pre_review_scan.sh
# Should show -rwxr-xr-x permissions

# 2. Script runs
./scripts/pre_review_scan.sh
# Should run both warden and validate, show results
```

---

## Result

- [x] PASS: Script created and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
