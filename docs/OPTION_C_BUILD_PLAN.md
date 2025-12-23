# Option C: Full Automation Build Plan

> **Status:** ACTIVE - Building NOW  
> **Decision Date:** December 22, 2025  
> **Erik's Decision:** "I don't want to work manually today. I want to work on setting up the automation today."

---

## Why Option C (Not Manual)

**Erik's Reality:**
- ✅ 4 months of manual copy/paste - pain is REAL
- ✅ Already doing multi-AI reviews manually - just need to automate
- ✅ "If we're just doing things copying and pasting, that is a clear sign that it should be automated"
- ✅ 3x speed potential if 3 tiers work in parallel
- ✅ No historical stats - can't compare to "before" anyway
- ✅ This solves real problems even for one project

**Multi-AI reviews are NOT "nice to have":**
- Different models catch different bugs (proven over 4 months)
- Already part of workflow - just automating existing process
- Main reason for building this system

**Key insight:** We're not introducing something new. We're automating what already works.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT SCAFFOLDING                      │
│                   (Automation System)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ├─→ Multi-AI Review System
                              │   ├─ Document Reviews (via APIs)
                              │   ├─ Code Reviews (via APIs)
                              │   └─ Real-time cost tracking
                              │
                              ├─→ Task Dispatch System
                              │   ├─ Parse sprint plan
                              │   ├─ Route to tiers
                              │   ├─ Handle escalations
                              │   └─ Track progress
                              │
                              ├─→ Build Execution
                              │   ├─ Option A: Via APIs
                              │   └─ Option B: Via Cursor (hybrid)
                              │
                              ├─→ Cost Monitoring
                              │   ├─ Real-time tracking
                              │   ├─ Per-API breakdown
                              │   ├─ Per-reviewer breakdown
                              │   └─ Cost gates
                              │
                              └─→ Prompt Versioning
                                  ├─ Version tracking
                                  ├─ Effectiveness comparison
                                  └─ Learning loop
```

---

## Phase 1: Multi-AI Review System (START HERE)

**Why first:** This is the main reason for the system. Document and code reviews via APIs.

### 1.1 Review Orchestrator

**What it does:**
- Takes a document or code + review prompts
- Dispatches to 3 APIs in parallel
- Collects responses
- Saves reviews to disk
- Reports total cost

**APIs to use:**
- OpenAI (GPT-4o for Tier 2 reviews, GPT-4 for Tier 1)
- Anthropic (Claude Sonnet for Tier 1/2, Haiku for Tier 3)
- Google AI (Gemini, if we want 3rd opinion)

**Parallel execution:**
```python
# Pseudocode
async def run_reviews(document, prompts):
    tasks = [
        call_openai(document, prompts['security']),
        call_anthropic(document, prompts['performance']),
        call_google(document, prompts['architecture'])
    ]
    reviews = await asyncio.gather(*tasks)
    return reviews, calculate_total_cost(reviews)
```

**Output:**
```
docs/sprint_reviews/round_1/
├── security_review_openai.md
├── performance_review_anthropic.md
├── architecture_review_google.md
└── COST_SUMMARY.json
```

**Cost tracking:**
```json
{
  "round": 1,
  "total_cost": 2.45,
  "breakdown": {
    "openai": {"model": "gpt-4o", "cost": 0.85, "tokens": 12000},
    "anthropic": {"model": "claude-sonnet", "cost": 0.90, "tokens": 15000},
    "google": {"model": "gemini-pro", "cost": 0.70, "tokens": 10000}
  },
  "timestamp": "2025-12-22T15:30:00Z"
}
```

---

### 1.2 Review Prompts (3 Personas)

**Security-Focused Skeptic:**
```markdown
You are a security-focused skeptical reviewer.

Your job: Find security vulnerabilities and critical risks.

Required sections (no sunshine!):
- CRITICAL SECURITY RISKS (minimum 3)
- AUTHENTICATION/AUTHORIZATION ISSUES (minimum 2)
- DATA EXPOSURE RISKS (minimum 2)
- IF I HAD TO HACK THIS, I'D... (minimum 2)

Do NOT judge if project is worth building.
DO provide constructive security feedback.

