# Claude Code CLI Review Recommendations

**Date:** 2026-01-06
**Author:** Claude Code CLI (Terminal)
**Context:** Post-mortem analysis of failed A+ review that missed critical template issues
**Status:** Living Document - Update as patterns emerge

---

## Executive Summary

**The Problem:** Gave project-scaffolding an A+ rating while missing 45+ hardcoded paths in templates that would propagate to 30 downstream projects. The "be grumpy" approach failed because **personality isn't process**.

**The Solution:** Replace subjective reviewing with systematic checklists + automated pre-review scans that catch common issues before human/AI review begins.

**Key Insight:** Templates have the highest blast radius in a scaffolding project. They must be checked FIRST, not last.

---

## What Went Wrong: The Failed A+ Review

### My Blind Spots

1. **Tunnel Vision on Scripts**
   - Focused on `scripts/*.py` because that's what Reviews #1-2 flagged
   - Never expanded scope to `templates/`, `.cursorrules`, config files
   - Assumed if `test_scripts_follow_standards.py` passed, everything was clean

2. **False Test Confidence**
   - Test explicitly checks `scripts/` directory only
   - Never questioned: "What does this test NOT check?"
   - Trusted passing tests without verifying their scope

3. **No Blast Radius Analysis**
   - Never asked: "Which files propagate to other projects?"
   - Templates are THE infection vector - should have been Priority #1
   - Treated all files as equally important (they're not)

4. **Checklist Blindness**
   - Had no systematic list of "must check" items
   - Relied on memory and intuition
   - Easy to skip entire categories of files

### The Result

- **7 hardcoded paths in `.cursorrules-template`** → Would copy to every new project
- **Silent failures in `warden_audit.py`** → CI reports success while failing
- **Deprecated Pydantic validators** → Technical debt from day one
- **Grade:** B (should have been) vs A+ (what I gave)

---

## The New Review System: Checklist + Automation

### Philosophy Shift

**OLD:** "Be grumpy" (subjective, unreliable)
**NEW:** "Execute the protocol" (systematic, repeatable)

**OLD:** One big review pass
**NEW:** Multi-pass with blast radius prioritization

**OLD:** Trust tests when they pass
**NEW:** Ask "what do tests NOT check?"

### Two-Layer Defense

**Layer 1: Automated Pre-Review Scan** (catches mechanical issues)
**Layer 2: Human/AI Checklist Review** (catches architectural issues)

---

## Layer 1: Automated Pre-Review Scan

### Purpose

Catch **common, detectable anti-patterns** before human/AI review. These are mechanical checks that don't require judgment.

### Implementation: `scripts/pre_review_scan.sh`

```bash
#!/bin/bash
# Mandatory pre-review scan for project-scaffolding
# Run this BEFORE any human/AI code review
# Exit code 1 = review must address failures

set -e

FAILED=0

echo "=================================="
echo "🔍 PRE-REVIEW SCAN - Project Scaffolding"
echo "=================================="
echo ""

# ============================================================
# TIER 1: BLAST RADIUS CHECKS (Propagation Sources)
# These have highest impact - they infect downstream projects
# ============================================================

echo "📋 TIER 1: BLAST RADIUS (Templates & Configs)"
echo "--------------------------------------------------"

echo -n "  [1.1] Checking templates/ for hardcoded paths... "
if grep -rn "/Users/" templates/ 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [1.2] Checking .cursorrules* for hardcoded paths... "
if grep -n "/Users/" .cursorrules* 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [1.3] Checking YAML files for hardcoded paths... "
if grep -rn "/Users/" *.yaml 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [1.4] Checking AGENTS.md for hardcoded paths... "
if grep -n "/Users/" AGENTS.md CLAUDE.md 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo ""

# ============================================================
# TIER 2: SECURITY & SAFETY
# ============================================================

echo "🔒 TIER 2: SECURITY & SAFETY"
echo "--------------------------------------------------"

echo -n "  [2.1] Checking for hardcoded API keys (sk-...)... "
if grep -rE "sk-[a-zA-Z0-9]{32,}" scripts/ scaffold/ templates/ 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [2.2] Checking for silent exception swallowing... "
if grep -rn "except.*:$" scripts/ scaffold/ 2>/dev/null | grep -v "# noqa" | grep "pass"; then
    echo "❌ FAIL (found 'except: pass')"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [2.3] Checking .env is gitignored... "
if git check-ignore .env >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
    FAILED=1
fi

echo ""

# ============================================================
# TIER 3: DEPENDENCY SAFETY
# ============================================================

echo "📦 TIER 3: DEPENDENCY SAFETY"
echo "--------------------------------------------------"

echo -n "  [3.1] Checking for unpinned dependencies (>=)... "
if grep -E "^[^#].*>=" requirements.txt 2>/dev/null; then
    echo "❌ FAIL (found >= without upper bound)"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [3.2] Checking anthropic version boundary... "
if grep -E "anthropic~=0\.[0-9]+" requirements.txt 2>/dev/null; then
    echo "⚠️  WARN (0.x -> 1.x was breaking change)"
    # Don't fail, just warn
else
    echo "✅ PASS"
fi

echo ""

# ============================================================
# TIER 4: CODE QUALITY
# ============================================================

echo "✨ TIER 4: CODE QUALITY"
echo "--------------------------------------------------"

echo -n "  [4.1] Checking for functions without type hints... "
# Simple check: functions with 'def ' but no '->'
UNTYPED=$(find scripts/ scaffold/ -name "*.py" -exec grep -l "^def " {} \; 2>/dev/null | \
    xargs grep "^def " 2>/dev/null | grep -v " -> " | wc -l)
if [ "$UNTYPED" -gt 0 ]; then
    echo "⚠️  WARN ($UNTYPED functions without return type)"
    # Don't fail, just warn
else
    echo "✅ PASS"
fi

echo ""

# ============================================================
# RESULTS
# ============================================================

echo "=================================="
if [ $FAILED -eq 0 ]; then
    echo "✅ PRE-REVIEW SCAN PASSED"
    echo "   Safe to proceed with human/AI review"
    exit 0
else
    echo "❌ PRE-REVIEW SCAN FAILED"
    echo "   Fix failures before requesting review"
    exit 1
fi
```

### Usage

**Before ANY code review:**
```bash
# Step 1: Run pre-review scan
./scripts/pre_review_scan.sh

# Step 2: If failures, fix them
# Step 3: Re-run scan until clean
# Step 4: THEN request human/AI review
```

**In CI/CD:**
```yaml
# GitHub Actions, Railway, etc.
- name: Pre-Review Scan
  run: |
    chmod +x scripts/pre_review_scan.sh
    ./scripts/pre_review_scan.sh
```

### What It Catches

- ✅ Hardcoded paths in templates (my biggest miss)
- ✅ Hardcoded paths in configs (.cursorrules)
- ✅ API keys in code
- ✅ Silent exception swallowing
- ✅ Unpinned dependencies
- ✅ .env not gitignored

### What It Doesn't Catch (needs human review)

- Architectural issues
- Logic bugs
- Complexity problems
- Documentation quality
- Test coverage gaps

---

## Layer 2: Human/AI Review Checklist

### Purpose

Catch **architectural and judgment issues** that automation can't detect. This is where human/AI review adds value.

### The Blast Radius Prioritization Framework

**Files are NOT equal. Check in this order:**

#### Tier 1: Propagation Sources (HIGHEST PRIORITY)
These files **copy to or influence** downstream projects.

**Must check FIRST:**
- [ ] All files in `templates/` directory
  - [ ] `.cursorrules.template`
  - [ ] `CLAUDE.md.template`
  - [ ] `AGENTS.md.template`
  - [ ] `TODO.md.template`
  - [ ] `.cursorignore.template`
  - [ ] Any other .template files

- [ ] Root-level config files that get referenced:
  - [ ] `AGENTS.md` (referenced by all projects)
  - [ ] `CLAUDE.md` (if exists at root)
  - [ ] `.cursorrules` (copied to new projects)
  - [ ] `.cursorignore` (copied to new projects)

- [ ] Data files used by other projects:
  - [ ] `EXTERNAL_RESOURCES.yaml`
  - [ ] Any other YAML/JSON data files

**Why First:** If these are broken, **every downstream project inherits the defect**. 10x blast radius.

#### Tier 2: Execution Critical
These files run automation that affects all projects.

**Check second:**
- [ ] All scripts in `scripts/`
  - [ ] Type hints on all functions
  - [ ] Proper error handling (no silent failures)
  - [ ] No hardcoded paths
  - [ ] No hardcoded secrets

- [ ] All modules in `scaffold/`
  - [ ] Same standards as scripts
  - [ ] Async error handling (if applicable)
  - [ ] Retry logic for external calls

- [ ] Governance files:
  - [ ] `.git/hooks/pre-commit`
  - [ ] Test files in `tests/`
  - [ ] CI/CD configs (if exists)

**Why Second:** These affect operations but don't propagate patterns to other projects.

#### Tier 3: Documentation
Important but lowest blast radius.

**Check last:**
- [ ] README.md
- [ ] docs/ directory
- [ ] patterns/ directory
- [ ] Any .md files

**Why Last:** Documentation bugs don't break systems. Fix these after Tier 1 & 2 are clean.

### The "Inverse Test" Technique

For every test that passes, ask:

**"What does this test NOT check?"**

Example:
```
Test: test_no_hardcoded_paths()
Checks: scripts/ directory
INVERSE QUESTION: What directories does it NOT check?
ANSWER: templates/, configs, root files
ACTION: Expand test OR manually verify those areas
```

This forces systematic gap analysis.

### The "Meta-Review" Questions

After completing review, ask yourself:

- [ ] Did I check ALL files in `templates/`?
- [ ] Did I verify what each passing test actually covers?
- [ ] Did I check `.cursorrules*` files?
- [ ] Did I scan YAML files for hardcoded paths?
- [ ] Did I check for deprecated API usage (Pydantic, etc.)?
- [ ] Did I verify error handling doesn't swallow exceptions?
- [ ] Did I check if dependency versions are safe?

If ANY answer is "no" or "not sure" → Review is incomplete.

---

## Review Checklist Template

Use this for EVERY review of project-scaffolding:

```markdown
# Code Review Checklist - Project Scaffolding

**Date:** YYYY-MM-DD
**Reviewer:** [Name/Model]
**Pre-Review Scan:** ✅ PASSED / ❌ FAILED

---

## TIER 1: PROPAGATION SOURCES (Must Check First)

### Templates (Highest Blast Radius)
- [ ] `templates/.cursorrules.template` - No hardcoded paths
- [ ] `templates/CLAUDE.md.template` - No hardcoded paths
- [ ] `templates/AGENTS.md.template` - No hardcoded paths
- [ ] `templates/TODO.md.template` - No hardcoded paths
- [ ] `templates/*.template` - All other templates checked

### Root Configs (Referenced by Projects)
- [ ] `AGENTS.md` - No hardcoded paths, accurate constraints
- [ ] `.cursorrules` - No hardcoded paths
- [ ] `.cursorignore` - Appropriate exclusions

### Data Files (Used by Scripts)
- [ ] `EXTERNAL_RESOURCES.yaml` - No hardcoded paths
- [ ] Schema validation script works
- [ ] Data structure is sound

**Tier 1 Grade:** ✅ PASS / ❌ FAIL
**If FAIL, stop here and fix before continuing**

---

## TIER 2: EXECUTION CRITICAL

### Scripts (scripts/)
- [ ] All functions have type hints
- [ ] No `except: pass` or silent failures
- [ ] Error handling returns status codes
- [ ] No hardcoded paths (verified by scan)
- [ ] No hardcoded secrets (verified by scan)

### Modules (scaffold/)
- [ ] Same standards as scripts
- [ ] Async error handling correct (if applicable)
- [ ] Retry logic present for external calls

### Governance
- [ ] `.git/hooks/pre-commit` is executable
- [ ] Test suite covers expected scope
- [ ] Tests actually pass (not just claimed)

**Tier 2 Grade:** ✅ PASS / ❌ FAIL

---

## TIER 3: DOCUMENTATION

### Core Docs
- [ ] README.md is accurate
- [ ] Standards docs are current
- [ ] Pattern docs have scar stories

### Consistency
- [ ] Docs don't contradict code
- [ ] Examples are runnable
- [ ] Links aren't broken

**Tier 3 Grade:** ✅ PASS / ❌ FAIL

---

## INVERSE TEST ANALYSIS

For each passing test, document what it DOESN'T check:

**Test:** `test_no_hardcoded_paths()`
- **Checks:** `scripts/` only
- **Doesn't Check:** `templates/`, configs, YAML files
- **Action Taken:** [Manual verification / Expanded test / Accepted risk]

**Test:** `test_scripts_have_type_hints()`
- **Checks:** `scripts/` only
- **Doesn't Check:** `scaffold/` modules
- **Action Taken:** [...]

---

## META-REVIEW

- [ ] Checked ALL files in templates/
- [ ] Verified test scope matches claims
- [ ] Scanned for deprecated APIs
- [ ] Verified dependency safety
- [ ] Checked exception handling
- [ ] No assumptions without verification

---

## FINAL GRADE & BLOCKERS

**Overall Grade:** [A+ / A / A- / B / C / D / F]

**Ship Blockers (Must Fix):**
1. [Issue and location]
2. [Issue and location]

**Recommended Fixes (Nice to Have):**
1. [Issue and location]

**Confidence Level:** [High / Medium / Low]
- High = Checked everything systematically
- Medium = Some assumptions made
- Low = Possible blind spots remain

**Ready to Propagate:** ✅ YES / ❌ NO
```

---

## Common Anti-Patterns Database

Maintain this list and scan for these EVERY review:

### Anti-Pattern #1: Hardcoded Absolute Paths

**What:** `/Users/eriksjaastad/...` or similar machine-specific paths

**Where to Look:**
- templates/*.template files
- .cursorrules*
- *.yaml files
- Scripts (scripts/, scaffold/)
- AGENTS.md, CLAUDE.md

**Scan Command:**
```bash
grep -rn "/Users/" templates/ .cursorrules* *.yaml scripts/ scaffold/ AGENTS.md CLAUDE.md
```

**Fix:**
- Use `Path.home() / "projects"`
- Use `os.getenv("PROJECTS_ROOT")`
- Use relative paths via `Path(__file__).parent`

---

### Anti-Pattern #2: Silent Exception Swallowing

**What:** `except: pass` or `except Exception: pass` without logging/re-raising

**Where to Look:**
- All Python files
- Especially in cleanup code or non-critical paths

**Scan Command:**
```bash
grep -rn "except.*:" scripts/ scaffold/ | grep "pass"
```

**Fix:**
- Log the error
- Return error status
- Re-raise if can't handle
- Document why silence is acceptable (rare)

---

### Anti-Pattern #3: Unpinned Dependencies

**What:** Using `>=` without upper bound

**Where to Look:**
- requirements.txt

**Scan Command:**
```bash
grep -E "^[^#].*>=" requirements.txt
```

**Fix:**
- Use `~=` for compatible releases
- Add upper bounds for major versions
- Pin exact versions in requirements.lock

---

### Anti-Pattern #4: Test Scope Mismatch

**What:** Test claims to check X but only checks subset of X

**Where to Look:**
- Test file names vs what they actually check
- Docstrings vs implementation

**Detection:**
- Read test code, verify scope matches name/docstring
- Ask "what does this NOT check?"

**Fix:**
- Expand test scope OR
- Rename test to match actual scope OR
- Add companion tests for unchecked areas

---

### Anti-Pattern #5: Deprecated API Usage

**What:** Using old APIs that have replacements (Pydantic `validator` → `field_validator`)

**Where to Look:**
- Import statements
- Decorator usage

**Detection:**
- Check library changelogs for deprecated features
- Look for deprecation warnings in test output

**Fix:**
- Upgrade to current API
- Add TODO if breaking change requires more work

---

## Integration with Scaffolding Workflow

### For New Projects

When creating a new project from templates:

1. **Before copying templates:**
   ```bash
   cd project-scaffolding
   ./scripts/pre_review_scan.sh
   ```

2. **Copy templates only if scan passes**

3. **After copying, verify new project:**
   ```bash
   cd new-project
   grep -rn "/Users/" .
   ```

### For Scaffolding Updates

When updating project-scaffolding itself:

1. **Run pre-review scan:**
   ```bash
   ./scripts/pre_review_scan.sh
   ```

2. **Fix any failures**

3. **Request human/AI review using checklist**

4. **Run meta-review before finalizing grade**

### For Downstream Projects

When auditing a project that used scaffolding:

1. **Check which template version it used:**
   - Look for template source comments
   - Check git history

2. **If old templates, check for inherited issues:**
   - Hardcoded paths from old `.cursorrules`
   - Deprecated patterns from old templates

3. **Upgrade path:**
   - Re-copy from current templates
   - Verify no regressions

---

## Lessons Learned: Why "Be Grumpy" Failed

### What Didn't Work

**"Be grumpy"** = Personality directive
- Subjective
- Hard to replicate
- Depends on mood/energy
- No guarantee of consistency
- Easy to have blind spots

**Result:** I was grumpy about scripts but never looked at templates. Grumpiness without scope = incomplete review.

### What Does Work

**"Execute the protocol"** = Process directive
- Objective checklist
- Same every time
- Works regardless of mood
- Systematic coverage
- Forces gap analysis

**Result:** Can't skip templates when they're #1 on the checklist.

### The Mental Model

**BAD:** "Try harder to find issues"
- Relies on effort/intuition
- No structure
- Random walk through codebase

**GOOD:** "Follow the checklist, run the scans"
- Structured approach
- Blast radius prioritization
- Automation catches mechanical issues
- Human/AI catches judgment issues

---

## Recommendations for Other Scaffolding Projects

If you're building scaffolding for other domains (not just project setup):

### 1. Identify Your "Templates"

**Question:** What files/patterns propagate from this project to others?

Those are your Tier 1 files. Check them first, always.

### 2. Build Your Anti-Pattern Database

**Question:** What mistakes have already happened in this project or similar ones?

Turn each mistake into a scannable pattern.

### 3. Write the Pre-Review Scan

Automate detection of your top 5 anti-patterns.

### 4. Create the Review Checklist

Based on blast radius of your specific project.

### 5. Test the Process

Have someone else follow your checklist. Do they catch what you catch?

---

## Future Enhancements

### Phase 2: Template Linting

Build a dedicated template linter:

```bash
scripts/lint_templates.sh

# Checks:
# - No hardcoded paths in any .template file
# - No secrets in templates
# - All template placeholders are documented
# - Templates follow current best practices
```

### Phase 3: Dependency Drift Detection

Automated check for breaking major version changes:

```python
# scripts/check_dependency_safety.py
# For each dependency:
# - Check if ~= range crosses major version boundary
# - Warn if so
# - Suggest safer range
```

### Phase 4: Review Quality Metrics

Track review effectiveness:

```
Reviews conducted: 10
Issues caught by pre-scan: 45
Issues caught by human review: 12
Issues missed (found later): 3

Scan effectiveness: 78%
Review effectiveness: 80%
Miss rate: 7%
```

Use metrics to improve scan + checklist.

---

## Conclusion: From Grumpy to Systematic

**The Failure:** Gave A+ while missing 45+ critical issues in templates.

**The Root Cause:** No systematic process. Relied on "being thorough" without defining what thorough means.

**The Solution:**
1. Automated pre-review scan (catches mechanical issues)
2. Blast-radius-prioritized checklist (ensures complete coverage)
3. Inverse test analysis (finds gaps)
4. Meta-review (validates the review itself)

**The Result:** Repeatable, reliable reviews that don't depend on mood or personality.

---

## Appendix: Quick Reference

### Before Every Review

```bash
# 1. Run pre-review scan
./scripts/pre_review_scan.sh

# 2. If it passes, start checklist review
# 3. Check Tier 1 (templates) FIRST
# 4. Then Tier 2 (scripts), then Tier 3 (docs)
# 5. Run inverse test analysis
# 6. Complete meta-review
# 7. Assign grade based on blockers
```

### Grade Scale (Revised)

- **A+** = Zero issues, all tiers clean, ready to propagate
- **A**  = Minor polish items, safe to ship
- **A-** = A few nice-to-haves, ship with caution
- **B**  = Architectural debt, needs focused work
- **C**  = Multiple critical issues, don't propagate
- **D**  = Systemic problems, needs major refactor
- **F**  = Unsafe to use

**Key:** Grade reflects WORST issue found, not average.

---

**Living Document:** Update this as new anti-patterns emerge or review process improves.

**Last Updated:** 2026-01-06 (Post failed A+ review)
**Next Review:** After next major scaffolding update
