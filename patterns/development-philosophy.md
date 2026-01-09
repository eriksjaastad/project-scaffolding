# Development Philosophy Patterns

> **Purpose:** Proven principles for building maintainable experimental projects  
> **Source:** Extracted from PROJECT_PHILOSOPHY.md + project experience  
> **Last Updated:** December 21, 2025

---

## Overview

These are principles that have proven themselves across multiple projects. They're not rules - they're patterns we wish we'd had earlier.

**Context:** We build experiments to explore and learn, not products to monetize. This changes how we think about development, testing, and success.

---

## Pattern 1: Layer-by-Layer Development

### What

Build incrementally useful layers, not "all or nothing" systems.

Each layer should:
- Be independently valuable
- Work without future layers
- Provide immediate utility
- Teach you what to build next

### Why It Works

**Traditional approach:**
```
Month 1-3: Build everything
Month 4: Ship complete system
Result: All or nothing, no learning until end
```

**Layer-by-layer approach:**
```
Week 1: Layer 1 (foundation) → Ship it, use it, learn
Week 2: Layer 2 (queries) → Ship it, use it, learn
Week 3: Layer 3 (automation) → Ship it, use it, learn
Result: Value at each step, can stop anywhere
```

### Implementation

**Structure your roadmap:**

```markdown
### Layer 1: Foundation ✅
**Goal:** Collect and store data
**Value:** Can manually query data, build reports
**Exit criteria:** 30 days of clean data
**Time:** 1-2 weeks

### Layer 2: Query Interface
**Goal:** Easy data access
**Value:** Find patterns without SQL
**Exit criteria:** Can answer common questions in <1 min
**Time:** 1-2 weeks

### Layer 3: Automation
**Goal:** Proactive insights
**Value:** Don't have to remember to check
**Exit criteria:** Daily summaries without manual work
**Time:** 1 week
```

**Key principle:** Each layer is shippable and valuable alone.

### Code Structure

Organize code by layers, not features:

```
project/
├── layer_1_foundation/
│   ├── data_collection.py
│   └── storage.py
├── layer_2_query/
│   ├── search.py
│   └── patterns.py
└── layer_3_automation/
    ├── scheduler.py
    └── insights.py
```

**Why:** Clear what works, what's next, what can be skipped.

### Evidence from Projects

**Cortana Personal AI:**
- Layer 1: Data collection (✅ complete, useful alone)
- Layer 2: Query interface (next, but Layer 1 already valuable)
- Layers 3-7: Planned, but not blocking value

**Trading Projects:**
- Layer 1: Data pipeline (✅ complete)
- Layer 2: Model arena (✅ complete)
- Layer 3: Automated grading (✅ complete)
- Each layer worked independently

**image-workflow:**
- Not explicitly layered, but evolved incrementally
- Each tool added value independently
- Could use any subset of tools

### When NOT to Use

- Simple projects (<1 week of work)
- Proof of concepts (throwaway code)
- One-time scripts

### Anti-Patterns

❌ **Layer dependency hell:**
```
Layer 3 requires Layer 2
Layer 2 requires Layer 1
Layer 1 requires full database
→ Can't start until everything is built
```

✅ **Independent layers:**
```
Layer 1: Works with just flat files
Layer 2: Adds DB, but Layer 1 still works
Layer 3: Adds automation, but can still use Layer 2 manually
```

---

## Pattern 2: Data Before Decisions

### What

Collect data for **30-60 days** before evaluating success or making major changes.

### Why It Works

**Gut feelings are wrong:**
- First week: "This is amazing!"
- Second week: "This is terrible!"
- Reality: Need longer timeline to see patterns

**Data reveals truth:**
- Week 1-2: Novelty effects (everything seems great or terrible)
- Week 3-4: Reality sets in (actual patterns emerge)
- Month 2: True patterns visible (can make informed decisions)

### Implementation

**Set explicit evaluation dates:**

