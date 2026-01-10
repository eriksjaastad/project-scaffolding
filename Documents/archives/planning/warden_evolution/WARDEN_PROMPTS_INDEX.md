# Warden Enhancement: Worker Task Prompts

**For Floor Manager Use**

Hand off these prompts to Workers **in order** (each builds on the previous):

---

## Task Order

### 1. WARDEN_PROMPT_1_FAST_FLAG.md ⏱️ 20 min
**Objective:** Add grep-based --fast flag for <1 second performance
**Critical:** This unblocks pre-commit hook usage
**Acceptance:** Performance benchmark shows <1 second execution

### 2. WARDEN_PROMPT_2_SEVERITY.md 🚦 25 min
**Objective:** Add P0/P1/P2 severity classification
**Critical:** Pre-commit hook needs to know what to block vs. warn
**Acceptance:** Output shows severity levels, exit code respects P0/P1

### 3. WARDEN_PROMPT_3_HARDCODED_PATHS.md 🛤️ 15 min
**Objective:** Detect /Users/, /home/ absolute paths as P1 violations
**Critical:** Prevents portability violations
**Acceptance:** Test file with hardcoded path triggers P1 error

### 4. WARDEN_PROMPT_4_TESTS.md ✅ 30 min
**Objective:** Add comprehensive test suite (80%+ coverage)
**Critical:** Production safety tool must be well-tested
**Acceptance:** 8 new tests pass, coverage >80%

---

## Total Estimated Time: 90 minutes

---

## Floor Manager Instructions

1. **Read research report first:** `WARDEN_RESEARCH_REPORT.md`
2. **Hand off prompts sequentially:** Don't start Task 2 until Task 1 complete
3. **Verify acceptance criteria:** Check every box before marking complete
4. **Test between tasks:** Run Warden after each task to confirm it works
5. **Halt on 3 failures:** If Worker fails same task 3x, alert Conductor

---

## Context Files Workers May Need

- `scripts/warden_audit.py` (the file being modified)
- `tests/test_security.py` (existing tests to extend)
- `Documents/archives/planning/warden_evolution/WARDEN_RESEARCH_REPORT.md` (background context)

---

## Final Verification (After All 4 Tasks)

```bash
# 1. Test fast mode works
time python scripts/warden_audit.py --root . --fast
# Expected: <1 second, finds scaffold/review.py issue as P0

# 2. Test severity classification
python scripts/warden_audit.py --root . | grep -E "P[0-2]"
# Expected: Severity labels in output

# 3. Test all tests pass
pytest tests/test_security.py::TestWardenEnhanced -v
# Expected: 8 tests pass

# 4. Test coverage
pytest tests/test_security.py --cov=scripts.warden_audit --cov-report=term
# Expected: >80% coverage
```

---

**Ready to hand off to Workers** ✅
