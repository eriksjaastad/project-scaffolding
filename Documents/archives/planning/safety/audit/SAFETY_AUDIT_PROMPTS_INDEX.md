# Safety Audit: Worker Task Prompts

**For Floor Manager Use**

Hand off these prompts to Workers **in order**:

---

## Task Order

### 1. SAFETY_PROMPT_1_FIX_UNLINK.md ⏱️ 10 min
**Objective:** Replace os.unlink with send2trash in scaffold/review.py
**Critical:** Eliminates last P0 violation in production code
**Acceptance:** Warden reports zero P0 issues

### 2. SAFETY_PROMPT_2_VALIDATE.md ✅ 10 min
**Objective:** Run full validation (Warden + tests)
**Critical:** Confirms fix doesn't break anything
**Acceptance:** All tests pass, Warden clean

---

## Total Estimated Time: 20 minutes

---

## Floor Manager Instructions

1. **Execute sequentially:** Don't start Task 2 until Task 1 complete
2. **Verify acceptance criteria:** Check every box before marking complete
3. **Run tests between tasks:** Ensure nothing breaks
4. **Halt on 3 failures:** If Worker fails same task 3x, alert Conductor

---

## Context Files Workers May Need

- `scaffold/review.py` (the file being modified)
- `scripts/warden_audit.py` (validation tool)
- `requirements.txt` (verify send2trash dependency)

---

## Final Verification (After Both Tasks)

```bash
# 1. Verify fix is in place
grep -n "send2trash" scaffold/review.py
# Expected: Line ~79 shows send2trash usage

# 2. Run Warden - should be clean
python scripts/warden_audit.py --root . --fast
# Expected: Zero P0 issues in production code

# 3. Run full test suite
pytest tests/ -v
# Expected: All tests pass

# 4. Verify send2trash import exists
grep -n "from send2trash import send2trash" scaffold/review.py
# Expected: Import at top of file
```

---

**Ready to hand off to Workers** ✅
