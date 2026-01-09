# Tiered Sprint Planner Template

> **Purpose:** Break down project work into tier-appropriate tasks for cost-effective execution  
> **Use After:** Phase 1 planning is complete (big idea → concrete plan)  
> **Pattern Reference:** `../patterns/tiered-ai-sprint-planning.md`

---

## How This Works

**DON'T tier during planning.** Planning IS Tier 1 work (architecture, breaking down, poking holes).

**DO tier during execution.** Once you have a solid plan, divide the work by complexity.

---

## Phase 1: Planning (Tier 1 - Keep Using Sonnet/Opus)

This phase is conversations with expensive models. That's correct and necessary.

**Typical Flow:**
1. **Big hand-wavy idea** - "I want to build [X]"
2. **Initial breakdown** - "Here are the major components..."
3. **Detailed breakdown** - "Component A needs tasks 1, 2, 3..."
4. **Poke holes** - "What am I missing? What will break?"
5. **Refine** - Iterate until plan feels solid
6. **Document** - Create comprehensive project doc (ROADMAP.md, ARCHITECTURE.md, etc.)

**Output:** Clear project documentation with concrete tasks

**Duration:** Few hours of back-and-forth chatting

**Estimated Cost:** $10-30 (worth it - this is architecture work)

> **Note:** Cost estimates are for backtesting against actual usage data, not real-time tracking.

---

## Phase 2: Task Tiering (This Template)

Now that you have a plan, divide the work into tiers.

### Step 1: Extract All Tasks

From your project docs, list every distinct task:

```markdown
## All Tasks (Untiered)

- [ ] Set up Electron app structure
- [ ] Design glassmorphism window
- [ ] Implement Three.js particle sphere
- [ ] Create breathing animation algorithm
- [ ] Build API abstraction layer
- [ ] Write tests for security layer
- [ ] Document installation process
- [ ] Create .gitignore and .env.example
- [ ] Implement Claude API adapter
- [ ] Implement OpenAI API adapter
- [ ] Design skin-swapping architecture
- [ ] Generate boilerplate for adapter pattern
- [ ] Write README with quick start
```

### Step 2: Score Each Task

For EACH task, calculate:

```
Tier Score = (Complexity + Ambiguity + Risk) / 3

Complexity (1-10):
  1-3 = Clear instructions, straightforward
  4-7 = Multiple steps, some unknowns
  8-10 = Complex architecture, many unknowns

Ambiguity (1-10):
  1-3 = Crystal clear what "done" looks like
  4-7 = Some interpretation needed
  8-10 = Unclear requirements

Risk (1-10):
  1-3 = Low risk if wrong, easy to fix
  4-7 = Medium risk, some rework if wrong
  8-10 = High risk (security, money, production)

Result:
  Score 1-3 → Tier 3 (Worker Bee)
  Score 4-7 → Tier 2 (Mid-Weight)
  Score 8-10 → Tier 1 (Big Brain)
```

### Step 3: Organize by Tier (Bottom-Up)

**IMPORTANT:** Start at the BOTTOM (Tier 3), work your way UP.

**Process:**
1. **Pass 1 - Tier 3:** Go through ALL tasks. What can Tier 3 handle with explicit instructions?
2. **Pass 2 - Tier 2:** From remaining tasks, what can Tier 2 implement with clear architecture?
3. **Pass 3 - Tier 1:** What's left? These are your Tier 1 tasks.
4. **Verification:** Go back through Tier 1 list - can these ONLY be done by Tier 1?

**Why bottom-up?** Catches tasks that LOOK complex but are actually Tier 3 with good instructions.

---

**TIER 3 TASKS** (Boilerplate, Docs, Clear Instructions)
```markdown
## Tier 1: Big Brain Work (Claude Sonnet, GPT-4, ~20% of tasks)

- [ ] Design skin-swapping architecture
  - Complexity: 9 (multi-component system)
  - Ambiguity: 8 (unclear how state transitions)
  - Risk: 7 (affects entire app)
  - Score: 8.0 → Tier 1 ✅

- [ ] Build API abstraction layer
  - Complexity: 8 (needs to support multiple providers)
  - Ambiguity: 6 (pattern exists but nuanced)
  - Risk: 8 (breaks if wrong)
  - Score: 7.3 → Tier 1 ✅

- [ ] Create breathing animation algorithm
  - Complexity: 7 (physics/easing math)
  - Ambiguity: 8 (needs to "feel right")
  - Risk: 5 (visual only)
  - Score: 6.7 → Tier 1 ✅
```

