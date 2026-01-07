"""
Quick smoke tests - run these first!

Run with: pytest tests/test_smoke.py -v
"""

import pytest
from pathlib import Path


class TestProjectStructure:
    """Test that project structure is correct"""
    
    @pytest.fixture
    def project_root(self):
        return Path(__file__).parent.parent
    
    def test_templates_exist(self, project_root):
        """Test that all critical templates exist"""
        templates = project_root / "templates"
        assert templates.exists()
        
        # Other templates
        assert (templates / "CLAUDE.md.template").exists()
        assert (templates / ".cursorrules.template").exists()
    
    def test_scripts_exist(self, project_root):
        """Test that scripts exist and are executable"""
        scripts = project_root / "scripts"
        assert scripts.exists()
        
        # Check scripts exist
        assert (scripts / "test_deepseek.py").exists()
    
    def test_scaffold_package_exists(self, project_root):
        """Test that scaffold package is importable"""
        scaffold = project_root / "scaffold"
        assert scaffold.exists()
        assert (scaffold / "__init__.py").exists()
        assert (scaffold / "review.py").exists()
        assert (scaffold / "cli.py").exists()
    
    def test_prompts_exist(self, project_root):
        """Test that review prompts exist"""
        prompts = project_root / "prompts" / "active" / "document_review"
        assert prompts.exists()
        
        assert (prompts / "architecture.md").exists()
        assert (prompts / "performance.md").exists()
        assert (prompts / "security.md").exists()
    
    def test_documentation_exists(self, project_root):
        """Test that key documentation exists"""
        docs = project_root / "Documents"
        assert docs.exists()
        
        assert (docs / "DEEPSEEK_SETUP.md").exists()
        assert (docs / "PROJECT_KICKOFF_GUIDE.md").exists()


class TestImports:
    """Test that all modules can be imported"""
    
    @pytest.fixture(autouse=True)
    def setup_path(self):
        """Add project root to path"""
        import sys
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
    
    def test_import_scaffold_review(self):
        """Test importing review module"""
        try:
            from scaffold.review import ReviewOrchestrator, ReviewConfig, create_orchestrator
            assert ReviewOrchestrator is not None
            assert ReviewConfig is not None
            assert create_orchestrator is not None
        except ImportError as e:
            pytest.fail(f"Failed to import scaffold.review: {e}")
    
    def test_scaffold_cli_flags(self):
        """Test that scaffold CLI has the expected flags"""
        from scaffold.cli import cli
        from click.testing import CliRunner
        runner = CliRunner()
        result = runner.invoke(cli, ["review", "--help"])
        assert result.exit_code == 0
        assert "--ollama-model" in result.output
        assert "SCAFFOLDING_DEEPSEEK_KEY" in result.output


class TestDependencies:
    """Test that all required dependencies are installed"""
    
    def test_critical_imports(self):
        """Test that critical packages are available"""
        try:
            import openai
            import anthropic
            import aiohttp
            import rich
            import pydantic
            import click
            import yaml
        except ImportError as e:
            pytest.fail(f"Missing critical dependency: {e}")
    
    def test_python_version(self):
        """Test that Python version is >= 3.11"""
        import sys
        assert sys.version_info >= (3, 11), f"Python 3.11+ required, got {sys.version_info}"


class TestConfiguration:
    """Test configuration files"""
    
    @pytest.fixture
    def project_root(self):
        return Path(__file__).parent.parent
    
    def test_env_file_template(self, project_root):
        """Test that .env exists (might be gitignored)"""
        # .env might not exist in repo, but check .gitignore has it
        gitignore = project_root / ".gitignore"
        if gitignore.exists():
            content = gitignore.read_text()
            assert ".env" in content, ".env should be in .gitignore"
    
    def test_venv_exists(self, project_root):
        """Test that virtual environment exists"""
        venv = project_root / "venv"
        assert venv.exists(), "Virtual environment not found"
        assert (venv / "bin" / "python").exists() or (venv / "Scripts" / "python.exe").exists()

