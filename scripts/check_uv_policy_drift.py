#!/usr/bin/env python3
"""
Lightweight UV Run-first policy drift checker.

Exits non-zero on drift. Keeps output concise and actionable.

Checks:
  1) README.md and QUICKSTART.md include 'UV Run-first Policy' marker text.
  2) scaffold/cli.py default RUN_COMMAND and TEST_COMMAND are uv-run-first.
  3) AGENTS.md custom tail (after SCAFFOLD:END) contains no canonical governance headings
     that duplicate scaffold-managed sections: workflow, infrastructure, constraints,
     journal, or obsidian.

Usage:
  uv run scripts/check_uv_policy_drift.py --root .
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


CANONICAL_TAIL_HEADINGS = {
    "THE WORKFLOW",
    "THE WORKFLOW ENFORCED",
    "MCP SERVER INFRASTRUCTURE",
    "UNIVERSAL CONSTRAINTS",
    "JOURNAL ENTRY PROTOCOL",
    "JOURNAL ENTRY PROTOCOL UNIVERSAL",
    "OBSIDIAN INTEGRATION",
    "OBSIDIAN INTEGRATION UNIVERSAL",
}


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _normalize_heading(text: str) -> str:
    """Normalize markdown heading text for stable comparisons."""
    normalized = re.sub(r"[^A-Za-z0-9]+", " ", text).upper()
    return re.sub(r"\s+", " ", normalized).strip()


def check_docs_have_marker(root: Path) -> List[str]:
    """Check README.md and QUICKSTART.md contain the UV policy marker heading."""
    errors: List[str] = []
    marker = "UV Run-first Policy"
    for name in ("README.md", "QUICKSTART.md"):
        p = root / name
        content = _read_text(p)
        if not content:
            errors.append(f"{name} missing or unreadable")
            continue
        if marker not in content:
            errors.append(f"{name} missing marker: '{marker}'")
    return errors


def check_scaffold_cli_defaults(root: Path) -> List[str]:
    """Check scaffold/cli.py contains uv-run-first defaults for RUN_COMMAND/TEST_COMMAND."""
    errors: List[str] = []
    path = root / "scaffold" / "cli.py"
    content = _read_text(path)
    if not content:
        return ["scaffold/cli.py missing or unreadable"]

    def _extract(key: str) -> Tuple[str | None, str]:
        # Match '"RUN_COMMAND": "..."' or "'RUN_COMMAND': '...'"
        pattern = rf"[\"\']{re.escape(key)}[\"\']\s*:\s*[\"\']([^\"\']+)[\"\']"
        m = re.search(pattern, content)
        return (m.group(1) if m else None, pattern)

    run_value, _ = _extract("RUN_COMMAND")
    test_value, _ = _extract("TEST_COMMAND")

    if run_value is None:
        errors.append("Could not find RUN_COMMAND default in scaffold/cli.py")
    elif not run_value.strip().startswith("uv run"):
        errors.append(
            f"RUN_COMMAND not uv-run-first (found: '{run_value}'). Expected to start with 'uv run'"
        )

    if test_value is None:
        errors.append("Could not find TEST_COMMAND default in scaffold/cli.py")
    elif not test_value.strip().startswith("uv run"):
        errors.append(
            f"TEST_COMMAND not uv-run-first (found: '{test_value}'). Expected to start with 'uv run'"
        )

    return errors


def check_agents_tail_no_duplicates(root: Path) -> List[str]:
    """Ensure AGENTS.md tail (after SCAFFOLD:END) does not reintroduce canonical blocks."""
    errors: List[str] = []
    path = root / "AGENTS.md"
    content = _read_text(path)
    if not content:
        return ["AGENTS.md missing or unreadable"]

    end_marker = "<!-- SCAFFOLD:END"
    end_idx = content.find(end_marker)
    if end_idx == -1:
        # If no marker, cannot validate tail; treat as warning-level failure to avoid silent drift.
        return ["AGENTS.md missing SCAFFOLD:END marker"]

    tail = content[end_idx:].splitlines()
    headings: List[str] = []
    in_fence = False
    for line in tail:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if re.match(r"^\s{0,3}#{1,6}\s+", line):
            heading_text = re.sub(r"^\s{0,3}#{1,6}\s+", "", line).strip()
            headings.append(_normalize_heading(heading_text))

    offending = [h for h in headings if h in CANONICAL_TAIL_HEADINGS]

    if offending:
        uniq = sorted(set(offending))
        errors.append(
            "AGENTS.md tail duplicates canonical governance blocks: "
            + "; ".join(uniq)
        )

    return errors


def run_checks(root: Path) -> List[str]:
    errors: List[str] = []
    errors += check_docs_have_marker(root)
    errors += check_scaffold_cli_defaults(root)
    errors += check_agents_tail_no_duplicates(root)
    return errors


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check for UV policy drift and governance duplication.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root to validate (default: current directory)")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    problems = run_checks(root)

    # Emit concise, actionable output
    if problems:
        for p in problems:
            print(f"FAIL: {p}")
        print(f"Summary: drift detected in {len(problems)} area(s).")
        return 1
    else:
        print("OK: README.md and QUICKSTART.md include 'UV Run-first Policy'.")
        print("OK: scaffold/cli.py defaults use 'uv run' for RUN_COMMAND and TEST_COMMAND.")
        print("OK: AGENTS.md tail contains no canonical governance duplicates.")
        print("Summary: no drift detected.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
