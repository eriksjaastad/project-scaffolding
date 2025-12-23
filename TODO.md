# Project Scaffolding - TODO

> **Purpose:** Track work specific to project-scaffolding meta-project  
> **Last Updated:** December 22, 2025

---

## 🎯 Next Active Task

### Step-by-Step Walkthrough of Complete System

**Goal:** Map out the entire flow from idea → shipped code

**When to do:** When Erik has full attention (not distracted by work computer)

**What to do:**
1. **Map each stage:** Idea → Sprint planning → Build → Code review → Ship
2. **Detail each step:** Who does what, what inputs/outputs, what prompts used
3. **Identify tools needed:** What exists, what needs building
4. **Check for over-engineering:** Are we making this too complex?
5. **Check for gaps:** What are we missing?

**Output:** Complete process diagram with:
- Clear stages
- Clear handoffs
- Clear prompts
- Clear automation opportunities
- **Reality check on complexity (over-engineering gauge)**

**Over-Engineering Concerns (Erik's Question):**

"How will we know if this is overly engineered?"

**Warning signs to watch for:**
1. **Complexity Tax:** Does setup take longer than first project delivery?
2. **Cognitive Overhead:** Is it harder to think about the system than just do the work?
3. **Maintenance Burden:** Are we spending more time fixing the system than using it?
4. **Diminishing Returns:** Is each new feature adding less value than the last?
5. **Analysis Paralysis:** Are we stuck planning instead of building?

**Reality checks:**
- If scaffolding project takes 2 weeks, first real project should ship in < 1 week
- If we're on TODO item #50 and still planning, we're over-engineering
- If Erik's image-workflow instincts kick in ("left alone too long"), pull back
- If we can't explain the system in 5 minutes, it's too complex

**Simple litmus test:**
- Can Erik start a new project in < 30 minutes using scaffolding?
- Does it make next project faster/better/cheaper?
- Would Erik use this if he wasn't building it?

If any answer is "no," we over-engineered.

**Status:** Ready when Erik has focus time

---

## 🔄 Previous Active Task (Completed for Now)

### Reevaluate TODO List for Tiered Implementation

**Status:** Planning phase in progress
- ✅ Captured automation pipeline vision
- ✅ Answered 7 critical questions
- ✅ Defined 3 rounds + 1 prompt generation approach
- ✅ Identified task dispatcher as first priority
- ⏸️ Paused: Erik distracted by work, will continue when focused

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

**Integration Alert:**
🔗 **Project Tracker will include monitoring for tiered system effectiveness**
- Track: Is tiered sprint planning working?
- Measure: Time saved, cost savings, quality maintained
- Learn: Which tasks tier well vs poorly
- Optimize: Adjust tiering based on actual data
- **Coming soon:** Integration between scaffolding patterns and tracker monitoring

**Why this matters:**
Everything is a learning opportunity. We're building the system, using the system, AND measuring if the system works. That's the meta-meta level.

---

## 📊 Learning & Analytics Layer (Critical!)

**The Problem Erik Identified:**
- Projects finish in days/weeks
- Data becomes available immediately  
- Waiting 3 months to review is TOO SLOW
- Need continuous learning loop

**The Separation:**
```
DOING THE WORK          REVIEWING THE RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sprint planning    ←→   Cost estimate accuracy
Build project      ←→   Tiering effectiveness  
Code reviews       ←→   Review quality/usefulness
Ship               ←→   Final quality assessment
```

**We need BOTH layers running:**
- **Execution layer:** Do the work
- **Learning layer:** Review how the work went

---

### Learning Loop Cadence

**NOT quarterly - that's way too slow!**

**Per-Project Learning (Immediate):**
After EACH project completes:
- [ ] **AUTOMATED:** Spin up local server with data export links
- [ ] Download actual costs from Cursor/APIs (via served links)
- [ ] Compare: Estimated costs vs actual costs
- [ ] Analyze: Where were we way off? Over? Under?
- [ ] Document: Lessons learned
- [ ] Update: Cost estimation models

**Frequency:** After every project (could be days apart!)

**Why:** Data is fresh, lessons are actionable, next project benefits immediately

**Automation (Remove the weakest link):**
Erik's insight: "Weakest link is relying on me to do something at the right time."

**Solution:** At end of sprint (all code reviews done):
```bash
# Automatically runs:
python scripts/data_export_server.py
```

**What it does:**
- Spins up local web server (e.g., http://localhost:8000)
- Shows page with links to:
  - Cursor API usage export
  - OpenAI API usage export
  - Anthropic API usage export
  - Any other relevant data sources
- Erik clicks links, exports data
- Data automatically goes to `project/analytics/raw/`
- Analysis script runs automatically

**Why this works:**
- Project completion triggers data collection
- In lockstep with finishing project
- Not relying on Erik to remember
- Data captured at the right moment

---

**Weekly Learning (Pattern Level):**
Every week:
- [ ] Review: Which tasks tier well consistently?
- [ ] Review: Which tasks always mis-tier?
- [ ] Review: Are reviews catching real issues?
- [ ] Review: Is one-pass code review working?
- [ ] Update: Tiering guidelines based on patterns

**Frequency:** Weekly (not monthly, not quarterly)

**Why:** Projects finish quickly, patterns emerge fast, need rapid iteration

---

**Monthly Learning (System Level):**
Every month:
- [ ] Review: Is the whole system worth it?
- [ ] Review: Cost savings vs added complexity?
- [ ] Review: Time saved vs time invested?
- [ ] Review: Quality improvement measurable?
- [ ] Decide: Continue, adjust, or abandon?

**Frequency:** Monthly reality checks

**Why:** Big picture assessment, course correction if needed

---

### Data Collection Points

**From Sprint Planning:**
- Estimated costs per task
- Estimated costs per tier
- Estimated total project cost
- Time to complete planning

**From Build Phase:**
- Actual API calls made
- Actual costs per task
- Escalations (Tier 3 → 2 → 1)
- One-pass success rate

**From Code Review:**
- Issues found by each reviewer
- Issues actually valid (not false positives)
- Issues that shipped to production (reviews missed)
- Review round count (should be 1)

**From Project Completion:**
- Total actual cost
- Total actual time
- Quality assessment (bugs found later?)
- Would we do this again?

---

### Learning Questions to Answer

**Cost estimation:**
- Where are estimates most accurate? (Tier 1/2/3?)
- What types of tasks consistently over/under-estimated?
- Is estimation improving over time?

**Tiering effectiveness:**
- Which tasks tier well?
- Which tasks always mis-tier?
- Is Tier 3 actually useful or just cheap-but-wrong?

**Review quality:**
- Which reviewers catch real issues?
- Which reviewers produce sunshine?
- Are adversarial prompts working?
- Is one-pass code review viable?

**System ROI:**
- Time: Faster than manual?
- Cost: Worth the AI spend?
- Quality: Better than without system?
- Stress: Reducing cognitive load?

---

### Analytics Integration (Project Tracker - SEPARATE PROJECT)

**SCOPE CLARITY:**
- **Project Scaffolding:** Standards, patterns, templates, recommendations
- **Project Tracker:** Actual implementation of monitoring/visualization
- **Relationship:** Scaffolding defines what to measure, Tracker implements it

**Project Tracker will show (Erik's vision):**
- All projects (which are active)
- Which have cron jobs running
- Which actively use AI (costing money)
- What hosted services each uses
- Active TODOs (first item, incomplete count)
- Cost estimates vs actual costs
- Tiering success rates
- Which patterns work/don't

**Project Tracker will do (for analytics):**
- Read cost estimates from sprint plans
- Read actual costs from billing data
- Calculate: Estimate accuracy per project
- Track: Tiering success rate
- Show: Which patterns work, which don't
- Alert: "Estimates consistently 50% low on Tier 2 tasks"

**Visualization ideas:**
```
COST ESTIMATION ACCURACY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project A: Estimated $180, Actual $165 (8% under) ✅
Project B: Estimated $200, Actual $320 (60% over) 🚨
Project C: Estimated $150, Actual $145 (3% under) ✅

Trend: Tier 2 tasks consistently 40% over estimate
Action: Revise Tier 2 cost multiplier

TIERING EFFECTIVENESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tier 3 success rate: 60% (40% needed escalation)
Tier 2 success rate: 85%
Tier 1 success rate: 95%

Insight: Tier 3 only useful for true boilerplate
Action: Be more conservative with Tier 3 assignments
```

**Why separation matters:**
- Project Scaffolding stays in scope (patterns, not implementations)
- Project Tracker is a real project (builds the actual monitoring)
- Scaffolding can recommend tracker patterns back to itself (meta-loop!)

---

### Where This Lives

**In project-scaffolding:**
- Pattern: How to do learning loop
- Template: Learning review checklist

**In project-tracker:**
- Implementation: Actual analytics/visualization
- Data collection: From projects
- Insights: What's working/not working

**In each project:**
- Data files: Cost estimates, actual costs, lessons learned
- Directory: `project/analytics/` or `project/metrics/`

---

### Immediate Action Items

**To enable learning loop:**
- [ ] Add cost estimates to sprint planner template
- [ ] Create post-project review checklist
- [ ] Define data format for tracking
- [ ] Build into Project Tracker (Phase 4?)
- [ ] Test on next project

**Status:** Critical for system to improve, design needed

---

## 💭 Vision: Full Automation Pipeline (Pie-in-the-Sky Ideal)

**From Erik (Dec 22, 2025 - Driving thoughts):**

### The Three-Stage Pipeline

```
STAGE 1: Project Creation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You + AI → Initial roadmap
     ↓
Multiple AI rounds (grumpy reviewers)
  - Not sunshine: "Great idea! You're so smart!"
  - Real critique: Poke holes, find issues
  - Multiple perspectives
     ↓
Human review/revision
     ↓
Output: Solid roadmap + tiered sprint plan

STAGE 2: Build Process (Automated Execution)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sprint plan (Tier 1/2/3) → Dispatch system
     ↓
Tier 3 builds boilerplate
Tier 2 builds features
Tier 1 handles architecture
     ↓
Output: Working code

STAGE 3: Code Review (Multi-AI Review)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Code → Multiple AI reviewers
  - Different models, different perspectives
  - Pattern: Already exists in image-workflow
     ↓
Human final review
     ↓
Output: Reviewed, merged code
```

### Directory Structure

**Default for all projects:**
```
project/
├── roadmap-reviews/
│   ├── 2025-12-22_claude-opus-4-review.md
│   ├── 2025-12-22_gpt-4-review.md
│   ├── 2025-12-22_gemini-review.md
│   └── 2025-12-23_revision-v2-reviews/
│
├── code-reviews/
│   ├── 2025-12-25_feature-x-reviews/
│   │   ├── claude-review.md
│   │   ├── gpt-review.md
│   │   └── grok-review.md
│   └── 2025-12-26_refactor-y-reviews/
│
└── docs/
    ├── ROADMAP.md (final version)
    └── SPRINT_PLAN.md (tiered)
```

**Why these directories:**
- Project Tracker can scan them for insights
- Learn which reviewers catch which issues
- Track improvement over time
- Audit trail of decisions

---

### Critical Questions (Holes to Poke)

#### Q1: Prompt Engineering Challenge
**Question:** How do you make reviewers "grumpy" without making them useless?

**Erik's answer:**
- Has a general prompt to work with (work in progress)
- **Discovery:** Told Claude "someone else made this project" → Claude shredded it
- Claude's response: "Well, you told me it was somebody else's project, so fuck them"
- **Magic discovered:** Framing matters! "Review this" vs "Review someone else's work"

**Prompt engineering approaches:**
1. **"Third-party" framing:** "You're reviewing someone else's project. Be critical."
2. **Adversarial framing:** "Your job is to find what's wrong. You get paid per issue found."
3. **Expert skeptic:** "You're a senior architect. This is a junior's proposal. What would you change?"

**Status:** Has starting point, needs iteration

---

#### Q2: Cost Explosion Risk
**Question:** How many AI calls are we making? Is $300/project worth it?

**Erik's answer:**
- Billing tracker will track costs (we'll know actual spend)
- Tiered system should help (save on Tier 2/3 during build phase)
- **Faith in the system:** Build costs will offset review costs
- January will be the real test

**Adjusted math:**
```
Stage 1: $60 (multiple reviewers, Tier 1 models)
Stage 2: $180 → Maybe $90 if Tier 2/3 do more work
Stage 3: $60 (code reviews, Tier 1 models)
Total: $210/project (if tiering works)
```

**Mitigation:** Billing tracker + tiered dispatch will show if it's working

**Status:** Accept risk, measure in January

---

#### Q3: Human Bottleneck Problem
**Question:** Where does human review fit?

**Erik's answer:**
- Human creates initial document
- AI does multiple review rounds
- Human reviews at the end
- **Key insight:** "It's just having you paste the prompts instead of me"
- Not fundamentally different from current workflow
- Automation = removing manual prompt pasting

**Current workflow:**
```
Erik → Document → Erik pastes to AI 1 → Erik pastes to AI 2 → Erik pastes to AI 3 → Erik reviews
```

**Automated workflow:**
```
Erik → Document → Script calls AI 1, 2, 3 in parallel → Erik reviews
```

**Time saved:** Maybe 30 minutes of copying/pasting per project
**Risk reduced:** No copy/paste errors, consistent prompts

**Status:** Human at start and end, automation in middle = good balance

---

#### Q4: Quality vs Speed Tradeoff
**Question:** Does more AI review = better quality?

**Erik's answer:**
- Never gone over 3 reviewers
- **Decision: 3 reviewers is the sweet spot**
- Each reviewer has different angle of skepticism
- Work in progress on defining those angles

**Three angles idea:**
1. **Security skeptic:** "What could go wrong? What's the attack surface?"
2. **Performance skeptic:** "Will this scale? Where are the bottlenecks?"
3. **Maintainability skeptic:** "Can someone else understand this in 6 months?"

Or different framing:
1. **Pessimist:** "This will fail because..."
2. **Realist:** "This could work if..."
3. **Optimist (but critical):** "This is good but needs..."

**Status:** 3 reviewers confirmed, need to define personas

---

#### Q5: Reviewer Diversity Problem
**Question:** Do we want different models or different prompts?

**Erik's answer:**
- **Stage 1 & 3 (Reviews):** Tier 1 models (Claude Sonnet, GPT-4, etc.)
- **Stage 2 (Build):** Tier 2 & 3 will save money
- **Experiment in January:** Integrate Kiro and Anti-Gravity IDEs
- Need to investigate how Kiro works

**Model strategy:**
- Reviews = expensive models (quality matters)
- Building = cheaper models where possible (tiered savings)
- Net cost: Should balance out

**New platforms to explore:**
- **Kiro:** Need to investigate API access
- **Anti-Gravity:** Already have access
- Both could add to reviewer diversity

**Status:** Tier 1 for reviews, need Kiro investigation

---

#### Q6: The "Sunshine Problem"
**Question:** How do you detect and prevent useless positive reviews?

**Erik's answer:**
- "That's gonna be hard to do"
- Leans heavily on AI expertise
- Doesn't know how to detect useless reviews
- **Asks:** "If you have ideas, I'm totally open"

**My ideas (Claude Sonnet 4.5):**

**Detection Strategy A: Structural Requirements**
Force reviewers to fill required sections:
```markdown
REQUIRED REVIEW FORMAT:

## CRITICAL RISKS (minimum 3)
1. [Must list at least 3 serious risks]
2. 
3. 

## EDGE CASES NOT HANDLED (minimum 3)
1. [What breaks in unusual scenarios?]
2.
3.

## ALTERNATIVE APPROACHES (minimum 2)
1. [What else could work? Why wasn't it chosen?]
2.

## ASSUMPTIONS THAT MIGHT BE WRONG (minimum 2)
1. [What are we taking for granted?]
2.

## IF I HAD TO BREAK THIS, I'D... (minimum 2)
1. [Adversarial thinking]
2.
```

**Why this works:** Can't say "looks great!" if forced to fill these sections.

---

**Detection Strategy B: Meta-Review**
After each review, another AI checks if the review is useful:

```
Prompt: "You're a review quality checker. 
Score this project review on:
- Specificity (1-10): Are critiques specific or vague?
- Actionability (1-10): Can you act on the feedback?
- Depth (1-10): Surface-level or deep analysis?
- Risk identification (1-10): Did it find real risks?

If any score < 6, this review is too shallow. 
Flag it and explain why."
```

**Cost:** Extra $1-2 per review, but catches sunshine reviews.

---

**Detection Strategy C: Word Pattern Analysis**
Flag reviews with too many positive words:

```python
sunshine_phrases = [
    "looks great",
    "perfect",
    "no issues",
    "you're so smart",
    "ship it",
    "I see no problems"
]

critical_phrases = [
    "concern",
    "risk",
    "could fail",
    "edge case",
    "what if",
    "assumption"
]

sunshine_count = count_phrases(review, sunshine_phrases)
critical_count = count_phrases(review, critical_phrases)

if sunshine_count > critical_count:
    flag_as_useless()
```

**Simple but effective:** Quick automated check.

---

**Detection Strategy D: Constructive Skeptic Framing**
Based on Erik's discovery, but avoiding "competitor" trap:

```
Prompt: "You're a senior architect reviewing a junior's project proposal.

Your job is NOT to judge if the idea is good or profitable.
Your job IS to make this idea as solid as possible.

Assume the project WILL be built. Your goal:
- Find every technical flaw
- Identify every edge case
- Question every assumption
- Suggest better approaches

Be ruthlessly critical of the EXECUTION, not the VISION.

Don't say: "This project won't make money" or "Who would use this?"
DO say: "This implementation will fail because..." or "What if the user does X?"

You're making it better, not killing it."
```

**Psychology:** Critical of HOW, not WHY. Focuses on technical execution, not business viability.

**Erik's constraint:** These are personal/learning projects. We want best implementation, not business critique.

---

**My recommendation: Combine A (structure) + D (constructive skeptic)**
- Force structured format with minimum items (A)
- Frame as "make it better" not "is it good" (D)
- Avoids money/usefulness rabbit holes
- Focuses on technical execution

**Status:** Multiple strategies available, recommend A + D

---

#### Q7: Integration Complexity
**Question:** How does this integrate with existing tools?

**Erik's answer:** "I'm not exactly sure what you mean by this"

**My clarification:**
You're building multiple systems:
- Tiered Sprint Planner (exists)
- Project Tracker (in progress)
- Dispatch System (planned)
- Roadmap Review Orchestrator (planned)
- Build Automation (planned)
- Code Review Orchestrator (planned)

**My question was:** Are these:
- **Option A:** One big integrated system (like n8n - everything in one place)
- **Option B:** Separate tools that coordinate (Unix philosophy - small tools, work together)
- **Option C:** Some integrated, some separate

**Example of complexity:**
If Roadmap Review Orchestrator is separate from Dispatch System, they need to:
- Share TODO format
- Both write to same directories
- Both report to Project Tracker
- Coordinate on task status

vs. if they're one system, integration is easier but system is more complex.

**My vote:** Option B (separate tools, coordinate via files/conventions)
- Roadmap reviews write to `roadmap-reviews/`
- Dispatch system reads `SPRINT_PLAN.md`
- Code reviews write to `code-reviews/`
- Project Tracker reads all three
- Each tool is simple, coordination via file formats

**Status:** Needs decision on architecture approach

### What Needs to Happen

**Where we are now:** Planning Phase (Tier 1 conversation - THIS conversation!)
- Defining the system
- Poking holes  
- Answering architecture questions
- **Sprint planning comes AFTER this**

---

**CRITICAL INSIGHT (Dec 22, driving thoughts + discussion):**

**Sprint planning process: 3 rounds + 1 prompt generation**

**Round 1-3: Create sprint plan**
- You + AI create initial roadmap
- 3 grumpy reviewers critique (different angles)
- Revise based on feedback
- Result: Solid sprint plan with Tier 1/2/3 tasks

**Round 4: Generate prompts + cost estimates**
- AI looks at finalized tasks
- Generates **build prompts** for each task (what Tier X needs to execute)
- Generates **code review prompts** for each task (what reviewers should check)
- **Estimates costs** per task and total project
- Context is fresh, prompts are specific

**Example output:**
```markdown
## Tier 2 Tasks

### Task: Implement user authentication
**Estimated cost:** ~$3 (Tier 2, medium complexity)

**Build prompt for Tier 2:**
"Implement user authentication with:
- bcrypt password hashing
- JWT tokens (15min expiry)
- Session storage in Redis
- Rate limiting (5 attempts/min)
Follow pattern in docs/architecture/AUTH.md"

**Code review prompt:**
"Review auth implementation for:
- Security: bcrypt properly configured?
- Tokens: Expiry enforced?
- Sessions: Redis connection handling?
- Rate limiting: Actually working?"
```

**Cost estimation purpose:**
- NOT for real-time tracking (not possible across IDEs)
- FOR backtesting against actual data
- Download Cursor usage data → compare estimates vs actual
- Learn: Where were we way off? Over or under?
- Improve: Adjust future estimates based on real results

**Project total estimate example:**
```
Tier 1: 10 tasks × $8 = $80
Tier 2: 30 tasks × $3 = $90
Tier 3: 20 tasks × $0.50 = $10
Total estimate: $180

(Compare against actual spend after project complete)
```

**Status:** Design this into sprint planner flow

---

**First Priority: Task Dispatcher/Runner**

**Why first:**
- Reusable between sprint planning phase AND code review phase
- Both need to call multiple AIs
- Both need to collect responses
- Both need structured output

**What it needs to do:**
1. Take a prompt (or set of prompts)
2. Send to multiple AIs (3 reviewers or 3 tiers)
3. Collect responses
4. Format output (markdown in appropriate directory)
5. Track status (what's done)

**Status:** Architecture needed (Tier 1), then build (Tier 2)

---

**Code Review Flow (Must Be One-Pass)**

Erik's concern: Can't have multiple review rounds on same code. That's failure.

**Correct flow:**
```
Code written (by Tier X)
    ↓
Reviewers review (3 AIs with specific prompts)
    ↓
Original AI implements changes
    ↓
Reviewers CHECK changes were made correctly
    ↓
DONE
```

**WRONG flow (red flag):**
```
Code written
    ↓
Review 1 → Changes → Review 2 → More changes → Review 3...
(This means Tier 3 isn't capable or instructions weren't clear)
```

**If multiple rounds needed:**
- Task was mis-tiered (should have been higher tier)
- Instructions weren't explicit enough
- Model not capable
- **FIX:** Re-tier task, escalate, or improve instructions

**Status:** Document this in sprint planner pattern

---
- [ ] **Stage 1 Manual Test:** Take next new project, do multi-AI roadmap review manually
  - Use 3 reviewers (Claude, GPT-4, Gemini)
  - Engineer "grumpy" prompts
  - Measure: Did reviews catch real issues?
  - Measure: Was it worth $15 vs just building?

- [ ] **Stage 3 Already Exists:** Study image-workflow code review pattern
  - What worked?
  - What didn't?
  - Extract pattern if proven

- [ ] **Stage 2 Don't Automate Yet:** Build dispatch system first, use manually

**Phase 2: If Manual Tests Work, Build Automation**
- [ ] Roadmap Review Orchestrator (script that calls multiple APIs)
- [ ] Build Dispatch System (already planned)
- [ ] Code Review Orchestrator (if image-workflow pattern proves out)

**Phase 3: Integration with Project Tracker**
- [ ] Scan roadmap-reviews/ and code-reviews/ directories
- [ ] Extract insights (which reviewers catch what)
- [ ] Optimize (adjust based on data)

---

### Directory Structure Pattern (Add to Templates)

When proven, add to scaffolding templates:

```
templates/
├── roadmap-reviews/
│   └── README.md (how to use this directory)
├── code-reviews/
│   └── README.md (how to use this directory)
└── .cursorrules.template (updated with review workflow)
```

---

### Prompt Engineering Challenges

**For each stage, need to engineer:**

**Stage 1 (Roadmap Review):**
- Constructive skeptic persona
- Must find N issues (not just praise)
- Specific, actionable feedback
- Compare to alternatives

**Stage 2 (Build Dispatch):**
- Clear tier identification
- Escalation triggers
- Error handling

**Stage 3 (Code Review):**
- Security focus
- Performance focus
- Maintainability focus
- Different reviewers = different angles

**This is hard!** Prompt engineering is Tier 1 work.

---

### Erik's Concern: Pushback Needed

**My pushback:**

**1. Cost:** $300/project is significant. Prove value before automating.

**2. Complexity:** Three stages × multiple AIs × orchestration = LOT of moving parts. Start with manual, automate gradually.

**3. Diminishing Returns:** After 3-5 reviewers, probably not much new insight. Test to find optimal N.

**4. Human Still Needed:** Automation doesn't replace judgment, it augments it. Don't remove human from critical decisions.

**5. Prompt Engineering is Hard:** Getting "grumpy but useful" reviewers is non-trivial. Needs iteration.

**6. Integration Debt:** More systems = more maintenance. Each automation adds technical debt.

**But...**

**It's a compelling vision IF:**
- Start small (manual tests)
- Prove value at each stage
- Automate only what's proven
- Measure effectiveness
- Iterate based on data

**The learning loop matters more than the automation.**

If manual multi-AI review teaches you something, that's valuable even without automation.

---

### Next Steps (If Pursuing This)

**Immediate (This Week):**
- [ ] Create prompts for "grumpy reviewer" personas
- [ ] Test on a small project (or refactor)
- [ ] Measure: Did it catch real issues?

**Short Term (This Month):**
- [ ] Extract image-workflow code review pattern
- [ ] Document what worked/didn't
- [ ] Decide if worth automating

**Long Term (2026):**
- [ ] If proven: Build orchestration
- [ ] If not: Learn from manual process, maybe automate later

---

**Status:** Vision documented, holes poked, needs discussion (Tier 1!)

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

**Clarification:** This means extracting patterns FROM agent_os TO scaffolding as reusable documentation. NOT about making every project use agent_os.

**Example:** "Run tracking pattern" = how to log execution status, timestamps, errors in SQLite. Other projects can use this pattern even if not using agent_os itself.

**Wait for:** agent_os architecture decisions, patterns proven across multiple projects

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
- [ ] Review patterns after each project (not quarterly - too slow!)
- [ ] Run learning loop weekly (pattern-level insights)
- [ ] Run learning loop monthly (system-level reality check)
- [ ] Update EXTERNAL_RESOURCES.md as services added (automated via Cursor rule)
- [ ] Extract patterns when 2-3 projects show same approach
- [ ] Update templates based on real usage (scaffolding is living, not static)
- [ ] Update cost estimation models based on actual data

### Documentation Health
- [ ] Keep README current with project status
- [ ] Archive outdated session notes (prevent "should have cleaned this 6 months ago")
- [ ] Ensure all patterns have "last updated" dates
- [ ] Check that examples still match current projects
- [ ] Document lessons learned from each project

**Note on cadence:**
- **Per-project:** Learn immediately (cost accuracy, tiering effectiveness)
- **Weekly:** Pattern-level insights (what's working/not working)
- **Monthly:** System-level reality check (is this worth it?)
- **NOT quarterly:** Way too slow when projects finish in days/weeks

---

## 📋 Project Scaffolding: Mission & Scope

**What We Are:**
> "A standards and [best practices] recommending body to help all projects get done quickly, at the highest quality, and at the lowest cost."

**Our Job:**
- Define patterns that work across projects
- Create templates that accelerate project starts
- Recommend processes that improve quality/speed/cost
- **Measure if our recommendations actually work** (meta level 3)
- Continuously improve based on real project data

**What We Are NOT:**
- Not a specific project implementation (that's Project Tracker's job)
- Not domain-specific code (that's trading/images/etc.)
- Not a product (we're the factory that builds factories)

**Success Criteria:**
- Other projects start faster because of scaffolding
- Other projects cost less because of scaffolding
- Other projects have higher quality because of scaffolding
- **We can prove it with data**

**Scope Boundary:**
- **IN SCOPE:** Patterns, templates, guidelines, measurements, recommendations
- **OUT OF SCOPE:** Implementing monitoring tools (Project Tracker), domain code (trading, images)

---

### Documentation Health
- [ ] Keep README current with project status
- [ ] Archive outdated session notes (prevent "should have cleaned this 6 months ago")
- [ ] Ensure all patterns have "last updated" dates
- [ ] Check that examples still match current projects

**Note on Tier 3:**
Need to figure out what Tier 3 is actually good at. Fast doesn't matter if code review is wrong and needs redoing. 

**Red flag:** If Tier 3 produces work that needs multiple review rounds, either:
- Task was mis-tiered (should be Tier 2)
- Instructions weren't explicit enough
- Model isn't capable for this type of work

**Goal:** One-pass reviews. If review fails, that's a tiering problem, not a "do it again" problem.

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

**project-tracker (SEPARATE PROJECT):**
- **Purpose:** Implement the monitoring/visualization that scaffolding defines
- **Relationship:** Scaffolding says "measure this," Tracker builds the tool
- Integration documented in `project-tracker/docs/INTEGRATION_WITH_SCAFFOLDING.md`
- Tracker reads EXTERNAL_RESOURCES.md
- Tracker shows which projects use scaffolding templates
- Tracker implements the analytics layer scaffolding designed
- **Erik's Vision:** Show all projects, active status, cron jobs, AI usage, hosted services, TODOs, cost tracking

**Other projects:**
- Source patterns from: image-workflow, Trading Co-Pilot, Cortana, Hologram
- Extract patterns TO: This project
- Apply patterns IN: All future projects

---

## Notes

**The three-level game:**
- **Level 1:** Domain projects (trading, images, AI) - Build things
- **Level 2:** Meta projects (scaffolding, tracker) - Build tools to build things
- **Level 3:** Measurement (analytics layer) - Measure if the tools work

**This is a Level 2 + 3 project:**
- Level 2: Define patterns, create templates
- Level 3: Measure if patterns/templates actually help

**Success = Other projects are easier/better/cheaper because of this one. And we can prove it.**

---

**Last Updated:** December 22, 2025  
**Next Review:** End of January 2026 (after holidays, new projects in 2026)