```markdown
## Trading Model Arena

**Started:** December 1, 2025
**Evaluation date:** January 15, 2025 (45 days)

**What we're measuring:**
- Model prediction accuracy
- Correlation with market movements
- Computational cost vs. value

**Decision criteria:**
- If <60% accuracy: Kill the project
- If 60-75%: Continue collecting data
- If >75%: Invest in productionizing

**Until then:** Just collect data, don't judge.
```

**Resist the urge to optimize early:**

```python
# ❌ Week 1: "This is slow, let me optimize"
# Result: Optimized the wrong thing

# ✅ Week 1: "This is slow, but let's collect data"
# Week 4: "Now I see the real bottleneck"
# Week 5: Optimize the right thing
```

### Evidence from Projects

**Trading Projects:**
- Explicit 30-day data collection period
- Not judging models until sufficient data
- Philosophy documented in PROJECT_PHILOSOPHY.md

**image-workflow:**
- 2.5 months of real usage before major refactoring
- Patterns became obvious over time
- Early "obvious optimizations" would've been wrong

**Cortana Personal AI:**
- 3 months of data backfilled before building features
- Can now make informed decisions about Layer 2
- Would've built wrong features in week 1

### When NOT to Use

- Obviously broken features (fix immediately)
- Security issues (fix immediately)
- Data corruption (fix immediately)
- Learning exercises (iterate quickly)

### Anti-Patterns

❌ **Premature optimization:**
```
Week 1: "This query is slow!"
Week 2: Added caching, indexes, optimization
Week 3: Realized we never run that query
```

❌ **Premature judgment:**
```
Week 1: "Users love this feature!"
Week 2: Shipped 5 variants
Month 2: Nobody actually uses any of them
```

✅ **Patient observation:**
```
Month 1: Collect usage data
Month 2: See real patterns
Month 3: Optimize/cut based on data
```

---

## Pattern 3: Consolidate on 3rd Duplicate

### What

**First instance:** Write custom code, learn the problem  
**Second instance:** Notice the similarity, resist abstracting  
**Third instance:** Now you know the pattern, extract it

### Why It Works

**Abstracting too early:**
- Don't fully understand the problem
- Make wrong abstractions
- End up fighting the abstraction later

**Abstracting too late:**
- Copy-paste bugs
- Maintenance burden
- Inconsistent implementations

**Third time is the charm:**
- You've seen the variations
- You know what's actually common
- You know what should be flexible
- You can name things properly

### Implementation

**Keep a "duplicate tracker":**

```markdown
## Potential Patterns

### Date-based file storage
- **Instance 1:** Cortana memories (data/memories/daily/YYYY-MM-DD.json)
- **Instance 2:** Trading journal (04_journal/daily/YYYY-MM-DD.md)
- **Instance 3:** ??? (waiting for 3rd instance)
- **Status:** Emerging pattern, watch for 3rd

### API with cost tracking
- **Instance 1:** Cortana (OpenAI tracking)
- **Instance 2:** ??? (waiting for 2nd)
- **Status:** Candidate pattern, too early to extract
```

**When you hit the 3rd instance:**

```python
# Now extract to utility

def save_daily_file(
    base_dir: Path,
    data: str,
    date: datetime,
    extension: str = ".json"
) -> Path:
    """
    Save data in date-based file structure.
    
    Pattern extracted after 3rd usage:
    - Cortana memories
    - Trading journal
    - image-workflow daily summaries
    """
    filename = f"{date.strftime('%Y-%m-%d')}{extension}"
    path = base_dir / filename
    path.write_text(data)
    return path
```

### Evidence from Projects

**This meta-project:**
- Explicitly waiting for 3rd instance of patterns
- Documents/ pattern seen in 2 projects (watching for 3rd)
- CLAUDE.md seen in 2 projects (watching for 3rd)

**image-workflow:**
- FileTracker abstracted after 3rd file operation pattern
- Companion file handling after 3rd usage
- Too early abstractions removed later

### When NOT to Use

- Obviously generic utilities (date formatting, etc.)
- Industry-standard patterns (REST APIs, etc.)
- Trivial helpers (< 5 lines of code)