Review this: [document]
```

**Performance-Focused Critic:**
```markdown
You are a performance-focused critical reviewer.

Your job: Find performance bottlenecks and scalability issues.

Required sections:
- PERFORMANCE BOTTLENECKS (minimum 3)
- SCALABILITY CONCERNS (minimum 2)
- DATABASE/API INEFFICIENCIES (minimum 2)
- IF I HAD TO MAKE THIS SLOW, I'D... (minimum 2)

Do NOT judge if project is worth building.
DO provide constructive performance feedback.

Review this: [document]
```

**Architecture Purist:**
```markdown
You are an architecture-focused purist reviewer.

Your job: Find architectural flaws and design issues.

Required sections:
- ARCHITECTURAL ISSUES (minimum 3)
- EDGE CASES NOT HANDLED (minimum 3)
- TECHNICAL DEBT CONCERNS (minimum 2)
- IF THIS DESIGN FAILS, IT'S BECAUSE... (minimum 2)

Do NOT judge if project is worth building.
DO provide constructive architectural feedback.

Review this: [document]
```

---

### 1.3 Cost Gates

**After each review round:**
```
┌─────────────────────────────────────────────────┐
│ Document Review Round 1 Complete                │
│                                                 │
│ Cost breakdown:                                 │
│   Security review (OpenAI):      $0.85         │
│   Performance review (Anthropic): $0.90         │
│   Architecture review (Google):   $0.70         │
│ ────────────────────────────────────────────── │
│ Total: $2.45                                    │
│                                                 │
│ Estimated Round 2 cost: ~$2.50                  │
│ Total so far + Round 2: ~$4.95                  │
│                                                 │
│ Continue to Round 2? [y/n]                      │
└─────────────────────────────────────────────────┘
```

**User controls:**
- Can stop after any round
- Can see cumulative cost
- Can compare to estimate

---

### 1.4 Tool: `scaffold review`

**Command:**
```bash
scaffold review --type document --input docs/VISION.md --round 1
```

**What it does:**
1. Reads document
2. Loads prompts from `prompts/active/document_review_*.md`
3. Dispatches to 3 APIs in parallel
4. Saves reviews to `docs/sprint_reviews/round_1/`
5. Saves cost summary
6. Prints cost breakdown
7. Asks: Continue to Round 2?

**Similar command for code review:**
```bash
scaffold review --type code --input src/auth.py --task "user authentication"
```

---

## Phase 2: Prompt Versioning System

**Why:** "We're going to be learning about prompting as we do this."

### 2.1 Directory Structure

```
prompts/
├── versions/
│   ├── document_review/
│   │   ├── security_v1.md
│   │   ├── security_v2.md
│   │   ├── performance_v1.md
│   │   └── CHANGELOG.md
│   ├── code_review/
│   │   ├── security_v1.md
│   │   ├── security_v2.md
│   │   └── CHANGELOG.md
│   └── build/
│       ├── tier3_v1.md
│       ├── tier3_v2.md
│       └── CHANGELOG.md
└── active/
    ├── document_review_security.md → ../versions/document_review/security_v2.md
    ├── document_review_performance.md
    ├── document_review_architecture.md
    ├── code_review_security.md
    ├── code_review_performance.md
    ├── code_review_quality.md
    ├── build_tier1.md
    ├── build_tier2.md
    └── build_tier3.md
```

---

### 2.2 Prompt Metadata

**Each prompt version has:**
```yaml
---
version: 2
created: 2025-12-22
replaced: security_v1.md
reason: "v1 missed edge cases around JWT expiration. v2 adds explicit checklist for token handling."
effectiveness:
  projects_used: 3
  critical_issues_found: 12
  false_positives: 2
  avg_cost: $0.90
author: erik
---
```

---

### 2.3 CHANGELOG Example

```markdown
# Document Review - Security Prompt - CHANGELOG

## v2 (2025-12-22)
**Changed:** Added explicit JWT token checklist
**Why:** v1 missed token expiration issues in 2/3 projects
**Effectiveness:** Caught 4 critical issues in next project
**Cost impact:** +$0.10 per review (more thorough)

