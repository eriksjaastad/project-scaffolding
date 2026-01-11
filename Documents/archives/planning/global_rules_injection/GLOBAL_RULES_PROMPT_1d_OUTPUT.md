# Worker Task 1d: Clean Output Formatting

**Worker Model:** Qwen 2.5 Coder (preferred) or DeepSeek-R1
**Estimated Time:** 5 minutes
**Objective:** Polish the dry-run output with mode display and better formatting

**Prerequisite:** Task 1c complete (detection function works)

---

## CONSTRAINTS (READ FIRST)

- DO NOT implement any update/inject/execute logic yet
- DO NOT add new arguments beyond what exists
- DO NOT change the core logic - only improve output formatting
- This completes Task 1 - DRY-RUN FOUNDATION ONLY

---

## 🎯 [ACCEPTANCE CRITERIA]

- [ ] Output shows "Mode: DRY-RUN" at the top
- [ ] Output shows "Scanning: /path/to/projects"
- [ ] Output is well-formatted with clear sections
- [ ] Exit code 0 on success
- [ ] Script matches the original Task 1 acceptance criteria

---

## Code Changes

Update main() with improved formatting:

```python
def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Push safety rules to all project .cursorrules files"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show what would change without modifying files (default)"
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=pathlib.Path("/Users/eriksjaastad/projects"),
        help="Projects root directory"
    )

    args = parser.parse_args()

    if not args.root.exists():
        logger.error(f"Projects root not found: {args.root}")
        sys.exit(1)

    # Show mode
    logger.info("Mode: DRY-RUN")
    logger.info(f"Scanning: {args.root}")
    logger.info("-" * 60)

    # Scan for .cursorrules files
    cursorrules_files = find_cursorrules_files(args.root)

    if not cursorrules_files:
        logger.warning("No .cursorrules files found")
        sys.exit(0)

    # Check compliance for each
    stats = {'ok': 0, 'needs_update': 0}

    for cr_path in cursorrules_files:
        compliance = check_compliance(cr_path)

        if compliance['has_trash_rule'] and compliance['has_silent_rule']:
            logger.info(f"OK: {compliance['project']} - has all safety rules")
            stats['ok'] += 1
        else:
            missing = []
            if not compliance['has_trash_rule']:
                missing.append("Trash rule")
            if not compliance['has_silent_rule']:
                missing.append("Silent rule")
            logger.info(f"NEEDS UPDATE: {compliance['project']} - missing: {', '.join(missing)}")
            stats['needs_update'] += 1

    logger.info("-" * 60)
    logger.info(f"Summary: {stats['ok']} OK, {stats['needs_update']} need update, {len(cursorrules_files)} total")
    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## Verification

```bash
# 1. Script runs with clean output
python scripts/update_cursorrules.py --dry-run

# Expected output format:
# INFO: Mode: DRY-RUN
# INFO: Scanning: /Users/eriksjaastad/projects
# INFO: ------------------------------------------------------------
# INFO: OK: hypocrisynow - has all safety rules
# INFO: NEEDS UPDATE: project-tracker - missing: Trash rule, Silent rule
# ... more projects ...
# INFO: ------------------------------------------------------------
# INFO: Summary: 1 OK, 15 need update, 16 total

# 2. Exit code is 0
python scripts/update_cursorrules.py --dry-run && echo "Exit code: 0"
```

---

## Task 1 Complete Checklist

After Task 1d, verify ALL original Task 1 acceptance criteria:

- [ ] **File Created:** `scripts/update_cursorrules.py` exists
- [ ] **Argparse:** Has `--dry-run`, `--root` arguments
- [ ] **Logging:** Uses Python logging module (not print)
- [ ] **Scanning:** Finds all .cursorrules files under projects root
- [ ] **Detection:** Correctly identifies if "Trash, Don't Delete" rule exists
- [ ] **Detection:** Correctly identifies if "Silent Failures" rule exists
- [ ] **Output:** Dry-run shows each project with status (OK/NEEDS UPDATE)
- [ ] **Exit Code:** Returns 0 on success

---

## FLOOR MANAGER PROTOCOL

Do not sign off until:
- [ ] All 5 micro-task acceptance criteria checked
- [ ] ALL 8 original Task 1 criteria verified
- [ ] Output format matches expected example
- [ ] Ready to proceed to Task 2 (Backup + Execute)

**Task 1 Foundation Complete. Ready for Task 2.**
