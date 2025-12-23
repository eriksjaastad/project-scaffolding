# Dogfooding Test: project-tracker

**Date:** December 23, 2025  
**Goal:** Use scaffolding to set up project-tracker and validate the system works

---

## Test Plan

### 1. Copy Templates
- [ ] Copy `.kiro/steering/` templates
- [ ] Copy `.cursorrules.template`
- [ ] Customize for project-tracker

### 2. Generate Kiro Specs
- [ ] Use `scripts/generate_kiro_specs.py` to create specs for "CLI status command"
- [ ] Review generated requirements, design, tasks
- [ ] Measure: time to generate, quality of output

### 3. Run Multi-AI Review
- [ ] Review the generated design doc
- [ ] Use DeepSeek + Kiro
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

### Kiro Spec Generation
**Command:**
```bash
python scripts/generate_kiro_specs.py \
    --project-root /Users/eriksjaastad/projects/project-tracker \
    --feature-name cli-status \
    --description "CLI command to show project status dashboard"
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
    --input /Users/eriksjaastad/projects/project-tracker/.kiro/specs/cli-status/design.md \
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

