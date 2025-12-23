# Project Scaffolding - TODO

> **Purpose:** Current actionable tasks for project-scaffolding  
> **Last Updated:** December 23, 2025

---

## ✅ What Exists & Works

**Templates:**
- `.kiro/` templates (steering + specs)
- `CLAUDE.md.template`
- `.cursorrules.template`
- `Documents/` structure
- `TIERED_SPRINT_PLANNER.md`

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

### 🚧 IN PROGRESS: Chunk 3 (Delete the Theater)
- [ ] Archive TODO.md brain dump → `docs/archives/planning-notes-dec-2025.md`
- [ ] Simplify over-generic templates
- [ ] Archive historical planning docs
- [ ] Clean up root directory

### ⏭️ NEXT: Chunk 4 (Dogfood & Validate)
- [ ] Test on real project
- [ ] Validate cost tracking
- [ ] Fix issues found during use

---

## 📋 Backlog (After Chunk 4)

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
