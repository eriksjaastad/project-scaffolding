"""Tests for the canonical AgentSync entrypoint."""

from pathlib import Path
import sys


def _ensure_repo_on_path() -> None:
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))


def test_parse_components_defaults_and_orders() -> None:
    _ensure_repo_on_path()

    from agentsync.sync import parse_components

    assert parse_components(None) == ["rules", "agents", "governance"]
    assert parse_components("governance,rules") == ["rules", "governance"]


def test_main_dispatches_only_selected_component(monkeypatch) -> None:
    _ensure_repo_on_path()

    from agentsync import sync

    calls: list[tuple[str, str | None, bool, bool, bool]] = []

    def fake_run_component(
        component: str,
        project_name: str | None,
        all_projects: bool,
        dry_run: bool,
        stage: bool,
    ) -> bool:
        calls.append((component, project_name, all_projects, dry_run, stage))
        return True

    monkeypatch.setattr(sync, "run_component", fake_run_component)

    exit_code = sync.main(["demo-project", "--components", "rules", "--dry-run"])

    assert exit_code == 0
    assert calls == [("rules", "demo-project", False, True, False)]


def test_scaffold_run_agentsync_uses_unified_rules_command() -> None:
    _ensure_repo_on_path()

    from scaffold.cli import _run_agentsync

    success, actions = _run_agentsync("demo-project", dry_run=True)

    assert success is True
    joined = "\n".join(actions)
    assert "agentsync/sync.py" in joined
    assert "--components rules" in joined


def test_extract_governance_version_from_title(tmp_path: Path) -> None:
    _ensure_repo_on_path()

    from agentsync.sync_governance import extract_version

    source = tmp_path / "governance.md"
    source.write_text("# Governance Protocol (v1.3)\n\npurpose: test\n")

    assert extract_version(source) == "1.3"


def test_extract_governance_version_from_metadata_line(tmp_path: Path) -> None:
    _ensure_repo_on_path()

    from agentsync.sync_governance import extract_version

    source = tmp_path / "governance.md"
    source.write_text("# Governance Protocol\n\nversion: 2026.03.12\n\npurpose: test\n")

    assert extract_version(source) == "2026.03.12"


def test_live_governance_source_has_parseable_version() -> None:
    _ensure_repo_on_path()

    from agentsync.sync_governance import SOURCE_FILE, extract_version

    assert extract_version(SOURCE_FILE) != "0.0.0"