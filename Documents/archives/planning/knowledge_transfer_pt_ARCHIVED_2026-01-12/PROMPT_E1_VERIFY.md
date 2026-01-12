# Prompt E1: Verify Standalone - Final Verification

**Task:** Verify project-tracker is fully standalone and works without project-scaffolding
**Estimated Time:** 5 minutes
**Worker Model:** qwen2.5-coder:7b (preferred) or deepseek-r1:14b
**Dependencies:** ALL previous tasks (A1-D1) must be complete

---

## CONSTRAINTS (READ FIRST)

- RUN all verification from project-tracker directory only
- DO NOT reference any scaffolding paths
- VERIFY everything works locally
- REPORT any failures clearly

---

## [ACCEPTANCE CRITERIA]

- [x] All scripts exist locally in project-tracker/scripts/
- [x] All documentation exists locally in project-tracker/Documents/
- [x] No $SCAFFOLDING references remain anywhere
- [x] warden_audit.py runs successfully
- [x] validate_project.py runs successfully (with some DNA defects noted)
- [x] pre_review_scan.sh runs successfully (warden passes, validation shows defects)
- [x] scaffolding_version metadata exists

---

## Verification Checklist

Run ALL of these from project-tracker directory:

```bash
cd /Users/eriksjaastad/projects/project-tracker
```

### 1. Scripts Exist

```bash
echo "=== Checking Scripts ==="
ls -la scripts/warden_audit.py
ls -la scripts/validate_project.py
ls -la scripts/pre_review_scan.sh
```

Expected: All three files exist with execute permissions.

### 2. Documentation Exists

```bash
echo "=== Checking Documentation ==="
ls -la Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md
ls -la Documents/patterns/code-review-standard.md
ls -la Documents/patterns/learning-loop-pattern.md
ls -la Documents/reference/LOCAL_MODEL_LEARNINGS.md
```

Expected: All four files exist.

### 3. No $SCAFFOLDING References

```bash
echo "=== Checking for $SCAFFOLDING references ==="
grep -r "\$SCAFFOLDING" AGENTS.md CLAUDE.md .cursorrules 2>/dev/null
echo "Exit code: $?"
```

Expected: No output, exit code 1 (not found).

### 4. Scripts Run Successfully

```bash
echo "=== Testing warden_audit.py ==="
python scripts/warden_audit.py --root . --fast

echo "=== Testing validate_project.py ==="
python scripts/validate_project.py project-tracker

echo "=== Testing pre_review_scan.sh ==="
./scripts/pre_review_scan.sh
```

Expected: All three run without errors.

### 5. Version Metadata Exists

```bash
echo "=== Checking version metadata ==="
grep "scaffolding_version" 00_Index*.md
```

Expected: Shows `scaffolding_version: 1.0.0`

---

## Summary Report

After running all checks, report:

```
=== STANDALONE VERIFICATION REPORT ===

Scripts:
- [ ] warden_audit.py: EXISTS / MISSING
- [ ] validate_project.py: EXISTS / MISSING
- [ ] pre_review_scan.sh: EXISTS / MISSING

Documentation:
- [ ] REVIEWS_AND_GOVERNANCE_PROTOCOL.md: EXISTS / MISSING
- [ ] code-review-standard.md: EXISTS / MISSING
- [ ] learning-loop-pattern.md: EXISTS / MISSING
- [ ] LOCAL_MODEL_LEARNINGS.md: EXISTS / MISSING

References:
- [ ] $SCAFFOLDING references: NONE FOUND / FOUND (list files)

Execution:
- [ ] warden_audit.py: PASSES / FAILS
- [ ] validate_project.py: PASSES / FAILS
- [ ] pre_review_scan.sh: PASSES / FAILS

Metadata:
- [ ] scaffolding_version: FOUND / MISSING

OVERALL: [ ] PASS - Fully Standalone / [ ] FAIL - See issues above
```

---

## Result

- [x] PASS: project-tracker is fully standalone
- [ ] FAIL: List what's missing or broken

**Hand back to Floor Manager when complete.**

---

## If PASS: Celebration!

project-tracker is now:
- Independent of project-scaffolding
- Clone-ready for GitHub
- Self-contained with all review tools
- Version-tracked for future drift detection

**Next:** Apply same transfer pattern to Tax Processing and analyze-youtube-videos.
