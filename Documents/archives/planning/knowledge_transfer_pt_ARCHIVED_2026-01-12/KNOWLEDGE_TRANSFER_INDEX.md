# Knowledge Transfer: project-tracker - Prompts Index

**Feature:** Transfer code review infrastructure from project-scaffolding to project-tracker (make standalone)
**Created:** January 12, 2026
**Executor:** Floor Manager (via Ollama MCP)
**Worker Models:** qwen2.5-coder:7b (primary), deepseek-r1:14b (backup)

---

## Context

From TODO.md:
> We built comprehensive code review infrastructure (validation tools, review orchestrator, patterns, protocols) but haven't properly transferred it to existing projects. project-tracker still references `$SCAFFOLDING/...` paths instead of having its own copies.

**The Architecture:** project-scaffolding is a TEMPLATE GENERATOR (like Create React App). Tools and patterns get COPIED to projects, not called from scaffolding. Projects must be standalone.

**Current State:**
- project-tracker references `$SCAFFOLDING/scripts/...` (WRONG - implies runtime dependency)
- project-tracker lacks validation/review tools locally
- If someone clones project-tracker from GitHub, review tools won't work

**Goal:** Make project-tracker fully standalone with all code review infrastructure.

---

## Done Criteria (Overall Transfer)

All must pass for transfer complete:

- [x] **A1: Copy warden_audit.py** - Security audit tool in project-tracker/scripts/
- [x] **A2: Copy validate_project.py** - Structure validation in project-tracker/scripts/
- [x] **A3: Create pre_review_scan.sh** - Pre-commit hook script
- [x] **A4: Copy REVIEWS_AND_GOVERNANCE_PROTOCOL.md** - Review standards doc
- [x] **A5: Copy code-review-standard.md** - Pattern documentation
- [x] **B1: Merge LOCAL_MODEL_LEARNINGS.md** - Combine learnings
- [x] **B2: Copy learning-loop-pattern.md** - Learning pattern doc
- [x] **C1: Update AGENTS.md** - Remove $SCAFFOLDING references
- [x] **C2: Update CLAUDE.md** - Reference local files
- [x] **C3: Update .cursorrules** - Reference local files
- [x] **D1: Add scaffolding_version metadata** - Track sync status
- [x] **E1: Verify standalone** - Test without scaffolding available

---

## Prompt Execution Order

Execute prompts in sequence. Some can be parallelized (noted below).

|| # | Prompt File | Description | Est. Time | Dependencies |
||---|-------------|-------------|-----------|--------------|
|| A1 | `PROMPT_A1_COPY_WARDEN.md` | Copy warden_audit.py to scripts/ | 3-5 min | None |
|| A2 | `PROMPT_A2_COPY_VALIDATE.md` | Copy validate_project.py to scripts/ | 3-5 min | None |
|| A3 | `PROMPT_A3_CREATE_PRE_REVIEW.md` | Create pre_review_scan.sh | 5-10 min | A1, A2 |
|| A4 | `PROMPT_A4_COPY_PROTOCOL.md` | Copy REVIEWS_AND_GOVERNANCE_PROTOCOL.md | 3-5 min | None |
|| A5 | `PROMPT_A5_COPY_PATTERN.md` | Copy code-review-standard.md pattern | 3-5 min | None |
|| B1 | `PROMPT_B1_MERGE_LEARNINGS.md` | Merge LOCAL_MODEL_LEARNINGS.md files | 5-10 min | None |
|| B2 | `PROMPT_B2_COPY_LEARNING_LOOP.md` | Copy learning-loop-pattern.md | 3-5 min | None |
|| C1 | `PROMPT_C1_UPDATE_AGENTS.md` | Update AGENTS.md references | 5-10 min | A1, A2, A4 |
|| C2 | `PROMPT_C2_UPDATE_CLAUDE.md` | Update CLAUDE.md references | 5-10 min | A1, A2, A4 |
|| C3 | `PROMPT_C3_UPDATE_CURSORRULES.md` | Update .cursorrules references | 5-10 min | A1, A2, A4, A5 |
|| D1 | `PROMPT_D1_ADD_VERSION.md` | Add scaffolding_version metadata | 3-5 min | All above |
|| E1 | `PROMPT_E1_VERIFY.md` | Verification tests | 5 min | All above |

**Total estimated time:** 45-85 minutes

