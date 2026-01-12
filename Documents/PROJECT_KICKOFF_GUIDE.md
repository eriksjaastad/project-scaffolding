# Project Kickoff Guide

> **Purpose:** How to start a new project using project-scaffolding templates and patterns  
> **Audience:** You (Erik) and AI collaborators starting fresh projects

---

## Quick Start: "I'm Starting a New Project"

### Step 1: Copy the Bones

```bash
# In your new project directory
NEW_PROJECT="PROJECTS_ROOT/my-new-project"
SCAFFOLDING="PROJECTS_ROOT/project-scaffolding"

cd "$NEW_PROJECT"

# 1. Copy structure
cp -r "$SCAFFOLDING/templates/Documents" ./Documents
cp "$SCAFFOLDING/templates/CLAUDE.md.template" ./CLAUDE.md
cp "$SCAFFOLDING/templates/AGENTS.md.template" ./AGENTS.md
cp "$SCAFFOLDING/templates/.cursorrules.template" ./.cursorrules
cp "$SCAFFOLDING/templates/.cursorignore.template" ./.cursorignore
cp "$SCAFFOLDING/templates/TODO.md.template" ./TODO.md
cp "$SCAFFOLDING/templates/README.md.template" ./README.md
cp "$SCAFFOLDING/templates/.gitignore" ./.gitignore

# 2. Copy .env.example if it exists
[[ -f "$SCAFFOLDING/templates/.env.example" ]] && cp "$SCAFFOLDING/templates/.env.example" ./.env.example
```

### Step 2: Customize Templates (Critical)

**Edit `AGENTS.md`:**
- Replace `{project_description}` with a clear summary.
- Update `{language}`, `{frameworks}`, and `{ai_strategy}`.
- Update `{run_command}` and `{test_command}`.
- This is the **Source of Truth** for AI assistants.

**Edit `CLAUDE.md`:**
- Update project summary and tech stack.
- List specific validation commands for the AI to run.
- This tells the AI **how to work** on this specific project.

**Edit `.cursorrules`:**
- Replace `[PROJECT_NAME]` and update the overview.
- Add project-specific safety rules.

**Edit `Documents/README.md`:**
- Update links and descriptions to match your new structure.

### Step 3: Create Project Index (MANDATORY)

**This is required. No project goes forward without this.**

```bash
# Copy template
cp "$SCAFFOLDING/templates/00_Index_Template.md" \
   "./00_Index_$(basename "$NEW_PROJECT").md"

# Edit the file:
# 1. Replace all [PLACEHOLDER] text
# 2. Write 3-sentence summary
# 3. List key components
# 4. Update tags in frontmatter
# 5. Set correct status
```

**What to write:**
- **Sentence 1:** What problem does this solve?
- **Sentence 2:** Key technologies/approach
- **Sentence 3:** Current status/next steps

**Example:**
```markdown
# trading-copilot

Multi-AI trading intelligence platform that compares GPT, Claude, and Gemini 
for market analysis. Built with Python, PostgreSQL on Railway with cron 
dispatcher for automated analysis. Layer 1-3 complete with full deployment 
pipeline ready for production.
```

**Tags to include:**
- `map/project` (always)
- `p/[project-name]` (your folder name)
- `type/[type]` (ai-agent, pipeline, webapp, etc.)
- `domain/[domain]` (finance, image-processing, etc.)
- `status/active` (always start as active)
- `tech/[tech]` (python, typescript, etc.)

**See:** `project-scaffolding/Documents/PROJECT_INDEXING_SYSTEM.md` for complete guide

### Step 4: Initialize Git

```bash
git init
git add -A
git commit -m "Initial commit: Project structure from scaffolding

- Added project index (mandatory)
- Copied scaffolding templates
- Ready for development"
```

**Verify index exists:**
```bash
ls -la 00_Index_*.md
# Should show: 00_Index_[YourProject].md
```

---

### Step 5: Validate Your Setup

Run validation to ensure your project structure is correct:

```bash
# Validate project (from any directory)
python "$SCAFFOLDING/scripts/validate_project.py" "$(basename $(pwd))"
```

