#!/usr/bin/env python3
"""
Test Coverage Runner

Runs pytest with coverage and generates an HTML report.

Usage:
    python scripts/tests/run_coverage.py

Requirements:
    pip install pytest pytest-cov coverage
"""

import subprocess
import sys
from pathlib import Path


def main():
    project_root = Path(__file__).parent.parent.parent

    print("=" * 60)
    print("Running Tests with Coverage")
    print("=" * 60)

    # Run pytest with coverage
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            "--cov=scripts",  # Adjust to your source directory
            "--cov-report=html:scripts/tests/htmlcov",
            "--cov-report=term-missing",
            "scripts/tests/",
            "-v"
        ],
        cwd=project_root,
        check=False
    )

    print()
    print("=" * 60)

    if result.returncode == 0:
        print("All tests passed!")
    else:
        print(f"Tests completed with exit code: {result.returncode}")

    report_path = project_root / "scripts" / "tests" / "htmlcov" / "index.html"
    print(f"Coverage report: file://{report_path}")
    print("=" * 60)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
