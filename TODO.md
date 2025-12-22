# Project Scaffolding - TODO

> **Purpose:** Track work specific to project-scaffolding meta-project  
> **Last Updated:** December 22, 2025

---

## 🎯 Next Active Task

### Reevaluate TODO List for Tiered Implementation

**Goal:** Apply tiered sprint planning TO the TODO list itself

**Task:** Break down the TODO list into Tier 1 / Tier 2 / Tier 3 tasks
- Tier 1 (Big Brain): Questions, architecture decisions, pattern design
- Tier 2 (Mid-Weight): Pattern extraction, documentation writing
- Tier 3 (Worker Bee): Maintenance, updates, simple docs

**Why:** First attempt to use our own tiered system on our own work (dogfooding!)

**Status:** Ready to start after gas run

---

## 🚨 Critical Missing Piece: Task Dispatch System

**The Problem:**
- We have planning side: Break TODO into Tier 1/2/3 ✅
- We DON'T have execution side: Automated dispatch to tiers ❌

**Without dispatch automation:**
- Need 3 chat windows per project (one per tier)
- 2 projects = 6 windows
- 3 projects = 9 windows
- **Unmanageable!**

**What We Need:**
A system that:
1. **Ingests the tiered TODO list** (parses Tier 1/2/3 sections)
2. **Dispatches tasks to appropriate tiers** (routes to correct chat/API)
3. **Tracks execution** (what's running, what's done)
4. **Prevents window juggling chaos**

**Possible Approaches:**

**Option A: Prompt Generator**
- Read TODO.md
- Generate ready-to-paste prompts for each tier
- Copy/paste into appropriate chat window
- Simple, no API needed

**Option B: CLI Dispatcher**
- `pt dispatch --tier 3 "next task"`
- Calls appropriate API (OpenAI/Anthropic) with tier-appropriate model
- Returns result, marks task complete
- More automated, needs API keys

**Option C: Web Dashboard + API**
- Visual task board (like Project Tracker)
- Click task → dispatches to appropriate API
- Shows results inline
- Most sophisticated, highest effort

**Decision Needed:**
- Which approach fits workflow best?
- Start simple (Option A) or build full system (Option B/C)?
- Should this be part of Project Tracker or separate tool?

**Related:**
- This is why Project Tracker exists (visibility + orchestration)
- This could be Project Tracker Phase 4: "Task Execution"
- Or separate tool: "Task Dispatcher"

**Status:** Discussion needed (Tier 1 work!)

---

## Current Status

**Phase:** Pattern extraction and template creation  
**Status:** Core patterns documented, templates created

---

## Open Questions

### Q1: Planning Phase Tiering
**Question:** How to handle tier escalation when planning? Bottom-up scoring?

**Context:** 
- Tiered Sprint Planner uses bottom-up tiering (Tier 3 → 2 → 1)
- But planning phase itself is Tier 1 work (architecture, breaking down problems)
- How to break down planning tasks by tier?

**Needs:**
- Discussion with Erik
- Examples from real planning sessions
- Pattern documentation if we find one

---

## Future Pattern Extraction (When Ready)

### From agent_os (When 2-3 Projects Use It)
- [ ] Run tracking pattern (status, timestamps, errors)
- [ ] Plugin system pattern (provider-agnostic infrastructure)
- [ ] Idempotent execution pattern (database constraints)

**Wait for:** agent_os architecture decisions, other projects adopting patterns

---

### Email Monitoring Pattern (When land + billing-tracker Built)
- [ ] Email monitoring agent pattern
- [ ] Criteria evaluation pattern
- [ ] Notification dispatch pattern

**Wait for:** land project and billing-tracker implementation

---

### Job Crawler Pattern (If Built)
- [ ] Job listing scraping
- [ ] Automated business opportunity identification
- [ ] Service arbitrage pattern

**Wait for:** Job crawler project to prove itself

---

## Maintenance Tasks

### Regular Updates
- [ ] Review patterns quarterly (are they still accurate?)
- [ ] Update EXTERNAL_RESOURCES.md as services added
- [ ] Extract patterns when 2-3 projects show same approach
- [ ] Update templates based on real project usage

### Documentation Health
- [ ] Keep README current with project status
- [ ] Archive outdated session notes
- [ ] Ensure all patterns have "last updated" dates
- [ ] Check that examples still match current projects

---

## Success Metrics

**Pattern Adoption:**
- How many new projects use scaffolding templates?
- Which patterns get adopted vs ignored?
- Are projects more consistent?

**Time Savings:**
- Does scaffolding reduce new project setup time?
- Are patterns saving time on repeat problems?

**Chaos Reduction:**
- Is EXTERNAL_RESOURCES.md preventing duplicate services?
- Are API key patterns preventing confusion?
- Is tiered sprint planning managing costs?

---

## Related Projects

**project-tracker:** 
- Integration documented in `project-tracker/docs/INTEGRATION_WITH_SCAFFOLDING.md`
- Tracker reads EXTERNAL_RESOURCES.md
- Tracker shows which projects use scaffolding templates

**Other projects:**
- Source patterns from: image-workflow, Trading Co-Pilot, Cortana, Hologram
- Extract patterns TO: This project
- Apply patterns IN: All future projects

---

## Notes

**The two-level game:**
- Level 1: Domain projects (trading, images, AI)
- Level 2: Meta projects (scaffolding, tracker)

This is a Level 2 project. It doesn't ship product. It ships TOOLS to build products.

Success = Other projects are easier because of this one.

---

**Last Updated:** December 22, 2025  
**Next Review:** End of January 2026 (after holidays, new projects in 2026)

