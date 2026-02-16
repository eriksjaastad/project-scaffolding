import textwrap
from pathlib import Path

import pytest


from scripts.check_uv_policy_drift import run_checks


def write(p: Path, content: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def make_pass_fixture(root: Path) -> None:
    write(
        root / "README.md",
        """
        # Project

        ## UV Run-first Policy (Effective: February 2026)
        Details about using uv run.
        """,
    )
    write(
        root / "QUICKSTART.md",
        """
        # Quickstart

        ## UV Run-first Policy
        Use `uv run` for new Python commands.
        """,
    )
    write(
        root / "scaffold/cli.py",
        """
        DEFAULTS = {
            "RUN_COMMAND": "uv run main.py",
            "TEST_COMMAND": "uv run -m pytest",
        }
        """,
    )
    write(
        root / "AGENTS.md",
        """
        <!-- SCAFFOLD:START - Do not edit between markers -->
        Canonical content
        <!-- SCAFFOLD:END - Custom content below is preserved -->

        ## Maintainers Note
        Tail content that is project-specific.
        """,
    )


def make_fail_fixture(root: Path) -> None:
    write(
        root / "README.md",
        """
        # Project
        (intentionally missing UV Run-first heading)
        """,
    )
    write(
        root / "QUICKSTART.md",
        """
        # Quickstart
        (intentionally missing UV Run-first heading)
        """,
    )
    write(
        root / "scaffold/cli.py",
        """
        DEFAULTS = {
            "RUN_COMMAND": "python main.py",
            "TEST_COMMAND": "pytest",
        }
        """,
    )
    write(
        root / "AGENTS.md",
        """
        <!-- SCAFFOLD:START - Do not edit between markers -->
        Canonical content
        <!-- SCAFFOLD:END - Custom content below is preserved -->

        # Obsidian Integration
        Duplicate of canonical heading in tail.
        """,
    )


def test_run_checks_pass(tmp_path: Path) -> None:
    make_pass_fixture(tmp_path)
    errors = run_checks(tmp_path)
    assert errors == []


def test_run_checks_fail(tmp_path: Path) -> None:
    make_fail_fixture(tmp_path)
    errors = run_checks(tmp_path)
    # Should detect at least three independent failures
    assert any("README.md" in e for e in errors)
    assert any("RUN_COMMAND" in e for e in errors)
    assert any("AGENTS.md tail" in e for e in errors)
    assert len(errors) >= 3

