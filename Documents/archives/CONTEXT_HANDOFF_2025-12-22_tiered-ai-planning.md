# Context Handoff: Tiered AI Sprint Planning Implementation

**Date:** December 22, 2025  
**From:** Claude Sonnet 4.5 (AI usage-billing tracker context)  
**To:** Next AI assistant in project-scaffolding context  
**Session:** Billing crisis → Pattern extraction → Cross-project setup

---

## What Just Happened

### The Crisis (Dec 22, Late Evening)
- Erik hit **86% of Cursor budget** ($172/$200) with 1 day left in billing cycle
- Already spent **$31.36 of $100 overage buffer**
- Total spend: **~$203** in 28 days (on track for $300/month)
- Root cause: Using Tier 1 models (Claude Sonnet 4.5, Cursor Max Mode) for EVERYTHING

### The Solution We Built
1. ✅ Created **tiered AI sprint planning pattern** (in this project)
2. ✅ Moved it from `AI usage-billing tracker` to `project-scaffolding/patterns/`
3. ✅ Made it universal across all Erik's projects
4. ✅ Updated `.cursorrules` in billing tracker to reference it

### Current Status
- Pattern document: `$PROJECTS_ROOT/project-scaffolding/patterns/tiered-ai-sprint-planning.md` ✅
- Status: 🟡 Emerging (needs 1 month validation)
- Next test cycle: Jan 23 - Feb 23, 2026

---

## What We Learned Tonight

### Discovery 1: BYOK Testing (FAILED)
**Test:** Enabled Cursor's "Bring Your Own Keys" (BYOK) feature
- Added OpenAI key to Cursor settings
- Added Anthropic key to Cursor settings
- **Result:** Cursor completely broke (couldn't send messages)
- **Fix:** Disabled keys, everything worked again

**Why it failed (theories):**
- Invalid/expired keys
- Missing permissions/scopes
- Rate limits hit immediately
- Wrong base URL override
- Cursor doesn't actually want BYOK usage

**Conclusion:** BYOK is NOT a reliable solution for tracking. Abandon this approach.

### Discovery 2: Erik's Real Backup Plan
When Cursor budget runs out, Erik has:
- ✅ **Google IDX** (Anti-Gravity) - Free tier
- ✅ **Amazon Kiro IDE** - Free tier (3-panel planning model)
- Strategy: Switch IDEs for rest of month (Erik calls this "protest mode" 😄)

**Our take:** It's low-tech but it WORKS. Sometimes that's the answer.

### Discovery 3: The Real Problem Isn't Pricing
Erik's frustration quote:
> "Cursor is a technology company, and I should have access to my data how I choose. I should be able to get my billing data by API."

**The actual protest-worthy issue:** Lack of data access, not cost.

---

## Key Decisions Made

### ✅ DECIDED: Drop Token Tracking Deep Dive (For Now)
We were planning to:
- Research where tokens are exposed in Cursor
- Design real-time cost tracking system
- Automate switching API keys at 80% usage

**Why we stopped:**
- BYOK broke Cursor completely
- Billing resets tomorrow (Dec 23)
- Not a crisis for THIS cycle
- Real solution = use cheaper models more often (tiered planning)

### ✅ DECIDED: Focus on Tiered AI Workflow
Instead of fighting Cursor's system, work WITH it:
- Use GPT-4o-mini (Tier 3) for 30% of work → save 95% on costs
- Use GPT-4o (Tier 2) for 50% of work → save 40% on costs
- Use Claude Sonnet 4.5 (Tier 1) for 20% of work → only when truly needed

**Expected result:** Stay under $200/month without switching IDEs.

### ✅ DECIDED: Validate Pattern in January
- Test cycle: Jan 23 - Feb 23, 2026
- Track actual spend by tier
- Adjust % allocations based on reality
- If successful → promote from 🟡 Emerging to 🟢 Proven

---

## What Needs to Happen Next (In This Project)

### Immediate (Next Session):
1. **Set up tier workflow documentation**
   - Create quick-reference guide: "Which tier for this task?"
   - Make it dead simple to choose (flowchart?)
   - Add to Erik's daily workflow

2. **Create tracking template**
   - Daily spend log (optional but helpful)
   - Weekly review checklist
   - Month-end analysis template

### Short-term (This Week):
3. **Test Tier 3 model for real tasks**
   - Erik needs to TRY using GPT-4o-mini for simple stuff
   - Build muscle memory for "Tier 3 first, escalate if stuck"

4. **Configure Cursor defaults**
   - Set default chat model to GPT-4o-mini (Tier 3)
   - Document when to manually switch to Tier 2/1

### Long-term (January):
5. **Validate the pattern**
   - Did Erik stay under $200?
   - Which tier allocations worked? (20/50/30 starting point)
   - Update pattern doc with learnings

6. **Cross-project adoption**
   - Add tiered planning to other project `.cursorrules`
   - Make it automatic across all Erik's work

---

## Files Modified Tonight

### In `project-scaffolding`:
- ✅ Created: `patterns/tiered-ai-sprint-planning.md` (full pattern doc)
- ✅ **Creating now:** `Documents/CONTEXT_HANDOFF_2025-12-22_tiered-ai-planning.md` (this file)

### In `AI usage-billing tracker`:
- ✅ Updated: `.cursorrules` (added reference to tiered planning)
- ✅ Organized: Moved docs to `Documents/`, billing_app to `integrations/`
- ✅ Recovered: Restored entire codebase after ChatGPT deletion (Dec 14)

---

## Erik's Project Philosophy (Context)

From `$PROJECTS_ROOT/Trading Projects/PROJECT_PHILOSOPHY.md`:
- **Explorer mindset:** Building experiments, not products
- **Two-level game:** Domain patterns + meta patterns (scaffolding)
- **Consolidate on 3rd duplicate:** Don't abstract until you see the pattern 3 times
- **Data first, evaluate after 30-60 days**

**This tiered AI planning is a META PATTERN** - applies across ALL projects.

---

## Known Issues / Open Questions

### Q1: Can tier selection be automated?
- Could an AI analyze the task description and suggest a tier?
- Would the cost of that analysis exceed the savings?
- Needs experimentation.

### Q2: Should tier budgets be dynamic?
- More aggressive with Tier 1 early in month?
- More conservative as you approach budget limit?
- Current plan: Static 20/50/30, adjust after validation.

### Q3: How to handle mid-task escalation?
- Start in Tier 3, get stuck, need Tier 1
- Track this as "escalation cost"?
- When is it better to restart with Tier 1 vs. continue escalating?

### Q4: BYOK - try again or give up?
- Test with fresh API keys (current ones might be invalid)
- Test one provider at a time (OpenAI only, then Anthropic only)
- Check if "Override Base URL" should be empty
- Or: Accept it's unreliable and move on

**Erik's position:** Move on. Use tiered planning instead. (Smart.)

---

## What Erik Is Doing Right Now

Quote from handoff request:
> "I think I might actually look up that there's a video of Rage Against The Machine when they're like barely in college or something. They look like little kids, and they're in a record store, and they have a concert in a record store."

**Translation:** Taking a break from billing crisis stress. Solid plan. 🎸

---

## Tone & Approach for Next AI

Erik is:
- ✅ **Collaborative:** Wants to be involved in decisions
- ✅ **Pragmatic:** Will take "low-tech but works" over "high-tech but broken"
- ✅ **Curious:** Loves diving deep into problems (sometimes too deep!)
- ⚠️ **Budget-conscious:** $200/month is a real constraint
- 🔥 **Frustrated with Cursor:** Not about pricing, about data access

**Best approach:**
1. Present options, let Erik choose
2. Explain tradeoffs clearly
3. Don't over-engineer if simple works
4. Validate "protest mode" feelings (they're valid!)
5. Keep him from rabbit holes when budget is tight

---

## Quick Reference: The Tiered System

```
TIER 1 (20% budget) - Claude Sonnet 4.5, GPT-4, Cursor Max Mode
→ Architecture, complex debugging, strategy, crisis recovery
→ $3-15 per million input tokens

TIER 2 (50% budget) - GPT-4o, Claude Haiku, Cursor Agent/Composer
→ Feature implementation, refactoring, testing, medium bugs
→ $2.50-5 per million input tokens

TIER 3 (30% budget) - GPT-4o-mini, GPT-3.5, Cursor Normal Mode
→ Boilerplate, docs, file cleanup, CSV parsing, simple CRUD
→ $0.15-0.50 per million input tokens
```

**Decision formula:**
```
Score = (Complexity + Ambiguity + Risk) / 3
  1-3 → Tier 3
  4-7 → Tier 2
  8-10 → Tier 1
```

**Default to Tier 3. Escalate only when stuck.**

---

## Related Projects

- **AI usage-billing tracker:** Where this pattern was born (billing crisis recovery)
- **Trading Projects:** Home of PROJECT_PHILOSOPHY.md (Erik's core principles)
- **AI Journal:** Where all sessions are logged (UTC timestamps, full model names)

---

## Git Status (As of Handoff)

### `project-scaffolding`:
- Last commit: (check `git log`)
- Uncommitted: This handoff doc (you'll need to commit it)
- Branch: Probably `main`

### `AI usage-billing tracker`:
- Last commit: Updated .cursorrules with tiered planning reference
- All changes committed ✅
- Dashboard running on port 8001 (might still be background process)

---

## Next AI: Your Mission

1. **Read this handoff** (you're doing it! 👍)
2. **Read the pattern doc:** `patterns/tiered-ai-sprint-planning.md`
3. **Help Erik set up the workflow:**
   - Make tier selection EASY and FAST
   - Create simple decision aids (flowchart, quick ref)
   - Get him practicing with Tier 3 models
4. **Track progress in January:**
   - Did he stay under $200?
   - Which tiers got over/under used?
   - Adjust the pattern based on reality
5. **Promote to proven pattern if successful:**
   - Change status from 🟡 Emerging to 🟢 Proven
   - Add real usage data to doc
   - Spread to all Erik's projects

---

## Parting Wisdom

**From tonight's session:**

> "Sometimes the low-tech solution (switching IDEs) beats the high-tech one (BYOK automation). And that's okay."

**The real win:** Not fighting Cursor's system, but using cheaper models strategically. That's the sustainable solution.

**Erik's closing vibe:** "Thelma and Louise" energy (ride or die with Claude Sonnet 4.5), but ready to be pragmatic and use Tier 3 more.

---

**End of handoff. Good luck! 🚀**

*- Claude Sonnet 4.5, signing off from AI usage-billing tracker context*  
*Dec 22, 2025, 11:47 PM Pacific*

