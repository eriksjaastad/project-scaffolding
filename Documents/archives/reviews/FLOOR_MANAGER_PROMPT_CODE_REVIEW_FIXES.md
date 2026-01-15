# Floor Manager Task: Code Review Remediation

**Source:** Claude Opus Code Review (CODE_REVIEW_CLAUDE_OPUS_v1.md)
**Date:** 2026-01-11
**Priority:** P0/P1 - Blocking issues identified

---

## Context for Floor Manager

A code review identified critical issues that prevent the codebase from functioning. The scripts have never been run, the test suite can't execute, and there's significant code duplication. This task addresses all blocking issues.

---

## Task 1: Fix Broken Script (P0 - CRITICAL)

### [FIX_MISSING_IMPORT]
**Worker Model:** DeepSeek-R1 / Qwen-2.5-Coder
**Objective:** Add missing `import re` to `scripts/reindex_projects.py` so the script doesn't crash on first run.

### DOWNSTREAM HARM ESTIMATE
- **If this fails:** Script crashes with `NameError: name 're' is not defined` on any execution
- **Known pitfalls:** Simple fix, but verify the import goes with other imports at the top
- **Timeout:** 60s

### LEARNINGS APPLIED
- [x] Consulted LOCAL_MODEL_LEARNINGS.md (date: 2026-01-10)
- [x] Task decomposed to micro-level (single line addition)
- [x] Using StrReplace/diff style (not full file rewrite)
- [x] Explicit "DO NOT" constraints: DO NOT modify any other code in the file

### [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)
- [x] **Import Added:** `import re` exists in `scripts/reindex_projects.py` (near line 24, with other stdlib imports)
- [x] **Syntax Valid:** `python -m py_compile scripts/reindex_projects.py` exits with code 0
- [x] **Script Runs:** `python scripts/reindex_projects.py --help` executes without `NameError`
- [x] **No Side Effects:** No other changes made to the file

---

## Task 2: Fix Test Environment (P0 - CRITICAL)

### [FIX_TEST_DEPENDENCIES]
**Worker Model:** DeepSeek-R1 / Qwen-2.5-Coder
**Objective:** Ensure `python-dotenv` is installed and tests can import it.

### DOWNSTREAM HARM ESTIMATE
- **If this fails:** Test suite cannot run at all; `ModuleNotFoundError: No module named 'dotenv'`
- **Known pitfalls:** May be environment-specific; verify using the correct venv
- **Timeout:** 120s

### LEARNINGS APPLIED
- [x] Consulted LOCAL_MODEL_LEARNINGS.md (date: 2026-01-10)
- [x] Task decomposed to micro-level
- [x] Verification step included

### [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)
- [x] **Dependency Installed:** `pip show python-dotenv` returns package info (not "not found")
- [x] **Import Works:** `python -c "from dotenv import load_dotenv; print('OK')"` prints "OK"
- [x] **Tests Run:** `pytest tests/ -v -m "not slow" --collect-only` shows tests collected (no import errors)

---

## Task 3: Extract Shared Utilities (P1 - HIGH)

### [EXTRACT_SAFE_SLUG]
**Worker Model:** DeepSeek-R1 / Qwen-2.5-Coder
**Objective:** Eliminate code duplication by extracting `safe_slug()` to a shared module.

### DOWNSTREAM HARM ESTIMATE
- **If this fails:** Security fixes need to be applied 3x; code drift between implementations
- **Known pitfalls:** Import paths must work from both `scaffold/` and `scripts/`; keep the MOST COMPLETE implementation (the one in `scaffold/review.py` with `base_path` parameter)
- **Timeout:** 300s

### LEARNINGS APPLIED
- [x] Consulted LOCAL_MODEL_LEARNINGS.md (date: 2026-01-10)
- [x] Task decomposed to micro-level
- [x] Using StrReplace/diff style for modifications
- [x] Explicit constraints: Keep the `scaffold/review.py` version as the canonical one (it has `base_path` parameter)

### Implementation Steps
1. Create `scaffold/utils.py` with `safe_slug()` function (copy from `scaffold/review.py:40-61`)
2. Update `scaffold/review.py` to import from `scaffold/utils`
3. Update `scripts/validate_project.py` to import from `scaffold.utils`
4. Update `scripts/reindex_projects.py` to import from `scaffold.utils`
5. Remove duplicate `safe_slug()` definitions from all three files

### [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)
- [x] **New File Exists:** `scaffold/utils.py` exists and contains `def safe_slug(`
- [x] **Canonical Version:** `scaffold/utils.py` has the `base_path` parameter (matches review.py version)
- [x] **No Duplicates:** `grep -rn "def safe_slug" scripts/ scaffold/` returns ONLY `scaffold/utils.py`
- [x] **Imports Work:** `python -c "from scaffold.utils import safe_slug; print('OK')"` prints "OK"
- [x] **Scripts Still Work:**
  - [x] `python scripts/reindex_projects.py --help` runs without error
  - [x] `python scripts/validate_project.py --help` runs without error
- [x] **Review Module Works:** `python -c "from scaffold.review import CodeReviewer; print('OK')"` prints "OK"

---

## Task 4: Remove Generated Artifact (P2 - MEDIUM)

### [REMOVE_REPOMIX]
**Worker Model:** DeepSeek-R1 / Qwen-2.5-Coder
**Objective:** Remove `repomix-output.xml` from repo and add to `.gitignore`.

### DOWNSTREAM HARM ESTIMATE
- **If this fails:** 24k+ line generated file stays in repo, bloating size
- **Known pitfalls:** File may already be in `.gitignore`; check first
- **Timeout:** 60s

### LEARNINGS APPLIED
- [x] Task decomposed to micro-level
- [x] Verification step included

### [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)
- [x] **File Removed:** `ls repomix-output.xml` returns "No such file or directory"
- [x] **Git Tracked:** `git rm repomix-output.xml` executed (or file already untracked)
- [x] **Gitignore Updated:** `grep "repomix-output.xml" .gitignore` returns a match
- [x] **Not Staged for Commit:** File won't reappear on next repomix run

---

## FLOOR MANAGER PROTOCOL

1. **Execute tasks in order:** P0 tasks (1, 2) MUST pass before P1 tasks (3, 4)
2. **Do not sign off** until every [ ] is marked [x]
3. **If any item fails:** Provide the specific error log to the Worker and demand a retry (Max 3 attempts)
4. **After any failure:** Ask "Was this preventable?" If a documented learning was ignored, log it
5. **Final verification:** After all tasks complete, run:
   ```bash
   # Verify no broken imports
   doppler run -- python -m py_compile scripts/*.py scaffold/*.py

   # Verify tests can at least be collected
   pytest tests/ --collect-only

   # Verify no duplicate safe_slug
   grep -rn "def safe_slug" scripts/ scaffold/
   ```

---

## Success State

When complete:
- All scripts run without import errors
- Test suite can execute
- `safe_slug()` exists in exactly ONE location
- `repomix-output.xml` is gone and gitignored

**Sign-off required before marking task Complete.**

---

*Generated from CODE_REVIEW_CLAUDE_OPUS_v1.md findings*
*Template per AGENTS.md v1.0*
