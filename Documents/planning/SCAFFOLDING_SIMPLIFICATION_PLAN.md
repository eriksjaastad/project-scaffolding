# Scaffolding Simplification Plan

**Date:** January 12, 2026
**Status:** ACTIVE - This is today's work
**Context:** Stopped 48-hour canary test to address architectural complexity

---

## The Problem

project-scaffolding has become overcomplicated:
- 12 micro-prompts for what should be file copies
- Documentation about how to document things
- Worker orchestration overhead exceeding the value it provides
- Simple tasks (cp, sed) wrapped in AI prompt ceremonies

**Root cause:** Optimizing for hypothetical scale before proving the basics work.

---

## What We Keep

### 1. Templates (Core Value)
- `.cursorrules-template`
- `AGENTS.md.template`
- `CLAUDE.md.template`
- `TODO.md.template`
- `CODE_REVIEW.md.template`

### 2. Safety Tools (Proven Value)
- `warden_audit.py` - catches dangerous code
- `validate_project.py` - structure validation
- send2trash pattern - no destructive deletes

### 3. Standards (Light Documentation)
- `PROJECT_STRUCTURE_STANDARDS.md`
- `CODE_QUALITY_STANDARDS.md`
- Pattern files in `patterns/`

### 4. Local Model Integration (Keep, But Simplify)
- Ollama MCP stays available
- LOCAL_MODEL_LEARNINGS.md for institutional memory
- Use local models for **code generation**, not file operations
- Floor Manager can call Workers when intelligence is needed, not for `cp` commands

---

## What We Cut/Simplify

### 1. Worker Orchestration for Simple Tasks
**Before:** 12 prompts with escalation protocols for file copies
**After:** Bash script or CLI command

### 2. Docs About Docs
**Cut or archive:**
- Excessive "how to use the template" sections
- Meta-documentation explaining the documentation system
- Keep reference docs, cut instructional overhead

### 3. Multi-Prompt Ceremonies
**Before:** PROMPT_A1, A2, A3... with indices and tracking tables
**After:** One CLI command: `./scaffold_cli.py apply <project>`

---

## The New Architecture

### apply_scaffolding CLI

One command to make a project standalone:

```bash
./scaffold_cli.py apply project-tracker
```

**What it does:**

1. **Copy scripts** (no AI needed)
   ```bash
   cp scripts/warden_audit.py $TARGET/scripts/
   cp scripts/validate_project.py $TARGET/scripts/
   ```

2. **Copy docs** (no AI needed)
   ```bash
   cp REVIEWS_AND_GOVERNANCE_PROTOCOL.md $TARGET/Documents/
   cp patterns/code-review-standard.md $TARGET/Documents/patterns/
   cp patterns/learning-loop-pattern.md $TARGET/Documents/patterns/
   ```

3. **Update references** (sed, no AI needed)
   ```bash
   sed -i '' 's|\$SCAFFOLDING/scripts/|./scripts/|g' $TARGET/AGENTS.md
   sed -i '' 's|\$SCAFFOLDING/scripts/|./scripts/|g' $TARGET/CLAUDE.md
   sed -i '' 's|\$SCAFFOLDING/scripts/|./scripts/|g' $TARGET/.cursorrules
   sed -i '' 's|\$SCAFFOLDING|.|g' $TARGET/AGENTS.md
   sed -i '' 's|\$SCAFFOLDING|.|g' $TARGET/CLAUDE.md
   sed -i '' 's|\$SCAFFOLDING|.|g' $TARGET/.cursorrules
   ```

4. **Add version metadata**
   ```bash
   # Append to index file
   echo "scaffolding_version: 1.0.0" >> $TARGET/00_Index_*.md
   echo "scaffolding_date: $(date +%Y-%m-%d)" >> $TARGET/00_Index_*.md
   ```

5. **Verify**
   ```bash
   grep -r "\$SCAFFOLDING" $TARGET/AGENTS.md $TARGET/CLAUDE.md $TARGET/.cursorrules
   # Should return nothing
   ```

**Output:** "Applied scaffolding v1.0.0 to project-tracker. 0 $SCAFFOLDING references remain."

---

## When Local Models ARE Useful

Keep local models for tasks that need intelligence:

| Task | Use Local Model? | Why |
|------|------------------|-----|
| File copy | ❌ No | `cp` is simpler |
| Find/replace | ❌ No | `sed` is simpler |
| Code generation | ✅ Yes | Models add value |
| Code review | ✅ Yes | Models add value |
| Refactoring | ✅ Yes | Models add value |
| Bug fixing | ✅ Yes | Models add value |

**Rule of thumb:** If a bash one-liner can do it, don't prompt an AI.

---

## Implementation Tasks

### Phase 1: Build the CLI (Today)

- [ ] **1.1** Create `scaffold_cli.py apply` command
- [ ] **1.2** Implement file copy logic
- [ ] **1.3** Implement sed replacements for $SCAFFOLDING
- [ ] **1.4** Implement version metadata injection
- [ ] **1.5** Implement verification (grep for remaining references)
- [ ] **1.6** Test on project-tracker

### Phase 2: Clean Up Docs (Today if time)

- [ ] **2.1** Archive the 12 knowledge transfer prompts (keep for reference)
- [ ] **2.2** Update TODO.md to reflect simpler architecture
- [ ] **2.3** Trim CLAUDE.md.template - less instruction, more reference

### Phase 3: Prove It Works (After CLI exists)

- [ ] **3.1** Run `./scaffold_cli.py apply project-tracker`
- [ ] **3.2** Run `./scaffold_cli.py apply Tax-processing`
- [ ] **3.3** Run `./scaffold_cli.py apply analyze-youtube-videos`
- [ ] **3.4** Verify all three are standalone (no $SCAFFOLDING refs)

---

## Success Criteria

After today:
1. `./scaffold_cli.py apply <project>` exists and works
2. project-tracker is standalone (no manual prompts needed)
3. The "how" is simpler than before
4. Local model integration preserved for real code tasks

---

## Notes

- Local models stay in the ecosystem - they're valuable for code generation
- This simplification is about matching tool to task
- Bash for file ops, AI for intelligence
- "Docs about docs" is a smell - keep docs that DO things, cut docs that EXPLAIN docs
