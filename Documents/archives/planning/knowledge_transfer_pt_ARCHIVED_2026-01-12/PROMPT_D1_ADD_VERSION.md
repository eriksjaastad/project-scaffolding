# Prompt D1: Add scaffolding_version Metadata

**Task:** Add scaffolding_version to project-tracker's index file for drift tracking
**Estimated Time:** 3-5 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b
**Dependencies:** All A, B, C tasks complete

---

## CONSTRAINTS (READ FIRST)

- ADD version metadata, do not remove existing content
- USE format: `scaffolding_version: X.X.X`
- PLACE in frontmatter or metadata section of index file
- PRESERVE all existing content

---

## [ACCEPTANCE CRITERIA]

- [x] scaffolding_version field exists in 00_Index_project-tracker.md
- [x] Version is set to current scaffolding version (1.0.0 for initial transfer)
- [x] Field is easily grep-able for drift detection
- [x] Existing index content preserved

---

## Context

**Why version tracking:**
- Enables drift detection (which projects are behind)
- Supports future sync bot (knows what version each project has)
- Documents when transfer occurred

**Version format:** `MAJOR.MINOR.PATCH`
- 1.0.0 = Initial transfer (today)
- Future updates increment as scaffolding improves

---

## Task

**Step 1: Find the index file**

```bash
ls -la [USER_HOME]/projects/project-tracker/00_Index*.md
```

**Step 2: Add version metadata**

Add this block near the top of the file (after title, before main content):

```markdown
---
## Scaffolding Metadata

| Field | Value |
|-------|-------|
| scaffolding_version | 1.0.0 |
| transferred_date | 2026-01-12 |
| source | project-scaffolding |

---
```

Or if the file uses YAML frontmatter, add:
```yaml
scaffolding_version: 1.0.0
transferred_date: 2026-01-12
```

---

## Verification

```bash
cd [USER_HOME]/projects/project-tracker

# 1. Version field exists
grep "scaffolding_version" 00_Index*.md
# Should return: scaffolding_version: 1.0.0

# 2. File still valid
head -30 00_Index*.md
# Should show valid markdown with new metadata
```

---

## Result

- [x] PASS: Version metadata added and verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