**What validation checks:**
- ✅ Required files present (00_Index_*.md, AGENTS.md, CLAUDE.md, .cursorrules, etc.)
- ✅ Project index has valid YAML frontmatter and required sections
- ✅ **DNA Integrity:** No hardcoded absolute paths (`/Users/...`, `/home/...`)
- ✅ **Security:** No exposed secrets (API keys like `sk-...`, `AIza...`)
- ✅ Mandatory directories exist (Documents/, etc.)

**Example output (clean project):**
```
✅ my-new-project (Fully Compliant)
```

**Example output (issues found):**
```
⚠️ my-new-project
   - Missing mandatory file: .cursorrules
   - Index file: Missing required section: ## Status
```

**Fix any issues and re-run validation until clean.**

**Ongoing validation:** Run validation periodically during development, especially before major commits or code reviews.

**Learn more:**
- **Full validation script:** `$SCAFFOLDING/scripts/validate_project.py`
- **Quick safety check:** `$SCAFFOLDING/scripts/warden_audit.py --root . --fast`
- **Review system:** See QUICKSTART.md Phase 6 for code review workflow

---

## Starting a Chat Session with AI

### Opening Prompt Template

```
Hi! I'm starting a new project and want to use the structure from project-scaffolding.

Project: [Name]
Idea: [Brief description]

I've already copied the templates:
- .cursorrules
- CLAUDE.md
- Documents/ structure

Context:
- Project scaffolding: PROJECTS_ROOT/project-scaffolding
- Tiered sprint planning: PROJECTS_ROOT/project-scaffolding/patterns/tiered-ai-sprint-planning.md
- My philosophy: PROJECTS_ROOT/project-scaffolding/PROJECT_PHILOSOPHY.md

Please:
1. Read CLAUDE.md to understand this project
2. Read my philosophy to understand my approach
3. Let's start Phase 1 planning (big idea → breakdown)

Ready to explore this idea?
```

---

## Phase 1: Planning (Tier 1 - Big Idea → Concrete Plan)

### What Happens Here

**This is hours of chatting with Tier 1 models** (Claude Sonnet, GPT-4). That's correct and necessary.

