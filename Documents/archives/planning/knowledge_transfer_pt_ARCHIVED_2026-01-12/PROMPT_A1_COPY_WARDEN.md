# Prompt A1: Copy warden_audit.py

**Task:** Copy warden_audit.py from project-scaffolding to project-tracker
**Estimated Time:** 3-5 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT use symlinks - make actual copy
- DO NOT reference $SCAFFOLDING - file must be local
- PRESERVE execute permissions (chmod +x)
- COPY exactly as-is (no modifications)

---

## [ACCEPTANCE CRITERIA]

- [x] File copied to project-tracker/scripts/warden_audit.py
- [x] File is executable (has +x permission)
- [x] File runs successfully: `python scripts/warden_audit.py --help`
- [x] No modifications to original content

---

## Task

Copy this file:

**Source:** `[USER_HOME]/projects/project-scaffolding/scripts/warden_audit.py`
**Destination:** `[USER_HOME]/projects/project-tracker/scripts/warden_audit.py`

Use:
```bash
cp [USER_HOME]/projects/project-scaffolding/scripts/warden_audit.py \
   [USER_HOME]/projects/project-tracker/scripts/warden_audit.py

chmod +x [USER_HOME]/projects/project-tracker/scripts/warden_audit.py
```

---

## Verification

```bash
cd [USER_HOME]/projects/project-tracker

# 1. File exists
ls -la scripts/warden_audit.py
# Should show file with -rwxr-xr-x permissions

# 2. File runs
doppler run -- python scripts/warden_audit.py --help
# Should show help text

# 3. Quick test
doppler run -- python scripts/warden_audit.py --root . --fast
# Should run without errors
```

---

## Result

- [x] PASS: File copied and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
