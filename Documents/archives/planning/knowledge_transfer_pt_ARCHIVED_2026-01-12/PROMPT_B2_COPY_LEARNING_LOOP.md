# Prompt B2: Copy learning-loop-pattern.md

**Task:** Copy learning loop pattern document from project-scaffolding to project-tracker
**Estimated Time:** 3-5 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT use symlinks - make actual copy
- DO NOT modify content
- CREATE patterns/ directory if it doesn't exist
- COPY exactly as-is

---

## [ACCEPTANCE CRITERIA]

- [x] patterns/ directory exists in project-tracker/Documents/
- [x] File copied to project-tracker/Documents/patterns/learning-loop-pattern.md
- [x] Content is identical to source
- [x] File is readable

---

## Task

**Step 1: Ensure directory exists**

```bash
mkdir -p [USER_HOME]/projects/project-tracker/Documents/patterns
```

**Step 2: Copy file**

**Source:** `[USER_HOME]/projects/project-scaffolding/patterns/learning-loop-pattern.md`
**Destination:** `[USER_HOME]/projects/project-tracker/Documents/patterns/learning-loop-pattern.md`

```bash
cp [USER_HOME]/projects/project-scaffolding/patterns/learning-loop-pattern.md \
   [USER_HOME]/projects/project-tracker/Documents/patterns/learning-loop-pattern.md
```

---

## Verification

```bash
cd [USER_HOME]/projects/project-tracker

# 1. Directory exists
ls -la Documents/patterns/

# 2. File exists
ls -la Documents/patterns/learning-loop-pattern.md

# 3. File is readable
head -20 Documents/patterns/learning-loop-pattern.md
# Should show first 20 lines
```

---

## Result

- [x] PASS: File copied and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
