# Project Scaffolding - TODO

> **Purpose:** Current actionable tasks for project-scaffolding  
> **Last Updated:** December 30, 2025  
> **Type:** Infrastructure

---

## ✅ What Exists & Works

**Templates:**
- `.kiro/` templates (steering + specs)
- `CLAUDE.md.template`
- `CLAUDE.md` (Project standard) ✅ NEW (Dec 30)
- `CODE_REVIEW.md.template` ✅ NEW (Dec 30)
- `.cursorrules.template`
- `Documents/` structure
- `TIERED_SPRINT_PLANNER.md`
- `TODO.md.template` ✅ NEW (Dec 30)

**Standards:**
- `TODO_FORMAT_STANDARD.md` (650 lines) ✅ NEW (Dec 30)
- `PROJECT_STRUCTURE_STANDARDS.md` (comprehensive) ✅ NEW (Dec 30)

**Automation:**
- Multi-AI review orchestrator (DeepSeek + Kiro CLI)
- Kiro spec generator script
- 24 passing tests

**Tracking:**
- `EXTERNAL_RESOURCES.md` (560 lines, actually useful!)
- Per-project API key pattern

**Patterns:**
- Tiered AI sprint planning
- Safety systems
- Development philosophy
- API key management

---

## 🎯 Current Sprint: Post-Claude-Code-Review Cleanup

### ✅ DONE: Chunk 1 (Quick Wins)
- Created `requirements.txt`
- Verified tests pass (24/24)
- Fixed silent reviewer skipping (red errors)
- Removed hardcoded paths

### ✅ DONE: Chunk 2 (Defensive Programming)
- Added retry logic (3x exponential backoff)
- Made Kiro parsing defensive
- Better error messages

### ✅ DONE: Chunk 3 (Clean up & Stability)
- Archived TODO.md brain dump → `docs/archives/planning-notes-dec-2025.md`
- Archived historical planning docs
- Cleaned up root directory
- Fixed UnboundLocalError in Kiro parsing
- Removed hardcoded Kiro CLI paths
- Fixed OpenAI retry logic
- Simplified over-engineered templates
- Standardized code review result naming (`CODE_REVIEW_ALL_CAPS`)
- Enforced Definition of Done (DoD) in CLI requests
- Created `templates/CODE_REVIEW.md.template`
- Documented `patterns/code-review-standard.md`
- Established **YAML SSOT Pattern** for data management
- Transitioned `EXTERNAL_RESOURCES.yaml` as the source of truth

### ⏭️ NEXT: Chunk 4 (Dogfood & Validate)
- [ ] Test on real project
- [ ] Validate cost tracking
- [ ] Fix issues found during use

---

## 📋 Backlog (After Chunk 4)

### 🔴 CRITICAL - Code Review System (NEW - Dec 30)

**Goal:** Standardize code review process across all projects

- [x] Create CODE_REVIEW.md.template
- [x] Define standard code review format:
  - [x] Review request info (date, author, purpose)
  - [x] Review checklist (Definition of Done)
  - [x] Reviewer notes and feedback
  - [x] Standard result naming (`CODE_REVIEW_ALL_CAPS`)
- [ ] Add to PROJECT_STRUCTURE_STANDARDS.md
- [ ] Document in PROJECT_KICKOFF_GUIDE.md
- [ ] Integrate with TODO.md format:
  - [ ] Add syntax: `- [ ] Task **[IN REVIEW]** - See CODE_REVIEW.md #123`
  - [ ] Update TODO_FORMAT_STANDARD.md
  - [ ] Update TODO.md.template
- [ ] Create examples from real code reviews
- [ ] Test with project-tracker (dogfood it!)

**Why this matters:**
- Project-tracker dashboard will display pending code reviews
- Alerts table will show code review status
- Need standard format to parse and display

---

### High Priority
- [ ] Add cost tracking log (`logs/cost-tracking.jsonl`)
- [ ] Validate pricing against real bills (monthly)
- [ ] Test Kiro spec generator on real feature

### Medium Priority
- [ ] Prompt versioning system
- [ ] AWS Activate research (Q2 2026)
- [ ] Google Cloud credits (Q2 2026)

### Low Priority
- [ ] Task dispatch system (only if manual tiering becomes painful)
- [ ] Multi-AI build automation (only after 3+ projects prove manual works)

---

## 🗑️ Deleted/Archived

**Archived (docs/archives/):**
- Original 1353-line TODO (brain dump)
- Historical planning docs (Option C build plan, system walkthrough, etc.)

**Reason:** Claude Code review identified "documentation about automation" not "automation"

---

## 🎯 Success Metrics

**This scaffolding is working if:**
1. ✅ New project setup takes < 30 min (vs. hours of copy-paste)
2. ✅ EXTERNAL_RESOURCES.md prevents duplicate signups
3. ✅ DeepSeek reviews save money vs. Cursor (backtest after 1 month)
4. ⏭️ Templates get customized (not shipped with placeholders)
5. ⏭️ Someone else can use it in < 30 min

**As of Dec 23:**
- Metrics 1-3: Proven
- Metrics 4-5: TBD (need dogfooding)

---

**Archive:** See `docs/archives/planning-notes-dec-2025.md` for historical brain dumps