## v1 (2025-12-15)
**Initial version**
**Effectiveness:** Caught 8/10 security issues
**Missed:** Token handling, session management edge cases
```

---

### 2.4 Comparison Tool

**Command:**
```bash
scaffold prompt compare --prompt security --versions v1,v2 --project cortana
```

**Output:**
```
Comparing security prompts v1 vs v2 on project: cortana

v1 (security_v1.md):
  Critical issues found: 2
  False positives: 1
  Cost: $0.80
  Missed: JWT expiration handling

v2 (security_v2.md):
  Critical issues found: 4
  False positives: 0
  Cost: $0.90
  Caught: All known issues

Recommendation: Use v2 (more effective, slight cost increase acceptable)
```

---

### 2.5 Learning Loop

**After each project:**
1. Review which prompts worked
2. Identify what was missed
3. Update prompts
4. Archive old version with explanation
5. Use new version on next project
6. Compare effectiveness

---

## Phase 3: Task Dispatch System

**Purpose:** Route tasks to appropriate tiers automatically.

### 3.1 Task Parser

**Reads:** `TIERED_SPRINT_PLANNER.md`

**Extracts:**
```python
{
  "tier_1_tasks": [
    {
      "id": "t1-001",
      "name": "Design database schema",
      "status": "pending",
      "cost_estimate": 10.00,
      "build_prompt": "You are a Tier 1 AI...",
      "review_prompt": "Review database schema for..."
    }
  ],
  "tier_2_tasks": [...],
  "tier_3_tasks": [...]
}
```

---

### 3.2 Tier Router

**Maps tiers to APIs:**
```python
TIER_CONFIG = {
    "tier_1": {
        "model": "claude-opus-4",
        "api": "anthropic",
        "max_cost": 50.00
    },
    "tier_2": {
        "model": "gpt-4o",
        "api": "openai",
        "max_cost": 10.00
    },
    "tier_3": {
        "model": "gpt-4o-mini",
        "api": "openai",
        "max_cost": 2.00
    }
}
```

---

### 3.3 Execution Options

**Option A: Full API Execution**
```bash
scaffold dispatch --tier 3 --execute
```
- Calls API directly
- Executes task automatically
- Saves result
- Tracks cost

**Option B: Hybrid (Cursor for Build)**
```bash
scaffold dispatch --tier 3 --cursor
```
- Generates prompt
- Opens Cursor with prompt pre-loaded
- Erik executes in Cursor (uses cheap credits)
- Marks task complete manually

**Why hybrid?**
- Cursor: $200/mo for $400 credits (2x value!)
- APIs: Pay per token (expensive)
- Reviews need API (for cost tracking)
- Build can use Cursor (for value)

---

### 3.4 Escalation Handling

**Tier 3 task needs escalation:**
```python
# AI response includes:
"🚨 ESCALATE TO TIER 2: Ambiguous business logic around user permissions"

# System detects escalation:
- Marks Tier 3 task as "escalated"
- Creates new Tier 2 task
- Includes context from Tier 3 attempt
- Routes to Tier 2 API
```

**Tracking:**
```json
{
  "task_id": "t3-005",
  "original_tier": 3,
  "escalated_to": 2,
  "reason": "Ambiguous business logic",
  "cost_original": 0.50,
  "cost_after_escalation": 3.00,
  "total_cost": 3.50
}
```

---

### 3.5 Progress Tracking

**Updates sprint plan automatically:**
```markdown
## Tier 3 Tasks
- [x] Create database schema (✅ Completed, $0.10, 2025-12-22)
- [x] Write test fixtures (✅ Completed, $0.08, 2025-12-22)
- [↗] Implement validation (🚨 Escalated to Tier 2, $0.50)
- [ ] Generate API docs (⏳ In Progress)
```

**Legend:**
- `[x]` = Completed
- `[↗]` = Escalated
- `[ ]` = Pending
- `[⏳]` = In Progress

---

## Phase 4: Cost Monitoring & Analytics

### 4.1 Real-Time Cost Dashboard

**While reviews/tasks running:**
```
┌────────────────────────────────────────────────────┐
│ Real-Time Cost Tracking                            │
│ Project: cortana-extension                         │
├────────────────────────────────────────────────────┤
│ SPRINT PLANNING                                    │
│   Document Review Round 1: $2.45                   │
│   Document Review Round 2: $2.60                   │
│   Subtotal: $5.05                                  │
│                                                    │
│ BUILD (In Progress)                                │
│   Tier 1 tasks (3): $28.50                        │
│   Tier 2 tasks (12/30): $36.00 (est. $90 total)  │
│   Tier 3 tasks (20/20): $10.00                    │
│   Subtotal so far: $74.50                         │
│                                                    │
│ CODE REVIEW (Pending)                              │
│   Estimated: $15.00                               │
│                                                    │
│ TOTAL SO FAR: $79.55                              │
│ ESTIMATED FINAL: $94.55                           │
│ ────────────────────────────────────────────────  │
│ Original Estimate: $180.00                        │
│ Variance: -47% (under budget!)                    │
└────────────────────────────────────────────────────┘
```

---

### 4.2 Per-API Breakdown

**Track usage per API:**
```
OpenAI Usage (December 2025):
  Total: $145.00
  Budget: $200.00
  Remaining: $55.00 (27%)
  
  By Project:
    cortana-extension: $75.00
    trading-analyzer: $50.00
    land-monitor: $20.00
  
  ⚠️ Warning: 73% of monthly budget used

