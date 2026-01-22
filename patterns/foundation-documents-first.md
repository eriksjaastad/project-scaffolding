# Foundation Documents First

**Pattern Type:** 🟢 Proven (learned through pain)
**First Applied:** January 2026
**Source Project:** project-scaffolding (meta-project itself)

---

## The Problem

**Symptom:** AI agents executing tasks inconsistently, getting confused in weird ways, or producing different interpretations of the same instructions across sessions.

**Root Cause:**
- Foundation documents (AGENTS.md, .cursorrules) were ambiguous
- You had the mental model in your head but documents didn't reflect it clearly
- Models could read them and each interpret differently
- Things would work... until they didn't
- The failures were WEIRD and inconsistent

**The Trap:** You can't see the problem early because:
1. **You have the mental model** - you know what you meant when you wrote it
2. **You trust models to "get it"** - "just go update that file" seems to work
3. **The ambiguity isn't obvious** - until you see downstream confusion
4. **Other problems are noisier** - code reviews, safety systems, external resources demand attention first

**The Scar:** Spending 2+ weeks building automation (code review systems, external resources tracking) on top of an ambiguous foundation, only to discover agents were interpreting basic roles and workflows differently.

---

## The Pattern

**Define roles and workflows with zero ambiguity in foundation documents BEFORE building any automation or delegation systems.**

Foundation documents are your **operating system**:
- `AGENTS.md` - The hierarchy, roles, constraints, workflow
- `.cursorrules` - Project-specific rules and standards
- `CLAUDE.md` - AI collaboration instructions

These documents are like a constitution. Everything seems fine until there's a dispute, and then you realize everyone interpreted the rules differently.

---

## When to Apply

✅ **Use this pattern when:**
- Starting a new project with AI collaboration
- Building automation that delegates work to other agents
- Onboarding new AI models to an existing workflow
- Experiencing "weird" inconsistencies in agent behavior
- About to scale from 1 agent to multiple agents

❌ **Skip this pattern when:**
- You're the only one working (no delegation)
- The project is a one-off script (no reuse)
- You're prototyping and will throw it away

---

## How to Apply

### Phase 1: Audit Current Foundation Documents

**Read them as if you've never seen them before:**
- [ ] Could someone with NO context follow these instructions?
- [ ] Are roles defined with constraints that are STRICTLY PROHIBITED?
- [ ] Is the workflow step-by-step with no room for interpretation?
- [ ] Are there examples showing correct vs. incorrect behavior?

**Red flags:**
- "The Floor Manager handles execution" (what does "handles" mean?)
- "Use best judgment" (whose judgment? based on what criteria?)
- "Follow standard practices" (which standards?)
- Multiple valid interpretations of the same sentence

### Phase 2: Eliminate All Ambiguity

**For each role, define:**
1. **Name** - What they're called
2. **Scope** - What domain they operate in
3. **Tools** - What they can use
4. **Constraints** - What they are STRICTLY PROHIBITED from doing
5. **Mandate** - Specific responsibilities (numbered list)

**For the workflow, define:**
1. **Step-by-step process** (numbered, sequential)
2. **Handoff points** - Who passes what to whom
3. **Quality gates** - Where verification happens
4. **Failure protocols** - What happens when things go wrong
5. **Success criteria** - How you know it's done

**Use strong language:**
- ✅ "STRICTLY PROHIBITED from writing code"
- ✅ "MUST verify by reading the files"
- ✅ "Only the Workers write code. Under no circumstances..."
- ❌ "Should avoid writing code"
- ❌ "Typically verifies..."
- ❌ "Usually the Workers write code"

### Phase 3: Add Examples and Templates

**Provide concrete templates:**
```markdown
### [TASK_TITLE]
**Worker Model:** [DeepSeek-R1 / Qwen-2.5-Coder]
**Objective:** [Brief 1-sentence goal]

### 🎯 [ACCEPTANCE CRITERIA] (MANDATORY CHECKLIST)
- [ ] **Functional:** [specific requirement]
- [ ] **Syntax:** [specific requirement]
- [ ] **Standards:** [specific requirement]
- [ ] **Verification:** [specific test command]
```

**Show anti-patterns:**
- ❌ "Fix the bug" (no acceptance criteria)
- ✅ "Fix the TypeError in utils.py line 47. Acceptance: pytest passes, no type errors"

### Phase 4: Test With Fresh Eyes

**Before you build anything:**
1. Show the docs to a new AI session (no context)
2. Ask them to explain the workflow back to you
3. Ask them what would happen in edge cases
4. Look for ANY confusion or questions - that's ambiguity

**If they ask clarifying questions, your docs aren't clear enough yet.**

---

## Why This Matters

### The Compounding Effect

Foundation documents are referenced by:
- Every project in your ecosystem
- Every AI agent you delegate to
- Every automation you build
- Every new team member (human or AI)

**Getting them right means:**
- ✅ No more mystery confusion
- ✅ New models/agents onboard faster
- ✅ You can delegate with confidence
- ✅ The system is teachable (not just "Erik knows how it works")
- ✅ Automation actually automates instead of creating new problems

**Getting them wrong means:**
- ❌ Every agent interprets rules differently
- ❌ Weird, inconsistent failures
- ❌ Time wasted debugging "why did it do that?"
- ❌ Can't scale beyond your own mental model
- ❌ Automation amplifies confusion

### The Lesson

**You can't know what needs to be clear until you see what's getting misunderstood.**

The fact that you discovered this through pain rather than planning? That's normal. The work you did building code review systems and external resources tracking wasn't wasted - it showed you where the real problem was.

This is like discovering your house has a cracked foundation after you've already built the second floor. You have to go back and fix it. But once you do, everything else becomes stable.

---

