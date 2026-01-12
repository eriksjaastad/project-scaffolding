# Prompt A2: Copy validate_project.py

**Task:** Copy validate_project.py from project-scaffolding to project-tracker
**Estimated Time:** 3-5 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT use symlinks - make actual copy
- DO NOT reference $SCAFFOLDING - file must be local
- PRESERVE execute permissions (chmod +x)
- UPDATE the script's internal PROJECT paths if hardcoded

---

## [ACCEPTANCE CRITERIA]

- [x] File copied to project-tracker/scripts/validate_project.py
- [x] File is executable (has +x permission)
- [x] Script updated to work from project-tracker context
- [x] File runs successfully: `python scripts/validate_project.py --help`

---

## Task

**Step 1: Copy file**

```bash
cp /Users/eriksjaastad/projects/project-scaffolding/scripts/validate_project.py \
   /Users/eriksjaastad/projects/project-tracker/scripts/validate_project.py

chmod +x /Users/eriksjaastad/projects/project-tracker/scripts/validate_project.py
```

**Step 2: Update internal paths**

The script has `PROJECTS_ROOT` environment variable usage - this should still work.
NO changes needed if it uses `os.getenv("PROJECTS_ROOT")`.

If it has hardcoded paths to project-scaffolding, those need updating.

---

## Verification

```bash
cd /Users/eriksjaastad/projects/project-tracker

# 1. File exists
ls -la scripts/validate_project.py
# Should show file with -rwxr-xr-x permissions

# 2. Help works
python scripts/validate_project.py --help
# Should show usage

# 3. Test on project-tracker itself
python scripts/validate_project.py project-tracker
# Should run validation
```

---

## Result

- [x] PASS: File copied and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