Anthropic Usage (December 2025):
  Total: $85.00
  Budget: $150.00
  Remaining: $65.00 (43%)
  
  By Project:
    cortana-extension: $45.00
    image-workflow: $40.00
```

---

### 4.3 Cost Gates

**Before each expensive operation:**
```
┌─────────────────────────────────────────────────┐
│ About to run: Code Review (15 tasks)           │
│                                                 │
│ Estimated cost: $15.00                          │
│ Current project total: $79.55                   │
│ After review total: ~$94.55                     │
│                                                 │
│ Monthly API usage:                              │
│   OpenAI: $145/$200 (73% used)                 │
│   Anthropic: $85/$150 (57% used)               │
│                                                 │
│ Continue? [y/n]                                 │
└─────────────────────────────────────────────────┘
```

---

### 4.4 Post-Project Analysis

**After project ships:**
```bash
scaffold analyze --project cortana-extension
```

**Output:**
```
Project Analysis: cortana-extension
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COST ANALYSIS
  Estimated: $180.00
  Actual:    $94.55
  Variance:  -47% (🎉 UNDER BUDGET!)
  
  By Stage:
    Sprint Planning: $5.05 (est. $10)
    Build:          $74.50 (est. $160)
    Code Review:    $15.00 (est. $10)
  
  By Tier:
    Tier 1: $28.50 (10 tasks, avg $2.85/task)
    Tier 2: $56.00 (30 tasks, avg $1.87/task)
    Tier 3: $10.00 (20 tasks, avg $0.50/task)
  
  Escalations: 2 (Tier 3→2)
    Impact: +$3.00 cost

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TIERING EFFECTIVENESS
  Tier 3: 18/20 succeeded (90%), 2 escalated
  Tier 2: 28/30 succeeded (93%), 2 escalated
  Tier 1: 10/10 succeeded (100%)
  
  Insight: Tiering is working well!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CODE REVIEW EFFECTIVENESS
  Tasks reviewed: 15
  Critical issues found: 4 (security: 2, performance: 2)
  One-pass success: 13/15 (87%)
  Two-pass needed: 2 (⚠️ red flag)
  
  Issues by Reviewer:
    Security (OpenAI):      2 critical, 3 medium
    Performance (Anthropic): 2 critical, 1 medium
    Quality (Google):        0 critical, 4 suggestions
  
  Insight: Security + Performance reviewers caught all critical issues.
  Action: Consider dropping Quality reviewer (no critical finds).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

COST SAVINGS VS ALL-TIER-1
  If all tasks Tier 1: ~$500.00
  Actual with tiering: $94.55
  Savings: $405.45 (81% reduction!)
  
  Conclusion: Tiering is VERY effective for this project type.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LESSONS LEARNED
  ✓ Database tasks tier well to Tier 3 (5/5 succeeded)
  ✓ API tasks suited for Tier 2 (complex but defined)
  ✗ Admin UI tasks under-estimated (2 escalations)
  → Update: Admin UI tasks default to Tier 2 (not Tier 3)
  
  ✓ Security reviewer caught JWT issues (saved production bug!)
  ✓ Performance reviewer caught N+1 query (10x speedup)
  ✗ Quality reviewer found no critical issues
  → Update: Drop Quality reviewer, keep Security + Performance

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROMPT EFFECTIVENESS
  security_v2.md: 2 critical issues found
  performance_v1.md: 2 critical issues found
  
  Recommendation: security_v2 is working well, keep it.
