# Claude Code Review - Chunked Action Plan

**Source:** `docs/CODE_REVIEW_2025-12-23.md`  
**Strategy:** Fix in logical chunks, validate between each

---

## 📊 Chunk Overview

| Chunk | Name | Time Est | Impact | When |
|-------|------|----------|--------|------|
| **1** | Quick Wins | ~30 min | High | NOW |
| **2** | Defensive Programming | ~2-3 hrs | Critical | Tomorrow |
| **3** | Delete the Theater | ~2-3 hrs | High | This week |
| **4** | Dogfood & Validate | TBD | Proof | After 1-3 |

**Total:** ~8-10 hours across 4 chunks

---

## ✅ CHUNK 1: Quick Wins (~30 minutes)

**Goal:** Fix easy stuff, build momentum, prove tests work

### Tasks:

- [ ] **1.1** Create complete `requirements.txt`
  - Add all dependencies: `aiohttp`, `tenacity`, `pyyaml`, `pytest`, `pytest-asyncio`
  - Document versions
  - **Validation:** `pip install -r requirements.txt` works

- [ ] **1.2** Verify tests actually run
  - Run `pytest tests/ -v -m "not slow"`
  - Should see 24 passing
  - **Validation:** No import errors

- [ ] **1.3** Fix silent reviewer skipping
  - `scaffold/cli.py:197-214`
  - Change "Skipping" from yellow warning to red error
  - Add `--allow-partial` flag if user wants to run with missing keys
  - **Validation:** Missing key = clear error, not silent skip

- [ ] **1.4** Remove hardcoded macOS paths
  - `templates/.cursorrules.template`
  - Remove `/Users/eriksjaastad/...` paths
  - Make templates truly generic
  - **Validation:** No hardcoded paths in templates

**After Chunk 1:**
- Tests provably work
- Missing keys fail loud
- Templates aren't Erik-specific
- ~30 min invested, immediate payoff

**Stop here and check in!**

---

## 🛡️ CHUNK 2: Defensive Programming (~2-3 hours)

**Goal:** Make it robust enough to rely on daily

### Tasks:

- [ ] **2.1** Add retry logic with exponential backoff
  - Install: `tenacity` library
  - Wrap all API calls in `scaffold/review.py`
  - 3 attempts, exponential backoff (2s → 4s → 8s)
  - **Validation:** Simulate network failure, verify retries

- [ ] **2.2** Fix Kiro CLI parsing to be defensive
  - `scaffold/review.py:368-379` - `_call_kiro()` method
  - Check for expected markers BEFORE parsing
  - If format changed, return structured error:
    ```python
    {"error": "Kiro output format changed", "raw_output": stdout}
    ```
  - Log raw output for debugging
  - **Validation:** Change Kiro output format, verify graceful error

- [ ] **2.3** Add timeout handling
  - Kiro CLI: 120s timeout → return timeout error (not silent fail)
  - All API calls: configurable timeout
  - **Validation:** Simulate slow API, verify timeout handling

- [ ] **2.4** Improve error messages
  - No more "Review failed" - say WHY
  - Include: which API, which model, error code
  - **Validation:** Trigger error, verify message is actionable

**After Chunk 2:**
- API failures retry automatically
- Kiro changes don't break silently
- Error messages tell you what's wrong
- ~3 hours invested, much more reliable

**Stop here and check in!**

---

## 🗑️ CHUNK 3: Delete the Theater (~2-3 hours)

**Goal:** Keep 20% that provides 80% value, delete the rest

### Tasks:

- [ ] **3.1** Archive the TODO.md brain dump
  - Create: `docs/archives/planning-notes-dec-2025.md`
  - Move: `TODO.md` lines 250-1000 → archive
  - Keep in TODO.md:
    - Current state (what exists)
    - Next 3-5 actionable tasks only
  - Delete all "Coming soon" sections
  - **Validation:** TODO.md < 200 lines, still useful

- [ ] **3.2** Simplify or delete over-generic templates
  - `templates/CLAUDE.md.template` - reduce from 400 → 50 lines
  - Keep only the critical sections
  - Or: just delete it, use Kiro steering templates instead
  - **Validation:** Can fill out template in < 5 min

- [ ] **3.3** Archive historical planning docs
  - Move to `docs/archives/`:
    - `OPTION_C_BUILD_PLAN.md`
    - `CONTEXT_HANDOFF_*.md`
    - `SYSTEM_WALKTHROUGH.md`
  - Keep only current, actionable docs in `docs/`
  - **Validation:** `docs/` is clear and focused

- [ ] **3.4** Clean up root directory
  - Delete or archive:
    - `kiro-antigravity info.md` (superseded by V2)
    - `more cost saving.md` (merge into main docs or delete)
    - `GEMINI_RESEARCH_PROMPT.md` (historical)
  - **Validation:** Root directory is clean

**After Chunk 3:**
- No more brain dumps
- No more "documentation about automation"
- Focus on what actually works
- ~3 hours invested, much clearer project

**Stop here and check in!**

---

## 🚀 CHUNK 4: Dogfood & Validate (TBD)

**Goal:** Use it on a real project, find remaining issues

### Tasks:

- [ ] **4.1** Pick a placeholder project
  - One of the 3 placeholder directories you mentioned
  - Small feature, not critical path

- [ ] **4.2** Use scaffolding to set it up
  - Copy templates
  - Generate Kiro specs
  - Run reviews
  - Document pain points

- [ ] **4.3** Run a real review
  - Use multi-AI review on actual document
  - Compare DeepSeek + Kiro output
  - Measure actual cost vs. estimate

- [ ] **4.4** Start cost tracking log
  - Create: `logs/cost-tracking.jsonl`
  - After each review: log timestamp, models, tokens, cost
  - Monthly: compare to bills

- [ ] **4.5** Fix issues found during dogfooding
  - Capture in new, focused TODO items
  - No brain dumps!

**After Chunk 4:**
- Proven on real project
- Cost tracking validated
- Remaining issues identified
- Ready for daily use

**Stop here and celebrate!** 🎉

---

## 🎯 Recommended Order

**Today (if tokens left):**
- Chunk 1: Quick Wins (~30 min)

**Tomorrow (fresh credits):**
- Chunk 2: Defensive Programming (~3 hours)

**This Week:**
- Chunk 3: Delete the Theater (~3 hours)
- Chunk 4: Dogfood & Validate (~2-4 hours)

---

## 💡 Key Insight

Claude Code's main critique: **"Documentation about automation, not automation"**

Our response: Fix the fragility (Chunk 2), delete the theater (Chunk 3), prove it works (Chunk 4).

---

**Ready to start Chunk 1?** Should take ~30 min and give immediate wins! 🚀

