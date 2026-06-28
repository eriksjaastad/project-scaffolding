"""
Tests for `scaffold install-hygiene` and `scaffold sync`.

These run against a tmp_path "portfolio" — never against the live ~/projects
tree. The Click invocations use CliRunner so we exercise the CLI surface end-
to-end (option parsing + summary output) in addition to the planner internals.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from scaffold import hygiene
from scaffold.cli import cli


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _init_repo(path: Path) -> None:
    """Create a minimal git repo at *path*."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "init", "-q"], cwd=path, check=True, capture_output=True
    )


def _make_project(
    base: Path,
    name: str,
    *,
    with_claude: bool = True,
    with_agents: bool = False,
    claude_body: str | None = None,
    agents_body: str | None = None,
    gitignore: str | None = None,
) -> Path:
    project = base / name
    _init_repo(project)
    if gitignore is not None:
        (project / ".gitignore").write_text(gitignore)
    if with_claude:
        body = (
            claude_body
            if claude_body is not None
            else f"# CLAUDE.md - {name}\n\nSome existing project notes.\n"
        )
        (project / "CLAUDE.md").write_text(body)
    if with_agents:
        body = (
            agents_body
            if agents_body is not None
            else f"# AGENTS.md - {name}\n\nMirror.\n"
        )
        (project / "AGENTS.md").write_text(body)
    return project


