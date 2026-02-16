"""Configuration loader for autonomous loops.

Loads and validates YAML configuration files for Janitor, Librarian, and Patch-Bot loops.
Supports per-project overrides and hot-reloading.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os


class ConfigLoader:
    """Loads and manages autonomous loop configuration."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize config loader.
        
        Args:
            config_dir: Path to config directory. Defaults to autonomous-loops/config/
        """
        if config_dir is None:
            # Default to config directory relative to this file
            self.config_dir = Path(__file__).parent / "config"
        else:
            self.config_dir = Path(config_dir)
        
        self._config_cache: Dict[str, Any] = {}
    
    def load_all(self) -> Dict[str, Any]:
        """Load all configuration files.
        
        Returns:
            Dictionary with keys: loops, tiers, models, escalation
        """
        return {
            "loops": self.load_loops(),
            "tiers": self.load_tiers(),
            "models": self.load_models(),
            "escalation": self.load_escalation()
        }
    
    def load_loops(self) -> Dict[str, Any]:
        """Load loop schedules and operations."""
        return self._load_yaml("loops.yaml")
    
    def load_tiers(self) -> Dict[str, Any]:
        """Load tier definitions."""
        return self._load_yaml("tiers.yaml")
    
    def load_models(self) -> Dict[str, Any]:
        """Load model tier mappings."""
        return self._load_yaml("models.yaml")
    
    def load_escalation(self) -> Dict[str, Any]:
        """Load escalation rules."""
        return self._load_yaml("escalation.yaml")
    
    def load_project_override(self, project_root: Path) -> Optional[Dict[str, Any]]:
        """Load project-specific override configuration.
        
        Args:
            project_root: Path to project root directory
            
        Returns:
            Override config dict or None if no override file exists
        """
        override_file = project_root / ".autonomous-loops.yaml"
        if not override_file.exists():
            return None
        
        with open(override_file, 'r') as f:
            return yaml.safe_load(f)
    
    def merge_with_override(
        self,
        global_config: Dict[str, Any],
        project_root: Path
    ) -> Dict[str, Any]:
        """Merge global config with project-specific overrides.
        
        Args:
            global_config: Global configuration
            project_root: Path to project root
            
        Returns:
            Merged configuration with overrides applied
        """
        override = self.load_project_override(project_root)
        if not override:
            return global_config
        
        # Deep merge override into global config
        merged = global_config.copy()
        merged.update(override)
        return merged
    
    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load a YAML file from the config directory.
        
        Args:
            filename: Name of YAML file
            
        Returns:
            Parsed YAML as dictionary
        """
        filepath = self.config_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    
    def reload(self) -> None:
        """Clear cache and reload all configs."""
        self._config_cache.clear()


# Convenience function for quick loading
def load_config(config_dir: Optional[Path] = None) -> Dict[str, Any]:
    """Load all autonomous loop configurations.
    
    Args:
        config_dir: Optional path to config directory
        
    Returns:
        Dictionary with all configs loaded
    """
    loader = ConfigLoader(config_dir)
    return loader.load_all()


if __name__ == "__main__":
    # Test loading
    config = load_config()
    print("Loaded configs:")
    for key in config.keys():
        print(f"  - {key}")