---

**TIER 2 TASKS** (Features, Implementation, Medium Complexity)
```markdown
## Tier 2: Mid-Weight Work (GPT-4o, Claude Haiku, ~50% of tasks)

- [ ] Implement Three.js particle sphere
  - Complexity: 6 (Three.js is known, but setup needed)
  - Ambiguity: 5 (examples exist)
  - Risk: 4 (can iterate)
  - Score: 5.0 → Tier 2 ✅

- [ ] Implement Claude API adapter
  - Complexity: 5 (follow established pattern)
  - Ambiguity: 4 (pattern defined in Tier 1)
  - Risk: 6 (must work correctly)
  - Score: 5.0 → Tier 2 ✅

- [ ] Write tests for security layer
  - Complexity: 6 (testing async flows)
  - Ambiguity: 3 (clear test cases)
  - Risk: 7 (security critical)
  - Score: 5.3 → Tier 2 ✅

- [ ] Design glassmorphism window
  - Complexity: 5 (CSS effects)
  - Ambiguity: 6 (aesthetic judgment)
  - Risk: 3 (easy to tweak)
  - Score: 4.7 → Tier 2 ✅
```

**TIER 3 TASKS** (Boilerplate, Docs, Simple Work)
```markdown
## Tier 3: Worker Bee Tasks (GPT-4o-mini, ~30% of tasks)

**CRITICAL:** Instructions must be VERY explicit. Include code examples if possible.

- [ ] Create .gitignore and .env.example
  - Complexity: 1 (standard files)
  - Ambiguity: 1 (known structure)
  - Risk: 2 (won't break anything)
  - Score: 1.3 → Tier 3 ✅
  - **Instructions:** "Create .gitignore for Python project with: venv/, __pycache__/, *.pyc, .env, .DS_Store, logs/"

- [ ] Document installation process
  - Complexity: 2 (straightforward steps)
  - Ambiguity: 2 (clear what to document)
  - Risk: 1 (docs only)
  - Score: 1.7 → Tier 3 ✅
  - **Instructions:** "Document these exact steps: 1. Clone repo, 2. Create venv, 3. Install requirements.txt, 4. Copy .env.example to .env"

- [ ] Generate boilerplate for adapter pattern
  - Complexity: 2 (copy-paste with tweaks)
  - Ambiguity: 1 (pattern is defined)
  - Risk: 2 (easy to fix)
  - Score: 1.7 → Tier 3 ✅
  - **Instructions:** "Using the pattern in api_abstraction.py, create GoogleAdapter class with same methods: chat(), stream(), get_models()"

- [ ] Write README with quick start
  - Complexity: 3 (needs context)
  - Ambiguity: 2 (standard README structure)
  - Risk: 1 (docs only)
  - Score: 2.0 → Tier 3 ✅
  - **Instructions:** "README sections: 1. Project name/description, 2. Installation (link to Documents/), 3. Quick start (3 commands), 4. License"

- [ ] Set up Electron app structure
  - Complexity: 3 (boilerplate with examples)
  - Ambiguity: 2 (documented process)
  - Risk: 3 (foundational but fixable)
  - Score: 2.7 → Tier 3 ✅
  - **Instructions:** "Use electron-forge init. Create src/main/, src/renderer/, src/preload/. Copy package.json scripts from Hologram project."
```

**Note:** See how explicit? If Tier 3 can't execute with these instructions, it's mis-tiered.

### Step 4: Set Execution Order

Within each tier, order by:
1. **Dependencies** (must be done before other tasks)
2. **Risk** (high-risk first, so you know early if approach works)
3. **Value** (user-visible features higher priority)

**Example:**

```markdown
## Sprint 1: Foundation (Week 1)

### Tier 3 (Start here - build foundation fast)
1. Set up Electron app structure ← Dependency for everything
2. Create .gitignore and .env.example ← Quick wins

### Tier 1 (Architecture while Tier 3 is fresh)
3. Build API abstraction layer ← Needed before adapters
4. Design skin-swapping architecture ← High complexity, do early

### Tier 2 (Implementation begins)
5. Implement Claude API adapter ← Uses Tier 1 abstraction
6. Design glassmorphism window ← User-visible

## Sprint 2: Visual Layer (Week 2)

### Tier 1 (Complex visual work)
1. Create breathing animation algorithm ← Complex, do with Tier 1

### Tier 2 (Implement the algorithm)
2. Implement Three.js particle sphere ← Uses Tier 1 algorithm
3. Write tests for security layer ← Medium complexity

### Tier 3 (Documentation)
4. Document installation process ← After implementation
5. Write README with quick start ← Final polish
```

