# Engineering Code Review: Project Scaffolding System

**Date:** December 23, 2025
**Reviewer:** Senior Principal Engineer Assessment
**Verdict:** **Needs Major Refactor**

> Good ideas, bad execution. There's value here, but it's drowning in documentation theater and fragile automation that will bite you when you need it most.

---

## Executive Summary

This project scaffolding system has genuine utility buried under layers of over-documentation and fragile automation. The core insight—routing AI tasks to cost-appropriate tiers—is valuable. The implementation is not ready for daily reliance.

**What works:** DeepSeek integration ($0.0064 for 3 reviews), EXTERNAL_RESOURCES.md, tiered planning mental model
**What doesn't:** Tests fail on import, Kiro CLI parsing is fragile, templates are too generic, TODO.md is unreadable

---

## 1) Engineering Verdict

### Rating: **Needs Major Refactor**

| Criterion | Score | Notes |
|-----------|-------|-------|
| Reliability | 3/10 | Tests don't run, no retry logic, fragile parsing |
| Usability | 4/10 | Too many placeholders, requires 4 API keys to function |
| Maintainability | 5/10 | Good code structure, but 1350-line TODO is unmanageable |
| Actual Utility | 6/10 | EXTERNAL_RESOURCES.md and DeepSeek reviews work |
| Documentation Quality | 4/10 | Over-documented plans, under-documented reality |

---

## 2) The "Theater vs. Tool" Test

### Components Evaluated

| Component | Verdict | Reasoning |
|-----------|---------|-----------|
| `EXTERNAL_RESOURCES.md` | ✅ **TOOL** | Actually solves "which project uses Cloudflare?" problem |
| Tiered Sprint Planning | 🟡 **CONCEPT** | Good mental model, but still manual process |
| DeepSeek integration | ✅ **TOOL** | Works, cheap ($0.0064 for 3 reviews), evidence in `reviews/` |
| `CLAUDE.md.template` | 🔴 **THEATER** | 400+ lines of placeholders you'll rewrite every time |
| `.cursorrules.template` | 🔴 **THEATER** | Hardcoded paths to `~/...` |
| Kiro spec generator | 🟡 **RISK** | Exists, untested on real projects, fragile CLI parsing |
| `TODO.md` | 🔴 **THEATER** | 1350+ lines of brain dump nobody will read |

### False Efficiency Identified

**The Tiered AI System isn't automated.** The pattern document is 358 lines explaining a concept. The "dispatcher" mentioned in TODO.md doesn't exist. You're still manually deciding which model to use.

**Cost estimates are guesses, not measurements.** `scaffold/review.py:256-267` uses hardcoded pricing with no input/output split and no validation against actual bills.

---

## 3) The "3-Month Test"

**Returning to this in 3 months, you will:**

- ❌ **Curse past-you** when tests don't run (missing `aiohttp`)
- ❌ **Rage-quit** when Kiro CLI changes output format and regex breaks
- 🟡 **Waste 20 minutes** re-reading TODO.md to find what's built vs. planned
- ✅ **Use EXTERNAL_RESOURCES.md** immediately (actually useful)

### The "Next Project Test"

1. Copy templates → Start replacing `[PLACEHOLDER]` → **Waste 30 minutes**
2. Try to run review system → Need 4 API keys configured → **Give up, do it manually**
3. Check EXTERNAL_RESOURCES.md for duplicate services → **Actually helpful**
4. Look at tiered sprint planner → Still manual tiering → **Just use Cursor**

---

## 4) Ten Failure Modes

| # | Failure Mode | Trigger | Code Location |
|---|--------------|---------|---------------|
| 1 | Kiro CLI output format changes | Any Kiro update | `scaffold/review.py:368-379` |
| 2 | DeepSeek API rate limited | High usage | `scaffold/review.py:306-329` (no retry) |
| 3 | Kiro CLI hangs | Network issues | 120s timeout, then silent failure |
| 4 | One API key missing | Incomplete setup | `cli.py:197-214` (silently skipped) |
| 5 | Model pricing changes | Monthly | Hardcoded rates diverge from reality |
| 6 | Python 3.11+ only | New machine | Hard requirement, not in requirements.txt |
| 7 | macOS hardcoded paths | Linux/CI | `/Applications/Kiro CLI.app/...` |
| 8 | aiohttp not installed | Fresh clone | `ModuleNotFoundError` on import |
| 9 | Prompt too long for context | Large documents | No truncation, API errors |
| 10 | Reviews compared across model versions | Model updates | Quality drift undetectable |

---

## 5) Technical Teardown

### Critical Bug 1: Tests Don't Run

```bash
$ pytest tests/ -v -m "not slow"
E   ModuleNotFoundError: No module named 'aiohttp'
```

The claim of "24 passing tests" is theater. Tests cannot even import.

### Critical Bug 2: Kiro Output Parsing is Fragile

**Location:** `scaffold/review.py:368-379`

```python
parts = cleaned_output.split('▸ Credits:')
if len(parts) > 0:
    content = parts[0].strip()
    lines = content.split('\n')
    start_idx = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('⠀') and not line.startswith('╭') and not line.startswith('│'):
            start_idx = i
            break
```

**Will break when:**
- Kiro changes credits line format
- Kiro changes ASCII art characters
- Kiro outputs in different language
- Kiro adds new decorative elements

### Critical Bug 3: No Retry Logic

