# Pre-Commit Hook: Worker Task Prompts

**For Floor Manager Use**

> **Note:** This is our first test of the Learning Loop Pattern. Pay attention to whether the new prompt structure (Downstream Harm Estimate, Learnings Applied) improves outcomes.

---

## Task Overview

| Task | File | Est. | Objective |
|------|------|------|-----------|
| **1** | `PRE_COMMIT_PROMPT_1_HOOK_SCRIPT.md` | 10 min | Create pre-commit hook that runs Warden |

**Total:** ~10 minutes (single micro-task)

---

## Why This Task is a Good Test

1. **Small scope** - One file, clear requirements
2. **No file integration** - Creating new file, not modifying existing
3. **Clear pass/fail** - Either the hook runs or it doesn't
4. **Low risk** - If it fails, nothing breaks

---

## Floor Manager Instructions

1. **This is a [learning-loop-pattern](../../../../writing/Documents/patterns/learning-loop-pattern.md) test** - Pay extra attention to whether the new prompt sections help
2. **Use the new template structure** - Prompt includes Downstream Harm Estimate and Learnings Applied
3. **After completion (success or failure):** Document in [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md)
4. **If failure:** Ask "Was this preventable?" and update Learning Debt Tracker if applicable

---

## Context Files Workers May Need

- `scripts/warden_audit.py` (the script the hook will call). See [REVIEWS_AND_GOVERNANCE_PROTOCOL](../../../REVIEWS_AND_GOVERNANCE_PROTOCOL.md).
- Existing `.git/hooks/` directory structure. See [PROJECT_STRUCTURE_STANDARDS](../../PROJECT_STRUCTURE_STANDARDS.md).

---

## Related Documentation
- [learning-loop-pattern](../../../../writing/Documents/patterns/learning-loop-pattern.md) - Pattern for autonomous learning.
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - Institutional memory for local models.
- [PRE_COMMIT_PROMPT_1_HOOK_SCRIPT](PRE_COMMIT_PROMPT_1_HOOK_SCRIPT.md) - The actual worker prompt.

---

- [Tiered AI Sprint Planning](patterns/tiered-ai-sprint-planning.md) - prompt engineering
## Final Verification

```bash
# 1. Hook file exists and is executable
ls -la .git/hooks/pre-commit
# Expected: -rwxr-xr-x

# 2. Hook runs successfully on clean repo
.git/hooks/pre-commit
# Expected: Exit 0, shows warden output

# 3. Hook blocks on violation (test with temp bad file)
echo "os.remove('test')" > /tmp/test_bad.py
cp /tmp/test_bad.py ./test_bad.py
git add test_bad.py
git commit -m "test"
# Expected: Commit blocked, warden shows P0 violation
trash test_bad.py
```

---

**Ready to hand off to Workers**

- [learning-loop-pattern](../../../../writing/Documents/patterns/learning-loop-pattern.md) - Pattern for autonomous learning.
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - Institutional memory for local models.
- [PRE_COMMIT_PROMPT_1_HOOK_SCRIPT](PRE_COMMIT_PROMPT_1_HOOK_SCRIPT.md) - The actual worker prompt.

---

## Final Verification

```bash
# 1. Hook file exists and is executable
ls -la .git/hooks/pre-commit
# Expected: -rwxr-xr-x

# 2. Hook runs successfully on clean repo
.git/hooks/pre-commit
# Expected: Exit 0, shows warden output

# 3. Hook blocks on violation (test with temp bad file)
echo "os.remove('test')" > /tmp/test_bad.py
cp /tmp/test_bad.py ./test_bad.py
git add test_bad.py
git commit -m "test"
# Expected: Commit blocked, warden shows P0 violation
trash test_bad.py
```

---

**Ready to hand off to Workers**
