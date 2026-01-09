# Tiered AI Sprint Planning

**Pattern Type:** 🟡 Emerging (needs validation)  
**First Applied:** December 22, 2025  
**Source Project:** AI usage-billing tracker (cost crisis recovery)

---

## The Problem

**Symptom:** Blowing through $300/month AI budget in 28 days by using expensive models (Claude Sonnet 4.5, Cursor Max Mode) for ALL tasks, including simple ones.

**Root Cause:**
- No mental model for "when to use which AI"
- Defaulting to "most powerful = best"
- Treating all work as equal complexity
- No cost awareness during work

**The Scar:** Hitting $200 limit + $100 overage with 2 days left in billing cycle.

---

## The Pattern

**Route AI tasks to cost-appropriate tiers based on complexity, ambiguity, and risk.**

### The Three Tiers

```
┌─────────────────────────────────────────────────┐
│ TIER 1: Big Brain (Sonnet 4.5, GPT-4, Gemini Pro)│
│ Cost: ~$15/million input tokens                 │
│ Use for: Architecture, debugging, strategy      │
│ Budget: 20% of monthly token spend              │
├─────────────────────────────────────────────────┤
│ TIER 2: Implementation (Gemini 3 Flash)         │
│ Cost: ~$0.075/million input tokens (40x cheaper!)│
│ Use for: Multi-file build, refactoring, tests   │
│ Budget: 50% of monthly token spend              │
├─────────────────────────────────────────────────┤
│ TIER 3: Worker Bees (GPT-4o-mini, Local Ollama) │
│ Cost: ~$0.15/million tokens or $0 (Local)       │
│ Use for: Boilerplate, docs, repetitive tasks   │
│ Budget: 30% of monthly token spend              │
└─────────────────────────────────────────────────┘
```

---

## When to Apply

✅ **Use this pattern when:**
- You have a monthly AI budget to manage
- You're using multiple AI models/services
- You're working across multiple projects
- You notice overspending on AI
- You want to optimize cost without sacrificing quality

❌ **Skip this pattern when:**
- You have unlimited AI budget
- You only use one AI service
- Cost is not a concern
- You're in "build at all costs" mode for a critical deadline

---

## How to Apply

### 1. Tier Decision Formula

Before starting ANY task, calculate:

```
Tier Score = (Complexity + Ambiguity + Risk) / 3

Complexity (1-10):
  1-3 = Instructions are clear, task is straightforward
  4-7 = Multiple steps, some unknowns
  8-10 = Complex architecture, many unknowns

Ambiguity (1-10):
  1-3 = Requirements are crystal clear
  4-7 = Some interpretation needed
  8-10 = Unclear what "done" looks like

Risk (1-10):
  1-3 = Low risk if wrong, easy to fix
  4-7 = Medium risk, some rework if wrong
  8-10 = High risk (production, security, money)

Result:
  Score 1-3 → Tier 3 (Worker Bee)
  Score 4-7 → Tier 2 (Mid-Weight)
  Score 8-10 → Tier 1 (Big Brain)
```

### 2. Task-to-Tier Mapping

**Tier 1 (20% budget):**
- System architecture from scratch
- Complex multi-file debugging
- Strategic product decisions
- Crisis recovery (like restoring deleted code)
- Security-critical code review
- Performance optimization requiring deep analysis

**Tier 2 (50% budget):**
- Implementing features with clear specs
- Refactoring individual modules
- Writing tests
- API integration with good docs
- Medium complexity bug fixes
- Code review of PRs

**Tier 3 (30% budget):**
- Writing documentation
- Generating boilerplate (models, tests, configs)
- File organization/cleanup
- CSV/JSON parsing
- Simple CRUD operations
- Formatting/linting fixes

### 3. Tool Configuration

**Cursor settings example:**
```json
{
  "cursor.chat.model": "gpt-4o-mini",  // Default to Tier 3
  "cursor.composer.model": "gpt-4o",   // Tier 2 for multi-file
  // Only use Max Mode manually when truly needed (Tier 1)
}
```

**Model selection:**
- Tier 3: Cursor Normal Mode, GPT-4o-mini
- Tier 2: Cursor Composer/Agent, GPT-4o
- Tier 1: Web Claude Sonnet, Cursor Max Mode (sparingly!)

---

## Budget Allocation

### Monthly $200 Budget Example:

| Tier | Model | Budget | Est. Sessions | Daily Budget |
|------|-------|--------|---------------|--------------|
| Tier 1 | Claude Sonnet 4.5 | $40 (20%) | 4-6 | $1.35/day |
| Tier 2 | GPT-4o / Haiku | $100 (50%) | 30-40 | $3.35/day |
| Tier 3 | GPT-4o-mini | $60 (30%) | 100+ | $2.00/day |

**Daily total:** ~$6.70/day to stay under $200/month

### Warning Signs:
- 🟡 Spending >$10/day → Over-using Tier 1
- 🔴 Hit $200 before day 25 → Emergency Tier 3 only mode
- 🟢 Under $5/day → Good balance!

---

## Emergency Budget Mode

**If you blow the budget with days left in cycle:**

**STRICT RULES:**
1. ⛔ NO Tier 1 (no Claude Sonnet, no Max Mode)
2. ⚠️ Minimize Tier 2 (GPT-4o only if absolutely necessary)
3. ✅ Tier 3 ONLY (GPT-4o-mini for everything)

**What you CAN still do:**
- Write boilerplate code
- Simple bug fixes
- Documentation
- File organization
- Testing (with clear specs)

**What you CANNOT do:**
- Complex debugging (defer to next cycle)
- Architecture changes (defer)
- Large refactors (defer)
- "Figure out how to..." exploratory work (defer)

---

## Implementation Checklist

