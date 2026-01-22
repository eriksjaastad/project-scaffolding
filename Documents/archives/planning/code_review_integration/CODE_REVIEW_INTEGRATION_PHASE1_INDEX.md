# Phase 1: Documentation Updates - Prompts Index

**Goal:** Make code review infrastructure discoverable and documented in all scaffolding templates and documentation

**Created:** January 11, 2026
**Executor:** Floor Manager (via Ollama MCP)
**Worker Models:** qwen2.5-coder:7b (primary), deepseek-r1:14b (backup)

---

## Context

From TODO.md Phase 1:
> We have comprehensive code review infrastructure (review orchestrator, validation scripts, DNA integrity scans, review prompts) but it's trapped in `project-scaffolding` and not documented or accessible to other projects that use the scaffolding.

**The Problem:**
- When scaffolding new projects, we copy templates but NOT the review system
- Projects don't know the code review workflow exists
- The powerful `validate_project.py` script (scans for hardcoded paths, secrets, etc.) only runs FROM scaffolding, not IN projects
- Templates don't reference or document the review infrastructure

**Phase 1 Goal:** Update all key documentation files to reference and explain the code review system.

---

## Done Criteria (Phase 1 Complete)

All must pass for Phase 1 complete:

- [ ] **Task 1.1:** QUICKSTART.md has Phase 6 section on validation and code review
- [ ] **Task 1.2:** AGENTS.md.template includes code review in Definition of Done
- [ ] **Task 1.3:** CLAUDE.md.template has code review and validation instructions
- [ ] **Task 1.4:** .cursorrules-template references code review standards
- [ ] **Task 1.5:** PROJECT_KICKOFF_GUIDE.md includes validation as a setup phase

---

## Prompt Execution Order

Execute prompts in sequence. Each is independent (can be done in any order, but this order makes sense for reviewing):

| # | Prompt File | Description | Est. Time | Status |
|---|-------------|-------------|-----------|--------|
| 1.1 | `PROMPT_1_1_UPDATE_QUICKSTART.md` | Add Phase 6: Validation and Code Review section | 5-10 min | [ ] |
| 1.2 | `PROMPT_1_2_UPDATE_AGENTS_TEMPLATE.md` | Add code review to DoD and constraints | 5-10 min | [ ] |
| 1.3 | `PROMPT_1_3_UPDATE_CLAUDE_TEMPLATE.md` | Add code review and validation section | 5-10 min | [ ] |
| 1.4 | `PROMPT_1_4_UPDATE_CURSORRULES_TEMPLATE.md` | Add validation to DoD and commands | 5-10 min | [ ] |
| 1.5 | `PROMPT_1_5_UPDATE_KICKOFF_GUIDE.md` | Add validation as Step 6 in kickoff | 5-10 min | [ ] |

**Total estimated time:** 25-50 minutes across all tasks

---

## Key Constraints (Apply to ALL Phase 1 Prompts)

These constraints are shared across all Phase 1 tasks:

```markdown
## CONSTRAINTS
- DO NOT rewrite entire files - use StrReplace for targeted changes
- DO NOT modify existing structure - only add new sections
- USE $SCAFFOLDING variable for all paths to scaffolding repo
- KEEP formatting consistent with existing file style
- REFERENCE these docs: REVIEWS_AND_GOVERNANCE_PROTOCOL.md, patterns/code-review-standard.md
```

---

## What We're Documenting

For context, here's what exists in project-scaffolding that needs to be surfaced:

### Validation System
- **Script:** `scripts/validate_project.py` - Validates structure, checks DNA integrity (hardcoded paths, secrets)
- **Quick scan:** `scripts/warden_audit.py --fast` - Fast safety check (< 1 sec)
- **What it catches:** Hardcoded `/Users/` paths, exposed API keys, missing required files

### Code Review System
- **Orchestrator:** `scaffold/review.py` - Multi-AI review (OpenAI, Anthropic, DeepSeek, Ollama)
- **Template:** `templates/CODE_REVIEW.md.template` - Review request format
- **Prompts:** `prompts/active/document_review/` - Architecture, security, performance review prompts
- **Protocol:** `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` - Full review standards
- **Pattern:** `patterns/code-review-standard.md` - Pattern documentation

