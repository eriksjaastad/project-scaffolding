# Learning Loop Pattern

> **Purpose:** Close the gap between documenting knowledge and applying it
> **Status:** Draft - evolved from late-night society/governance conversation
> **Created:** January 10, 2026

---

## The Problem We're Solving

**Knowledge externalization:** When we document a learning but don't apply it, the cost is deferred to a future session. The person who documents isn't the one who pays when it fails to get applied.

This is the same failure mode Erik identified in societal systems:

> *"We have an accounting system that rewards speed and spectacle, and an accountability system that arrives after the decision-makers are gone."*

In our system:
- We document learnings (speed/spectacle of "look, we learned something!")
- We don't apply them consistently (accountability arrives in future sessions when things break)
- Future sessions pay the cost of re-learning

**The documentation is write-only. The learning loop has a gap.**

---

## Insight from Society/Governance Thinking

Erik's late-night conversation with GPT about economic externalities revealed parallel patterns:

| Society Problem | Our Problem |
|-----------------|-------------|
| Externalities get pushed to future generations | Learning costs get pushed to future sessions |
| "Book it now or pay later with interest" | Document it now, but who applies it? |
| No mechanism to make decision-makers feel the cost | No mechanism to make prompters feel skipped learnings |

**The solution in both cases:** Make the cost visible and immediate, not deferred and diffuse.

---

## Proposed Mechanism: The Four Bridges

### Bridge 1: Downstream Harm Estimate

Every task prompt should include a **Downstream Harm Estimate**:

```markdown
### ⚠️ DOWNSTREAM HARM ESTIMATE
- **If this fails:** [What breaks? Who pays? How long to recover?]
- **Known pitfalls:** [What patterns from LOCAL_MODEL_LEARNINGS.md apply here?]
- **Assumptions that would break this:** [What's the confidence range?]
```

**Why it works:**
- Forces the Super Manager to consult learnings BEFORE drafting
- Makes hidden costs visible upfront
- Creates a "50-year receipt" for tasks (who pays if it goes wrong?)

**Example:**
```markdown
### ⚠️ DOWNSTREAM HARM ESTIMATE
- **If this fails:** Script corrupts cursorrules files. Recovery requires git restore. ~15 min per affected project.
- **Known pitfalls:** DeepSeek-R1 needs 300s timeout for file-heavy tasks (LOCAL_MODEL_LEARNINGS.md). Task requires file writes.
- **Assumptions that would break this:** Assumes all projects have .cursorrules in root. If nested, detection fails silently.
```

---

### Bridge 2: Pre-Flight Block (Not Reminder)

**Current state:** "Remember to read learnings before prompting"
**Problem:** Remembering is optional. Optional things get skipped.

**Proposed:** A structural block that prevents work without acknowledgment.

Option A: **Learnings Checksum in Prompts**
```markdown
### 📚 LEARNINGS APPLIED
- [x] Timeout: 300s for file-heavy tasks (learned Jan 10)
- [x] Decomposition: Micro-tasks for DeepSeek (learned Jan 10)
- [x] Diff style: StrReplace over full rewrites (learned Jan 10)

_Last consulted LOCAL_MODEL_LEARNINGS.md: 2026-01-10_
```

If this section is missing or stale, the Floor Manager should **block execution** and request it.

Option B: **Automated Prompt Validator**
A script that parses prompts and checks for required sections before they go to Workers. Fails fast if harm estimate or learnings acknowledgment is missing.

---

### Bridge 3: Preventable Failure Flag

When a task fails, the Floor Manager should ask:

> "Was this failure covered by an existing learning that wasn't applied?"

If yes, log it as a **Preventable Failure**:

```markdown
| Date | Failure | Was it Preventable? | Which Learning? |
|------|---------|---------------------|-----------------|
| Jan 10 | Timeout | YES | "300s for file-heavy" |
| Jan 10 | Full rewrite timeout | YES | "Use StrReplace" |
```

**Why it works:**
- Creates a "shame log" for skipped learnings (immediate cost)
- Makes the cost of not reading visible
- Over time, tracks which learnings are most frequently ignored

---

### Bridge 4: Learning Debt Tracker

Documented learnings have a lifecycle:

