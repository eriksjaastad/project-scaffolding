# Prompt 1.1: Add Code Review Section to QUICKSTART.md

**Task:** Add "Phase 6: Validation and Code Review" section to QUICKSTART.md
**Estimated Time:** 5-10 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b

---

## CONSTRAINTS (READ FIRST)

- DO NOT rewrite the entire file - use StrReplace
- DO NOT modify existing phases
- INSERT between Phase 5 and "Existing Project Checklist"
- KEEP formatting consistent with existing sections

---

## [ACCEPTANCE CRITERIA]

- [ ] Section added after Phase 5 (around line 177)
- [ ] Validation workflow documented with commands
- [ ] Code review workflow documented with commands
- [ ] Links to REVIEWS_AND_GOVERNANCE_PROTOCOL.md and patterns/code-review-standard.md
- [ ] File structure intact

---

## Code to Add (Use StrReplace)

**old_string (find this in QUICKSTART.md):**
```markdown
**Reference:** `Documents/PROJECT_KICKOFF_GUIDE.md` for detailed planning workflow

---

## Existing Project Checklist
```bash

**new_string (replace with this):**

```markdown
---

### Phase 6: Validation and Code Review

Once your project is set up, use the scaffolding's validation and review infrastructure to ensure quality.

#### Validate Your Project Structure

**Command:**
```bash
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**What it checks:**
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
   - DNA Defect: Absolute path found in scripts/helper.py
```

**Fix issues and re-run validation until clean.**

---

#### Request Code Reviews

When you're ready for architectural review, security audit, or performance analysis:

**Step 1: Create review request**
```bash
# Use the template
cp "$SCAFFOLDING/templates/CODE_REVIEW.md.template" ./CODE_REVIEW_REQUEST.md

# Edit CODE_REVIEW_REQUEST.md:
# - Fill out "Definition of Done" section (what makes this code "done"?)
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
- Cost summary: `$SCAFFOLDING/review_outputs/round_1/COST_SUMMARY.json`

**Step 4: Archive in your project**
```bash
# Copy the most relevant review to your project
cp "$SCAFFOLDING/review_outputs/round_1/CODE_REVIEW_CLAUDE_SONNET.md" \
   ./Documents/archives/reviews/
```

---

#### Ongoing Validation During Development

Run validation periodically as you build:

```bash
# Quick check (< 1 second)
doppler run -- python "$SCAFFOLDING/scripts/warden_audit.py" --root . --fast

# Full validation
doppler run -- python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**Best practice:** Validate before major commits or before requesting code reviews.

---

#### Learn More About Code Review System

- **Full Protocol:** `$SCAFFOLDING/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- **Pattern Documentation:** `$SCAFFOLDING/patterns/code-review-standard.md`
- **Review Prompts:** `$SCAFFOLDING/prompts/active/document_review/` (architecture, security, performance)
- **Multi-AI Orchestrator:** `$SCAFFOLDING/scaffold/review.py` (supports OpenAI, Anthropic, DeepSeek, Ollama)

**Key principle:** The review system is centralized in `project-scaffolding` to maintain consistency across all your projects. Projects reference and use it via `$SCAFFOLDING` commands.

---
```bash

---

## Verification

After implementing, verify:

```bash
# 1. Section exists
grep -n "Phase 6: Validation and Code Review" QUICKSTART.md
# Should return line number around 178-180

# 2. Structure intact
grep -n "## Existing Project Checklist" QUICKSTART.md
# Should return line number (should be ~80 lines after Phase 6)

# 3. Links valid
ls -la REVIEWS_AND_GOVERNANCE_PROTOCOL.md patterns/code-review-standard.md
# Both should exist
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

