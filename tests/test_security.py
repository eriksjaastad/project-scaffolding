"""
Security-focused adversarial tests - The Dark Territory

These tests focus on what can go WRONG, not what goes right.
Based on web-Claude's feedback about testing the inverse cases.

Run with: pytest tests/test_security.py -v
"""

import pytest
from pathlib import Path
import tempfile
from unittest.mock import patch, MagicMock


class TestPathTraversal:
    """Test path traversal prevention in safe_slug"""

    def test_safe_slug_prevents_parent_directory_traversal(self):
        """Test that ../../ is sanitized"""
        from scaffold.utils import safe_slug

        malicious_inputs = [
            "../../etc/passwd",
            "../../../root/.ssh/id_rsa",
            "..\\..\\Windows\\System32",
            "....//....//etc/passwd"
        ]

        for malicious in malicious_inputs:
            result = safe_slug(malicious, base_path=Path("/tmp"))
            # Should strip all path traversal attempts
            assert ".." not in result
            assert "/" not in result
            assert "\\" not in result
            # Should still return something usable
            assert len(result) > 0

    def test_safe_slug_with_base_path_validation(self):
        """Test that safe_slug enforces base_path boundary"""
        from scaffold.utils import safe_slug

        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)

            # This should work - stays within base
            result = safe_slug("normal_name", base_path=base)
            target = (base / result).resolve()
            assert target.is_relative_to(base.resolve())

            # This should be caught - but safe_slug sanitizes it first
            result = safe_slug("../../etc/passwd", base_path=base)
            # After sanitization, it becomes "etc_passwd" which is safe
            assert result == "etc_passwd"

    def test_safe_slug_handles_null_bytes(self):
        """Test that null bytes are handled"""
        from scaffold.utils import safe_slug

        # Null bytes can truncate strings in C-based APIs
        malicious = "normal\x00../../etc/passwd"
        result = safe_slug(malicious)
        assert "\x00" not in result


class TestFileSizeLimits:
    """Test file size bomb protection"""

    @pytest.mark.asyncio
    async def test_review_rejects_oversized_document(self):
        """Test that 501KB document is rejected"""
        from scaffold.review import create_orchestrator

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create 501KB file (just over limit)
            huge_file = Path(tmpdir) / "huge.md"
            huge_file.write_text("x" * (501 * 1024))

            orchestrator = create_orchestrator()

            # Should raise ValueError about file size
            with pytest.raises(ValueError, match="too large"):
                await orchestrator.run_review(
                    document_path=huge_file,
                    configs=[],
                    round_number=1,
                    output_dir=Path(tmpdir)
                )

    def test_safe_slug_handles_extremely_long_input(self):
        """Test that 10KB input doesn't cause performance issues"""
        from scaffold.utils import safe_slug

        # 10KB of repeated characters
        long_input = "a" * 10000

        # Should complete quickly and return something reasonable
        result = safe_slug(long_input)
        assert len(result) <= 255  # Typical filesystem limit


class TestConcurrentOperations:
    """Test concurrent safety of file operations"""

    def test_atomic_write_prevents_partial_reads(self):
        """Test that save_atomic prevents reading half-written files"""
        from scaffold.review import save_atomic

        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "test.md"

            # Write large content atomically
            large_content = "x" * 100000
            save_atomic(target, large_content)

            # Read should get all or nothing
            result = target.read_text()
            assert len(result) == len(large_content)

    def test_atomic_write_cleanup_on_failure(self):
        """Test that temp files are cleaned up on failure"""
        from scaffold.review import save_atomic

        with tempfile.TemporaryDirectory() as tmpdir:
            blocking_file = Path(tmpdir) / "not_a_directory"
            blocking_file.write_text("content")
            target = blocking_file / "test.md"

            with pytest.raises(Exception):
                save_atomic(target, "content")

            # Verify no temp files left behind
            temp_files = list(Path(tmpdir).glob("tmp*"))
            assert len(temp_files) == 0


class TestAPIFailureHandling:
    """Test graceful degradation when APIs fail"""

    @pytest.mark.asyncio
    async def test_review_handles_network_timeout(self):
        """Test that network timeouts are handled gracefully"""
        from scaffold.review import create_orchestrator, ReviewConfig
        import asyncio

        orchestrator = create_orchestrator()

        with tempfile.TemporaryDirectory() as tmpdir:
            doc = Path(tmpdir) / "test.md"
            doc.write_text("# Test\n\n## Definition of Done\n- Test")

            prompt = Path(tmpdir) / "prompt.md"
            prompt.write_text("Review this")

            # Mock that causes timeout
            with patch('scaffold.review.AsyncOpenAI') as mock_client:
                mock_client.return_value.chat.completions.create.side_effect = asyncio.TimeoutError()

                orchestrator.deepseek_client = mock_client.return_value

                config = ReviewConfig(
                    name="Test Reviewer",
                    api="deepseek",
                    model="deepseek-chat",
                    prompt_path=prompt
                )

                # Should not crash, should return error in result
                summary = await orchestrator.run_review(
                    document_path=doc,
                    configs=[config],
                    round_number=1,
                    output_dir=Path(tmpdir)
                )

                # Should have error result
                assert len(summary.results) == 1
                assert summary.results[0].error is not None


class TestValidationEdgeCases:
    """Test edge cases in validation scripts"""

    def test_safety_workflow_does_not_call_retiring_scripts(self):
        """Safety CI must not depend on retiring validation scripts."""
        workflow = Path(".github/workflows/safety-check.yml").read_text()

        assert "scripts/warden_audit.py" not in workflow
        assert "scripts/validate_project.py" not in workflow
        assert "pytest tests/ -v" in workflow

    def test_pre_review_scan_does_not_call_retiring_scripts(self):
        """Pre-review scan should stay usable after old safety scripts are deleted."""
        scan = Path("scripts/pre_review_scan.sh").read_text()

        assert "scripts/warden_audit.py" not in scan
        assert "scripts/validate_project.py" not in scan
        assert "pytest tests/test_security.py" in scan

    def test_git_hooks_do_not_allowlist_retiring_scripts(self):
        """Git hook templates should not special-case scripts that are being retired."""
        for hook_name in ("pre-commit", "pre-push"):
            hook = (Path("templates/git-hooks") / hook_name).read_text()
            assert "warden_audit" not in hook
            assert "validate_project" not in hook

    def test_installed_pre_push_does_not_allowlist_retiring_scripts(self):
        """The installed local pre-push hook should match the retiring-script cleanup."""
        hook = Path(".git/hooks/pre-push").read_text()

        assert "warden_audit" not in hook
        assert "validate_project" not in hook


# Mark slow tests
pytestmark = pytest.mark.security
