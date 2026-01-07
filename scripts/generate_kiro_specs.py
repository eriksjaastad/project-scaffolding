#!/usr/bin/env python3
"""
Kiro Spec Generator - Automate creation of Kiro specs

Usage:
    python scripts/generate_kiro_specs.py \
        --project-root /path/to/project \
        --feature-name user-auth \
        --description "JWT-based authentication with refresh tokens"
"""

import argparse
import subprocess
import re
from pathlib import Path
from typing import Optional


class KiroSpecGenerator:
    """Generate Kiro specifications programmatically"""
    
    KIRO_CLI = "/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli"
    
    def __init__(self, project_root: str) -> None:
        self.project_root = Path(project_root)
        self.kiro_dir = self.project_root / ".kiro"
        
    def ensure_kiro_structure(self) -> None:
        """Create .kiro directory structure if it doesn't exist"""
        (self.kiro_dir / "specs").mkdir(parents=True, exist_ok=True)
        (self.kiro_dir / "steering").mkdir(parents=True, exist_ok=True)
        print(f"✅ Created .kiro structure in {self.project_root}")
    
    def copy_steering_templates(self, template_dir: Optional[str] = None) -> None:
        """Copy steering templates if they don't exist"""
        if template_dir is None:
            # Default to scaffolding templates
            template_dir = Path(__file__).parent.parent / "templates" / ".kiro" / "steering"
        else:
            template_dir = Path(template_dir)
        
        steering_dir = self.kiro_dir / "steering"
        
        for template in ["product.md", "tech.md", "structure.md"]:
            target = steering_dir / template
            if not target.exists():
                source = template_dir / template
                if source.exists():
                    target.write_text(source.read_text())
                    print(f"✅ Copied {template} to .kiro/steering/")
                else:
                    print(f"⚠️  Template {template} not found in {template_dir}")
    
    def generate_requirements(self, feature_name: str, description: str) -> str:
        """Generate requirements.md using Kiro CLI"""
        prompt = f"""
You are a technical architect creating a requirements document for Kiro specs.

Feature: {feature_name}
Description: {description}

Generate a requirements.md document following this structure:

# {feature_name} - Requirements

## Overview
[Feature summary]

## Functional Requirements
[List of what the feature must do]

## Non-Functional Requirements
[Performance, security, reliability]

## Constraints
[Technical and business constraints]

## Success Criteria
[How we know it's complete]

## Dependencies
[What this depends on]

## Edge Cases
[Unusual scenarios to handle]

## Open Questions
[Questions needing clarification]

Be specific, measurable, and actionable. Use REQ-X.X format for requirements.
"""
        
        print(f"🤖 Generating requirements for {feature_name}...")
        result = self._call_kiro(prompt)
        return self._clean_kiro_output(result)
    
    def generate_design(self, feature_name: str, requirements_path: str) -> str:
        """Generate design.md based on requirements"""
        requirements = Path(requirements_path).read_text()
        
        prompt = f"""
You are a technical architect creating an architecture design document for Kiro specs.

Feature: {feature_name}

Requirements:
{requirements}

Generate a design.md document following this structure:

# {feature_name} - Architecture Design

## Design Overview
[High-level approach]

## Architecture
[Components and their responsibilities]

## Data Model
[Models and relationships]

## Data Flow
[How data moves through the system]

## API Design
[Endpoints if applicable]

## Edge Cases
[How to handle edge cases]

## Performance Considerations
[Optimization strategies]

## Security Considerations
[How to protect data]

## Testing Strategy
[How to test this]

## Risks & Mitigation
[What could go wrong and how to prevent it]

Be specific about implementation details. Include code examples where helpful.
"""
        
        print(f"🤖 Generating design for {feature_name}...")
        result = self._call_kiro(prompt)
        return self._clean_kiro_output(result)
    
    def generate_tasks(self, feature_name: str, requirements_path: str, design_path: str) -> str:
        """Generate tasks.md based on requirements and design"""
        requirements = Path(requirements_path).read_text()
        design = Path(design_path).read_text()
        
        prompt = f"""
You are a technical architect creating an implementation task list for Kiro specs.

Feature: {feature_name}

Requirements:
{requirements}

Design:
{design}

Generate a tasks.md document following this structure:

# {feature_name} - Implementation Plan

## Task Breakdown

Break this into phases:
- Phase 1: Setup & Infrastructure
- Phase 2: Core Implementation
- Phase 3: API/CLI Layer
- Phase 4: Testing & Validation
- Phase 5: Documentation & Polish

For each task:
- [ ] **X.Y** Task name
  - Specific actions
  - _Requirements: [REQ-X.X]_
  - _Estimated: X hours_

Include checkpoints between phases.
Link each task to specific requirements.
Identify dependencies between tasks.

Be specific, actionable, and include time estimates.
"""
        
        print(f"🤖 Generating tasks for {feature_name}...")
        result = self._call_kiro(prompt)
        return self._clean_kiro_output(result)
    
    def generate_full_spec(self, feature_name: str, description: str) -> None:
        """Generate complete spec (requirements + design + tasks)"""
        # Create spec directory
        spec_dir = self.kiro_dir / "specs" / feature_name
        spec_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate requirements
        requirements = self.generate_requirements(feature_name, description)
        requirements_path = str(spec_dir / "requirements.md")
        Path(requirements_path).write_text(requirements)
        print(f"✅ Created {requirements_path}")
        
        # Generate design
        design = self.generate_design(feature_name, requirements_path)
        design_path = str(spec_dir / "design.md")
        Path(design_path).write_text(design)
        print(f"✅ Created {design_path}")
        
        # Generate tasks
        tasks = self.generate_tasks(feature_name, requirements_path, design_path)
        tasks_path = spec_dir / "tasks.md"
        tasks_path.write_text(tasks)
        print(f"✅ Created {tasks_path}")
        
        print(f"\n🎉 Complete spec generated in {spec_dir}")
        print(f"\nNext steps:")
        print(f"  1. Review and refine: {spec_dir}")
        print(f"  2. Use Kiro CLI to iterate: kiro-cli chat --no-interactive 'Review {spec_dir}/design.md'")
        print(f"  3. Hand off tasks to Tier 2/3 for implementation")
    
    def _call_kiro(self, prompt: str) -> str:
        """Call Kiro CLI with a prompt"""
        result = subprocess.run(
            [self.KIRO_CLI, "chat", "--no-interactive", "--trust-all-tools"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
            check=True
        )
        
        return result.stdout
    
    def _clean_kiro_output(self, output: str) -> str:
        """Remove ANSI codes and extract content"""
        # Remove ANSI escape codes
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        cleaned = ansi_escape.sub('', output)
        
        # Extract content before "▸ Credits:"
        parts = cleaned.split('▸ Credits:')
        if len(parts) > 0:
            content = parts[0].strip()
            # Remove ASCII art banner
            lines = content.split('\n')
            start_idx = 0
            for i, line in enumerate(lines):
                if line.strip() and not line.startswith('⠀') and not line.startswith('╭') and not line.startswith('│'):
                    start_idx = i
                    break
            content = '\n'.join(lines[start_idx:]).strip()
            return content
        
        return cleaned.strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Kiro specs programmatically")
    parser.add_argument("--project-root", required=True, help="Path to project root")
    parser.add_argument("--feature-name", required=True, help="Feature name (e.g., user-auth)")
    parser.add_argument("--description", required=True, help="Feature description")
    parser.add_argument("--template-dir", help="Path to steering templates (optional)")
    parser.add_argument("--skip-steering", action="store_true", help="Skip copying steering templates")
    
    args = parser.parse_args()
    
    generator = KiroSpecGenerator(args.project_root)
    
    # Setup structure
    generator.ensure_kiro_structure()
    
    # Copy steering templates if needed
    if not args.skip_steering:
        generator.copy_steering_templates(args.template_dir)
    
    # Generate full spec
    generator.generate_full_spec(args.feature_name, args.description)


if __name__ == "__main__":
    main()