## Real Example: Project Scaffolding (January 2026)

### Before (Ambiguous)

**AGENTS.md (old version):**
```markdown
3. The Floor Manager: Orchestrator and Tool Executor.
   THE HANDS. You take Worker blueprints and physically
   apply them using tools.
```

**What went wrong:**
- "Orchestrator" - does that mean planning? executing? both?
- "THE HANDS" - but also "take Worker blueprints" - so who's thinking?
- "Physically apply" - with what tools? when?
- Multiple models interpreted this differently
- Sometimes Floor Manager would write code, sometimes not
- Confusion about whether to use Ollama MCP or write code directly

### After (Crystal Clear)

**AGENTS.md (new version):**
```markdown
3. The Floor Manager (QA & Messenger)
   - Role: Orchestrator, Quality Assurance Lead, Context Bridge
   - Tools: Ollama MCP (ollama_run, ollama_run_many)
   - Constraint: STRICTLY PROHIBITED from generating logic or writing code
   - Mandate:
     1. Relay: Pass Super Manager prompts to Workers via MCP
     2. Context Bridge: Provide necessary files to Workers when requested
     3. Verify: Inspect Worker output against Checklist
     4. Sign-Off: Only mark tasks "Complete" after all items pass
   - Identity: You are a Gatekeeper. You must independently verify
     by reading files before reporting to Conductor.
```

**What changed:**
- Role is named: "QA & Messenger"
- Tools are explicit: "Ollama MCP with these functions"
- Constraint is absolute: "STRICTLY PROHIBITED from writing code"
- Mandate is numbered steps: no ambiguity about order
- Identity is clear: "Gatekeeper" not "hands"

**Result:** Zero confusion about what Floor Manager does. Workflow works consistently.

---

## Implementation Checklist

### Starting a New Project
- [ ] Copy AGENTS.md as-is (don't customize until proven)
- [ ] Read it out loud - does every sentence have one interpretation?
- [ ] Define roles with STRICTLY PROHIBITED constraints
- [ ] Write workflow as numbered steps
- [ ] Add prompt template with acceptance criteria format
- [ ] Test with a fresh AI session (no context)

### Fixing an Existing Project
- [ ] Identify symptoms (weird failures, inconsistent behavior)
- [ ] Audit foundation docs for ambiguity
- [ ] Rewrite sections using strong language
- [ ] Add examples and anti-patterns
- [ ] Update all projects that reference these docs
- [ ] Re-test workflows with clear criteria

---

## Common Mistakes

### ❌ Anti-Pattern 1: "The docs are clear to me"
**Problem:** You wrote them with your mental model. Of course they're clear to you.
**Fix:** Test with a fresh AI that has zero context. If they ask questions, it's not clear.

### ❌ Anti-Pattern 2: "I'll fix it when I see problems"
**Problem:** By the time you see problems, you've built automation on top of confusion.
**Fix:** Invest 2 hours upfront to eliminate ambiguity. Saves 20 hours of debugging later.

### ❌ Anti-Pattern 3: "Just update that file for me"
**Problem:** You don't verify what the agent actually wrote. Could be adding more ambiguity.
**Fix:** Always read the updated docs yourself. Ensure they're clearer than before.

### ❌ Anti-Pattern 4: "Soft language is friendlier"
**Problem:** "Should avoid" leaves room for interpretation. "Try to" means "maybe don't."
**Fix:** Use absolute constraints: NEVER, ALWAYS, STRICTLY PROHIBITED, MUST.

---

## Success Metrics

**After fixing foundation documents:**

**Week 1:**
- [ ] Zero clarifying questions from agents about roles/workflow
- [ ] Consistent behavior across different AI models
- [ ] Delegation works first try (no "why did it do that?")

**Month 1:**
- [ ] New agents onboard in < 5 minutes (read docs, start working)
- [ ] Can scale to multiple agents working in parallel
- [ ] Automation actually saves time instead of creating problems

**Month 3:**
- [ ] Foundation docs are referenced by multiple projects
- [ ] Other humans/AIs can understand the system without your explanation
- [ ] The system is teachable, not tribal knowledge

---

## Related Patterns

- **Safety Systems** - Foundation docs should define safety constraints
- **Tiered AI Sprint Planning** - Requires clear role definitions to route work appropriately
- **The Caretaker Role** - Floor Manager as gatekeeper is caretaker for Workers

---

## Status

🟢 **Proven Pattern** - Hard-won through experience

**Evidence:** Project Scaffolding (January 2026)
- Spent 2 weeks building on ambiguous foundation
- Agents got confused in weird, inconsistent ways
- Rewrote AGENTS.md and .cursorrules with zero ambiguity
- Immediate clarity, consistent behavior, successful delegation

---

## The Key Insight

**You can't automate on top of an ambiguous foundation. You'll just automate confusion.**

Fix your operating system first. Then build.

---

*Pattern extracted from project-scaffolding meta-project after discovering agents were interpreting roles differently despite weeks of working together.*

*"The foundation problem you don't see until later" - Erik Sjaastad, January 2026*

## Related Documentation

- [[CODE_REVIEW_ANTI_PATTERNS]] - code review
- [[LOCAL_MODEL_LEARNINGS]] - local AI
- [[PROJECT_KICKOFF_GUIDE]] - project setup
- [[PROJECT_STRUCTURE_STANDARDS]] - project structure
- [[automation_patterns]] - automation
- [[prompt_engineering_guide]] - prompt engineering
- [[queue_processing_guide]] - queue/workflow
- [[ai_model_comparison]] - AI models
- [[case_studies]] - examples
- [[orchestration_patterns]] - orchestration
- [[session_documentation]] - session notes
- [[testing_strategy]] - testing/QA
- [[project-scaffolding/README]] - Project Scaffolding
