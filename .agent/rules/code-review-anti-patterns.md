# Code Review Anti-Patterns

purpose: Recurring defects to scan for during reviews (supplements governance checklist)
scope: Anti-patterns NOT fully covered by REVIEWS_AND_GOVERNANCE_PROTOCOL.md checklist items

## AP-1: Hardcoded Absolute Paths

check: grep -rn "/Users/" templates/ *.yaml scripts/ scaffold/ AGENTS.md CLAUDE.md
fix: use Path.home(), os.getenv("PROJECTS_ROOT"), or Path(__file__).parent
note: governance M1 covers detection; this provides the scan command

## AP-2: Silent Exception Swallowing

check: grep -rn "except.*:" scripts/ scaffold/ | grep "pass"
fix: log with logging.error(), return error status, re-raise, or document why silence is acceptable
note: governance M2 covers detection; this provides the scan command

## AP-3: Unpinned Dependencies

check: grep -E "^[^#].*>=[0-9]" requirements.txt | grep -v "~="
fix: use ~= for compatible releases, pin exact versions for stability
note: governance D1 covers review; this provides the scan command

## AP-4: Test Scope Mismatch

detect: test name/docstring claims broader scope than implementation covers
check: read test code, ask "what does this test NOT check?"
fix: expand scope, rename to match actual scope, or add companion tests

## AP-5: Deprecated API Usage

detect: import statements using old APIs (e.g., Pydantic validator instead of field_validator)
check: library changelogs, deprecation warnings in test output
fix: upgrade to current API, add TODO if breaking change requires more work

## AP-6: Interactivity in CI/CD

detect: scripts using input(), interactive prompts in non-interactive environments
fix: add --yes or --non-interactive flags, detect TTY and skip prompts
banned: blocking on user input in automated pipelines

---
version: 2.0.0
established: 2026-01-15
updated: 2026-03-26 — trimmed from 126 lines, kept scan commands, removed prose explanations
