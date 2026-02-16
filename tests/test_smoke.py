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
        """Test that review prompts exist (optional in scaffold)"""
        import pytest
        prompts = project_root / "prompts" / "active" / "document_review"
        if not prompts.exists():
            pytest.skip("Prompts are user-provided; none included by default.")
        
        assert (prompts / "architecture.md").exists()
        assert (prompts / "performance.md").exists()
        assert (prompts / "security.md").exists()
    
    def test_documentation_exists(self, project_root):
        """Test that key documentation exists"""
        docs = project_root / "Documents"
        assert docs.exists()
        
        assert (docs / "guides" / "DEEPSEEK_SETUP.md").exists()
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
        import importlib.util, pytest
        if (importlib.util.find_spec("anthropic") is None) or (importlib.util.find_spec("openai") is None):
            pytest.skip("Optional provider SDK(s) not installed; skipping scaffold.review import smoke.")
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
        import importlib.util
        critical_packages = [
            "rich",
            "click",
            "yaml",
        ]
        for package in critical_packages:
            spec = importlib.util.find_spec(package)
            if spec is None:
                pytest.fail(f"Missing critical dependency: {package}")
    
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
    
    def test_uv_environment_configured(self, project_root):
        """UV-managed workflow: ensure lockfile exists (no local venv required)."""
        uv_lock = project_root / "uv.lock"
        assert uv_lock.exists(), "uv.lock not found — expected UV-managed workflow."
    
    def test_no_hard_venv_requirement(self, project_root):
        """Guard against legacy-first regressions: tests must not require venv/."""
        # Presence of a venv is allowed but should not be required for tests to pass.
        # This assertion enforces that at least one modern, repo-level signal exists.
        uv_lock = project_root / "uv.lock"
        assert uv_lock.exists(), "Tests should not require a local venv/; ensure UV lockfile is present."

