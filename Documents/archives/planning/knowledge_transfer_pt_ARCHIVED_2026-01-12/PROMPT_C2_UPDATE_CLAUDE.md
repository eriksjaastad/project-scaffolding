# Prompt C2: Update CLAUDE.md - Replace $SCAFFOLDING with Relative Paths

**Task:** Update CLAUDE.md to use relative paths instead of $SCAFFOLDING references
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b
**Dependencies:** A1, A2, A4 (files must be copied first)

---

## CONSTRAINTS (READ FIRST)

- REPLACE all `$SCAFFOLDING/` references with relative paths (`./`)
- USE `./scripts/` for scripts (runs from project root)
- USE `./Documents/` for documentation
- DO NOT break markdown formatting
- PRESERVE all other content

---

## [ACCEPTANCE CRITERIA]

- [x] No `$SCAFFOLDING` references remain in CLAUDE.md
- [x] All script paths use `./scripts/` format
- [x] All document paths use `./Documents/` format
- [x] File is valid markdown
- [x] grep for "$SCAFFOLDING" returns nothing

---

## Architecture Decision (Reference)

**We use RELATIVE PATHS, not variables:**
- Correct: `python ./scripts/warden_audit.py`
- Wrong: `python $SCAFFOLDING/scripts/warden_audit.py`
- Wrong: `python $PROJECT/scripts/warden_audit.py`

**Why:** Simplest, no environment variable resolution needed, works immediately after git clone.

---

## Task

**Step 1: Find all $SCAFFOLDING references**

```bash
grep -n "\$SCAFFOLDING" [USER_HOME]/projects/project-tracker/CLAUDE.md
```

**Step 2: Replace each reference**

Common replacements:
| Old (find this) | New (replace with) |
|-----------------|-------------------|
| `$SCAFFOLDING/scripts/warden_audit.py` | `./scripts/warden_audit.py` |
| `$SCAFFOLDING/scripts/validate_project.py` | `./scripts/validate_project.py` |
| `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md` | `./Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md` |
| `$SCAFFOLDING/patterns/` | `./Documents/patterns/` |
| `$SCAFFOLDING/Documents/reference/LOCAL_MODEL_LEARNINGS.md` | `./Documents/reference/LOCAL_MODEL_LEARNINGS.md` |

Use sed or manual edit:
```bash
sed -i '' 's|\$SCAFFOLDING/scripts/|./scripts/|g' [USER_HOME]/projects/project-tracker/CLAUDE.md
sed -i '' 's|\$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md|./Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md|g' [USER_HOME]/projects/project-tracker/CLAUDE.md
sed -i '' 's|\$SCAFFOLDING/patterns/|./Documents/patterns/|g' [USER_HOME]/projects/project-tracker/CLAUDE.md
sed -i '' 's|\$SCAFFOLDING/Documents/|./Documents/|g' [USER_HOME]/projects/project-tracker/CLAUDE.md
sed -i '' 's|\$SCAFFOLDING/|./|g' [USER_HOME]/projects/project-tracker/CLAUDE.md
```

---

## Verification

```bash
cd [USER_HOME]/projects/project-tracker

# 1. No $SCAFFOLDING references remain
grep "\$SCAFFOLDING" CLAUDE.md
# Should return nothing (exit code 1)

# 2. File still valid (spot check)
head -50 CLAUDE.md
# Should show valid markdown

# 3. Paths look correct
grep -E "\./scripts/|\./Documents/" CLAUDE.md
# Should show the new relative paths
```

---

## Result

- [x] PASS: All references updated, verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
