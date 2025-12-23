"""
Tests for Kiro integration

Run with: pytest tests/test_kiro.py -v
"""

import pytest
import subprocess
import tempfile
from pathlib import Path
import shutil
import os

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_kiro_specs import KiroSpecGenerator


class TestKiroCLI:
    """Test Kiro CLI basic functionality"""
    
    @pytest.fixture
    def kiro_cli(self):
        """Path to Kiro CLI"""
        return "/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli"
    
    def test_kiro_cli_exists(self, kiro_cli):
        """Test that Kiro CLI is installed"""
        assert Path(kiro_cli).exists(), f"Kiro CLI not found at {kiro_cli}"
    
    def test_kiro_cli_version(self, kiro_cli):
        """Test that Kiro CLI responds to version command"""
        result = subprocess.run(
            [kiro_cli, "--version"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Kiro CLI version command failed"
        assert "kiro-cli" in result.stdout.lower()
    
    def test_kiro_cli_whoami(self, kiro_cli):
        """Test that user is logged into Kiro"""
        result = subprocess.run(
            [kiro_cli, "whoami"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Kiro whoami command failed"
        assert "not logged in" not in result.stdout.lower(), "User not logged into Kiro"
    
    def test_kiro_cli_chat_simple(self, kiro_cli):
        """Test simple Kiro chat command"""
        result = subprocess.run(
            [kiro_cli, "chat", "--no-interactive", "Say hello"],
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"Kiro chat failed: {result.stderr}"
        assert len(result.stdout) > 0, "Kiro returned empty response"
    
    def test_kiro_agent_list(self, kiro_cli):
        """Test that we can list agents"""
        result = subprocess.run(
            [kiro_cli, "agent", "list"],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "Kiro agent list failed"
        # Kiro outputs to stderr, not stdout
        output = result.stdout + result.stderr
        assert "kiro_default" in output or "kiro_planner" in output


class TestKiroSpecGenerator:
    """Test the Kiro spec generation script"""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory"""
        temp_dir = tempfile.mkdtemp(prefix="test_kiro_")
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def generator(self, temp_project):
        """Create a KiroSpecGenerator instance"""
        return KiroSpecGenerator(temp_project)
    
    def test_ensure_kiro_structure(self, generator, temp_project):
        """Test that .kiro directory structure is created"""
        generator.ensure_kiro_structure()
        
        kiro_dir = Path(temp_project) / ".kiro"
        assert kiro_dir.exists()
        assert (kiro_dir / "specs").exists()
        assert (kiro_dir / "steering").exists()
    
    def test_copy_steering_templates(self, generator, temp_project):
        """Test that steering templates are copied"""
        generator.ensure_kiro_structure()
        
        # Use templates from project
        template_dir = Path(__file__).parent.parent / "templates" / ".kiro" / "steering"
        generator.copy_steering_templates(str(template_dir))
        
        steering_dir = Path(temp_project) / ".kiro" / "steering"
        assert (steering_dir / "product.md").exists()
        assert (steering_dir / "tech.md").exists()
        assert (steering_dir / "structure.md").exists()
    
    @pytest.mark.slow
    def test_generate_requirements(self, generator):
        """Test requirements generation (slow - calls Kiro API)"""
        requirements = generator.generate_requirements(
            feature_name="test-feature",
            description="A test feature for testing"
        )
        
        assert len(requirements) > 100, "Requirements too short"
        assert "Requirements" in requirements or "requirements" in requirements
        assert "test-feature" in requirements or "test" in requirements.lower()
    
    @pytest.mark.slow
    def test_generate_full_spec(self, generator, temp_project):
        """Test full spec generation (slow - calls Kiro API 3 times)"""
        generator.ensure_kiro_structure()
        generator.generate_full_spec(
            feature_name="test-auth",
            description="JWT-based authentication with refresh tokens"
        )
        
        spec_dir = Path(temp_project) / ".kiro" / "specs" / "test-auth"
        assert spec_dir.exists()
        assert (spec_dir / "requirements.md").exists()
        assert (spec_dir / "design.md").exists()
        assert (spec_dir / "tasks.md").exists()
        
        # Check file contents
        requirements = (spec_dir / "requirements.md").read_text()
        assert len(requirements) > 100
        
        design = (spec_dir / "design.md").read_text()
        assert len(design) > 100
        
        tasks = (spec_dir / "tasks.md").read_text()
        assert len(tasks) > 100


class TestKiroTemplates:
    """Test that Kiro templates are valid"""
    
    @pytest.fixture
    def template_dir(self):
        """Path to Kiro templates"""
        return Path(__file__).parent.parent / "templates" / ".kiro"
    
    def test_templates_exist(self, template_dir):
        """Test that all template files exist"""
        assert template_dir.exists()
        
        # Steering templates
        assert (template_dir / "steering" / "product.md").exists()
        assert (template_dir / "steering" / "tech.md").exists()
        assert (template_dir / "steering" / "structure.md").exists()
        
        # Spec templates
        spec_dir = template_dir / "specs" / "FEATURE_NAME"
        assert (spec_dir / "requirements.md").exists()
        assert (spec_dir / "design.md").exists()
        assert (spec_dir / "tasks.md").exists()
        
        # README
        assert (template_dir / "README.md").exists()
    
    def test_templates_not_empty(self, template_dir):
        """Test that templates have content"""
        for template in [
            "steering/product.md",
            "steering/tech.md",
            "steering/structure.md",
            "specs/FEATURE_NAME/requirements.md",
            "specs/FEATURE_NAME/design.md",
            "specs/FEATURE_NAME/tasks.md"
        ]:
            content = (template_dir / template).read_text()
            assert len(content) > 100, f"Template {template} is too short"
    
    def test_templates_have_placeholders(self, template_dir):
        """Test that templates have placeholder text"""
        product = (template_dir / "steering" / "product.md").read_text()
        assert "[Project Name]" in product or "[" in product
        
        requirements = (template_dir / "specs" / "FEATURE_NAME" / "requirements.md").read_text()
        assert "[Feature Name]" in requirements or "[" in requirements


class TestKiroIntegrationWorkflow:
    """Test the full Kiro workflow end-to-end"""
    
    @pytest.fixture
    def temp_project(self):
        """Create a temporary project directory"""
        temp_dir = tempfile.mkdtemp(prefix="test_kiro_workflow_")
        yield temp_dir
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.mark.slow
    @pytest.mark.integration
    def test_full_workflow(self, temp_project):
        """Test complete workflow: generate specs → review with CLI"""
        # Step 1: Generate specs
        generator = KiroSpecGenerator(temp_project)
        generator.ensure_kiro_structure()
        generator.generate_full_spec(
            feature_name="auth",
            description="Simple authentication system"
        )
        
        # Step 2: Verify files created
        spec_dir = Path(temp_project) / ".kiro" / "specs" / "auth"
        requirements_path = spec_dir / "requirements.md"
        design_path = spec_dir / "design.md"
        
        assert requirements_path.exists()
        assert design_path.exists()
        
        # Step 3: Review with Kiro CLI
        kiro_cli = "/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli"
        
        # Change to project directory so Kiro can read .kiro/
        os.chdir(temp_project)
        
        result = subprocess.run(
            [kiro_cli, "chat", "--no-interactive", 
             f"Review the design in {design_path} for major flaws"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        assert result.returncode == 0, f"Kiro review failed: {result.stderr}"
        assert len(result.stdout) > 100, "Kiro review response too short"


# Configure pytest markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")

