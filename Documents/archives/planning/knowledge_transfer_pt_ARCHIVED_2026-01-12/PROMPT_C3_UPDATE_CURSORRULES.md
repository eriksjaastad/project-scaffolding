# Prompt C3: Update .cursorrules - Replace $SCAFFOLDING with Relative Paths

**Task:** Update .cursorrules to use relative paths instead of $SCAFFOLDING references
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b
**Dependencies:** A1, A2, A4, A5 (files must be copied first)

---

## CONSTRAINTS (READ FIRST)

- REPLACE all `$SCAFFOLDING/` references with relative paths (`./`)
- USE `./scripts/` for scripts (runs from project root)
- USE `./Documents/` for documentation
- DO NOT break the cursorrules format
- PRESERVE all other content (especially safety rules)

---

## [ACCEPTANCE CRITERIA]

- [x] No `$SCAFFOLDING` references remain in .cursorrules
- [x] All script paths use `./scripts/` format
- [x] All document paths use `./Documents/` format
- [x] File format is intact (cursorrules still works)
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
grep -n "\$SCAFFOLDING" /Users/eriksjaastad/projects/project-tracker/.cursorrules
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
sed -i '' 's|\$SCAFFOLDING/scripts/|./scripts/|g' /Users/eriksjaastad/projects/project-tracker/.cursorrules
sed -i '' 's|\$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md|./Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md|g' /Users/eriksjaastad/projects/project-tracker/.cursorrules
sed -i '' 's|\$SCAFFOLDING/patterns/|./Documents/patterns/|g' /Users/eriksjaastad/projects/project-tracker/.cursorrules
sed -i '' 's|\$SCAFFOLDING/Documents/|./Documents/|g' /Users/eriksjaastad/projects/project-tracker/.cursorrules
sed -i '' 's|\$SCAFFOLDING/|./|g' /Users/eriksjaastad/projects/project-tracker/.cursorrules
```

---

## Verification

```bash
cd /Users/eriksjaastad/projects/project-tracker

# 1. No $SCAFFOLDING references remain
grep "\$SCAFFOLDING" .cursorrules
# Should return nothing (exit code 1)

# 2. File still valid (spot check)
head -50 .cursorrules
# Should show valid content

# 3. Paths look correct
grep -E "\./scripts/|\./Documents/" .cursorrules
# Should show the new relative paths
```

---

## Result

- [x] PASS: All references updated, verified
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
