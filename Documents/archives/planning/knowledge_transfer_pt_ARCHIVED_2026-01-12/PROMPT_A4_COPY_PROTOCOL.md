# Prompt A4: Copy REVIEWS_AND_GOVERNANCE_PROTOCOL.md

**Task:** Copy review protocol document from project-scaffolding to project-tracker
**Estimated Time:** 3-5 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT use symlinks - make actual copy
- DO NOT modify content
- ENSURE destination directory exists
- COPY exactly as-is

---

## [ACCEPTANCE CRITERIA]

- [x] File copied to project-tracker/Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
- [x] Content is identical to source
- [x] File is readable

---

## Task

Copy this file:

**Source:** `/Users/eriksjaastad/projects/project-scaffolding/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
**Destination:** `/Users/eriksjaastad/projects/project-tracker/Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`

Use:
```bash
cp /Users/eriksjaastad/projects/project-scaffolding/REVIEWS_AND_GOVERNANCE_PROTOCOL.md \
   /Users/eriksjaastad/projects/project-tracker/Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
```

---

## Verification

```bash
cd /Users/eriksjaastad/projects/project-tracker

# 1. File exists
ls -la Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md

# 2. File is readable
head -20 Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
# Should show first 20 lines

# 3. Compare sizes (should match)
wc -l /Users/eriksjaastad/projects/project-scaffolding/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
wc -l Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
# Line counts should match
```

---

## Result

- [x] PASS: File copied and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
