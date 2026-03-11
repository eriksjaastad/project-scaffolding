"""Tests for agent config health checker."""

from scaffold.agent_health import (
    _count_lines,
    _prose_ratio,
    _boilerplate_ratio,
    check_file,
    check_project,
    format_report,
    FileHealth,
    ProjectHealth,
)


class TestCountLines:
    def test_empty(self):
        assert _count_lines("") == 0

    def test_single_line(self):
        assert _count_lines("hello") == 1

    def test_multiple_lines(self):
        assert _count_lines("a\nb\nc\n") == 3

    def test_no_trailing_newline(self):
        assert _count_lines("a\nb\nc") == 3


class TestProseRatio:
    def test_empty(self):
        assert _prose_ratio("") == 0.0

    def test_all_headings(self):
        content = "# Heading\n## Sub\n### Sub sub\n"
        assert _prose_ratio(content) == 0.0

    def test_all_lists(self):
        content = "- item one\n- item two\n* item three\n1. numbered\n"
        assert _prose_ratio(content) == 0.0

    def test_prose_paragraph(self):
        content = (
            "This is a long prose paragraph that goes on and on about something important.\n"
            "Another long prose line that describes something in great detail here.\n"
            "Yet another sentence that keeps going to fill up the line count.\n"
        )
        ratio = _prose_ratio(content)
        assert ratio > 0.5

    def test_mixed_content(self):
        content = (
            "# Title\n"
            "- list item\n"
            "- another item\n"
            "This is a long prose paragraph that goes on and on about something important.\n"
            "## Next Section\n"
            "- more list\n"
        )
        ratio = _prose_ratio(content)
        assert 0 < ratio < 1.0

    def test_code_blocks_excluded(self):
        content = (
            "```python\n"
            "This is a very long line inside a code block that should not count as prose content at all.\n"
            "Another very long code line that describes implementation details and should be ignored.\n"
            "```\n"
        )
        assert _prose_ratio(content) == 0.0


class TestBoilerplateRatio:
    def test_empty(self):
        assert _boilerplate_ratio("") == 0.0

    def test_no_markers(self):
        content = "# Custom content\n- rule one\n- rule two\n"
        assert _boilerplate_ratio(content) == 0.0

    def test_all_managed(self):
        content = (
            "<!-- AGENTSYNC:START -->\n"
            "managed line 1\n"
            "managed line 2\n"
            "<!-- AGENTSYNC:END -->\n"
        )
        assert _boilerplate_ratio(content) == 1.0

    def test_mixed(self):
        content = (
            "# Custom header\n"
            "<!-- AGENTSYNC:START -->\n"
            "managed line\n"
            "<!-- AGENTSYNC:END -->\n"
            "# Custom footer\n"
        )
        ratio = _boilerplate_ratio(content)
        assert 0.3 < ratio < 0.8

    def test_warning_headers_counted(self):
        content = (
            "This file is managed by sync_governance.py\n"
            "# Content\n"
            "- rule\n"
        )
        ratio = _boilerplate_ratio(content)
        assert ratio > 0


class TestCheckFile:
    def test_nonexistent_file(self, tmp_path):
        fh = check_file(tmp_path / "missing.md", tmp_path)
        assert not fh.exists
        assert fh.line_count == 0
        assert fh.warnings == []

    def test_small_file(self, tmp_path):
        f = tmp_path / "CLAUDE.md"
        f.write_text("# Rules\n- be concise\n- no fluff\n")
        fh = check_file(f, tmp_path)
        assert fh.exists
        assert fh.line_count == 3
        assert not fh.over_limit
        assert fh.warnings == []

    def test_over_limit_file(self, tmp_path):
        f = tmp_path / "CLAUDE.md"
        f.write_text("\n".join([f"- rule {i}" for i in range(250)]) + "\n")
        fh = check_file(f, tmp_path)
        assert fh.over_limit
        assert any("250 lines" in w for w in fh.warnings)


class TestCheckProject:
    def test_empty_project(self, tmp_path):
        ph = check_project(tmp_path)
        assert ph.project == tmp_path.name
        assert not ph.has_claude_md
        assert not ph.has_agents_md
        assert not ph.has_agent_rules

    def test_project_with_claude_md(self, tmp_path):
        (tmp_path / "CLAUDE.md").write_text("# Rules\n- be concise\n")
        ph = check_project(tmp_path)
        assert ph.has_claude_md
        assert not ph.has_agents_md

    def test_project_with_agent_rules(self, tmp_path):
        rules_dir = tmp_path / ".agent" / "rules"
        rules_dir.mkdir(parents=True)
        (rules_dir / "00-overview.md").write_text("# Overview\n")
        (rules_dir / "01-safety.md").write_text("# Safety\n- no rm\n")
        ph = check_project(tmp_path)
        assert ph.has_agent_rules
        # 2 top-level (CLAUDE.md, AGENTS.md) + 2 rule files
        assert len(ph.files) == 4


class TestFormatReport:
    def test_clean_report(self):
        results = [
            ProjectHealth(
                project="test-project",
                files=[FileHealth(path="CLAUDE.md", exists=True, line_count=50)],
                warning_count=0,
            )
        ]
        report = format_report(results, verbose=True)
        assert "test-project" in report
        assert "0 with warnings" in report

    def test_warnings_shown(self):
        results = [
            ProjectHealth(
                project="bad-project",
                files=[
                    FileHealth(
                        path="CLAUDE.md",
                        exists=True,
                        line_count=300,
                        over_limit=True,
                        warnings=["300 lines (limit: 200)"],
                    )
                ],
                warning_count=1,
            )
        ]
        report = format_report(results)
        assert "!!" in report
        assert "300 lines" in report


class TestCLICommand:
    def test_help(self):
        from scaffold.cli import cli
        from click.testing import CliRunner

        runner = CliRunner()
        result = runner.invoke(cli, ["agent-health", "--help"])
        assert result.exit_code == 0
        assert "agent config files" in result.output.lower()
