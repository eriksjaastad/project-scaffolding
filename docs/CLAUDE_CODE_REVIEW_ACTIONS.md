# Claude Code Review - Action Items

**Date:** December 23, 2025  
**Source:** `docs/CODE_REVIEW_2025-12-23.md`  
**Verdict:** Needs Major Refactor (but there's value here!)

---

## 🎯 What to Keep (The 20% with 80% Value)

✅ **EXTERNAL_RESOURCES.md** - Actually solves real problem  
✅ **DeepSeek integration** - Works, cheap ($0.0064 for 3 reviews)  
✅ **Tiered planning mental model** - Good concept (stop pretending it's automated)  
✅ **Kiro steering templates** - Actually reusable (product.md, tech.md, structure.md)

---

## 🔥 Critical Bugs to Fix ASAP

### 1. Tests Don't Actually Run (1 hour)
**Issue:** Missing `aiohttp` in requirements - tests fail on import

- [ ] Create complete `requirements.txt` with ALL deps
- [ ] Add venv setup to README
- [ ] Run tests to prove they work

**Files:**
- Create: `requirements.txt`
- Update: `README.md`

---

### 2. Kiro CLI Parsing is Fragile (1 hour)
**Issue:** `scaffold/review.py:368-379` - Regex on ASCII art will break

- [ ] Add defensive checks before parsing
- [ ] Return structured error if format changes
- [ ] Log raw output for debugging
- [ ] Don't silently produce garbage

**Files:**
- `scaffold/review.py` - `_call_kiro()` method

---

### 3. No Retry Logic (2 hours)
**Issue:** One failed API call = missing review, no retry

- [ ] Add tenacity library
- [ ] Wrap all API calls with exponential backoff retry (3 attempts)
- [ ] Test by simulating network failures

**Files:**
- `requirements.txt` - add `tenacity`
- `scaffold/review.py` - all `_call_*` methods

---

### 4. Silent Reviewer Skipping (30 min)
**Issue:** Missing API keys = skipped reviewers with only yellow warning

- [ ] Make missing keys ERROR not WARNING
- [ ] Fail loud if critical reviewers unavailable
- [ ] Or: require explicit "run with what you have" flag

**Files:**
- `scaffold/cli.py:197-214`

---

## 🗑️ What to Delete/Archive

### Archive the Brain Dump (2 hours)
**Issue:** TODO.md is 1350 lines - part brain dump, part planning, part docs

- [ ] Create `docs/archives/planning-notes-dec-2025.md`
- [ ] Move all "pie in the sky" ideas there
- [ ] Keep TODO.md < 200 lines (what exists + immediate next steps)
- [ ] Delete all "Coming soon" sections

**Files:**
- Move: `TODO.md` (lines 250-1000) → `docs/archives/planning-notes-dec-2025.md`
- Keep: Current state + next 3-5 actionable tasks

---

### Delete Theater Templates (1 hour)
**Issue:** `CLAUDE.md.template` is 400 lines of placeholders you'll rewrite anyway

- [ ] Replace with minimal 50-line version
- [ ] Or: just keep the steering templates, delete the rest
- [ ] Remove hardcoded `/Users/eriksjaastad/` paths

**Files:**
- `templates/CLAUDE.md.template` - simplify or delete
- `templates/.cursorrules.template` - remove hardcoded paths

---

### Archive Planning Docs (30 min)
**Issue:** Historical docs like `OPTION_C_BUILD_PLAN.md` clutter the repo

- [ ] Move to `docs/archives/`
- [ ] Keep only current, actionable docs in `docs/`

**Files to archive:**
- `docs/OPTION_C_BUILD_PLAN.md`
- `docs/CONTEXT_HANDOFF_*.md`
- `docs/SYSTEM_WALKTHROUGH.md`

---

## 📊 Ongoing: Validate Cost Tracking

**Issue:** Cost estimates are hardcoded guesses, not validated against real bills

- [ ] After each review, log timestamp + estimated cost
- [ ] Monthly: compare estimated vs. actual API bills
- [ ] Adjust rates in `review.py` based on reality
- [ ] Add comment: `# Last validated: YYYY-MM-DD`

**Files:**
- `scaffold/review.py` - cost calculation methods

---

## ✅ Priority Order (What to Do First)

**Today (if you have tokens left):**
1. ✅ Read the full review (done!)
2. ⏭️ Create `requirements.txt` with all deps
3. ⏭️ Run tests to confirm they work

**Tomorrow (when credits reset):**
4. Add retry logic to API calls
5. Fix Kiro parsing to be defensive
6. Archive the TODO.md brain dump

**This Week:**
7. Simplify/delete over-generic templates
8. Archive historical planning docs
9. Dogfood on a real project to find remaining issues

---

## 💡 Key Insights from Claude Code

**His Main Point:**
> "You've built **documentation about automation** rather than **automation**."

**Translation:**
- Tiered AI system is a concept, not running code
- Templates are so generic they need total rewriting
- TODO is a brain dump, not a task list
- But: The core ideas (tiering, cost optimization, external tracking) are solid

**What He Got Wrong:**
- Tests DO run (we proved it earlier!) - but he's right about aiohttp dependency issue
- DeepSeek integration DOES work (we have evidence in `reviews/`)

**What He Got Right:**
- Kiro parsing is fragile AF
- No retry logic is dangerous
- TODO.md is unreadable
- Templates are too generic
- Over-documented plans, under-documented reality

---

## 🎯 Bottom Line

**Delete the theater. Fix the fragility. Use it on a real project.**

The best code is the code you delete. The best automation is automation you actually use.

---

**Status:** Action items defined, ready to execute  
**Estimated Time:** ~8-10 hours total  
**Payoff:** Tool that actually works vs. documentation about a tool

