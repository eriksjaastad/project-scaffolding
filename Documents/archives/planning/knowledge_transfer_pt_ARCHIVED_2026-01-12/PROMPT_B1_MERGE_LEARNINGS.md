# Prompt B1: Merge LOCAL_MODEL_LEARNINGS.md

**Task:** Copy LOCAL_MODEL_LEARNINGS.md from scaffolding and merge with existing MODEL_LEARNINGS.md
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT delete existing MODEL_LEARNINGS.md content
- MERGE both files - keep content from both
- CREATE reference/ directory if it doesn't exist
- PRESERVE formatting and structure

---

## [ACCEPTANCE CRITERIA]

- [x] reference/ directory exists in project-tracker/Documents/
- [x] LOCAL_MODEL_LEARNINGS.md exists in project-tracker/Documents/reference/
- [x] Contains content from BOTH source files (scaffolding + existing project-tracker)
- [x] File is readable and well-formatted

---

## Task

**Step 1: Check if existing file exists**

```bash
ls -la [USER_HOME]/projects/project-tracker/Documents/reference/MODEL_LEARNINGS.md
```

**Step 2: Ensure directory exists**

```bash
mkdir -p [USER_HOME]/projects/project-tracker/Documents/reference
```

**Step 3: Copy scaffolding version**

```bash
cp [USER_HOME]/projects/project-scaffolding/Documents/reference/LOCAL_MODEL_LEARNINGS.md \
   [USER_HOME]/projects/project-tracker/Documents/reference/LOCAL_MODEL_LEARNINGS.md
```

**Step 4: If MODEL_LEARNINGS.md exists, merge content**

If project-tracker already has MODEL_LEARNINGS.md:
- Read both files
- Combine unique sections
- Keep the scaffolding structure (it's more comprehensive)
- Append any project-tracker specific learnings to the appropriate sections

If no existing file, just use the copied file as-is.

---

## Verification

```bash
cd [USER_HOME]/projects/project-tracker

# 1. File exists
ls -la Documents/reference/LOCAL_MODEL_LEARNINGS.md

# 2. File has content
wc -l Documents/reference/LOCAL_MODEL_LEARNINGS.md
# Should have substantial content (100+ lines)

# 3. File is readable
head -30 Documents/reference/LOCAL_MODEL_LEARNINGS.md
# Should show formatted markdown
```

---

## Result

- [x] PASS: File created/merged and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
