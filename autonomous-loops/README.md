"""
Autonomous Loop Configuration System
====================================

This directory contains configuration files for the three autonomous loops:
- Janitor: Continuous health monitoring
- Librarian: Template drift detection and auto-fix
- Patch-Bot: Bounded automated fixes

## Configuration Files

- `loops.yaml`: Loop schedules and tier definitions
- `tiers.yaml`: Tier-based monitoring frequency
- `models.yaml`: Model tier mappings for different task complexities
- `escalation.yaml`: Cost thresholds and escalation rules

## Usage

```python
from autonomous_loops.config_loader import load_config

# Load all configs
config = load_config()

# Access specific configs
tier_config = config['tiers']
model_config = config['models']
```

## Per-Project Overrides

Projects can override global settings by creating a `.autonomous-loops.yaml` file in their root:

```yaml
tier: 1  # Override to hourly monitoring
autonomy_level: fix_safe  # Allow safe auto-fixes
healthcheck_cmd: "pytest tests/"
allowed_paths:
  - "scripts/"
  - "tests/"
```

See `examples/project-override.yaml` for a complete example.