### Setup (One-time):
- [ ] Calculate your monthly AI budget
- [ ] Allocate % to each tier (20/50/30 is starting point)
- [ ] Configure tool defaults (Cursor → GPT-4o-mini default)
- [ ] Document tier decision criteria for your team
- [ ] Set up daily spending tracking (optional but helpful)

### Daily Workflow:
- [ ] Before each task: Calculate tier score
- [ ] Use appropriate model for the tier
- [ ] Track your spending (mental or actual)
- [ ] Review at end of day: Did you stay in budget?
- [ ] Adjust tomorrow's plan if over

### Weekly Review:
- [ ] Check total spend vs. budget
- [ ] Identify tasks that used wrong tier
- [ ] Adjust tier boundaries if needed
- [ ] Plan next week with tier allocations

---

## Common Mistakes

### ❌ Anti-Pattern 1: "Always use the best"
**Problem:** Defaulting to Tier 1 for everything  
**Fix:** Ask "Does this NEED Tier 1?" Default to Tier 3, escalate only when stuck

### ❌ Anti-Pattern 2: "Documentation needs smart AI"
**Problem:** Using Tier 1/2 for docs and boilerplate  
**Fix:** Tier 3 is GREAT at repetitive, well-defined tasks. Use it!

### ❌ Anti-Pattern 3: "I'll track it later"
**Problem:** No awareness of spending until bill arrives  
**Fix:** Mental check each session: "What tier am I using? Why?"

### ❌ Anti-Pattern 4: "This is kind of complex, use Tier 1"
**Problem:** Over-estimating complexity, using expensive models unnecessarily  
**Fix:** Start with Tier 2. If you get stuck for >15 min, THEN escalate to Tier 1

---

## Cursor-Specific Notes

### Cursor Has 3 Modes (Map to Tiers):

**Normal Mode → Tier 3:**
- Single file edits, simple questions
- Default: GPT-4o-mini
- Cost: Low

**Agent/Composer Mode → Tier 2:**
- Multi-file changes, refactoring
- Default: GPT-4o
- Cost: Medium

**Max Mode → Tier 1:**
- Most powerful models, largest context
- Cost: VERY HIGH (can be 10x-20x normal!)
- Use: <5% of the time, ONLY when truly stuck

### The Max Mode Trap:
**Max Mode feels amazing** but can cost $20-50 per extended session. Use it like a credit card in an emergency: rarely and with full awareness of cost.

---

## Real Example: Today's Session

**Task:** Recover from ChatGPT deleting entire codebase

| Action | Tier Used | Should Use | Savings |
|--------|-----------|------------|---------|
| Restore deleted files | 1 ✅ | 1 | $0 (correct - crisis!) |
| Organize Documents/ folder | 1 ❌ | 3 | $3 |
| Write TODO.md | 1 ❌ | 3 | $2 |
| Write cleanup doc | 1 ❌ | 3 | $1 |
| Strategic planning | 1 ✅ | 1 | $0 (correct - architecture) |

**Session cost:** ~$15  
**Optimized cost:** ~$9  
**Lesson:** Use Tier 1 for crisis/strategy, then switch to Tier 3 for execution

---

## Variations

### For Teams:
- Assign tier budgets per person
- Junior devs: More Tier 2/3, less Tier 1
- Senior devs: More Tier 1 for architecture
- Track team-wide spending

### For Agencies/Consultants:
- Bill clients based on tier used
- Tier 1 = premium rate, Tier 3 = standard rate
- Show cost savings from efficient tier usage

### For Projects with Deadlines:
- Temporarily increase Tier 1 budget during crunch
- Reduce Tier 3 work (docs can wait)
- Track "emergency tier overrides"

---

## Measuring Success

**After 1 month:**
- [ ] Did you stay under budget?
- [ ] Did quality suffer? (If yes, allocate more to higher tiers)
- [ ] Which tier was over/under used?
- [ ] Adjust tier % allocation

**After 3 months:**
- [ ] Are tier decisions becoming automatic?
- [ ] Have you reduced spend by 30-50%?
- [ ] Are you getting same results with lower cost?

---

## Related Patterns

- **Cost Tracking** (this enables informed tier decisions)
- **Token Budgeting** (more granular version of this pattern)
- **Model Selection** (choosing right tool for the job)

---

## Open Questions

1. **Can we automate tier detection?**
   - Could an AI analyze the task and suggest a tier?
   - Would that cost more than it saves?

2. **Should tier boundaries be dynamic?**
   - Adjust based on available budget remaining in cycle?
   - Higher tiers early in month, more conservative at end?

3. **How to handle "escalation mid-task"?**
   - Started in Tier 3, got stuck, need Tier 1
   - Track this as "escalation cost"?

4. **Team coordination:**
   - How do multiple people share a budget?
   - Who gets Tier 1 access when budget is low?

---

## Status

🟡 **Emerging Pattern** - Needs validation

**Next Steps:**
1. Test for 1 month (January 2026)
2. Track actual spend vs. budget by tier
3. Adjust tier % allocations based on reality
4. Validate formula (complexity + ambiguity + risk)
5. If successful: Promote to 🟢 Proven Pattern

---

## Why This Matters

**The insight:** Not all AI work is equal. Using a $0.015/1K token model for docs that a $0.0003/1K token model could do is burning 50x more money for the same output.

**The discipline:** Force yourself to ask "What's the right tool for THIS job?" instead of defaulting to "What's my favorite tool?"

**The result:** Work smarter, not poorer. Get 2-3x more done for the same budget by routing work appropriately.

---

*Pattern extracted from AI usage-billing tracker project after hitting $300 spend in 28 days*  
*Author: Claude Sonnet 4.5 (ironically, using Tier 1 to create a pattern about not over-using Tier 1!)*