@pytest.fixture
def portfolio(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A fake ~/projects root with PROJECTS_ROOT pointed at it."""
    root = tmp_path / "projects"
    root.mkdir()
    monkeypatch.setattr(hygiene, "PROJECTS_ROOT", root)
    return root


# ---------------------------------------------------------------------------
# Fragment / template invariants
# ---------------------------------------------------------------------------


def test_fragment_has_markers():
    rendered = hygiene.render_fragment()
    assert hygiene.BEGIN_MARKER in rendered
    assert hygiene.END_MARKER in rendered
    # Markers wrap the body verbatim.
    body = hygiene.fragment_body()
    assert body in rendered


def test_fragment_documents_phase_b_and_c_enforcement():
    """
    Acceptance: after install, a fresh agent reading the inserted block learns
    that Phase B blocks main edits and that stale branches/stashes are surfaced
    (non-blocking) rather than gated at session end.
    Verify via doc inspection (not by triggering hooks, per card #6154).
    """
    body = hygiene.fragment_body()
    # Phase B: no direct main edits
    assert "main" in body and "feature branch" in body.lower()
    # Stale branches/stashes are surfaced, not blocked — the former session-end
    # gate was removed (Stop fires every turn, not at session end).
    assert "stale branches" in body.lower()
    assert "/cleanup" in body
    assert "session-end" not in body.lower()
    # Phase D + F surfaces are named so an agent knows where to go
    assert "pt handoff" in body
    assert "pt migration" in body


# ---------------------------------------------------------------------------
# .gitignore behavior
# ---------------------------------------------------------------------------


def test_gitignore_added_when_missing(portfolio: Path):
    project = _make_project(portfolio, "alpha")
    result = hygiene.plan_for_project(project)
    written = hygiene.apply_result(result)
    gi = (project / ".gitignore").read_text()
    assert ".scratch/" in gi
    assert any(c.path.name == ".gitignore" for c in written)


def test_gitignore_idempotent_when_present(portfolio: Path):
    project = _make_project(portfolio, "alpha", gitignore="node_modules/\n.scratch/\n")
    result = hygiene.plan_for_project(project)
    gi_change = next(c for c in result.changes if c.path.name == ".gitignore")
    assert gi_change.is_noop
    assert "already" in gi_change.note


def test_gitignore_idempotent_when_present_no_trailing_slash(portfolio: Path):
    project = _make_project(portfolio, "alpha", gitignore=".scratch\n")
    result = hygiene.plan_for_project(project)
    gi_change = next(c for c in result.changes if c.path.name == ".gitignore")
    assert gi_change.is_noop


def test_gitignore_preserves_existing_entries(portfolio: Path):
    pre = "venv/\n*.pyc\ndist/\n"
    project = _make_project(portfolio, "alpha", gitignore=pre)
    result = hygiene.plan_for_project(project)
    hygiene.apply_result(result)
    post = (project / ".gitignore").read_text()
    # Order preserved, entries kept.
    assert post.startswith(pre)
    assert post.rstrip().endswith(".scratch/")


# ---------------------------------------------------------------------------
# CLAUDE.md / AGENTS.md behavior
# ---------------------------------------------------------------------------


def test_creates_claude_md_when_missing(portfolio: Path):
    project = _make_project(portfolio, "alpha", with_claude=False)
    result = hygiene.plan_for_project(project)
    hygiene.apply_result(result)
    text = (project / "CLAUDE.md").read_text()
    assert text.startswith("# CLAUDE.md - alpha")
    assert hygiene.BEGIN_MARKER in text
    assert hygiene.END_MARKER in text


def test_appends_to_existing_claude_md_without_markers(portfolio: Path):
    pre = "# CLAUDE.md - alpha\n\nOriginal content stays put.\n"
    project = _make_project(portfolio, "alpha", claude_body=pre)
    result = hygiene.plan_for_project(project)
    hygiene.apply_result(result)
    text = (project / "CLAUDE.md").read_text()
    # Original preserved at the top
    assert text.startswith(pre)
    # Block appended at end
    assert hygiene.BEGIN_MARKER in text
    assert hygiene.END_MARKER in text
    assert text.index(hygiene.BEGIN_MARKER) > text.index("Original content")


def test_install_is_idempotent(portfolio: Path):
    project = _make_project(portfolio, "alpha")
    # First pass: writes
    result1 = hygiene.plan_for_project(project)
    hygiene.apply_result(result1)
    snapshot = {f: (project / f).read_text() for f in ("CLAUDE.md", ".gitignore")}
    # Second pass: no-op
    result2 = hygiene.plan_for_project(project)
    assert not result2.has_changes
    written = hygiene.apply_result(result2)
    assert written == []
    # Files unchanged
    for f, content in snapshot.items():
        assert (project / f).read_text() == content


def test_drift_refresh_overwrites_block(portfolio: Path):
    """Existing markers with stale content: install replaces the block in place."""
    stale = (
        "# CLAUDE.md - alpha\n\n"
        "Some prefix content.\n\n"
        f"{hygiene.BEGIN_MARKER}\n"
        "## OLD HYGIENE TEXT\n\nThis block is stale.\n"
        f"{hygiene.END_MARKER}\n\n"
        "Some suffix content.\n"
    )
    project = _make_project(portfolio, "alpha", claude_body=stale)
    result = hygiene.plan_for_project(project)
    assert result.has_changes
    hygiene.apply_result(result)
    text = (project / "CLAUDE.md").read_text()
    # Prefix + suffix preserved
    assert "Some prefix content." in text
    assert "Some suffix content." in text
    # Stale body gone, canonical body present
    assert "OLD HYGIENE TEXT" not in text
    assert "Locked Hygiene Contract" in text
    # Exactly one marker pair
    assert text.count(hygiene.BEGIN_MARKER) == 1
    assert text.count(hygiene.END_MARKER) == 1


def test_multiple_markers_refused(portfolio: Path):
    bad = (
        "# CLAUDE.md\n"
        f"{hygiene.BEGIN_MARKER}\n## first\n{hygiene.END_MARKER}\n"
        f"{hygiene.BEGIN_MARKER}\n## second\n{hygiene.END_MARKER}\n"
    )
    project = _make_project(portfolio, "alpha", claude_body=bad)
    result = hygiene.plan_for_project(project)
    assert hygiene.is_refused(result)
    # Refused changes are not written
    pre_text = (project / "CLAUDE.md").read_text()
    hygiene.apply_result(result)
    assert (project / "CLAUDE.md").read_text() == pre_text


def test_agents_md_mirror_updated_when_present(portfolio: Path):
    project = _make_project(portfolio, "alpha", with_agents=True)
    result = hygiene.plan_for_project(project)
    hygiene.apply_result(result)
    claude_text = (project / "CLAUDE.md").read_text()
    agents_text = (project / "AGENTS.md").read_text()
    assert hygiene.BEGIN_MARKER in claude_text
    assert hygiene.BEGIN_MARKER in agents_text


def test_agents_md_not_created_if_absent(portfolio: Path):
    """We only update AGENTS.md if the project already has one."""
    project = _make_project(portfolio, "alpha", with_agents=False)
    hygiene.apply_result(hygiene.plan_for_project(project))
    assert not (project / "AGENTS.md").exists()


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def test_discover_skips_non_git_dirs(portfolio: Path):
    _make_project(portfolio, "alpha")
    # Not a git repo
    (portfolio / "loose-dir").mkdir()
    found = [p.name for p in hygiene.discover_projects(portfolio)]
    assert "alpha" in found
    assert "loose-dir" not in found


def test_discover_skips_protected(portfolio: Path, monkeypatch: pytest.MonkeyPatch):
    _make_project(portfolio, "alpha")
    _make_project(portfolio, "openclaw")  # in IGNORE list per scan_config.yaml
    monkeypatch.setattr(hygiene, "PROTECTED_PROJECTS", {"openclaw"})
    found = [p.name for p in hygiene.discover_projects(portfolio)]
    assert "alpha" in found
    assert "openclaw" not in found


def test_discover_skips_hidden_dirs(portfolio: Path):
    _make_project(portfolio, ".hidden-repo")
    _make_project(portfolio, "alpha")
    found = [p.name for p in hygiene.discover_projects(portfolio)]
    assert ".hidden-repo" not in found
    assert "alpha" in found


# ---------------------------------------------------------------------------
# Dry-run safety (CLI)
# ---------------------------------------------------------------------------


def test_dry_run_does_not_write(portfolio: Path):
    project = _make_project(portfolio, "alpha")
    mtimes_before = {
        p.name: p.stat().st_mtime
        for p in project.iterdir()
        if p.is_file()
    }
    runner = CliRunner()
    result = runner.invoke(cli, ["install-hygiene", str(project)])
    assert result.exit_code == 0, result.output
    assert "DRY-RUN" in result.output
    mtimes_after = {
        p.name: p.stat().st_mtime
        for p in project.iterdir()
        if p.is_file()
    }
    assert mtimes_before == mtimes_after
    # And nothing got created
    assert not (project / ".gitignore").exists()


def test_apply_actually_writes(portfolio: Path):
    project = _make_project(portfolio, "alpha")
    runner = CliRunner()
    result = runner.invoke(cli, ["install-hygiene", str(project), "--apply"])
    assert result.exit_code == 0, result.output
    assert "APPLY" in result.output
    assert (project / ".gitignore").exists()
    assert hygiene.BEGIN_MARKER in (project / "CLAUDE.md").read_text()


def test_all_flag_enumerates_and_respects_protected(
    portfolio: Path, monkeypatch: pytest.MonkeyPatch
):
    _make_project(portfolio, "alpha")
    _make_project(portfolio, "beta")
    _make_project(portfolio, "openclaw")
    monkeypatch.setattr(hygiene, "PROTECTED_PROJECTS", {"openclaw"})
    runner = CliRunner()
    result = runner.invoke(cli, ["install-hygiene", "--all"])
    assert result.exit_code == 0, result.output
    # Dry-run still shows the projects it would touch.
    assert "alpha" in result.output
    assert "beta" in result.output
    # Excluded project not enumerated at all (not even as SKIP).
    assert "openclaw" not in result.output


def test_install_requires_target_or_all(portfolio: Path):
    runner = CliRunner()
    result = runner.invoke(cli, ["install-hygiene"])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# scaffold sync
# ---------------------------------------------------------------------------


def test_sync_reports_drift(portfolio: Path):
    stale = (
        "# CLAUDE.md - alpha\n\n"
        f"{hygiene.BEGIN_MARKER}\n## stale\n{hygiene.END_MARKER}\n"
    )
    project = _make_project(portfolio, "alpha", claude_body=stale)
    runner = CliRunner()
    result = runner.invoke(cli, ["sync", str(project)])
    assert result.exit_code == 0, result.output
    assert "DRIFT" in result.output
    # Block unchanged in detection mode
    assert "## stale" in (project / "CLAUDE.md").read_text()


def test_sync_apply_refreshes(portfolio: Path):
    stale = (
        "# CLAUDE.md - alpha\n\n"
        f"{hygiene.BEGIN_MARKER}\n## stale\n{hygiene.END_MARKER}\n"
    )
    project = _make_project(portfolio, "alpha", claude_body=stale)
    runner = CliRunner()
    result = runner.invoke(cli, ["sync", str(project), "--apply"])
    assert result.exit_code == 0, result.output
    text = (project / "CLAUDE.md").read_text()
    assert "## stale" not in text
    assert "Locked Hygiene Contract" in text


def test_sync_no_drift_after_install(portfolio: Path):
    project = _make_project(portfolio, "alpha")
    hygiene.apply_result(hygiene.plan_for_project(project))
    reports = hygiene.detect_drift(project)
    assert reports  # we did install CLAUDE.md
    assert all(not r.drift for r in reports)


def test_sync_treats_missing_markers_as_drift(portfolio: Path):
    project = _make_project(portfolio, "alpha")  # CLAUDE.md but no markers
    reports = hygiene.detect_drift(project)
    assert any(r.drift and "no markers" in r.detail for r in reports)
