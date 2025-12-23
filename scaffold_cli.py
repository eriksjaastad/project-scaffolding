#!/usr/bin/env python3
"""
Setup script to make scaffold command available
"""

from pathlib import Path
import sys

# Add scaffold directory to Python path
scaffold_dir = Path(__file__).parent
sys.path.insert(0, str(scaffold_dir))

from scaffold.cli import cli

if __name__ == "__main__":
    cli()

