# Knowledge Cycle Discussion

> **Date:** January 10, 2026
> **Participants:** Erik (Conductor), Claude Opus (Super Manager), Gemini Flash (Floor Manager)
> **Status:** Active Discussion
> **Trigger:** Post-mortem on Global Rules Injection implementation

---

## The Problem We Identified

After documenting learnings from Worker timeouts in `LOCAL_MODEL_LEARNINGS.md`, Erik asked:

> "We are writing all this down, but who's reading it? I never asked you to read it. I didn't ask the floor manager to read it. So how is this continual learning being implemented in a day-to-day kind of way?"

**The documentation is write-only.** We capture knowledge but there's no mechanism to ensure it gets applied.

---

## Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| 1. Add to CLAUDE.md | Tell Super Manager to read learnings before drafting | Simple | Relies on remembering |
| 2. Floor Manager Pre-Flight | Add to AGENTS.md duties | Explicit | Another thing to forget |
| 3. Embed in Templates | Bake patterns directly into prompt templates | Can't be skipped | Templates might be too rigid? |
| 4. Start-of-Session Ritual | First action is read learnings | Cultural | Hard to enforce |
| 5. Pattern Cards in Prompts | Force drafter to select patterns | Conscious choice | Extra step |

**Initial conclusion:** Option 3 - if knowledge isn't in the prompt itself, it won't get used.

---

## Context Cost Question

Erik asked: "How much is reading LOCAL_MODEL_LEARNINGS.md going to blow out your context?"

**Analysis:**
- LOCAL_MODEL_LEARNINGS.md is ~290 lines currently
- For Super Manager (Claude): ~1-2% of context, not a problem
- For Floor Manager: Doesn't need full doc, just operational rules
- For Workers: Need nothing - they just execute

**Conclusion:** Super Manager can absorb full learnings. Floor Manager only needs the "compiled" output (the templates with rules baked in).

---

## The Knowledge Cycle (Proposed)

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
│   ┌─────────────┐                                               │
│   │   REVIEW    │  ← Super Manager reads learnings              │
│   │             │    before next prompting effort               │
│   └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐                                               │
│   │   UPDATE    │  ← Super Manager updates prompt               │
│   │  (Templates)│    templates with new patterns                │
│   └─────────────┘                                               │
│         │                                                       │
│         ▼                                                       │
│   ┌─────────────┐                                               │
│   │   APPLY     │  ← Floor Manager uses updated                 │
│   │             │    templates for Workers                      │
│   └─────────────┘                                               │
│         │                                                       │
│         └───────────────────────────────────────────────────────┘
```

**Key Insight:**
- `LOCAL_MODEL_LEARNINGS.md` = Source code (the "why", history, context)
- `Prompt Templates` = Compiled executable (the "what to do")

The templates become the mechanism for applying institutional knowledge.

---

## Who Needs What

| Role | What They Read | Why |
|------|----------------|-----|
| **Super Manager** | Full LOCAL_MODEL_LEARNINGS.md | Drafts prompts, needs to understand patterns and reasoning |
| **Floor Manager** | Just the templates (with rules baked in) | Dispatches and verifies, follows operational rules |
| **Workers** | Just the prompt | Execute the task, no institutional memory needed |

---

## Open Question: Are Templates Flexible Enough?

Erik raised a concern:

> "Is the template flexible enough for that? At least the way I picture a template, it's kind of a narrow thing."

**The tension:**
- Traditional templates are rigid (fill-in-the-blank)
- We need something that can evolve with learnings
- But also provides structure and enforces rules

**Possible evolution:**

Maybe it's not a "template" but a "prompt framework" or "prompt scaffold":

```
PROMPT SCAFFOLD
├── Fixed Structure (always present)
│   ├── CONSTRAINTS section
│   ├── ACCEPTANCE CRITERIA format
│   └── FLOOR MANAGER PROTOCOL
│
├── Operational Rules (updated from learnings)
│   ├── Timeout settings (currently: 300s for file-heavy)
│   ├── Output style (currently: diff/StrReplace preferred)
│   └── Escalation rules (currently: 3-strike)
│
└── Task-Specific Content (varies per task)
    ├── Objective
    ├── Code to write/modify
    └── Verification steps
