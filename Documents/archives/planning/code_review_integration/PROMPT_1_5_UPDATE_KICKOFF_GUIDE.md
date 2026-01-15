# Prompt 1.5: Add Validation Step to PROJECT_KICKOFF_GUIDE.md

**Task:** Add "Step 6: Validate Your Setup" section after Step 5 (Initialize Git)
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT rewrite the entire file - use StrReplace
- INSERT new Step 6 after Step 4 (Initialize Git)
- KEEP formatting consistent with existing steps
- USE $SCAFFOLDING variable for paths

---

## [ACCEPTANCE CRITERIA]

- [ ] New Step 6 added after Step 4
- [ ] Validation command documented
- [ ] Example output shown (clean vs issues)
- [ ] References to validation docs included
- [ ] File structure intact

---

## Code to Add (Use StrReplace)

**old_string (find this in PROJECT_KICKOFF_GUIDE.md):**
```markdown
### Step 4: Initialize Git

```bash
git init
git add -A
git commit -m "Initial commit: Project structure from scaffolding

- Added project index (mandatory)
- Copied scaffolding templates
- Ready for development"
```

**Verify index exists:**
ls -la 00_Index_*.md
# Should show: 00_Index_[YourProject].md
---
## Starting a Chat Session with AI
```bash

**new_string:**
```markdown
### Step 4: Initialize Git

```bash
git init
git add -A
git commit -m "Initial commit: Project structure from scaffolding

- Added project index (mandatory)
- Copied scaffolding templates
- Ready for development"
```

**Verify index exists:**
ls -la 00_Index_*.md
# Should show: 00_Index_[YourProject].md

---

### Step 5: Validate Your Setup

Run validation to ensure your project structure is correct:

```bash
# Validate project (from any directory)
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**What validation checks:**
- ✅ Required files present (00_Index_*.md, AGENTS.md, CLAUDE.md, .cursorrules, etc.)
- ✅ Project index has valid YAML frontmatter and required sections
- ✅ **DNA Integrity:** No hardcoded absolute paths (`[absolute_path]/...`, `/home/...`)
- ✅ **Security:** No exposed secrets (API keys like `sk-...`, `AIza...`)
- ✅ Mandatory directories exist (Documents/, etc.)

**Example output (clean project):**
```bash
✅ my-new-project (Fully Compliant)
```

**Example output (issues found):**
```bash
⚠️ my-new-project
   - Missing mandatory file: .cursorrules
   - Index file: Missing required section: ## Status
```

**Fix any issues and re-run validation until clean.**

**Ongoing validation:** Run validation periodically during development, especially before major commits or code reviews.

**Learn more:**
- **Full validation script:** `$SCAFFOLDING/scripts/validate_project.py`
- **Quick safety check:** `$SCAFFOLDING/scripts/warden_audit.py --root . --fast`
- **Review system:** See QUICKSTART.md Phase 6 for code review workflow

---
## Starting a Chat Session with AI
```bash

---

## Verification

After implementing, verify:

```bash
# 1. Step 5 exists
grep -n "Step 5: Validate Your Setup" Documents/PROJECT_KICKOFF_GUIDE.md
# Should return line number around 110-115

# 2. Validation command included
grep "validate_project.py" Documents/PROJECT_KICKOFF_GUIDE.md
# Should find the command

# 3. Structure intact ("Starting a Chat Session" still exists)
grep -n "## Starting a Chat Session with AI" Documents/PROJECT_KICKOFF_GUIDE.md
# Should return line number (should be ~40 lines after Step 5)
```

---

## Result

- [ ] PASS: Step added, verification succeeds
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