```
OBSERVED → DOCUMENTED → COMPILED → APPLIED
```

**Learning Debt** = Documented but not yet Compiled into templates.

Track this explicitly:

```markdown
## Learning Debt (Uncompiled)

| Learning | Documented | Compiled Into |
|----------|------------|---------------|
| 300s timeout | ✅ Jan 10 | ❌ Not in templates yet |
| StrReplace preference | ✅ Jan 10 | ❌ Not in templates yet |
| Micro-task decomposition | ✅ Jan 10 | ❌ Not in templates yet |
```

**Trigger for compilation:** When a learning has caused 2+ preventable failures, it MUST be compiled into templates. No more deferral.

---

## How This Closes the Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   FAILURE/SUCCESS                                               │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐                                               │
│   │  DOCUMENT   │  ← Floor Manager writes to                    │
│   │  (Learnings)│    LOCAL_MODEL_LEARNINGS.md                   │
│   └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  TRACK DEBT │  ← Learning added to "uncompiled" tracker │   │  ◄── NEW
│   └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐                                               │
│   │   REVIEW    │  ← Super Manager reads learnings              │
│   │             │    BEFORE drafting (blocked if stale)         │  ◄── ENFORCED
│   └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │   ESTIMATE  │  ← Downstream Harm Estimate required        │   │  ◄── NEW
│   └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐                                               │
│   │   APPLY     │  ← Floor Manager uses prompt with             │
│   │             │    baked-in learnings                         │
│   └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  FAIL CHECK │  ← If failed: Was it preventable?           │   │  ◄── NEW
│   │             │    If yes: Flag + increment debt trigger     │
│   └─────────────────────────────────────────────────────────┘   │
│         │                                                       │
│         └───────────────────────────────────────────────────────┘
```

---

## The Fuzzy vs Explicit Tension

Erik's concern: "I really wanted to get around relying on prompts. Prompts are fragile."

**This pattern doesn't eliminate prompts, but it:**

1. **Reduces prompt fragility** by baking known pitfalls into the prompt structure (Harm Estimate section)
2. **Creates feedback loops** that catch when fragility causes failure (Preventable Failure Flag)
3. **Evolves toward robustness** by forcing compilation after repeated failures

**The fuzzy part:** Learnings can stay "documented but uncompiled" until they prove their importance (2+ preventable failures).

**The explicit part:** Once compiled, they're structural. Can't be skipped.

---

## What This Doesn't Solve

1. **Cross-project learning transfer** - How does `project-scaffolding` pass learnings to other projects? (Future pattern needed)

2. **Model-specific prompt optimization** - Each model might need different compiled rules. (Future: model-specific templates)

3. **The "who triggers compilation" question** - Still manual. Could be automated with a script that reads the debt tracker.

---

## Relation to Societal Governance Ideas

From Erik's GPT conversation, these principles apply:

| Principle | Application Here |
|-----------|------------------|
| **"Externality as Debt"** | Learning Debt Tracker - uncompiled learnings are explicit debt |
| **"50-Year Receipt"** | Downstream Harm Estimate - who pays if this fails? |
| **"Pay for outcomes, not outputs"** | Preventable Failure Flag - measure "did we apply learning" not "did we document" |
| **"AI as adversarial auditor"** | Floor Manager checks "was this preventable?" after every failure |
| **"Discount rate fight"** | Refusing to defer learning application to future sessions |

---

## Next Steps

- [ ] Add "Downstream Harm Estimate" section to prompt template in AGENTS.md
- [ ] Add "Learnings Applied" acknowledgment section to prompt template
- [ ] Create Learning Debt Tracker section in LOCAL_MODEL_LEARNINGS.md
- [ ] Test on next Worker task
- [ ] After 2 weeks: Review preventable failure rate

---

## Related Documents

- `KNOWLEDGE_CYCLE_DISCUSSION.md` - The original stuck-point discussion
- `LOCAL_MODEL_LEARNINGS.md` - Where learnings are documented
- `AGENTS.md` - Where prompt templates live
- The late-night society conversation (January 9, 2026) - Source of governance parallels

---

*This pattern evolved from a connection Erik noticed between AI governance and societal governance. The insight: externalized costs in both systems lead to write-only documentation and deferred accountability.*
