# Task: Validate Safety Audit Fix

**Worker Model:** DeepSeek-R1 / Qwen-2.5-Coder
**Objective:** Confirm the os.unlink fix is complete and nothing is broken

---

## Context

Task 1 replaced `os.unlink` with `send2trash` in `scaffold/review.py`. Now we need to verify:
1. Warden no longer reports P0 issues in production code
2. All existing tests still pass
3. The change is syntactically correct

---

## Your Task

Run the following verification commands and report results:

### Step 1: Run Warden Audit
```bash
doppler run -- python scripts/warden_audit.py --root . --fast
```

**Expected output:**
- Zero P0 (Critical) issues in production code
- P2 (Warning) in test files is acceptable
- Exit code 0 (success)

### Step 2: Run Full Test Suite
```bash
pytest tests/ -v
```

**Expected output:**
- All tests pass
- No import errors
- No runtime errors

### Step 3: Verify send2trash Dependency
```bash
grep "send2trash" requirements.txt
```

**Expected output:**
- `send2trash` appears in requirements.txt (already present)

---

## 🎯 [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)

- [x] **Warden Clean:** `python scripts/warden_audit.py --root . --fast` reports 0 P0 issues
- [x] **Tests Pass:** `pytest tests/ -v` shows all tests passing (Warden tests pass; other pre-existing environment failures noted)
- [x] **Dependency Present:** `send2trash` is in requirements.txt
- [x] **No Regressions:** No new test failures introduced

---

## FLOOR MANAGER PROTOCOL

Do not sign off until every [ ] is marked [x].

**If Warden still reports P0:**
- Check if scaffold/review.py was actually modified
- Verify os.unlink is completely replaced
- Send Worker back to Task 1

**If tests fail:**
- Check if failure is related to the send2trash change
- If related: send Worker back to fix
- If unrelated: document as pre-existing issue

**Success looks like:**
```bash
INFO: --- Audit Summary ---
INFO: Projects scanned: 1
INFO: P0 (Critical): 0      ← THIS IS THE KEY
INFO: P1 (Error): 0
INFO: P2 (Warning): 3       ← Warnings in test files are OK
```

---

**Estimated time:** 10 minutes
