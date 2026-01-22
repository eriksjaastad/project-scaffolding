# Prompt 1.2: Add Code Review to AGENTS.md Template

**Task:** Add code review to Definition of Done and reference validation in constraints
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT rewrite the entire file - use StrReplace
- DO NOT modify existing DoD items
- ADD one item to DoD section
- ADD one item to Constraints section
- KEEP formatting consistent with template style

---

## [ACCEPTANCE CRITERIA]

- [ ] New DoD item added about code review
- [ ] New constraint added about validation
- [ ] References to REVIEWS_AND_GOVERNANCE_PROTOCOL.md included
- [ ] Uses $SCAFFOLDING variable for paths
- [ ] File structure intact

---

## Code to Add (Use StrReplace)

**Change 1: Add to Definition of Done**

**old_string:**
```markdown
## 📋 Definition of Done (DoD)
- [ ] Code is documented with type hints.
- [ ] Technical changes are logged to `project-tracker/data/WARDEN_LOG.yaml` (formerly `_obsidian/WARDEN_LOG.yaml`).
- [ ] `00_Index_*.md` is updated with recent activity.
- [ ] [Project-specific DoD item]
```

**new_string:**
```markdown
## 📋 Definition of Done (DoD)
- [ ] Code is documented with type hints.
- [ ] Technical changes are logged to `project-tracker/data/WARDEN_LOG.yaml` (formerly `_obsidian/WARDEN_LOG.yaml`).
- [ ] `00_Index_*.md` is updated with recent activity.
- [ ] Code validated (no hardcoded paths, no secrets exposed).
- [ ] Code review completed (if significant architectural changes).
- [ ] [Project-specific DoD item]
```

---

**Change 2: Add to Critical Constraints**

**old_string:**
```markdown
## ⚠️ Critical Constraints
- NEVER hard-code API keys, secrets, or credentials in script files. Use `.env` and `os.getenv()`.
- NEVER use absolute paths (e.g., machine-specific paths). ALWAYS use relative paths or `PROJECT_ROOT` env var.
- {constraint_1}
- {constraint_2}
```

**new_string:**
```markdown
## ⚠️ Critical Constraints
- NEVER hard-code API keys, secrets, or credentials in script files. Use `.env` and `os.getenv()`.
- NEVER use absolute paths (e.g., machine-specific paths). ALWAYS use relative paths or `PROJECT_ROOT` env var.
- ALWAYS run validation before considering work complete: `python "$SCAFFOLDING/scripts/validate_project.py" [project-name]`
- {constraint_1}
- {constraint_2}

**Code Review Standards:** See `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md` for full review process.
```

---

## Verification

After implementing, verify:

```bash
# 1. DoD updated
grep -A 3 "Definition of Done" templates/AGENTS.md.template | grep "Code validated"
# Should find the new line

# 2. Constraints updated
grep "validate_project.py" templates/AGENTS.md.template
# Should find the validation command

# 3. Review reference added
grep "REVIEWS_AND_GOVERNANCE_PROTOCOL" templates/AGENTS.md.template
# Should find the reference
```

---

## Result

- [ ] PASS: Changes added, verification succeeds
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**


## Related Documentation

- [[CODE_REVIEW_ANTI_PATTERNS]] - code review
- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[LOCAL_MODEL_LEARNINGS]] - local AI
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure

