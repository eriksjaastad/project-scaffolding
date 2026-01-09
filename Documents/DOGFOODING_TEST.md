# Dogfooding Test: project-tracker

**Date:** December 23, 2025  
**Goal:** Use scaffolding to set up project-tracker and validate the system works

---

## Test Plan

### 1. Copy Templates
- [ ] Copy `.specs/steering/` templates
- [ ] Copy `.cursorrules.template`
- [ ] Customize for project-tracker

### 2. Generate Specs
- [ ] Create specs for "CLI status command"
- [ ] Review generated requirements, design, tasks
- [ ] Measure: time to generate, quality of output

### 3. Run Multi-AI Review
- [ ] Review the generated design doc
- [ ] Use DeepSeek + Ollama
- [ ] Measure: cost, time, quality

### 4. Track Actual Costs
- [ ] Create `logs/cost-tracking.jsonl`
- [ ] Log each API call
- [ ] Compare estimates vs. actuals

---

## Results

### Template Copy
**Time:** 
**Issues found:** 
**Customization needed:** 

### Spec Generation
**Command:**
```bash
# Manual spec creation or use AI to generate
# Create specs in Documents/specs/cli-status/
```

**Time to generate:** 
**Files created:** 
**Quality:** 
**Usable without editing?** 

### Multi-AI Review
**Command:**
```bash
python scaffold_cli.py review \
    --type document \
    --input $PROJECTS_ROOT/project-tracker/.specs/specs/cli-status/design.md \
    --round 1
```

**Cost:** 
**Time:** 
**Quality:** 
**Issues caught:** 

---

## Lessons Learned

**What worked:**
- 

**What didn't:**
- 

**What to fix:**
- 

---

## Next Steps

Based on this test:
- [ ] Fix issues found
- [ ] Update templates
- [ ] Update scaffolding docs
- [ ] Ready for real use