```

The "Operational Rules" section is what gets updated when we learn new things.

---

## The Deeper Concern: Prompt Fragility

Erik raised a fundamental concern:

> "I really wanted to get around relying on prompts. My worry about prompts is they're fragile - the results are varied. It's not as bad as 'this prompt needs to be worded exactly like this,' but still."

**The tension:**
- We're building a system that relies on prompts to Workers
- Prompts are inherently variable in their results
- We want something more robust than "hope the prompt works"
- But we don't have an alternative yet

**What we're NOT trying to build:**
- A brittle system where one wrong word breaks everything
- A prompt library that requires constant tweaking
- Dependency on "prompt engineering magic"

**What we ARE trying to build:**
- A system where knowledge gets applied consistently
- Guardrails that work even when prompts are imperfect
- Something that degrades gracefully when Workers struggle

---

## Where We're Stuck

### Stuck Point 1: The Prompt Paradox
We need prompts to communicate with Workers, but we don't want to be over-reliant on precise prompt wording. How do we make the system robust to prompt variation?

### Stuck Point 2: Knowledge Application Without Reading
We want learnings to be applied, but we can't guarantee anyone reads the learnings doc. Baking rules into prompts helps, but creates duplication and maintenance burden.

### Stuck Point 3: No Clear Trigger
What kicks off the "update templates with new learnings" step? If it's manual, it'll be forgotten. If it's automatic, how does that work?

### Stuck Point 4: Template vs. Framework vs. ???
The word "template" feels too rigid. "Scaffold" or "framework" might be better, but we haven't defined what that actually looks like in practice.

### Stuck Point 5: Fuzzy vs. Explicit
Erik wants something "fuzzy" - organic and automatic. But AI systems often need explicit instructions. How do we bridge that gap?

---

## Questions Still Open

1. **Where do operational rules live?**
   - In each prompt file? (Duplication)
   - In a shared "rules header" that gets included? (DRY but more complex)
   - In the PROMPTS_INDEX.md that Floor Manager reads first?

2. **What triggers a template update?**
   - After every session with failures?
   - Weekly review?
   - When LOCAL_MODEL_LEARNINGS.md has new entries?

3. **Who is responsible for the "compile" step?**
   - Super Manager before drafting new prompts?
   - A dedicated "update templates" task?

4. **How do we version this?**
   - Do prompts reference "v1.2 of operational rules"?
   - Or is it always "latest"?

5. **Can we reduce prompt dependency?**
   - Are there structural/architectural changes that make prompt precision less critical?
   - What would a "prompt-light" workflow look like?

---

## Next Steps

- [x] Decide on template vs. scaffold vs. framework terminology → Using "prompt template" with embedded operational sections
- [x] Define where operational rules live → Embedded in AGENTS.md prompt template (Downstream Harm Estimate, Learnings Applied sections)
- [x] Create the first "compiled" prompt scaffold with today's learnings → Done: AGENTS.md updated
- [ ] Test on next Worker task to see if it works
- [ ] Document what we learn from that test
- [x] Create Learning Loop Pattern → `patterns/learning-loop-pattern.md`
- [x] Add Learning Debt Tracker → `LOCAL_MODEL_LEARNINGS.md`

---

## Update: January 10, 2026 (Night) - Breakthrough via Society Parallel

Erik noticed a parallel between this knowledge cycle problem and a late-night conversation about societal governance/economics. The core insight:

**The learning loop gap is an EXTERNALITY problem.**

When you document a learning but don't apply it:
- The cost is deferred to a future session
- The person who documents isn't the one who pays the cost of not applying it
- There's no mechanism to "book" that cost now

**Solution framework:** Make skipping learnings COSTLY at the moment of skipping, not later.

See `patterns/learning-loop-pattern.md` for the full pattern, including:
- **Downstream Harm Estimate** - Force upfront acknowledgment of "who pays if this fails"
- **Learning Debt Tracker** - Explicit tracking of uncompiled learnings
- **Preventable Failure Flag** - Ask "was this covered by existing learning?" after every failure
- **Pre-Flight Block** - Structural enforcement, not just reminders

This moves us past Stuck Point 5 (Fuzzy vs Explicit) by:
- Fuzzy: Learnings can stay "documented but uncompiled" initially
- Explicit: Once they cause 2+ preventable failures, they MUST be compiled

---

## Session Notes

**Erik's key insight:** The knowledge cycle needs to be "fuzzy" - organic and automatic, not rigid and forgettable.

**Claude's key insight:** The template is the "compiled knowledge" - if patterns aren't in the prompt, they won't be applied.

**Floor Manager's key insight:** (From retrospective) "If the Worker can't do it, the task is either too big or the model is wrong for the job. Stop and rethink."

---

*This document captures our discussion. To be updated as we refine the approach.*
