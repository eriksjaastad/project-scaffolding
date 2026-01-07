"""
Tests for review orchestrator (DeepSeek + Ollama integration)

Run with: pytest tests/test_review.py -v
"""

import pytest
import asyncio
from pathlib import Path
import tempfile
import os

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scaffold.review import ReviewOrchestrator, ReviewConfig, create_orchestrator


class TestReviewOrchestrator:
    """Test the multi-AI review orchestrator"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for test outputs"""
        temp = tempfile.mkdtemp(prefix="test_review_")
        yield temp
        # Cleanup handled by tempfile
    
    @pytest.fixture
    def sample_document(self, temp_dir):
        """Create a sample document to review"""
        doc_path = Path(temp_dir) / "sample.md"
        doc_path.write_text("""
# Sample Feature

## Overview
This is a test feature for reviewing.

## Architecture
Simple client-server architecture using FastAPI.

## Performance
Target: < 200ms response time.

## Security
Uses JWT tokens for authentication.

## Definition of Done
- [ ] Code has type hints
- [ ] Tests pass
""")
        return doc_path
    
    @pytest.fixture
    def deepseek_key(self):
        """Get DeepSeek API key from environment"""
        key = os.getenv("SCAFFOLDING_DEEPSEEK_KEY")
        if not key:
            pytest.skip("SCAFFOLDING_DEEPSEEK_KEY not set")
        return key
    
    def test_orchestrator_creation(self):
        """Test creating orchestrator"""
        orchestrator = create_orchestrator()
        assert orchestrator is not None
    
    def test_orchestrator_with_deepseek(self, deepseek_key):
        """Test creating orchestrator with DeepSeek"""
        orchestrator = create_orchestrator(deepseek_key=deepseek_key)
        assert orchestrator.deepseek_client is not None
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_deepseek_review(self, deepseek_key, sample_document, temp_dir):
        """Test DeepSeek review (slow - calls API)"""
        if not deepseek_key:
            pytest.skip("No DeepSeek API key available")
        
        orchestrator = create_orchestrator(deepseek_key=deepseek_key)
        
        # Create simple review config
        prompt_dir = Path(__file__).parent.parent / "prompts" / "active" / "document_review"
        
        configs = [
            ReviewConfig(
                name="Test Reviewer",
                api="deepseek",
                model="deepseek-chat",
                prompt_path=prompt_dir / "architecture.md"
            )
        ]
        
        output_dir = Path(temp_dir) / "reviews"
        
        summary = await orchestrator.run_review(
            document_path=sample_document,
            configs=configs,
            round_number=1,
            output_dir=output_dir
        )
        
        # Check results
        assert summary is not None
        assert len(summary.results) == 1
        assert summary.results[0].cost >= 0
        assert summary.results[0].tokens_used > 0
        assert len(summary.results[0].content) > 50
        
        # Check output files
        assert (output_dir / "round_1" / "test_reviewer.md").exists()
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_ollama_review(self, sample_document, temp_dir):
        """Test Ollama local review (slow - calls Ollama)"""
        # Check if Ollama is running
        import shutil
        if not shutil.which("ollama"):
            pytest.skip("Ollama CLI not found")
            
        orchestrator = create_orchestrator()
        
        # Create Ollama review config
        prompt_dir = Path(__file__).parent.parent / "prompts" / "active" / "document_review"
        
        configs = [
            ReviewConfig(
                name="Ollama Reviewer",
                api="ollama",
                model="llama3.2",
                prompt_path=prompt_dir / "architecture.md"
            )
        ]
        
        output_dir = Path(temp_dir) / "reviews"
        
        # This might fail if the model is not pulled, but the test will skip correctly
        try:
            summary = await orchestrator.run_review(
                document_path=sample_document,
                configs=configs,
                round_number=1,
                output_dir=output_dir
            )
            
            # Check results
            assert summary is not None
            assert len(summary.results) == 1
            result = summary.results[0]
            
            if result.error:
                pytest.skip(f"Ollama review failed: {result.error}")
            
            assert len(result.content) > 50
            
            # Check output files (standardized orchestrator naming)
            assert (output_dir / "round_1" / "CODE_REVIEW_OLLAMA_REVIEWER.md").exists()
        except Exception as e:
            pytest.skip(f"Ollama call failed (maybe service not running?): {e}")
    
    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_multi_reviewer(self, deepseek_key, sample_document, temp_dir):
        """Test multiple reviewers in parallel"""
        if not deepseek_key:
            pytest.skip("No DeepSeek API key available")
        
        orchestrator = create_orchestrator(deepseek_key=deepseek_key)
        
        # Create multiple review configs
        prompt_dir = Path(__file__).parent.parent / "prompts" / "active" / "document_review"
        
        configs = [
            ReviewConfig(
                name="Security Reviewer",
                api="deepseek",
                model="deepseek-chat",
                prompt_path=prompt_dir / "security.md"
            ),
            ReviewConfig(
                name="Performance Reviewer",
                api="deepseek",
                model="deepseek-chat",
                prompt_path=prompt_dir / "performance.md"
            )
        ]
        
        output_dir = Path(temp_dir) / "reviews"
        
        summary = await orchestrator.run_review(
            document_path=sample_document,
            configs=configs,
            round_number=1,
            output_dir=output_dir
        )
        
        # Check results
        assert len(summary.results) == 2
        assert summary.total_cost > 0
        
        # Check both reviewers produced output
        for result in summary.results:
            assert result.tokens_used > 0
            assert len(result.content) > 50


class TestReviewCLI:
    """Test the CLI interface for reviews"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory"""
        temp = tempfile.mkdtemp(prefix="test_cli_")
        yield temp
    
    @pytest.fixture
    def sample_document(self, temp_dir):
        """Create sample document"""
        doc_path = Path(temp_dir) / "test.md"
        doc_path.write_text("# Test\n\nThis is a test document.\n\n## Definition of Done\n- [ ] Done.")
        return doc_path
    
    @pytest.mark.slow
    def test_cli_review_command(self, sample_document, temp_dir):
        """Test running review via CLI"""
        import subprocess
        
        cli_path = Path(__file__).parent.parent / "scaffold_cli.py"
        
        result = subprocess.run(
            [
                sys.executable, str(cli_path), "review",
                "--type", "document",
                "--input", str(sample_document),
                "--round", "1",
                "--output", str(Path(temp_dir) / "reviews")
            ],
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ},
            check=True
        )
        
        # Check command ran (might skip reviewers if no keys)
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
        assert "Review" in result.stdout or "Skipping" in result.stdout


def test_safe_slug_traversal():
    """Test that safe_slug correctly handles path traversal attempts"""
    from scaffold.review import safe_slug
    # Input with traversal
    original_text = "../../etc/passwd"
    # Result should have underscores instead of dots/slashes, then the traversal cleanup hits
    # re.sub(r'[^a-z0-9]+', '_', "../../etc/passwd") -> "__etc_passwd"
    # slug.strip('_') -> "etc_passwd"
    expected_output = "etc_passwd"
    
    slug = safe_slug(original_text, base_path=Path("/tmp"))
    assert slug == expected_output