**Location:** `scaffold/review.py:149`

```python
results = await asyncio.gather(*tasks, return_exceptions=True)
```

Exceptions caught but not retried. One failed API call = one missing review = incomplete analysis.

### Critical Bug 4: Silent Reviewer Skipping

**Location:** `cli.py:197-214`

```python
if api == "deepseek" and not deepseek_key:
    console.print(f"[yellow]Skipping {display_name} (no DeepSeek key)[/yellow]")
    continue
```

No error, no failure, just fewer reviews. Yellow warning easily missed.

### Over-Engineering Red Flags

| Issue | Evidence |
|-------|----------|
| 1350-line TODO.md | Part brain dump, part documentation, part planning notes |
| 702-line sprint planner | Instructions for a manual process |
| 400-line CLAUDE.md template | So many placeholders it needs rewriting |
| Hardcoded macOS paths | `/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli` |

---

## 6) The "Actually Useful" Core

### Most Valuable Feature: EXTERNAL_RESOURCES.md

This solves a real problem: "which project uses Cloudflare?" It's 560 lines but organized, actionable, and will save billing confusion.

**If you delete everything else, keep this.**

### Delete Candidates

| File/Section | Reason |
|--------------|--------|
| `TODO.md` lines 250-1000 | Brain dump about unbuilt systems |
| `templates/CLAUDE.md.template` | 400 lines of placeholders you'll rewrite |
| `docs/OPTION_C_BUILD_PLAN.md` | Historical planning doc |
| `docs/CONTEXT_HANDOFF_*.md` | Session notes (archive instead) |
| All "Coming soon" sections | Adds complexity without value |

### The 80/20

**20% that provides 80% of value:**
1. `EXTERNAL_RESOURCES.md` - solves real problem
2. DeepSeek integration in `review.py` - works, cheap, proven
3. `patterns/tiered-ai-sprint-planning.md` - good mental model
4. Kiro steering templates in `templates/.kiro/steering/` - actually reusable

**80% that provides 20% of value:**
- Everything else

---

## 7) Remediation Plan

### Step 1: Fix the Tests (1 hour)

**Success Criteria:** `pytest tests/ -v` runs without import errors

**Actions:**
1. Create `requirements.txt` with ALL dependencies including `aiohttp`, `pyyaml`
2. Add `venv` setup instructions to README.md
3. Run tests in CI to prove they actually pass

### Step 2: Add Retry Logic to All API Calls (2 hours)

**Success Criteria:** API calls retry 3x with exponential backoff before failing

**Action:** Add to `scaffold/review.py`:

```python
import tenacity

@tenacity.retry(
    stop=tenacity.stop_after_attempt(3),
    wait=tenacity.wait_exponential(multiplier=1, min=2, max=10),
    reraise=True
)
async def _call_with_retry(self, api_func, *args, **kwargs):
    return await api_func(*args, **kwargs)
```

### Step 3: Make Kiro Parsing Defensive (1 hour)

**Success Criteria:** Kiro integration returns structured error if output format changes

**Actions:**
1. Check for expected markers before parsing
2. If markers missing, return `{"error": "Kiro output format changed", "raw_output": ...}`
3. Log raw output for debugging
4. Don't silently produce garbage

### Step 4: Archive Brain Dump, Keep Actionable (2 hours)

**Success Criteria:** TODO.md is < 200 lines of current actionable items

**Actions:**
1. Create `docs/archives/planning-notes-dec-2025.md`
2. Move all hypothetical system designs there
3. Keep only: "What exists" + "Immediate next steps"
4. Delete all "Coming soon" and "Future consideration" sections

### Step 5: Validate Cost Tracking Against Real Bills (Ongoing)

**Success Criteria:** Cost estimates within 20% of actual API bills after 1 month

**Actions:**
1. After each review run, log timestamp + estimated cost
2. At month end, compare estimated total vs. actual bills
3. Adjust hardcoded rates in `review.py`
4. Add comment: `# Last validated: YYYY-MM-DD against actual billing`

---

## 8) Key Questions Answered

| Question | Answer |
|----------|--------|
| Is this better than "copy from last project"? | Barely. Templates are too generic. EXTERNAL_RESOURCES.md is the exception. |
| Will templates ship with `[PLACEHOLDER]`? | Yes. Every `[Project Name]` proves this. |
| Is tiered AI workflow provably cheaper? | Theoretically. $0.0064 reviews prove concept, but no Cursor comparison. |
| Does automation save more time than maintenance? | Not yet. Kiro parsing will break. Missing deps will confuse. |
| Can another dev use this in < 30 minutes? | No. Tests won't run. Kiro won't be installed. API keys not configured. |

---

## 9) Summary

You've built **documentation about automation** rather than **automation**.

### Keep:
- `EXTERNAL_RESOURCES.md` - actually useful
- DeepSeek review integration - works, but add retry logic
- Tiered planning concept - good mental model, stop pretending it's automated

### Delete/Archive:
- Brain dumps in TODO.md
- Over-generic templates
- Historical planning documents
- "Coming soon" sections

### Bottom Line:

Delete the brain dumps, fix the tests, and actually use this on a real project before adding more features. The best code is often the code you delete.

---

*Review conducted: December 23, 2025*
*Methodology: Full codebase analysis including scaffold/, scripts/, templates/, tests/, docs/, patterns/*