---

## Phase 3: Execution

Now you execute using the appropriate tier for each task.

> **CRITICAL:** Use the escalation-aware prompts below. Don't fight a wrong-tier model for hours.

### For Tier 3 Tasks (Worker Bee)

**Prompt Template:**

```
You are a Worker Bee AI (Tier 3 - GPT-4o-mini). 

Your specialty: Well-defined tasks with clear instructions.

Current task: [Task name]
Context: [Link to project docs or describe]
Requirements: [Specific requirements]

Please:
1. Generate the code/content
2. Follow existing patterns in the codebase
3. Ask clarifying questions if requirements are unclear

⚠️ ESCALATION RULE:
If this task requires:
- Architectural decisions
- Complex problem-solving beyond clear instructions
- Ambiguous requirements you cannot clarify with questions

Then respond IMMEDIATELY with: "🚨 ESCALATE TO TIER 2: [Reason]"

Do NOT attempt more than 2 tries. Escalate immediately if stuck.
```

**Estimated Cost:** ~$0.50-1 per task

> **Note:** Cost estimates for backtesting, not real-time tracking.

---

### For Tier 2 Tasks (Mid-Weight)

**Prompt Template:**

```
You are a Mid-Weight AI (Tier 2 - GPT-4o).

Your specialty: Feature implementation, refactoring, testing.

Current task: [Task name]
Context: [Link to architecture docs]
Constraints: [Performance, security, etc.]

Please:
1. Review the architecture/design
2. Implement following best practices
3. Include error handling
4. Write tests if applicable

⚠️ ESCALATION RULE:
If this task requires:
- Fundamental architectural decisions not defined in docs
- Resolving ambiguous requirements (not just implementation details)
- High-risk design choices affecting multiple systems

Then respond IMMEDIATELY with: "🚨 ESCALATE TO TIER 1: [Reason]"

Do NOT make architectural assumptions. Escalate on first sign of ambiguity.
```

**Estimated Cost:** ~$2-4 per task

> **Note:** Cost estimates for backtesting, not real-time tracking.

---

### For Tier 1 Tasks (Big Brain)

**Prompt Template:**

```
You are a Big Brain AI (Tier 1 - Claude Sonnet/GPT-4).

Your specialty: Architecture, complex problems, ambiguous requirements.

Current task: [Task name]
Context: [Full project context]
Challenge: [What makes this complex]

Please:
1. Analyze the problem space
2. Consider multiple approaches
3. Identify trade-offs
4. Recommend a solution with rationale
5. Anticipate edge cases and failure modes

Note: If this turns out to be straightforward, just implement it. Don't overthink.
```

**Estimated Cost:** ~$5-10 per task

> **Note:** Cost estimates for backtesting, not real-time tracking.

---

## Tier Escalation System

### The Problem: Getting Stuck with Wrong-Tier Model

**Scenario:** You're using GPT-4o-mini (Tier 3) for what looked like simple boilerplate, but it keeps struggling. You spend an hour trying to make it work.

**Solution:** Built-in escalation protocol in your prompts.

---

### Escalation Protocol

**For Tier 3 (Worker Bee) Prompts:**

```
You are a Worker Bee AI (Tier 3 - GPT-4o-mini). 

Your specialty: Well-defined tasks with clear instructions.

Current task: [Task name]
Context: [Link to project docs or describe]
Requirements: [Specific requirements]

Please:
1. Generate the code/content
2. Follow existing patterns in the codebase
3. Ask clarifying questions if requirements are unclear

⚠️ ESCALATION RULE:
If this task requires:
- Architectural decisions
- Complex problem-solving beyond clear instructions
- Ambiguous requirements you cannot clarify with questions

Then respond IMMEDIATELY with: "🚨 ESCALATE TO TIER 2: [Reason]"

Do NOT attempt more than 2 tries. Escalate immediately if stuck.
```

---

**For Tier 2 (Mid-Weight) Prompts:**

```
You are a Mid-Weight AI (Tier 2 - GPT-4o).

Your specialty: Feature implementation, refactoring, testing.

Current task: [Task name]
Context: [Link to architecture docs]
Constraints: [Performance, security, etc.]

Please:
1. Review the architecture/design
2. Implement following best practices
3. Include error handling
4. Write tests if applicable

⚠️ ESCALATION RULE:
If this task requires:
- Fundamental architectural decisions not defined in docs
- Resolving ambiguous requirements (not just implementation details)
- High-risk design choices affecting multiple systems

Then respond IMMEDIATELY with: "🚨 ESCALATE TO TIER 1: [Reason]"

Do NOT make architectural assumptions. Escalate on first sign of ambiguity.
```

