---
# REQUIRED: What this command does (shown in /help)
description: Brief description of what this command does

# OPTIONAL: Hint for arguments (shown after command name)
argument-hint: <required_arg> [optional_arg]

# OPTIONAL: Hooks for this command
hooks:
  # Runs when command finishes
  Stop:
    - type: command
      command: "python .claude/hooks/validators/my-validator.py"
---

# Command Name

## Purpose

[What this command accomplishes]

## Arguments

- `$ARGUMENTS`: [What the user should provide]
- `$CLAUDE_PROJECT_DIR`: Path to project root (available automatically)

## Workflow

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Validation

This command validates its output using [validator name].
If validation fails, fix the issues before completing.

## Example Usage

```
/command-name path/to/file.csv
/command-name some-argument --flag
```

## Notes

[Any additional context or caveats]