**Flow:**
1. **Hand-wavy big idea** - "I want to build X"
2. **Circular discussion** - Going around exploring angles
3. **AI encouragement** - "Yeah, that sounds great!"
4. **Get more specific** - Break down components
5. **Pass around for feedback** - Get AI reviews (like Hologram's 7-AI review)
6. **Refine, refine, refine**
7. **Eventually coalesces into task list**

**Outputs:**
- `ROADMAP.md` - Long-term vision
- `ARCHITECTURE.md` or `Documents/architecture/` - System design
- `Documents/*.md` - Core documentation (in root)
- Maybe `Documents/vision/` - Design vision
- Maybe `Documents/reviews/` - AI feedback sessions

**Duration:** Few hours of back-and-forth

**Cost:** $10-30 (worth it - this is architecture)

---

## Phase 2: Task Tiering (Still Tier 1)

Once you have a solid plan, use the **Tiered Sprint Planner**.

### Prompt for This Phase

```
We've finished Phase 1 planning. Now I want to tier the execution work.

Please read:
- Tiered Sprint Planner: PROJECTS_ROOT/project-scaffolding/templates/TIERED_SPRINT_PLANNER.md
- Our project docs: [ROADMAP.md, ARCHITECTURE.md, etc.]

Task:
1. Extract ALL tasks from our planning docs
2. Score each task (complexity + ambiguity + risk)
3. Organize into Tier 1, 2, 3
4. Suggest execution order

Create a tiered sprint document in: Documents/SPRINT_PLAN.md
```

**Output:** `Documents/SPRINT_PLAN.md` with tiered task list

**Duration:** 30-60 minutes

**Cost:** $3-5

---

## Phase 3: Execution (Mixed Tiers)

Now you execute using appropriate tiers.

### Tier 3 Tasks (GPT-4o-mini)

**Start here!** Knock out the boilerplate fast.

**Example prompt:**
```
You are a Tier 3 Worker Bee (GPT-4o-mini).

Task: Create .gitignore for [Node/Python/etc] project

Requirements:
- Ignore node_modules, __pycache__, .env files
- Ignore IDE files (.vscode, .idea)
- Ignore OS files (.DS_Store)
- Ignore logs

Please generate the .gitignore file.
```

### Tier 2 Tasks (GPT-4o)

**Implementation work.** Most of your time here.

**Example prompt:**
```
You are a Tier 2 Mid-Weight AI (GPT-4o).

Task: Implement [Feature X] following architecture defined in Documents/architecture/

Context: [Link to relevant docs]

Please:
1. Implement the feature
2. Include error handling
3. Follow existing code patterns
4. Write basic tests
```

### Tier 1 Tasks (Claude Sonnet/GPT-4)

**Complex/ambiguous work.** Use sparingly.

**Example prompt:**
```
You are a Tier 1 Big Brain AI (Claude Sonnet).

Task: Design the [Complex System X] architecture

Challenge: [What makes this hard]

Context: [Full project context]

Please:
1. Analyze the problem space
2. Propose 2-3 approaches
3. Recommend one with rationale
4. Identify risks and edge cases
```

---

## Phase 4: Code Reviews (Quality Control)

**Goal:** Ensure every significant change is reviewed by multiple AI models.

### Standardization Rules

1. **Request Requirements:**
   - Every review request MUST include a **Definition of Done (DoD)**.
   - Use `templates/CODE_REVIEW.md.template` for the request.
   - See `patterns/code-review-standard.md` for details.

2. **Standard Result Format:**
   - Results are saved with the prefix `CODE_REVIEW_` in all caps.
   - This enables dashboard tracking (e.g., `CODE_REVIEW_SECURITY_REVIEWER.md`).

3. **How to Run:**
   ```bash
   scaffold review --type code --input path/to/your/request.md --round 1
   ```

---

## Adding to Cursor Rules

### Required Sections in `.cursorrules`

**1. Project Overview:**
```markdown
## Project: [Name]

[2-3 sentence description]

**Current phase:** [Planning / Implementation / etc]
**Key constraints:** [Budget, performance, privacy, etc]
```

**2. Tiered AI Reference:**
```markdown
## Tiered AI Approach

This project uses tiered AI planning to manage costs.

**Pattern:** PROJECTS_ROOT/project-scaffolding/patterns/tiered-ai-sprint-planning.md
**Sprint Planner:** PROJECTS_ROOT/project-scaffolding/templates/TIERED_SPRINT_PLANNER.md

Before starting work:
1. Check Documents/SPRINT_PLAN.md for task tier
2. Use appropriate model for the tier
3. Default to Tier 3, escalate only when stuck
```

**3. External Resources:**
```markdown
## External Resources

When adding ANY external service (API, cloud platform, database, etc):

**MUST update:** PROJECTS_ROOT/project-scaffolding/EXTERNAL_RESOURCES.md

Document:
- Service name
- Which project uses it
- Cost
- Purpose
- API key location
```

**4. Project-Specific Safety Rules:**
```markdown
## Safety Rules

🔴 NEVER modify:
- [List your read-only files/dirs]

🟡 Careful with:
- [List files needing care]

✅ Safe to modify:
- [List freely editable code]
```

---

## Project Structure Template

```
my-new-project/
├── README.md                  # Project overview
├── ROADMAP.md                 # Long-term vision (from Phase 1)
├── CLAUDE.md                  # AI collaboration guide
├── .cursorrules               # Cursor-specific rules
├── .gitignore                 # Standard ignores
├── .env.example               # Environment template
├── TODO.md                    # Current work (optional)
│
├── Documents/                 # From scaffolding template
│   ├── README.md              # Documentation index (Grand Central Station)
│   ├── ARCHITECTURE.md        # Core Architecture
│   ├── OPERATIONS.md          # Core Operations
│   ├── guides/                # How-to documents
│   ├── reference/             # Standards, knowledge
│   ├── safety/                # Safety systems
│   └── archives/              # Historical docs
│
├── Documents/                      # Additional docs (optional)
│   ├── SPRINT_PLAN.md         # Tiered task list
│   ├── architecture/          # Detailed architecture
│   ├── reviews/               # AI feedback sessions
│   └── vision/                # Design vision
│
├── src/                       # Your source code
├── tests/                     # Tests (if applicable)
├── data/                      # Data files (if applicable)
└── config/                    # Configuration (if applicable)
```

---

## Checklist: New Project Setup

### Initial Setup (10 minutes)
- [ ] Create project directory
- [ ] Copy templates from scaffolding
- [ ] Customize `.cursorrules` (project name, overview)
- [ ] Customize `CLAUDE.md` (tech stack, patterns)
- [ ] Initialize git
- [ ] Create `.env.example` if needed

### Phase 1 Planning (Few hours - Tier 1)
- [ ] Chat with Claude Sonnet/GPT-4 about big idea
- [ ] Break down into components
- [ ] Refine and iterate
- [ ] Get AI feedback (optional: multi-model review)
- [ ] Document in ROADMAP.md, ARCHITECTURE.md
- [ ] Create initial Core Standards in Documents/ root (Architecture, Operations, etc.)

### Phase 2 Tiering (30-60 min - Tier 1)
- [ ] Extract all tasks from planning docs
- [ ] Score each task (complexity + ambiguity + risk)
- [ ] Organize into Tier 1, 2, 3
- [ ] Set execution order
- [ ] Document in `Documents/SPRINT_PLAN.md`
- [ ] Set tier budgets (20% / 50% / 30%)

### Phase 3 Execution (Ongoing - Mixed tiers)
- [ ] Start with Tier 3 tasks (foundation)
- [ ] Move to Tier 1 tasks (architecture)
- [ ] Execute Tier 2 tasks (implementation)
- [ ] Track spending by tier
- [ ] Update sprint plan as needed
- [ ] Mark tasks complete

### External Resources (Throughout)
- [ ] When adding any service, update EXTERNAL_RESOURCES.md
- [ ] Create separate API keys per project
- [ ] Document credential locations
- [ ] Update cost tracking

---

## Common Patterns

### Pattern 1: Multi-Model Review

After Phase 1 planning, get feedback from multiple models:

```
I've completed Phase 1 planning for [Project].

Please review this ROADMAP.md and provide:
1. What's missing?
2. What could break?
3. What's over-engineered?
4. What's under-specified?

Be critical. I need reality checks, not cheerleading.
```

**Run with:** Claude Opus 4, GPT-4, Gemini, Grok (like Hologram did)

**Cost:** $5-10 total

**Value:** Catches blind spots before you build

---

### Pattern 2: Spike Testing

For risky/unknown technical approaches, do spikes:

```
Spike 1: Performance Testing
- Build minimal prototype
- Measure FPS, CPU, memory
- Pass/fail against targets
- Document in Documents/spikes/
```

**Use Tier 2** for spikes (implementation with measurement)

---

### Pattern 3: Milestone Screenshots

Capture visual progress (especially for UI projects):

```
Documents/milestones/
├── 2025-12-19_phase-0-complete.png
├── 2025-12-20_first-animation.png
└── MILESTONES.md (describe each)
```

**Why:** Motivating, shareable, documents progress

---

## Anti-Patterns to Avoid

### ❌ Starting Without Planning

Don't jump straight to code. Do Phase 1 planning first (hours of chatting).

**Why:** Waste time building wrong thing, expensive to pivot later.

---

### ❌ Using Tier 1 for Everything

Don't use Claude Sonnet for boilerplate just because you like it.

**Why:** Burn budget 50x faster for same output.

---

### ❌ Skipping External Resources Doc

Don't add services without updating EXTERNAL_RESOURCES.md.

**Why:** Future-you (in 4 months) will get a bill and not know which project.

---

### ❌ Shared API Keys

Don't reuse API keys across projects (even from agent_os).

**Why:** Can't attribute costs, can't isolate failures, can't control blast radius.

---

### ❌ No Git From Start

Don't wait to initialize git "until the project is real."

**Why:** Lose history, can't experiment safely, no backup.

---

## Success Metrics

**After 1 week:**
- [ ] Project structure in place
- [ ] Phase 1 planning complete
- [ ] Tasks tiered and organized
- [ ] Started execution

**After 1 month:**
- [ ] Staying within tier budgets
- [ ] Making progress on sprint tasks
- [ ] Documentation up to date
- [ ] No surprise bills (resources tracked)

**After 3 months:**
- [ ] Project delivering value (even if incomplete)
- [ ] Tiering is automatic
- [ ] Documentation makes onboarding easy
- [ ] Extracting patterns for scaffolding

---

## Questions & Troubleshooting

### Q: Should every project use this structure?

**A:** Use for projects expected to last >1 week. Skip for one-off scripts or experiments.

---

### Q: What if I don't know which tier a task is?

**A:** Default to Tier 3. If it struggles, escalate to Tier 2. Only use Tier 1 when Tier 2 is stuck.

---

### Q: Can I change the tier % allocations?

**A:** Yes! 20/50/30 is a starting point. Adjust based on your project's needs (heavy architecture? More Tier 1).

---

### Q: Do I need all the Documents/ subdirectories?

**A:** No. Start with what you need (probably just Core Standards in root and `guides/`). Add others as needed.

---

### Q: What if Cursor settings don't reference scaffolding?

**A:** Add to `.cursorrules`:
```markdown
## Scaffolding Reference

This project uses patterns from:
PROJECTS_ROOT/project-scaffolding/

Key references:
- Patterns: patterns/
- Templates: templates/
- Philosophy: PROJECT_PHILOSOPHY.md
- External resources: EXTERNAL_RESOURCES.md
```

---

## Self-Learning Projects (Skills Management)

This scaffolding promotes projects that improve over time by capturing what works.

### The Core Idea

As you work with AI agents, you'll develop reusable instructions (skills). These learnings should be captured somewhere - the question is where.

### Three Approaches

| Approach | Best For | Trade-offs |
|----------|----------|------------|
| **Per-project skills** | Project-specific patterns | Simple, self-contained; may duplicate across projects |
| **Shared skills library** | Cross-project patterns | All projects benefit; requires ecosystem-level thinking |
| **Both** | Mature ecosystems | Best of both; skills can migrate as they mature |

### Recommendation

**Start with per-project skills.** Keep reusable instructions in your `.cursorrules` or `CLAUDE.md`.

**Extract to a shared library** when you find yourself copying the same instructions across 3+ projects. This follows our "consolidate on 3rd duplicate" philosophy.

### Per-Project Skills

Keep skills in:
- `.cursorrules` - Cursor-specific instructions
- `CLAUDE.md` - Claude-specific instructions
- `Documents/` - Longer-form playbooks

**Good for:**
- "Never modify production database" (project-specific)
- "This project uses Next.js 14" (tech stack)
- Custom debugging workflows for this codebase

### Shared Skills Library

If you want a centralized library:

```bash
mkdir -p "$PROJECTS_ROOT/agent-skills-library"
```

**Structure:**
- `playbooks/` - Tool-agnostic instructions
- `cursor-rules/` - Cursor adapters
- `claude-skills/` - Claude adapters

**Good for:**
- PR review checklists
- Debugging routines
- Code quality standards
- Testing strategies

**Reference:** See `agent-skills-library/INTEGRATION_GUIDE.md` if you have one.

### Skills Can Move

Skills often start project-specific and graduate to shared:

1. You create a debugging workflow in Project A
2. You copy it to Project B (that's fine)
3. You need it in Project C → **extract to shared library**
4. All projects now reference the shared version

### Integration Checklist

When scaffolding a project, ask:

- [ ] Does this project have reusable AI instructions?
- [ ] Are skills managed per-project, shared, or both?
- [ ] Is there a learning loop for capturing what works?

See `patterns/learning-loop-pattern.md` for establishing feedback cycles.

---

## Related Files

- **Tiered Sprint Planner:** `templates/TIERED_SPRINT_PLANNER.md`
- **Tiered AI Pattern:** `patterns/tiered-ai-sprint-planning.md`
- **Development Philosophy:** `patterns/development-philosophy.md`
- **Safety Systems:** `patterns/safety-systems.md`
- **Learning Loop Pattern:** `patterns/learning-loop-pattern.md` - How to create reinforcement learning cycles
- **External Resources:** `EXTERNAL_RESOURCES.md`
- **Project Philosophy:** `PROJECT_PHILOSOPHY.md`

---

*Part of the [project-scaffolding](https://github.com/eriksjaastad/project-scaffolding) meta-project.*

**Last Updated:** December 22, 2025

