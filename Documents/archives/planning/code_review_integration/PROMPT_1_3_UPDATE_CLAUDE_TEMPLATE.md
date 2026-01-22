# Prompt 1.3: Add Code Review Section to CLAUDE.md Template

**Task:** Add "Code Review and Validation" section explaining review workflow and validation commands
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT rewrite the entire file - use StrReplace
- INSERT new section after "Validation Commands" section
- KEEP formatting consistent with template style
- USE $SCAFFOLDING variable for paths

---

## [ACCEPTANCE CRITERIA]

- [ ] New "Code Review and Validation" section added
- [ ] When to review documented
- [ ] How to request review documented with commands
- [ ] How to validate documented with commands
- [ ] Section placed logically (after "Validation Commands")

---

## Code to Add (Use StrReplace)

**old_string (find this in CLAUDE.md.template):**
```markdown
---

## Common Patterns

[Provide frequently-used code patterns specific to your project]
```bash

**new_string:**
```markdown
---

## Code Review and Validation

### When to Request a Code Review

Request architectural review, security audit, or performance analysis when:
- Making significant architectural decisions
- Implementing security-critical code paths
- Before merging major features
- When unsure about design approach

### How to Request a Review

**Step 1: Create review request**
```bash
# Use the template
cp "$SCAFFOLDING/templates/CODE_REVIEW.md.template" ./CODE_REVIEW_REQUEST.md

# Edit CODE_REVIEW_REQUEST.md:
# - Fill out "Definition of Done" section
# - Describe what you want reviewed
# - Specify review focus (architecture/security/performance)
```

**Step 2: Run multi-AI review**
```bash
cd "$SCAFFOLDING"
source venv/bin/activate
doppler run -- python scaffold_cli.py review --type document --input /path/to/your/CODE_REVIEW_REQUEST.md --round 1
```

**Step 3: Review results**
- Reviews saved to: `$SCAFFOLDING/review_outputs/round_1/CODE_REVIEW_*.md`
- Copy relevant reviews to: `Documents/archives/reviews/`

### How to Validate Your Work

Run validation to check for common issues:

```bash
# Quick safety check (< 1 second)
doppler run -- python "$SCAFFOLDING/scripts/warden_audit.py" --root . --fast

# Full project validation
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**What validation catches:**
- ✅ Hardcoded absolute paths (`[absolute_path]/...`, `/home/...`)
- ✅ Exposed secrets (API keys like `sk-...`, `AIza...`)
- ✅ Missing required files (00_Index_*.md, AGENTS.md, etc.)
- ✅ Invalid project structure

**Best practice:** Validate before major commits or before requesting code reviews.

### Learn More

- **Full Protocol:** `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- **Pattern Docs:** `$SCAFFOLDING/patterns/code-review-standard.md`
- **Review Prompts:** `$SCAFFOLDING/prompts/active/document_review/`

---

## Common Patterns

[Provide frequently-used code patterns specific to your project]
```bash

---

## Verification

After implementing, verify:

```bash
# 1. Section exists
grep -n "Code Review and Validation" templates/CLAUDE.md.template
# Should return line number around 197-200

# 2. Commands included
grep "validate_project.py" templates/CLAUDE.md.template
grep "scaffold_cli.py review" templates/CLAUDE.md.template
# Both should be found

# 3. Structure intact
grep -n "## Common Patterns" templates/CLAUDE.md.template
# Should return line number (should be ~50 lines after new section)
```

---

## Result

- [ ] PASS: Section added, verification succeeds
- [ ] FAIL: Describe error

**Hand back to Floor Manager when complete.**


## Related Documentation

- [[CODE_REVIEW_ANTI_PATTERNS]] - code review
- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[LOCAL_MODEL_LEARNINGS]] - local AI
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure

