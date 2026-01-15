# Prompt 1.4: Add Validation to .cursorrules Template

**Task:** Add code validation to Definition of Done and add validation command to Execution Commands
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT rewrite the entire file - use StrReplace
- ADD one item to Definition of Done
- ADD one command example to Execution Commands
- UPDATE Related Files section
- KEEP formatting consistent

---

## [ACCEPTANCE CRITERIA]

- [ ] Validation added to Definition of Done
- [ ] Validation command added to Execution Commands
- [ ] Related Files section references review protocol
- [ ] Uses $SCAFFOLDING variable
- [ ] File structure intact

---

## Code to Add (Use StrReplace)

**Change 1: Update Definition of Done**

**old_string:**
```markdown
## 📋 Definition of Done (Project-Specific)

- [ ] Code follows project coding standards (see below)
- [ ] Changes logged to `[relevant log file if applicable]`
- [ ] Documentation updated (if user-facing changes)
- [ ] Tests pass: `[specific test command]`
- [ ] **Index updated** (if new patterns, components, or major structure changes)
```bash

**new_string:**
```markdown
## 📋 Definition of Done (Project-Specific)

- [ ] Code follows project coding standards (see below)
- [ ] Code validated (no hardcoded paths, no secrets exposed)
- [ ] Changes logged to `[relevant log file if applicable]`
- [ ] Documentation updated (if user-facing changes)
- [ ] Tests pass: `[specific test command]`
- [ ] **Index updated** (if new patterns, components, or major structure changes)
```bash

---

**Change 2: Add to Execution Commands**

**old_string:**
```markdown
## 🚀 Execution Commands

```bash
# Environment
source venv/bin/activate

# Run tests
[your test command]

# Run main script
[your run command]
```
```bash

**new_string:**
```markdown
## 🚀 Execution Commands

```bash
# Environment
source venv/bin/activate

# Validate project (before commits)
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" [project-name]

# Run tests
[your test command]

# Run main script
[your run command]
```
```bash

---

**Change 3: Update Related Files**

**old_string:**
```markdown
## 🔗 Related Files

- **Ecosystem Constitution:** `AGENTS.md`
- **Review Protocol:** `REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- **Project Index:** `[[00_Index_[project-name]]]`
- [Add project-specific references]
```bash

**new_string:**
```markdown
## 🔗 Related Files

- **Ecosystem Constitution:** `AGENTS.md`
- **Review Protocol:** `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- **Code Review Pattern:** `$SCAFFOLDING/patterns/code-review-standard.md`
- **Project Index:** `[[00_Index_[project-name]]]`
- [Add project-specific references]
```bash

---

## Verification

After implementing, verify:

```bash
# 1. DoD updated
grep "Code validated" templates/.cursorrules-template
# Should find the new line

# 2. Command added
grep "validate_project.py" templates/.cursorrules-template
# Should find the validation command

# 3. Related files updated
grep "code-review-standard.md" templates/.cursorrules-template
# Should find the pattern reference
```

---

## Result

- [ ] PASS: Changes added, verification succeeds
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**