```

---

## Phase 5: End-to-End Flow

### Full Project Lifecycle

```bash
# 1. Create new project
scaffold new cortana-extension

# 2. Create vision document (manual with AI)
# → docs/VISION.md

# 3. Create initial sprint plan (manual with AI)
# → docs/TIERED_SPRINT_PLANNER.md

# 4. Run document reviews (automated)
scaffold review --type document --input docs/TIERED_SPRINT_PLANNER.md --round 1
# Cost: $2.45
# Continue to Round 2? [y]

scaffold review --type document --input docs/TIERED_SPRINT_PLANNER.md --round 2
# Cost: $2.60
# Total so far: $5.05

# 5. Revise sprint plan based on reviews (manual with AI)
# → docs/TIERED_SPRINT_PLANNER.md (updated)

# 6. Generate build/review prompts (automated)
scaffold prompts generate --input docs/TIERED_SPRINT_PLANNER.md
# → Adds prompts to each task in sprint plan

# 7. Execute build (hybrid: Cursor for code, APIs for decisions)
scaffold dispatch --tier 3 --cursor
# Opens Cursor with Tier 3 tasks
# Erik builds in Cursor (cheap credits)

scaffold dispatch --tier 2 --cursor
# Opens Cursor with Tier 2 tasks

scaffold dispatch --tier 1 --execute
# Runs Tier 1 tasks via API (needs smart AI)
# Cost: $28.50

# 8. Run code reviews (automated)
scaffold review --type code --tasks completed
# Runs reviews for all completed tasks
# Cost: $15.00

# 9. Fix issues (hybrid: Cursor for fixes)
scaffold review --type code --tasks completed --recheck
# Re-checks fixed code (one pass only!)

# 10. Ship (manual: deploy, update EXTERNAL_RESOURCES.md)

# 11. Analyze (automated)
scaffold analyze --project cortana-extension
# → docs/analytics/cortana-extension_analysis.md
# → Updates patterns based on learnings
```

---

## Build Order & Timeline

### Week 1: Core Infrastructure

**Day 1-2: Review Orchestrator**
- API integrations (OpenAI, Anthropic, Google)
- Parallel execution
- Cost tracking
- File I/O

**Day 3: Cost Monitoring**
- Real-time dashboard
- Cost gates
- Per-API tracking

**Day 4: Prompt System**
- Directory structure
- Versioning
- CHANGELOG format

**Day 5: Testing & Integration**
- Test with real document review
- Verify cost tracking
- Debug issues

---

### Week 2: Task Dispatch & Analytics

**Day 1-2: Task Parser**
- Parse sprint plan markdown
- Extract tasks by tier
- Extract prompts

**Day 3: Tier Router**
- Route to APIs
- Handle escalations
- Progress tracking

**Day 4: Analytics**
- Post-project analysis
- Comparison to estimates
- Lesson extraction

**Day 5: End-to-End Testing**
- Full workflow test
- Real project (small one)
- Iterate on UX

---

## Tech Stack

**Language:** Python 3.11+

**Dependencies:**
- `openai` - OpenAI API
- `anthropic` - Anthropic API
- `google-generativeai` - Google AI
- `aiohttp` - Async HTTP
- `rich` - Beautiful terminal output
- `pydantic` - Data validation
- `pyyaml` - YAML parsing
- `click` - CLI framework

**Structure:**
```
project-scaffolding/
├── scaffold/
│   ├── cli.py (main CLI)
│   ├── review.py (review orchestrator)
│   ├── dispatch.py (task dispatcher)
│   ├── cost.py (cost tracking)
│   ├── prompts.py (prompt management)
│   └── analyze.py (analytics)
├── prompts/ (prompt versions)
├── templates/ (project templates)
└── tests/
```

---

## API Key Management

**Per-Project Keys (from EXTERNAL_RESOURCES.md):**
```bash
# For reviews (need cost tracking)
SCAFFOLDING_OPENAI_KEY=sk-...
SCAFFOLDING_ANTHROPIC_KEY=sk-ant-...

