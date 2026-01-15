# Task: Replace os.unlink with send2trash

**Worker Model:** DeepSeek-R1 / Qwen-2.5-Coder
**Objective:** Fix the P0 safety violation in scaffold/review.py

---

## Context

The file `scaffold/review.py` uses `os.unlink()` at line 79 to delete a temp file during error cleanup. This violates the ecosystem's "Trash, Don't Delete" safety rule and triggers a P0 (Critical) alert from Warden.

**Current code (lines 73-82):**
```bash
try:
    os.replace(temp_name, path)
except Exception as e:
    logger.error(f"Atomic write failed for {path}: {e}")
    if os.path.exists(temp_name):
        try:
            os.unlink(temp_name)  # ← THIS IS THE PROBLEM
        except Exception as cleanup_err:
            logger.warning(f"Failed to cleanup temp file {temp_name}: {cleanup_err}")
    raise
```

---

## Your Task

1. **Add import** at top of file (with other imports):
   ```bash
   from send2trash import send2trash
   ```

2. **Replace os.unlink** with send2trash:
   ```bash
   send2trash(temp_name)
   ```

3. **Update the warning message** to reflect new behavior:
   ```bash
   logger.warning(f"Failed to trash temp file {temp_name}: {cleanup_err}")
   ```

---

## 🎯 [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)

- [x] **Import Added:** `from send2trash import send2trash` appears in imports section
- [x] **Function Replaced:** `os.unlink(temp_name)` is now `send2trash(temp_name)`
- [x] **Message Updated:** Warning says "trash" not "cleanup"
- [x] **No Other Changes:** Only these specific lines modified
- [x] **Syntax Valid:** File has no Python syntax errors (`python -m py_compile scaffold/review.py`)

---

## FLOOR MANAGER PROTOCOL

Do not sign off until every [ ] is marked [x]. Verify by:
```bash
# Check import exists
grep -n "from send2trash import send2trash" scaffold/review.py

# Check os.unlink is gone
grep -n "os.unlink" scaffold/review.py
# Expected: No matches (or only in comments)

# Check send2trash is used
grep -n "send2trash(temp_name)" scaffold/review.py

# Syntax check
doppler run -- python -m py_compile scaffold/review.py && echo "Syntax OK"
```

If any item fails, provide the specific error to the Worker and demand a retry (Max 3 attempts).

---

**Estimated time:** 10 minutes