### Anti-Patterns

❌ **Premature abstraction:**
```
Instance 1: "I might need this elsewhere, let me abstract"
Instance 2: "Actually, this is slightly different"
Result: Fighting the abstraction, eventual rewrite
```

❌ **Analysis paralysis:**
```
Instance 5: "Still not sure the pattern is stable"
Result: Copy-paste bugs everywhere
```

✅ **Patient pattern recognition:**
```
Instances 1-2: Learn the problem space
Instance 3: Extract the proven pattern
```

---

## Pattern 4: Tests for Fragile Parts

### What

Write tests for code that breaks easily, skip tests for code that's obviously correct or throwaway.

**Test:**
- Data parsers (formats change)
- Business logic (subtle bugs)
- Edge cases (off-by-one errors)
- Integration points (APIs, databases)

**Don't test:**
- One-off scripts (not reused)
- Simple CRUD (obviously correct)
- Glue code (just calling libraries)
- UI (changes too fast early on)

### Why It Works

**Traditional approach:**
```
Write tests for everything
Result: 
- High test maintenance
- Slows iteration
- Tests break more than code
```

**Focused approach:**
```
Write tests for fragile parts
Result:
- Fast iterations
- Tests catch real bugs
- Low maintenance burden
```

### Implementation

**Ask: "How could this break?"**

```python
# HIGH RISK - Test this
def parse_date(date_str: str) -> date:
    """
    Parse YYYY-MM-DD format.
    
    Why test: Many edge cases
    - Invalid formats
    - Out of range values
    - Timezone confusion
    """
    pass

# LOW RISK - Don't test
def get_config_path() -> Path:
    """
    Return path to config file.
    
    Why not test: Obviously correct
    - Just path concatenation
    - One line
    - Can't really break
    """
    return Path(__file__).parent / "config.json"
```

**Testing progression:**

```markdown
## Layer 1 (Foundation)
- Manual testing
- Establish patterns
- Learn what breaks

## Layer 2 (Query Interface)  
- Add tests for parsers
- Test business logic
- Still manual for UI

## Layer 3 (Automation)
- Test critical paths
- Integration tests
- Keep UI manual
```

### Evidence from Projects

**image-workflow:**
- Tests for utils (data parsers, file operations)
- No tests for workflow scripts (manual tools)
- Tests for fragile parts only

**Cortana Personal AI:**
- Manual testing for Layer 1
- Planning automated tests for Layer 2
- Focus on data integrity tests

**Trading Projects:**
- Tests for grading logic (critical)
- Tests for data parsing (fragile)
- No tests for dashboard (changes too fast)

### When NOT to Use

- **Critical infrastructure** (payments, security) - test everything
- **Public APIs** (breaking changes hurt users) - test thoroughly
- **Regulated systems** (compliance) - test per requirements

### Anti-Patterns

❌ **Test theater:**
```python
def test_add_numbers():
    assert add(2, 3) == 5  # Testing obvious things
```

❌ **Brittle tests:**
```python
def test_ui_layout():
    # Breaks every time UI changes
    # Doesn't catch real bugs
```

✅ **Focused tests:**
```python
def test_date_parser_edge_cases():
    # Invalid format
    with pytest.raises(ValueError):
        parse_date("invalid")
    
    # Boundary condition
    assert parse_date("2024-02-29")  # Leap year
    
    # This catches real bugs
```

---

## Pattern 5: "Every Safety System Was a Scar"

### What

Build safety systems AFTER experiencing the failure, not before.

### Why It Works

See `safety-systems.md` for full details.

**Key insight:** You don't know what will break until it breaks. Guessing leads to:
- Wrong protections (defending against non-risks)
- Over-engineering (complex systems for simple problems)
- Under-engineering (missing the real risks)

**Better:** Wait for the scar, learn the lesson, build focused protection.

### Implementation

See `safety-systems.md` for six proven patterns.

### Evidence from Projects

