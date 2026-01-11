"""Tests for update_cursorrules.py - Global Rules Injection script."""

import json
import pathlib
import shutil
import pytest
import sys

# Import the module to test
# Ensure scripts directory is in path
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "scripts"))
from update_cursorrules import (
    find_cursorrules_files,
    check_compliance,
    inject_safety_rules,
    create_backup,
    run_rollback,
    parse_projects_filter,
    SAFETY_RULES_SECTION,
)


class TestFindCursorrulesFiles:
    """Tests for project scanning."""

    def test_finds_cursorrules_in_project_dirs(self, tmp_path):
        """Should find .cursorrules files in project directories."""
        # Setup: Create fake project structure
        (tmp_path / "project-a").mkdir()
        (tmp_path / "project-a" / ".cursorrules").write_text("# Project A")
        (tmp_path / "project-b").mkdir()
        (tmp_path / "project-b" / ".cursorrules").write_text("# Project B")
        (tmp_path / "project-c").mkdir()  # No .cursorrules

        # Execute
        found, missing = find_cursorrules_files(tmp_path)

        # Verify
        assert len(found) == 2
        project_names = {f.parent.name for f in found}
        assert project_names == {"project-a", "project-b"}

    def test_skips_hidden_directories(self, tmp_path):
        """Should skip directories starting with . or _"""
        (tmp_path / ".hidden").mkdir()
        (tmp_path / ".hidden" / ".cursorrules").write_text("# Hidden")
        (tmp_path / "_private").mkdir()
        (tmp_path / "_private" / ".cursorrules").write_text("# Private")
        (tmp_path / "visible").mkdir()
        (tmp_path / "visible" / ".cursorrules").write_text("# Visible")

        found, _ = find_cursorrules_files(tmp_path)

        assert len(found) == 1
        assert found[0].parent.name == "visible"

    def test_filters_by_project_names(self, tmp_path):
        """Should filter to only specified projects."""
        for name in ["alpha", "beta", "gamma"]:
            (tmp_path / name).mkdir()
            (tmp_path / name / ".cursorrules").write_text(f"# {name}")

        found, _ = find_cursorrules_files(tmp_path, projects_filter={"alpha", "gamma"})

        assert len(found) == 2
        project_names = {f.parent.name for f in found}
        assert project_names == {"alpha", "gamma"}


class TestCheckCompliance:
    """Tests for rule detection."""

    def test_detects_compliant_file(self, tmp_path):
        """Should detect when both rules are present."""
        cr_path = tmp_path / ".cursorrules"
        cr_path.write_text("""
# My Project

## Safety Rules
- **Trash, Don't Delete:** Never use rm
- **No Silent Failures:** Always log errors
""")

        result = check_compliance(cr_path)

        assert result['has_trash_rule'] is True
        assert result['has_silent_rule'] is True

    def test_detects_missing_trash_rule(self, tmp_path):
        """Should detect when Trash rule is missing."""
        cr_path = tmp_path / ".cursorrules"
        cr_path.write_text("""
# My Project
- **No Silent Failures:** Always log
""")

        result = check_compliance(cr_path)

        assert result['has_trash_rule'] is False
        assert result['has_silent_rule'] is True

    def test_detects_missing_silent_rule(self, tmp_path):
        """Should detect when Silent Failures rule is missing."""
        cr_path = tmp_path / ".cursorrules"
        cr_path.write_text("""
# My Project
- **Trash, Don't Delete:** Use send2trash
""")

        result = check_compliance(cr_path)

        assert result['has_trash_rule'] is True
        assert result['has_silent_rule'] is False


class TestInjectSafetyRules:
    """Tests for rule injection."""

    def test_injects_rules_to_empty_file(self):
        """Should append rules to minimal file."""
        content = "# My Project\n"

        result = inject_safety_rules(content, has_trash=False, has_silent=False)

        assert "Trash, Don't Delete" in result
        assert "No Silent Failures" in result

    def test_idempotent_when_already_compliant(self):
        """Should not modify already-compliant content."""
        content = f"# My Project\n{SAFETY_RULES_SECTION}"

        result = inject_safety_rules(content, has_trash=True, has_silent=True)

        # Should be unchanged
        assert result.count("Trash, Don't Delete") == 1


class TestBackupAndRollback:
    """Tests for backup and rollback functionality."""

    def test_backup_creates_copy(self, tmp_path):
        """Should create backup copy of file."""
        # Setup
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        cr_path = project_dir / ".cursorrules"
        cr_path.write_text("Original content")

        backup_dir = tmp_path / "backups"
        manifest_entries = []

        # Execute
        backup_path = create_backup(cr_path, backup_dir, manifest_entries)

        # Verify
        assert backup_path.exists()
        assert backup_path.read_text() == "Original content"
        assert len(manifest_entries) == 1
        assert manifest_entries[0]['project'] == "my-project"

    def test_rollback_restores_content(self, tmp_path):
        """Should restore file from backup."""
        # Setup: Create original and modify it
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        cr_path = project_dir / ".cursorrules"
        cr_path.write_text("Original content")

        backup_dir = tmp_path / "backups"
        manifest_entries = []

        # Create backup then modify
        create_backup(cr_path, backup_dir, manifest_entries)
        cr_path.write_text("Modified content")

        # Write manifest
        manifest = [{
            'timestamp': '2026-01-10T12:00:00',
            'projects_root': str(tmp_path),
            'files_modified': manifest_entries
        }]
        backup_dir.mkdir(exist_ok=True)
        (backup_dir / "manifest.json").write_text(json.dumps(manifest))

        # Execute rollback
        success = run_rollback(backup_dir)

        # Verify
        assert success is True
        assert cr_path.read_text() == "Original content"


class TestParseProjectsFilter:
    """Tests for project filter parsing."""

    def test_parses_comma_separated_list(self):
        """Should parse comma-separated project names."""
        result = parse_projects_filter("alpha,beta,gamma")
        assert result == {"alpha", "beta", "gamma"}

    def test_handles_whitespace(self):
        """Should trim whitespace from project names."""
        result = parse_projects_filter("alpha , beta,  gamma ")
        assert result == {"alpha", "beta", "gamma"}

    def test_returns_none_for_empty_input(self):
        """Should return None when no filter specified."""
        assert parse_projects_filter(None) is None
        assert parse_projects_filter("") is None
