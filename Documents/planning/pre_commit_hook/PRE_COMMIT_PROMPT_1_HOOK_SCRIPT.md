# Worker Task: Create Pre-Commit Hook

**Worker Model:** Qwen 2.5 Coder (preferred) or DeepSeek-R1
**Objective:** Create a git pre-commit hook that runs Warden to block commits with safety violations

---

## ⚠️ DOWNSTREAM HARM ESTIMATE

- **If this fails:** No pre-commit hook exists. Commits with dangerous code (os.remove, hardcoded paths) can slip through. Recovery: Just re-run the task.
- **Known pitfalls:**
  - Hook must be executable (chmod +x)
  - Must use correct shebang for portability
  - Exit codes matter: 0 = allow commit, non-zero = block
- **Timeout:** 120s (this is a small file creation, not file-heavy)

---

## 📚 LEARNINGS APPLIED

- [x] Consulted LOCAL_MODEL_LEARNINGS.md (date: Jan 10, 2026)
- [x] Task is micro-level (~10 min) - appropriate for local models
- [x] Creating new file (not modifying) - no StrReplace needed
- [x] Explicit constraints included below

---

## CONSTRAINTS (READ FIRST)

- DO NOT modify any existing files
- DO NOT use Python for the hook script - use bash for simplicity
- DO NOT add complex logic - just call warden and pass through exit code
- COPY the code template below exactly

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] **Code Provided:** Worker provides complete bash script for pre-commit hook
- [ ] **Shebang:** Starts with `#!/usr/bin/env bash`
- [ ] **Calls Warden:** Script runs `python scripts/warden_audit.py --root . --fast`
- [ ] **Exit Code Logic:** Passes through Warden's exit code (0 = success, 1 = failure)
- [ ] **Skip Flag:** Mentions `--no-verify` git flag in comments
- [ ] **Output:** Shows what Warden found before blocking/allowing

---

## Exact Code to Provide

Provide this code for the Floor Manager to write to `.git/hooks/pre-commit`:

```bash
#!/usr/bin/env bash
#
# Pre-commit hook: Run Warden safety audit before allowing commits
# Blocks commits if Warden finds P0/P1 violations
#
# To skip in emergencies: git commit --no-verify
#

set -euo pipefail

echo "Running Warden safety audit..."
echo "================================"

# Run warden in fast mode
# Exit code 0 = clean, exit code 1 = violations found
python scripts/warden_audit.py --root . --fast

WARDEN_EXIT=$?

if [ $WARDEN_EXIT -ne 0 ]; then
    echo "================================"
    echo "COMMIT BLOCKED: Warden found safety violations"
    echo "Fix the issues above or use 'git commit --no-verify' to skip (emergency only)"
    exit 1
fi

echo "================================"
echo "Warden audit passed. Proceeding with commit."
exit 0
```

---

## Verification Steps (For Floor Manager)

1. **Write file:** Write the code above to `.git/hooks/pre-commit`
2. **Make executable:** `chmod +x .git/hooks/pre-commit`
3. **Test:** Run `.git/hooks/pre-commit` and verify exit codes.

---

## FLOOR MANAGER PROTOCOL

1. Do not sign off until every [ ] is marked [x]
2. If any item fails, provide the specific error to the Worker and retry (Max 3 attempts)
3. **After any failure:** Ask "Was this preventable?" If a documented learning was ignored, log it in LOCAL_MODEL_LEARNINGS.md → Learning Debt Tracker

**This is a Learning Loop Pattern test.** Document the outcome regardless of success/failure.
