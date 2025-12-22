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

**Integration Alert:**
🔗 **Project Tracker will include monitoring for tiered system effectiveness**
- Track: Is tiered sprint planning working?
- Measure: Time saved, cost savings, quality maintained
- Learn: Which tasks tier well vs poorly
- Optimize: Adjust tiering based on actual data
- **Coming soon:** Integration between scaffolding patterns and tracker monitoring

**Why this matters:**
Everything is a learning opportunity. We're building the system, using the system, AND measuring if the system works. That's the meta-meta level.

**Status:** Discussion needed (Tier 1 work!)

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

**The problem:**
- Too nice: "Everything's perfect!" (not helpful)
- Too grumpy: "Everything sucks!" (also not helpful)
- Right balance: Constructive criticism with specific actionable feedback

**Solution needed:**
- Prompt engineering for "constructive skeptic" persona
- Examples of good critique vs bad critique
- Calibration: Test prompts, measure usefulness

**Who solves this:** Tier 1 (architecture of prompts)

---

#### Q2: Cost Explosion Risk
**Question:** How many AI calls are we making?

**Math:**
```
Stage 1 (Project Creation):
  - 1 initial roadmap (you + Claude): $5
  - 5 grumpy reviewers: 5 × $3 = $15
  - 2 revision rounds: 2 × (you + Claude + reviewers) = $40
  Total: ~$60 per project

Stage 2 (Build):
  - Tier 1 tasks: 10 × $8 = $80
  - Tier 2 tasks: 30 × $3 = $90
  - Tier 3 tasks: 20 × $0.50 = $10
  Total: ~$180 per project

Stage 3 (Code Review):
  - 5 files × 3 reviewers × $2 = $30
  - 2 review rounds = $60
  Total: ~$60 per project

GRAND TOTAL: ~$300 per project
```

**Questions:**
- Is $300/project worth it?
- Which stages provide most value?
- Can we skip any rounds?
- Should smaller projects use fewer reviewers?

---

#### Q3: Human Bottleneck Problem
**Question:** Where does human review fit?

**The tension:**
- Full automation = fast but risky
- Human-in-loop = safe but slow
- Hybrid = complicated

**Current pipeline has human review after:**
1. Stage 1 (before building)
2. Stage 3 (before merging)

**But NOT in Stage 2 (build)** - is that safe?

**Risk:** Automated build goes wrong direction, waste time/money

**Solution options:**
- A) Full automation, trust the system
- B) Checkpoints: Human review at key milestones
- C) Parallel tracks: Human codes alongside automation, compare results

**Decision needed:** How much automation vs human oversight?

---

#### Q4: Quality vs Speed Tradeoff
**Question:** Does more AI review = better quality?

**Hypothesis:** Diminishing returns after N reviewers

**To test:**
- Start with 3 reviewers, measure quality
- Add 4th reviewer, does quality improve?
- Add 5th reviewer, still improving?
- Find optimal N (probably 3-5)

**Project Tracker integration:**
- Track: # of reviewers vs bugs found later
- Learn: Optimal reviewer count per project type
- Optimize: Adjust based on data

---

#### Q5: Reviewer Diversity Problem
**Question:** Do we want different models or different prompts?

**Option A: Different models (Claude, GPT, Gemini)**
- Pro: Genuinely different architectures, different blind spots
- Con: Expensive, some models worse than others

**Option B: Same model, different prompts (multiple Claudes with different personas)**
- Pro: Cheaper, controlled diversity
- Con: Same underlying model = similar biases

**Option C: Hybrid (2-3 models, each with different prompts)**
- Pro: Real diversity, manageable cost
- Con: Complex to orchestrate

**Decision needed:** Which option?

---

#### Q6: The "Sunshine Problem"
**Question:** How do you detect and prevent useless positive reviews?

**Example useless review:**
```
"This is a great idea! You're so smart! 
I see no issues. Ship it!"
```

**Detection strategies:**
- A) Word count minimum (must be >500 words)
- B) Required sections (must address: risks, edge cases, alternatives)
- C) Critique quota ("find at least 3 potential issues")
- D) Meta-review: Another AI checks if review is useful

**Implementation:**
- Prompt: "Your job is to find problems. If you don't find at least 3 concerns, you're not doing your job."
- Format: "RISKS: [list], EDGE CASES: [list], ALTERNATIVES: [list]"
- Validation: Check if these sections exist and have content

---

#### Q7: Integration Complexity
**Question:** How does this integrate with existing tools?

**Current tools:**
- Tiered Sprint Planner (scaffolding)
- Project Tracker (in progress)
- Dispatch system (planned)

**New tools needed:**
- Roadmap Review Orchestrator
- Build Automation System  
- Code Review Orchestrator

**Question:** Are these separate tools or one big system?

**My vote:** Separate but coordinated
- Roadmap Review: Part of project kickoff (scaffolding related)
- Build Automation: Part of dispatch system
- Code Review: Standalone (already exists in image-workflow)

---

### What Needs to Happen

**Phase 1: Prove Value (Don't Build Full System Yet)**
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

