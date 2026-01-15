# Global Rules Injection: Worker Task Prompts

**For Floor Manager Use**

Hand off these prompts to Workers **in order** (each builds on the previous).

> **UPDATE Jan 10, 2026:** Task 1 has been decomposed into micro-tasks (1a-1d) after DeepSeek-R1 timeout issues. See `LOCAL_MODEL_LEARNINGS.md` for pattern details.

---

## Task Order

### Phase 1: Core Foundation (Micro-Tasks)

Task 1 was decomposed into 4 atomic micro-tasks after timeout issues with DeepSeek-R1.

| Task | File | Est. | Objective |
|------|------|------|-----------|
| **1a** | `GLOBAL_RULES_PROMPT_1a_SKELETON.md` | 5 min | File skeleton with imports and argparse |
| **1b** | `GLOBAL_RULES_PROMPT_1b_SCANNER.md` | 5 min | Add find_cursorrules_files() function |
| **1c** | `GLOBAL_RULES_PROMPT_1c_DETECTION.md` | 5 min | Add check_compliance() function |
| **1d** | `GLOBAL_RULES_PROMPT_1d_OUTPUT.md` | 5 min | Polish output formatting |

**Phase 1 Total:** 20 minutes (was 30 min as single task)

**Model Recommendation:** Qwen 2.5 Coder (less reasoning overhead than DeepSeek-R1)

---

### Phase 2: Execute & Safety (Original Tasks 2-3)

| Task | File | Est. | Objective |
|------|------|------|-----------|
| **2** | `GLOBAL_RULES_PROMPT_2_BACKUP_EXECUTE.md` | 25 min | Backup functionality, --execute flag |
| **3** | `GLOBAL_RULES_PROMPT_3_ROLLBACK.md` | 20 min | Manifest logging, --rollback flag |

**Note:** If Task 2 times out, decompose into 2a (backup) + 2b (execute) + 2c (inject).

---

### Phase 3: Precision & Testing (Original Tasks 4-5)

| Task | File | Est. | Objective |
|------|------|------|-----------|
| **4** | `GLOBAL_RULES_PROMPT_4_CANARY_CREATE.md` | 20 min | --projects flag, --create flag |
| **5** | `GLOBAL_RULES_PROMPT_5_TESTS.md` | 15 min | Test suite, 80%+ coverage |

---

## Total Estimated Time

- Phase 1 (micro-tasks): 20 min
- Phase 2: 45 min
- Phase 3: 35 min
- **Total: ~100 minutes**

---

## Floor Manager Instructions

1. **Read design doc first:** `Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md`
2. **Use micro-tasks for Phase 1:** Hand off 1a → 1b → 1c → 1d sequentially
3. **Model selection:** Prefer Qwen 2.5 Coder for code generation tasks
4. **Verify between tasks:** Run the script after each micro-task
5. **Timeout handling:** If any task times out, alert Conductor - may need further decomposition
6. **Halt on 3 failures:** If Worker fails same task 3x, alert Conductor

---

## Micro-Task Pattern (NEW)

Each micro-task prompt includes:

1. **CONSTRAINTS section** - Explicit "DO NOT" rules to prevent scope creep
2. **Exact code to copy** - Reduces model invention/deviation
3. **5-minute estimate** - If it takes longer, task is too complex
4. **Simple verification** - Quick checks the Floor Manager can run

This pattern addresses the DeepSeek-R1 timeout observed earlier today. See `Documents/reference/LOCAL_MODEL_LEARNINGS.md` for full documentation.

---

## Context Files Workers May Need

- `Documents/planning/GLOBAL_RULES_INJECTION_DESIGN.md` (full design spec)
- `templates/.cursorrules-template` (template for --create flag)
- `scripts/warden_audit.py` (reference for argparse/logging patterns)

---

## Projects Root

Workers need to know: `[USER_HOME]/projects`

---

## Final Verification (After All Tasks)

```bash
# 1. Test dry-run shows all projects
doppler run -- python scripts/update_cursorrules.py --dry-run
# Expected: Lists 16 projects with compliance status

# 2. Test canary deployment (dry-run first!)
doppler run -- python scripts/update_cursorrules.py --dry-run --projects "project-tracker,tax-organizer,analyze-youtube-videos"
# Expected: Shows only 3 projects

# 3. Test execute creates backup
doppler run -- python scripts/update_cursorrules.py --execute --projects "project-tracker"
# Expected: Backup created in _cursorrules_backups/, file modified

# 4. Test rollback works
doppler run -- python scripts/update_cursorrules.py --rollback
# Expected: Restores from most recent backup

# 5. Test all tests pass
pytest tests/test_update_cursorrules.py -v
# Expected: 8+ tests pass

# 6. Test coverage
pytest tests/test_update_cursorrules.py --cov=scripts.update_cursorrules --cov-report=term
# Expected: >80% coverage
```

---

## Canary Deployment Plan (Post-Implementation)

After all tasks complete and tests pass:

1. **Phase 2:** Execute canary on 3 approved projects
   ```bash
   doppler run -- python scripts/update_cursorrules.py --execute --projects "project-tracker,tax-organizer,analyze-youtube-videos"
   ```

2. **Monitor 48 hours** - Check for:
   - Projects still build/run
   - No Cursor complaints
   - No AI confusion

3. **Phase 3:** Full rollout (after canary success)
   ```bash
   doppler run -- python scripts/update_cursorrules.py --execute
   ```

---

## Archived Prompts

The original Task 1 prompt (`GLOBAL_RULES_PROMPT_1_CORE_DRYRUN.md`) is preserved for reference but should NOT be used. Use micro-tasks 1a-1d instead.

---

**Ready to hand off to Workers**
