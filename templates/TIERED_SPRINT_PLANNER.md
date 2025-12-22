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

**Cost:** $10-30 (worth it - this is architecture work)

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

### Step 3: Organize by Tier

**TIER 1 TASKS** (Architecture, Complex, High-Risk)
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

- [ ] Generate boilerplate for adapter pattern
  - Complexity: 2 (copy-paste with tweaks)
  - Ambiguity: 1 (pattern is defined)
  - Risk: 2 (easy to fix)
  - Score: 1.7 → Tier 3 ✅

- [ ] Create .gitignore and .env.example
  - Complexity: 1 (standard files)
  - Ambiguity: 1 (known structure)
  - Risk: 2 (won't break anything)
  - Score: 1.3 → Tier 3 ✅

- [ ] Document installation process
  - Complexity: 2 (straightforward steps)
  - Ambiguity: 2 (clear what to document)
  - Risk: 1 (docs only)
  - Score: 1.7 → Tier 3 ✅

- [ ] Write README with quick start
  - Complexity: 3 (needs context)
  - Ambiguity: 2 (standard README structure)
  - Risk: 1 (docs only)
  - Score: 2.0 → Tier 3 ✅

- [ ] Set up Electron app structure
  - Complexity: 3 (boilerplate with examples)
  - Ambiguity: 2 (documented process)
  - Risk: 3 (foundational but fixable)
  - Score: 2.7 → Tier 3 ✅
```

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
4. Flag if this task is more complex than expected (might need Tier 2)
```

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
5. Flag if you encounter architectural ambiguity (might need Tier 1)
```

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
```

---

## Budget Tracking (Optional)

Track your spend by tier:

```markdown
## Week 1 Budget Log

### Tier 1 Sessions
- [ ] API abstraction layer design: ~$5
- [ ] Skin-swapping architecture: ~$8
- [ ] **Tier 1 Total: $13 / $20 weekly budget** ✅

### Tier 2 Sessions
- [ ] Claude adapter implementation: ~$3
- [ ] Glassmorphism window: ~$2
- [ ] Three.js particle sphere: ~$4
- [ ] **Tier 2 Total: $9 / $25 weekly budget** ✅

### Tier 3 Sessions
- [ ] Electron boilerplate: ~$0.50
- [ ] .gitignore/.env.example: ~$0.25
- [ ] README: ~$0.75
- [ ] **Tier 3 Total: $1.50 / $5 weekly budget** ✅

**Week 1 Total: $23.50 / $50 weekly budget** ✅
```

---

## Red Flags

### 🚩 Task Mis-Tiered

**Symptom:** Tier 3 model says "This is more complex than I can handle"

**Fix:** Escalate to Tier 2. Update your tier scoring - you underestimated complexity.

---

### 🚩 Spending Too Much on Tier 1

**Symptom:** Burning through Tier 1 budget in first 2 weeks

**Fix:**
1. Are you using Tier 1 for implementation? (Should be Tier 2)
2. Are you using Tier 1 for docs? (Should be Tier 3)
3. Re-tier your task list with stricter scoring

---

### 🚩 Quality Issues from Tier 3

**Symptom:** Tier 3 code is buggy or doesn't match requirements

**Fix:** 
1. Were requirements clear enough? (Write more detailed spec)
2. Was task actually more complex? (Re-tier to Tier 2)
3. Is Tier 3 model appropriate for your domain? (Some domains need Tier 2 minimum)

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
- [ ] Did you stay within tier budgets?
- [ ] Were tasks correctly tiered? (or did you have to escalate?)
- [ ] Did Tier 3 handle simple tasks well?
- [ ] Did you avoid using Tier 1 for boilerplate?

**After 1 month:**
- [ ] Total spend under monthly budget?
- [ ] Task tiering becoming intuitive?
- [ ] Quality maintained across all tiers?

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
- [ ] Budget allocated per tier (20% / 50% / 30%)
- [ ] Tier-specific prompts prepared
- [ ] Ready to execute!

---

*This template is part of the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) meta-project.*

**Pattern Reference:** `../patterns/tiered-ai-sprint-planning.md`  
**Last Updated:** December 22, 2025