All three source projects have extensive scar stories documented.

---

## Pattern 6: Let Projects Be Experiments

### What

Projects exist to explore and learn, not to ship and monetize.

**This changes everything:**
- Success = learning, not revenue
- Can kill projects without guilt
- Can explore "impractical" ideas
- Quality bar is "does it teach me something?"

### Why It Works

**Product mindset:**
```
Must ship features
Must serve customers
Must generate revenue
→ Can't explore dead ends
→ Can't kill projects
→ Pressure to "succeed"
```

**Experiment mindset:**
```
Collect interesting data
Find cool patterns
Learn new techniques
→ Dead ends are valuable
→ Killing projects is success
→ Learning is winning
```

### Implementation

**Document the exploration goal:**

```markdown
## Project: [Name]

**Exploration question:** What can we learn about [domain]?

**Success criteria:**
- ✅ Collect meaningful data
- ✅ Learn something new
- ✅ Document patterns
- ❌ Revenue
- ❌ Users
- ❌ "Shipping"

**Kill criteria:**
- Not teaching us anything new
- Not interesting anymore
- Better exploration elsewhere

**Time box:** [X] months before deciding
```

**Two-level game:**

Every project has two outputs:
1. **Domain insights** - What did we learn about [trading/images/etc]?
2. **Meta insights** - What did we learn about building projects?

The meta insights are the real product (this scaffolding project!).

### Evidence from Projects

**PROJECT_PHILOSOPHY.md:**
- Explicitly states "we're explorers, not founders"
- Documents the two-level game
- Permission to kill projects

**All projects:**
- No monetization pressure
- Free to explore dead ends
- Meta-project extracts the learnings

### When NOT to Use

- **Paid consulting** - clients expect results
- **Team projects** - others may have different goals
- **Infrastructure** - systems that must work

### Anti-Patterns

❌ **Premature productization:**
```
Week 1: "Let's add user accounts!"
Week 2: "Need a pricing page!"
Week 3: "Marketing strategy?"
Result: Lost sight of exploration
```

❌ **Guilt about killing projects:**
```
Month 3: "This isn't working"
Month 6: "Still forcing it"
Month 12: "Wasted a year"
Result: Sunk cost fallacy
```

✅ **Experimental mindset:**
```
Month 1-2: Collect data, explore
Month 3: Learned X, Y, Z
Month 4: This direction isn't interesting
Decision: Kill it, extract learnings, move on
```

---

## Pattern 7: Show the Full Picture

### What

AI collaborators (and humans) connect better with full context.