**Can parallelize:** A1, A2, A4, A5, B1, B2 (no dependencies on each other)

---

## Key Constraints (Apply to ALL Prompts)

These constraints must be included in every prompt:

```markdown
## CONSTRAINTS (READ FIRST)
- DO NOT reference $SCAFFOLDING variable - files must be local
- DO NOT create symlinks - make actual copies
- PRESERVE original file metadata (dates, permissions where relevant)
- UPDATE all internal references to be project-relative
- TIMEOUT: Keep tasks atomic (5-10 min max)
```

---

## Files to Transfer

### From project-scaffolding → project-tracker

**Scripts:**
- `scripts/warden_audit.py` → `project-tracker/scripts/warden_audit.py`
- `scripts/validate_project.py` → `project-tracker/scripts/validate_project.py`
- NEW: `scripts/pre_review_scan.sh` (create from template)

**Documentation:**
- `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` → `project-tracker/Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`
- `patterns/code-review-standard.md` → `project-tracker/Documents/patterns/code-review-standard.md`
- `patterns/learning-loop-pattern.md` → `project-tracker/Documents/patterns/learning-loop-pattern.md`

**Reference:**
- `Documents/reference/LOCAL_MODEL_LEARNINGS.md` → MERGE with `project-tracker/Documents/reference/MODEL_LEARNINGS.md`

**Templates:**
- `templates/CODE_REVIEW.md.template` → `project-tracker/Documents/templates/CODE_REVIEW.md.template` (if doesn't exist)

---

## Reference Paths

### project-scaffolding paths:
- `/Users/eriksjaastad/projects/project-scaffolding/`

### project-tracker paths:
- `/Users/eriksjaastad/projects/project-tracker/`

**Important:** All prompts should use ABSOLUTE paths to avoid ambiguity.

---

## Escalation Protocol

If a Worker times out or fails:

1. **Strike 1:** Retry with same model (qwen2.5-coder:7b)
2. **Strike 2:** Switch model (qwen2.5-coder:7b → deepseek-r1:14b)
3. **Strike 3:** HALT and report to Conductor

**CRITICAL:** DO NOT manually implement failed Worker tasks. That violates AGENTS.md protocol.

---

## Progress Tracking

|| Prompt | Status | Worker Model | Strikes | Notes |
||--------|--------|--------------|---------|-------|
|| A1 | [x] | gemini-3-flash | 0 | - |
|| A2 | [x] | gemini-3-flash | 0 | - |
|| A3 | [x] | gemini-3-flash | 0 | - |
|| A4 | [x] | gemini-3-flash | 0 | - |
|| A5 | [x] | gemini-3-flash | 0 | - |
|| B1 | [x] | gemini-3-flash | 0 | - |
|| B2 | [x] | gemini-3-flash | 0 | - |
|| C1 | [x] | gemini-3-flash | 0 | - |
|| C2 | [x] | gemini-3-flash | 0 | - |
|| C3 | [x] | gemini-3-flash | 0 | - |
|| D1 | [x] | gemini-3-flash | 0 | - |
|| E1 | [x] | gemini-3-flash | 0 | - |

**Overall Status:** [ ] Not Started / [ ] In Progress / [x] Complete

---

## Post-Transfer Verification

After all prompts complete, verify:

```bash
cd /Users/eriksjaastad/projects/project-tracker

# 1. Scripts exist locally
ls -la scripts/warden_audit.py scripts/validate_project.py scripts/pre_review_scan.sh

# 2. No $SCAFFOLDING references remain
grep -r "\$SCAFFOLDING" AGENTS.md CLAUDE.md .cursorrules
# Should return nothing

# 3. Scripts work standalone
python scripts/warden_audit.py --root . --fast
python scripts/validate_project.py project-tracker

# 4. Version metadata exists
grep "scaffolding_version" 00_Index_project-tracker.md
# Should return version number

# All should pass
```

---

## Related Documents

- **Parent task:** `project-scaffolding/TODO.md` (Knowledge Transfer Architecture section)
- **Architecture decision:** project-scaffolding is template generator, not runtime dependency
- **Learning patterns:** `Documents/reference/LOCAL_MODEL_LEARNINGS.md`
- **Transfer guide:** `project-tracker/Documents/SCAFFOLDING_TRANSFER_GUIDE.md` (update after completion)

---

**Hand to Floor Manager to begin knowledge transfer.**
