#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
[Validator Name]

Purpose: [What this validator checks]
Used by: [Which agent/command uses this]

Exit codes:
- 0: Validation passed, continue
- 2: Validation failed, block and return errors to Claude

Usage:
  # Test directly
  echo '{"tool_input": {"file_path": "test.csv"}}' | python this_validator.py

  # Or with file argument
  python this_validator.py path/to/file.csv
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Optional: Log to file for debugging
LOG_FILE = Path(__file__).parent / "validator.log"


def log(message: str) -> None:
    """Append timestamped message to log file."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def validate(file_path: Path) -> list[str]:
    """
    Validate the target and return list of errors.

    Args:
        file_path: Path to the file or directory to validate

    Returns:
        List of error messages. Empty list = validation passed.
    """
    errors = []

    # Example validation logic - replace with your own
    if not file_path.exists():
        errors.append(f"File not found: {file_path}")
        return errors

    # Add your validation logic here
    # Example: Check file extension
    # if file_path.suffix.lower() != ".csv":
    #     errors.append(f"Expected CSV file, got: {file_path.suffix}")

    # Example: Check file is not empty
    # if file_path.stat().st_size == 0:
    #     errors.append(f"File is empty: {file_path}")

    return errors


def main():
    """Main entry point for hook."""
    log("=" * 40)
    log("VALIDATOR TRIGGERED")
    log(f"sys.argv: {sys.argv}")

    # Determine target from args or stdin
    target = None

    # Check command line argument first
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        log(f"Target from argv: {target}")
    else:
        # Read from stdin (hook passes context as JSON)
        try:
            stdin_data = sys.stdin.read()
            log(f"stdin length: {len(stdin_data)}")

            if stdin_data.strip():
                hook_input = json.loads(stdin_data)
                log(f"hook_input keys: {list(hook_input.keys())}")

                # Extract file path from hook context
                tool_input = hook_input.get("tool_input", {})
                file_path = tool_input.get("file_path") or tool_input.get("path")

                if file_path:
                    target = Path(file_path)
                    log(f"Target from stdin: {target}")
        except json.JSONDecodeError as e:
            log(f"JSON decode error: {e}")

    # Default to current directory if no target
    if target is None:
        target = Path(".")
        log("Target defaulted to current directory")

    # Run validation
    errors = validate(target)

    # Report results
    if errors:
        log(f"RESULT: BLOCK ({len(errors)} errors)")
        for err in errors:
            log(f"  - {err}")

        # Return blocking response to Claude
        print(json.dumps({
            "decision": "block",
            "reason": "Validation failed:\n" + "\n".join(f"- {e}" for e in errors)
        }))
        sys.exit(2)
    else:
        log("RESULT: PASS")

        # Return success
        print(json.dumps({}))
        sys.exit(0)


if __name__ == "__main__":
    main()
