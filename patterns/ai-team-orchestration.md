# AI Team Orchestration Pattern

> **Purpose:** How to structure multi-agent AI workflows with clear roles, metrics, and guardrails
> **Created:** January 2026
> **Core Insight:** You're not training models - you're training *processes*

---

## The Core Idea

Success = the AI team repeatedly ships **verifiable changes** (diffs + passing tests) under strict constraints.

Multi-agent orchestration isn't about giving AI "personalities" or "seniority levels." It's about defining **task lanes** that map to real outcomes:

| Role | Job | Output |
|------|-----|--------|
| **Manager** | Reads specs, breaks work into tasks, assigns with acceptance criteria, enforces budgets | Task plan |
| **Worker** | Does one narrow job, produces minimal diffs | Code changes |
| **Reviewer** | Validates against criteria, runs tests, catches regressions | Approval or revision request |

This is **generator / implementer / verifier** - not junior/mid/senior.

---

## Task Lane Definitions

### Manager

**Responsibilities:**
- Read the spec or requirements
- Generate a small task plan (N tasks max)
- Assign tasks to workers with clear acceptance criteria
- Stop the run based on budgets and stop conditions
- Track progress and decide when "done"

**Does NOT:**
- Write code
- Make implementation decisions
- Override reviewer feedback

---

### Worker(s)

**Responsibilities:**
- Do one narrow job at a time
- Produce a **diff** (or patch) with minimal scope
- Prefer small changes over rewrites
- Follow the acceptance criteria exactly

**Does NOT:**
- Decide what to work on
- Skip tests
- Expand scope beyond the task

---

### Reviewer

**Responsibilities:**
- Validate worker output against acceptance criteria
- Run tests and check for regressions
- Perform "don't break other stuff" sanity checks
- Request at most **one targeted revision** per task (unless explicitly configured otherwise)

**Does NOT:**
- Rewrite the worker's code
- Add new requirements
- Approve work that fails tests

---

## Metrics to Track Every Run

Each run should output a report for comparison over time:

| Metric | Why It Matters |
|--------|----------------|
| Tasks completed | Basic throughput |
| Tests passing (yes/no) | Correctness |
| Iterations per task | Efficiency |
| Regressions introduced | Quality control |
| Cost estimate / token usage | Budget management |
| Reviewer "caught it?" rate | Reviewer effectiveness |
| Wall time per run | Performance |

Over time, this becomes your feedback loop: "Does this orchestration policy work?"

---

## Guardrails (Non-Negotiable)

Even in development, enforce these:

### Max Iterations
- Example: 3 loops per task maximum
- Prevents infinite revision cycles
- Forces clear acceptance criteria

### Budget Cap
- Example: $X or N tokens per run
- Prevents runaway costs
- Forces efficiency

### Diff Size Cap
- Example: Max 200 lines changed per task
- Prevents "rewrite the entire repo" behavior
- Forces incremental work

### Stop-If-Worse Rule
- If tests get worse than baseline, stop immediately
- Require manual approval to continue
- Prevents compounding regressions

### No External Side Effects
- No network calls to external services
- No real credentials
- No writing outside designated paths
- Prevents "expensive campfire story" failures

---

## Scenario Types

Use these patterns to test and refine your orchestration:

### Scenario A: Bug Hunt (Best Starting Point)

**Goal:** Fix a set of known bugs with minimal diffs until all tests pass.

**Setup:**
- Codebase contains 3-10 intentionally broken behaviors
- Tests fail with symptoms, not exact line instructions
- Manager picks one bug at a time

**Why it works:**
- Very clear pass/fail criteria
- Cheap to run repeatedly
- Forces debugging + minimal diffs
- Great for comparing orchestration policies

---

### Scenario B: Feature + Constraints

**Goal:** Implement a new feature from a strict spec.

**Setup:**
- A spec defines exact requirements
- Tests enforce expected behavior, edge cases, error handling
- Manager breaks spec into 2-5 small tasks

**Why it works:**
- Measures planning quality
- Measures ability to follow constraints
- Reveals "model drift" (skipping requirements)

---

### Scenario C: Refactor Without Breaking

**Goal:** Improve structure or performance while keeping behavior identical.

**Setup:**
- Tests already pass
- Code has known issues (duplication, ugly interfaces, slow functions)
- Task: refactor for clarity/performance, keep tests green

**Why it works:**
- Forces discipline
- Tests whether reviewer catches subtle behavior changes
- Mimics real codebase maintenance

---

## Difficulty Progression

Start small, measure, tweak, level up:

### Level 0: Single Task
- 1 bug or 1 small feature
- 1 worker
- Strict iteration cap
- **Goal:** Learn the loop mechanics

### Level 1: Multi-Task
- 5 bugs or 1 medium feature
- Manager chooses order
- **Metric:** Cost per task completed

### Level 2: Feature + Constraints
- Small spec + tests
- **Metric:** Spec compliance rate

### Level 3: Refactor Without Breaking
- Tiny module refactor
- **Metric:** Regression rate, reviewer catch rate

### Level 4: Mixed Workload (Realistic)
- 2 bugs + 1 feature + 1 refactor
- Manager must triage and budget
- **Metric:** Overall throughput and quality

---

## Model Routing by Task Type

Route to appropriate models based on task complexity:

| Task Type | Model Tier | Rationale |
|-----------|------------|-----------|
| Task breakdown | Cheap/Fast | Simple decomposition |
| Generating tests | Cheap/Fast | Formulaic output |
| Doc updates | Cheap/Fast | Low stakes |
| Simple fixes | Cheap/Fast | Narrow scope |
| Most implementation | Mid | Balance of speed/quality |
| Debugging | Mid | Requires reasoning |
| High-risk integration | Expensive | Stakes justify cost |
| Repeated failures (2+ attempts) | Expensive | Need stronger model |
| Final review | Expensive | Quality gate |

**Rule:** Don't run expensive models in parallel by default.

See: `local-ai-integration.md` for specific model recommendations.

---

## Definition of Done (Per Run)

A run is "done" when:

- [ ] Tests pass OR the system hits stop conditions
- [ ] A run report is saved (metrics + artifacts)
- [ ] Diffs are stored (even failed attempts)
- [ ] No regressions introduced (or explicitly approved)

---

## The Whole Point

You're building a repeatable system where you can:

1. **Change one orchestration rule**
2. **Rerun the exact same scenario**
3. **See if outcomes improve** (cost down, regressions down, completion up)

That's how you get to "I can hand work off to an AI team and not worry" - through measured iteration, not hope.

---

## Integration with Erik Ecosystem

### Connects To:
- **local-ai-integration.md** - Model selection and routing
- **tiered-ai-sprint-planning.md** - Sprint-level task planning
- **safety-systems.md** - Guardrails and stop conditions
- **learning-loop-pattern.md** - Iteration and improvement cycles

### Implementation Notes:
- Manager role maps to "Super Manager" in AGENTS.md hierarchy
- Worker role maps to "Floor Manager" or specialized agents
- Reviewer role can be human, AI, or automated tests
- Metrics should feed into project-tracker for visibility

---

*This pattern extracted from AI Training Lab research, January 2026*
