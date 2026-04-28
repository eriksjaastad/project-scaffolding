"""Focused tests for scaffolded git hook templates."""

from pathlib import Path
import subprocess


HOOKS_DIR = Path("templates") / "git-hooks"


def test_pre_push_blocks_dangerous_patterns_without_warden() -> None:
    """Pre-push should be self-contained and block dangerous diff patterns."""
    content = (HOOKS_DIR / "pre-push").read_text()

    assert "warden_audit.py" not in content
    assert "validate_project.py" not in content
    assert "PUSH BLOCKED" in content
    assert "rm -rf" in content
    assert "rmtree" in content


def test_git_hook_templates_have_valid_bash_syntax() -> None:
    """Hook templates should pass a bash syntax check."""
    hook_paths = [
        HOOKS_DIR / "pre-commit",
        HOOKS_DIR / "pre-push",
        HOOKS_DIR / "install-hooks.sh",
    ]

    result = subprocess.run(
        ["bash", "-n", *map(str, hook_paths)],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )

    assert result.returncode == 0, result.stderr