# For project builds (separate keys)
CORTANA_OPENAI_KEY=sk-...
TRADING_OPENAI_KEY=sk-...
```

**Cost tracking:**
- Reviews use `SCAFFOLDING_*` keys (tracks scaffolding system costs)
- Builds use project-specific keys (tracks project costs)
- Analytics shows both separately

---

## Cost Explosion Mitigation

**1. Dry Run Mode**
```bash
scaffold review --dry-run
# Shows: "Would cost ~$2.45"
# Doesn't actually call APIs
```

**2. Budget Limits**
```yaml
# .scaffold/config.yml
budgets:
  openai:
    monthly: 200
    per_project: 50
  anthropic:
    monthly: 150
    per_project: 40
  
alerts:
  at_percent: 80
  fail_at_percent: 100
```

**3. Cost Estimates Before Execution**
- Every operation shows estimate first
- User confirms before running
- Running total always visible

**4. Per-Stage Reports**
```
Sprint Planning: $5.05 ✅
Build: $74.50 (in progress)
Total so far: $79.55
Remaining budget: $100.45
```

**5. Comparison Mode**
```
Cost with tiering: $94.55
Cost if all Tier 1: ~$500
Savings: 81%
```

---

## Success Metrics (End of January 2026)

**Erik's Adjusted Metrics:**

1. **Cost Reduction**
   - Measure: Tiering cost vs hypothetical all-Tier-1 cost
   - Target: 50%+ savings
   - Challenge: No historical data, so compare to "what if"

2. **Speed (3x Goal)**
   - Measure: If 3 tiers work in parallel, 3x faster
   - Target: Project in 2 days vs 6 days
   - Challenge: Hard to measure without baseline

3. **Bug Reduction**
   - Measure: Bugs found in production after reviews
   - Target: Fewer than last month (already improved with roadmaps)
   - Note: Already seeing benefits from roadmap work

4. **Prompt Effectiveness**
   - Measure: Which prompts catch most issues
   - Target: Continuous improvement in prompt versions
   - This is NEW learning (no baseline)

5. **Cost vs Value**
   - Measure: Is cost explosion happening?
   - Target: Cost ≤ 2x current spend
   - Red flag: If cost 2x but speed not 2x

---

## Questions & Clarifications

**Q: Why APIs for reviews but maybe Cursor for build?**
A: APIs give real-time cost tracking. Cursor gives cheap credits ($20 for $400 value). Use APIs where we need data, Cursor where we need value.

**Q: How do we track Cursor costs?**
A: We can't in real-time. But Cursor shows usage in settings. We manually export at end of month.

**Q: What if API costs explode?**
A: Cost gates at every stage. User approves before continuing. Can stop anytime.

**Q: 3x speed - realistic?**
A: If 3 tiers work truly in parallel (not blocking each other), yes. If they block each other, no.

**Q: Biggest risk?**
A: Cost explosion. Mitigation: dry-run mode, cost gates, budget limits, comparison to estimates.

---

## Next Immediate Steps

1. **Set up project structure**
   ```bash
   mkdir -p scaffold/{review,dispatch,cost,prompts,analyze}
   touch scaffold/{cli,review,dispatch,cost,prompts,analyze}.py
   ```

2. **Install dependencies**
   ```bash
   pip install openai anthropic google-generativeai aiohttp rich pydantic click
   ```

3. **Create prompt templates**
   ```bash
   mkdir -p prompts/{versions,active}
   # Create security/performance/architecture prompts
   ```

4. **Build review orchestrator (Day 1)**
   - OpenAI integration
   - Parallel execution
   - Cost tracking
   - File save

5. **Test with real document**
   - Use existing `docs/VISION.md`
   - Run 3 reviews
   - Verify cost tracking
   - Iterate

---

**Status:** Ready to build  
**Start:** TODAY (December 22, 2025)  
**Target:** Week 1 done by December 29, Week 2 done by January 5

**Let's do this!** 🚀