---

**For Tier 1 (Big Brain) Prompts:**

```
You are a Big Brain AI (Tier 1 - Claude Sonnet/GPT-4).

Your specialty: Architecture, complex problems, ambiguous requirements.

Current task: [Task name]
Context: [Full project context]
Challenge: [What makes this complex]

Please:
1. Analyze the problem space
2. Consider multiple approaches
3. Identify trade-offs
4. Recommend a solution with rationale
5. Anticipate edge cases and failure modes

Note: If this turns out to be straightforward, just implement it. Don't overthink.
```

---

### Erik's Escalation Checklist

When you catch yourself spending >30 minutes on a task that's not progressing:

**Stop. Ask:**
1. **Is the model struggling?** → Escalate
2. **Are requirements unclear?** → Escalate to Tier 1 for architecture decision
3. **Is this taking way longer than expected?** → Probably mis-tiered
4. **Am I re-explaining the same thing?** → Model doesn't have capability, escalate

**Then:**
1. Document what you tried (so next tier doesn't repeat)
2. Copy the escalation prompt for next tier
3. Include context: "Tier 3 struggled with [X], attempted [Y, Z]"
4. Update your sprint plan: mark task as higher tier

---

### Tier Migration Examples

**Example 1: Tier 3 → Tier 2**

```markdown
TASK: Create .gitignore for Python project
ATTEMPTED WITH: GPT-4o-mini (Tier 3)
ISSUE: Project uses unusual tools (PyTorch, CUDA) - mini doesn't know patterns
ESCALATED TO: GPT-4o (Tier 2)
RESULT: Generated comprehensive .gitignore with ML-specific patterns
LESSON: Specialized domains need Tier 2 minimum
```

---

**Example 2: Tier 2 → Tier 1**

```markdown
TASK: Implement caching layer for API responses
ATTEMPTED WITH: GPT-4o (Tier 2)
ISSUE: Unclear if cache should be in-memory, Redis, or database
         Unclear cache invalidation strategy
         Unclear if this affects other services
ESCALATED TO: Claude Sonnet (Tier 1)
RESULT: Analyzed system architecture, recommended Redis with TTL strategy
        Provided implementation plan for Tier 2 to execute
LESSON: "Implement X" hides architectural decisions - needs Tier 1 first
```

---

### Anti-Pattern: The Sunk Cost Trap

**DON'T DO THIS:**

```
11:00 PM: GPT-4o-mini struggling with task
11:15 PM: "Let me try explaining it differently..."
11:30 PM: "Maybe if I give it an example..."
11:45 PM: "One more attempt with clearer instructions..."
12:15 AM: "Just need to tweak this one part..."
12:45 AM: "Finally got it!" (spent $2 on mini, wasted 1.75 hours)

SHOULD HAVE: Escalated at 11:15 PM, finished by 11:30 PM with Tier 2 ($3)
```

---

### Automation Idea: Multi-Model Document Review

**Pattern from Hologram project:**

The Hologram project used multi-model review for Phase 1 planning documents (see `hologram/Documents/reviews/`):
1. Take initial ROADMAP.md or architecture doc
2. Send to multiple AI models (Claude Opus, GPT-4, Gemini, Grok, etc.)
3. Each model reviews independently
4. Collect feedback: what's missing, what could break, what's over-engineered
5. Revise document based on consensus

**Example from Hologram:**
- 7 different AIs reviewed the roadmap
- Found "unprecedented consensus"
- Caught blind spots before building

**How this applies to Tiered Sprint Planning:**

During Phase 1 (planning), automate the multi-model review:
1. Write initial project doc (ROADMAP.md)
2. Script sends it to multiple models via API
3. Each responds with structured feedback
4. Compare reviews side-by-side
5. Revise based on common themes

**Why this matters:**
- Catches architectural flaws early (cheap to fix)
- Parallel review faster than sequential
- Builds confidence in plan quality
- Multiple perspectives reveal blindspots

**Implementation:**
- Script that calls Claude API, OpenAI API, Google AI API, etc.
- Structured prompt: "Review this doc for: missing pieces, risks, over-engineering"
- Collect all responses in `Documents/reviews/` directory
- Human reads, identifies patterns, revises

**Note:** This is for Phase 1 (planning docs), not for tiering execution tasks.

**Future consideration:** Worth exploring if you find Phase 1 plans often need major revisions after starting implementation.

---

## Red Flags

### 🚩 Task Mis-Tiered

**Symptom:** Tier 3 model says "This is more complex than I can handle" OR you're spending >30 minutes on no progress

**Fix:** 
1. Stop immediately - don't fall into sunk cost trap
2. Use escalation prompt for next tier
3. Document what was tried
4. Update sprint plan to mark task as higher tier

---

### 🚩 Spending Too Much Time (Not Money)

**Symptom:** Task is taking 3x longer than estimated

**Fix:**
1. Is the model capable? (Escalate if not)
2. Are requirements clear? (Go back to Tier 1 for architecture decision)
3. Is scope creep happening? (Break into smaller tasks)
4. Update task estimates based on reality

---

### 🚩 Quality Issues from Lower Tiers

**Symptom:** Tier 3 code is buggy, doesn't match requirements, or needs major rework

**Fix:** 
1. Were requirements clear enough? (Write more detailed spec)
2. Was task actually more complex? (Re-tier to Tier 2)
3. Is this domain too specialized? (Some domains need Tier 2 minimum)
4. Update tiering guidelines based on what you learned

---

### 🚩 Tier 1 Overuse

**Symptom:** Using Claude Sonnet for boilerplate tasks because you like it

**Fix:**
1. Remind yourself: Tier 1 is for architecture and complex problems
2. Force yourself to try Tier 3 first (default down, escalate up)
3. Build discipline: tier by task complexity, not model preference

---

## Examples from Real Projects

### Hologram Project

**Tier 1 work:**
- API abstraction layer architecture
- Security layer design (Red Switch concept)
- Orchestrator architecture
- Skin-swapping state management

**Tier 2 work:**
- Electron app setup (following examples)
- Three.js integration
- Individual API adapters (Claude, OpenAI)
- Glassmorphism CSS effects

**Tier 3 work:**
- Boilerplate for adapter pattern
- README documentation
- .gitignore setup
- TypeScript config files

---

### Trading Projects

**Tier 1 work:**
- Fuzzy grading system design
- Model arena architecture
- Cron dispatcher pattern

**Tier 2 work:**
- Individual model API integrations
- Discord webhook implementation
- Database schema implementation
- Railway deployment setup

**Tier 3 work:**
- CSV data parsing
- Logging setup
- README and documentation
- Environment variable configuration

---

## Success Metrics

**After 1 sprint (2 weeks):**
- [ ] Were tasks correctly tiered? (or did you have to escalate?)
- [ ] Did Tier 3 handle simple tasks well?
- [ ] Did you avoid using Tier 1 for boilerplate?
- [ ] Did escalation protocol work when needed?
- [ ] Are you getting better at scoring task complexity?

**After 1 month:**
- [ ] Task tiering becoming intuitive?
- [ ] Quality maintained across all tiers?
- [ ] Escalations happening smoothly (not fighting wrong-tier models)?
- [ ] Building patterns: "These tasks always need Tier 2"?

---

## Tips

**Tip 1: Default to Tier 3**
When in doubt, start with Tier 3. If it struggles, escalate to Tier 2. Only use Tier 1 when Tier 2 is stuck.

**Tip 2: Batch Similar Tasks**
Do all Tier 3 tasks in one session. Then Tier 2. Then Tier 1. Context switching is expensive.

**Tip 3: Front-Load Tier 1**
Do architecture work (Tier 1) early in sprint. Then Tier 2/3 can execute without ambiguity.

**Tip 4: Document As You Go**
When Tier 1 makes architectural decisions, document immediately. Tier 2/3 needs clear guidance.

**Tip 5: Review & Adjust**
Every sprint, review your tier allocations. Adjust %s based on reality (20/50/30 is just a starting point).

---

## Template Checklist

Before starting execution:

- [ ] Phase 1 planning complete (project docs exist)
- [ ] All tasks extracted and listed
- [ ] Each task scored (complexity + ambiguity + risk)
- [ ] Tasks organized into Tier 1, 2, 3
- [ ] Execution order determined (dependencies, risk, value)
- [ ] Tier-specific prompts prepared (including escalation rules)
- [ ] Ready to execute!

---

*This template is part of the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) meta-project.*

**Pattern Reference:** `../patterns/tiered-ai-sprint-planning.md`  
**Last Updated:** December 22, 2025