**Give them:**
- Project philosophy (why this exists)
- Current status (where we are)
- Constraints (what limits us)
- History (what we've tried)
- Goals (where we're going)

### Why It Works

**Minimal context:**
```
Human: "Add a cache to this function"
AI: [Adds generic cache]
Result: Doesn't fit the project patterns
```

**Full context:**
```
Human: "Add a cache - we're optimizing for low cost, not speed.
        Layer 1 is complete, Layer 2 is next.
        See ROADMAP.md for architecture."
AI: [Adds cost-conscious cache that fits Layer 2 plans]
Result: Better solutions, fewer iterations
```

### Implementation

**Start sessions with context:**

```markdown
## Session Start

Quick context for this session:
- **Project:** Cortana Personal AI
- **Phase:** Layer 1 complete, planning Layer 2
- **Today's goal:** Add semantic search
- **Constraints:** Cost <$1/day, privacy-first
- **Key files:** ROADMAP.md, CLAUDE.md
```

**Maintain context files:**
- `README.md` - What is this?
- `ROADMAP.md` - Where is this going?
- `CLAUDE.md` - How do we build this?
- `TODO.md` - What's current?

### Evidence from Projects

**All projects have context files:**
- README for overview
- CLAUDE.md for standards
- Some have ROADMAP.md for vision

**This conversation:**
- You asked about project goals
- I gave full context (philosophy, patterns, projects)
- Led to much better understanding

---

## Development Philosophy Summary

**Seven proven patterns:**

1. **Layer-by-Layer Development** - Ship useful layers incrementally
2. **Data Before Decisions** - 30-60 days before judging
3. **Consolidate on 3rd Duplicate** - Don't abstract too early
4. **Tests for Fragile Parts** - Not everything needs tests
5. **Every Safety System Was a Scar** - Learn what breaks, then protect
6. **Let Projects Be Experiments** - Learning > shipping
7. **Show the Full Picture** - Context enables better work

**Common theme:** Patience over urgency. Learning over shipping. Patterns over predictions.

---

## When to Apply These Patterns

### ✅ Good fit:
- Exploratory projects
- Data collection experiments
- Learning new domains
- Solo or small team work
- No external deadlines

### ⚠️ Adapt carefully:
- Client work (expectations differ)
- Team projects (alignment needed)
- Time-sensitive work (can't wait 60 days)
- Mission-critical systems (test everything)

### ❌ Don't force:
- Simple scripts (overkill)
- Proof of concepts (too structured)
- Following tutorials (just learn)

---

## Growing This Document

Add new patterns when you notice:
- A principle helping across 2+ projects
- A decision framework you wish you'd had earlier
- A development approach that reduces friction
- A mindset shift that changes outcomes

Don't force it. Let patterns emerge from experience.

---

*Based on PROJECT_PHILOSOPHY.md and battle-tested experience from image-workflow, Cortana Personal AI, and Trading Projects.*

**Remember:** These are patterns, not rules. Use what helps, adapt what doesn't fit, ignore what doesn't apply.


8. **The Super Manager Hierarchy** - Orchestrate AI via specialized roles

---

## Pattern 8: The Super Manager Hierarchy

### What
Orchestrate complex project launches by separating AI agents into specialized roles based on their "altitude" of thinking.

1. **The Conductor (Erik):** Defines the "Vision" and "Vibe." Sets the constraints and high-level mission orders. The only human in the loop.
2. **The Super Manager (Erik with context of all projects):** Operates at the meta-level (scaffolding). Writes prompts based on to-do lists. Has strategic view across all projects. **DOES NOT WRITE CODE. DOES NOT USE TOOLS.** Only drafts prompts for Workers.
3. **The Floor Manager (Claude Code/Cursor - AI with project context):** **THE MESSENGER** - receives prompts from Super Manager and passes them to Workers via Ollama MCP. **DOES NOT WRITE CODE. DOES NOT GENERATE LOGIC.** Only facilitates communication.
4. **The Workers (Local Ollama Models via MCP):** DeepSeek-R1, Qwen3, etc. **THE BRAIN AND THE HANDS** - do ALL actual work. Read prompts, read files, write code, modify files - EVERYTHING.

### Why It Works
- **Prevents Context Drowning:** The Floor Manager doesn't need to know every detail of the billing history; the Super Manager handles cross-project concerns like "EXTERNAL_RESOURCES."
- **Enforces Standards:** The Super Manager writes prompts that reference "Gold Standard" templates and ensures Workers follow them.
- **High-Speed Execution:** By having Workers do ALL the actual work while the Floor Manager simply relays prompts, the system moves 10x faster with lower costs (local models are free).

### Implementation
- **Project Indexing:** Every project must have a `00_Index_[ProjectName].md` so the Super Manager can orient itself instantly.
- **Handoff Protocols:** Super Manager writes structured "Mission Orders" (prompts) that Floor Manager passes to Workers.
- **Governance Logs:** Maintain a central `EXTERNAL_RESOURCES.md` at the Super Manager level to find aliases and nicknames across all projects.

### Evidence from Projects
**Muffin Pan Recipes Kickoff:**
- Conductor (Erik) provided the "Oven-less" vision.
- Super Manager identified the "Mission Control" alias in the 3D Pose Factory project and wrote prompts.
- Floor Manager relayed prompts to Workers via Ollama MCP.
- Workers (Local Ollama models) executed the Phase 0-2 build in a single 8-hour marathon.