### Commands to Document
```bash
# Validation
python "$SCAFFOLDING/scripts/validate_project.py" [project-name]
python "$SCAFFOLDING/scripts/warden_audit.py" --root . --fast

# Code review
cd "$SCAFFOLDING"
python scaffold_cli.py review --type document --input [file] --round 1
```

---

## Escalation Protocol

If a Worker times out or fails:

1. **Strike 1:** Retry with same model (qwen2.5-coder:7b)
2. **Strike 2:** Switch model (qwen2.5-coder:7b → deepseek-r1:14b)
3. **Strike 3:** HALT and report to Conductor

**CRITICAL:** DO NOT manually implement failed Worker tasks. That violates AGENTS.md protocol.

---

## Floor Manager Instructions

### How to Execute Phase 1

**For each prompt (1.1 through 1.5):**

1. **Send to Worker via Ollama MCP:**
   ```
   Model: qwen2.5-coder:7b
   Timeout: 300000 (5 minutes - file modification tasks)
   Prompt: [Contents of TASK_X_X file]
   ```

2. **Verify the work:**
   - Run verification commands listed in the prompt
   - Read the modified file to confirm changes
   - Check off acceptance criteria

3. **Sign off or escalate:**
   - ✅ All criteria met: Mark task [x] complete in table above
   - ❌ Failure: Follow 3-Strike Escalation Protocol
   - After Strike 3: HALT, do NOT do the work yourself

4. **Update progress table:**
   - Mark status as [x] when task passes verification
   - Note which worker model succeeded
   - Document any issues in Notes column

### After All Tasks Complete

Run final verification to ensure Phase 1 is truly done:

```bash
# 1. Check all files modified
grep -l "validation\|code review" \
  QUICKSTART.md \
  templates/AGENTS.md.template \
  templates/CLAUDE.md.template \
  templates/.cursorrules-template \
  Documents/PROJECT_KICKOFF_GUIDE.md

# Should return all 5 files

# 2. Verify no broken references
for file in QUICKSTART.md templates/*.template Documents/PROJECT_KICKOFF_GUIDE.md; do
  echo "Checking $file..."
  grep -o '\$SCAFFOLDING/[^)]*' "$file" | while read path; do
    real_path="${path#\$SCAFFOLDING/}"
    if [ ! -e "$real_path" ]; then
      echo "  BROKEN: $path"
    fi
  done
done

# Should show no BROKEN links
```

**Only after this passes:** Mark Phase 1 [x] Complete below and report to Conductor.

---

## Progress Tracking

| Prompt | Status | Worker Model | Strikes | Notes |
|--------|--------|--------------|---------|-------|
| 1.1 | [x] | qwen2.5-coder:7b | 0 | Added Phase 6 section to QUICKSTART.md |
| 1.2 | [x] | qwen2.5-coder:7b | 0 | Added DoD + validation constraint to AGENTS template |
| 1.3 | [x] | qwen2.5-coder:7b | 0 | Added Code Review & Validation section to CLAUDE template |
| 1.4 | [x] | qwen2.5-coder:7b | 0 | Added validation + review refs to .cursorrules template |
| 1.5 | [x] | qwen2.5-coder:7b | 0 | Added validation step to PROJECT_KICKOFF_GUIDE.md |

**Phase 1 Status:** [ ] Not Started / [x] In Progress / [ ] Complete

---

## Related Documents

- **Parent task list:** `TODO.md` (Code Review Infrastructure Integration section)
- **Learnings:** `Documents/reference/LOCAL_MODEL_LEARNINGS.md`
- **Protocol:** `AGENTS.md` (Hierarchy and workflow)
- **Review standards:** `REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- **Pattern docs:** `patterns/code-review-standard.md`

---

**Hand to Floor Manager to begin Phase 1 execution.**


## Related Documentation

- [[CODE_REVIEW_ANTI_PATTERNS]] - code review
- [[DOPPLER_SECRETS_MANAGEMENT]] - secrets management
- [[LOCAL_MODEL_LEARNINGS]] - local AI
- [[PROJECT_KICKOFF_GUIDE]] - project setup
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure

