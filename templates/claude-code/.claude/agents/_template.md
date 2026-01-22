---
# REQUIRED: Unique identifier (lowercase, hyphens only)
name: my-agent-name

# REQUIRED: When should Claude delegate to this agent?
# Be specific - Claude uses this to decide when to use this agent
description: Description of what this agent does. Use when [specific trigger].

# OPTIONAL: Tools this agent can use (defaults to all if omitted)
# Common tools: Read, Write, Edit, Bash, Grep, Glob
tools: Read, Write, Edit, Grep, Glob

# OPTIONAL: Tools to explicitly deny
# disallowedTools: Bash

# OPTIONAL: Model to use (sonnet, opus, haiku, inherit)
# - sonnet: Good balance of speed/quality (default)
# - opus: Best quality, slower, more expensive
# - haiku: Fast, cheap, less capable
# - inherit: Use same model as parent
model: sonnet

# OPTIONAL: Permission mode
# - default: Normal permission prompts
# - acceptEdits: Auto-accept file edits
# - plan: Read-only exploration mode
# permissionMode: default

# OPTIONAL: Hooks scoped to this agent
hooks:
  # Runs AFTER Read/Write/Edit - validate output
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/my-validator.py"
    - matcher: "Write"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/my-validator.py"

  # Runs BEFORE tool use - block dangerous operations
  # PreToolUse:
  #   - matcher: "Bash"
  #     hooks:
  #       - type: command
  #         command: "python .claude/hooks/validators/safety-check.py"

  # Runs when agent finishes - final validation
  # Stop:
  #   - type: command
  #     command: "python .claude/hooks/validators/final-check.py"
---

You are a [ROLE] specialist.

## Purpose

[One sentence describing what this agent does]

## Workflow

When invoked:
1. [First step]
2. [Second step]
3. [Third step]

## Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Validation

Your hooks automatically validate [what]. If validation fails, you'll receive specific errors - fix them before proceeding.

## Output Format

[How results should be formatted/reported]
