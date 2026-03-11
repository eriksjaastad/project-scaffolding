"""Focused tests for scaffolded git hook templates."""

from pathlib import Path
import subprocess


HOOKS_DIR = Path("templates") / "git-hooks"


def test_pre_push_runs_agentsync_rules_sync() -> None:
    """Pre-push should auto-run rules sync via the unified sync entrypoint."""
    content = (HOOKS_DIR / "pre-push").read_text()

    assert "agentsync/sync.py" in content
    assert "--components rules" in content
    assert "git status --porcelain -- CLAUDE.md .agent/rules/instructions.md" in content
    assert "PROJECT_SCAFFOLDING_ROOT" in content


def test_post_merge_runs_agent_health_scan() -> None:
    """Post-merge should run the agent-health scanner for the current project."""
    content = (HOOKS_DIR / "post-merge").read_text()

    assert "agent-health" in content
    assert "--project" in content
    assert "PROJECT_SCAFFOLDING_ROOT" in content
    assert ".scaffolding-version" in content


def test_install_hooks_script_installs_post_merge() -> None:
    """Hook installer should install the post-merge hook."""
    content = (HOOKS_DIR / "install-hooks.sh").read_text()

    assert '"$SCRIPT_DIR/post-merge"' in content
    assert '"$HOOKS_DIR/post-merge"' in content
    assert "Installed: post-merge" in content


def test_agentsync_template_readme_mentions_pre_push_workflow() -> None:
    """Template docs should describe the pre-push sync workflow."""
    content = (Path("templates") / ".agentsync" / "README.md").read_text()

    assert "Sync before push" in content
    assert "Commit regenerated files" in content
    assert "--components rules --dry-run" in content


def test_git_hook_templates_have_valid_bash_syntax() -> None:
    """Hook templates should pass a bash syntax check."""
    hook_paths = [
        HOOKS_DIR / "pre-commit",
        HOOKS_DIR / "post-merge",
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