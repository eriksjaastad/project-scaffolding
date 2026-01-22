# Claude Code Hooks and Sub-Agents

> **Purpose:** Reference guide for building self-validating agents using Claude Code's hooks and sub-agent system.
>
> **Why this matters:** Hooks add deterministic validation to your AI workflow. Instead of hoping Claude remembers to validate, hooks *guarantee* validation runs every time. Trust goes up because validation is automatic, not optional.

---

## Table of Contents

1. [Why Self-Validating Agents?](#why-self-validating-agents)
2. [The .claude/ Directory Structure](#the-claude-directory-structure)
3. [Hooks: The Three Types](#hooks-the-three-types)
4. [Sub-Agents: Specialized Workers](#sub-agents-specialized-workers)
5. [Commands: User-Invokable Prompts](#commands-user-invokable-prompts)
6. [The Nested Relationship](#the-nested-relationship)
7. [Creating Templates](#creating-templates)
8. [Examples](#examples)
9. [Common Questions](#common-questions)
10. [Resources](#resources)

---

## Why Self-Validating Agents?

### The Problem

When you ask Claude to do something, you're trusting its judgment to:
- Validate its own work
- Catch errors before moving on
- Follow your standards consistently

But Claude can forget. It can skip validation if it thinks it's not needed. You're relying on LLM judgment for quality control.

### The Solution

**Hooks** inject deterministic code into Claude's workflow:

```
Without hooks:
  Claude reads CSV → Claude decides if it looks valid → continues

With hooks:
  Claude reads CSV → [PostToolUse hook fires] → Python script validates →
  If invalid: Claude MUST fix it before continuing
  If valid: Claude continues
```

The validation isn't optional. It's not a suggestion in a prompt. It's **code that runs every single time**.

### The Trust Equation

> "We have edits from our agent that we know worked because we gave them the tools to validate their own work." — IndyDevDan

- **Without hooks:** You trust Claude's judgment
- **With hooks:** You trust deterministic code that runs automatically

---

## The .claude/ Directory Structure

```
your-project/
└── .claude/
    ├── settings.json      # Permissions and global hooks
    ├── commands/          # Custom slash commands (/my-command)
    │   └── my-command.md
    ├── agents/            # Sub-agents (specialized workers)
    │   └── my-agent.md
    └── hooks/
        └── validators/    # Python scripts for validation
            ├── csv-validator.py
            └── json-validator.py
```

### What Each Piece Does

| Directory | Purpose | When to Use |
|-----------|---------|-------------|
| `settings.json` | Global permissions, allowed tools, global hooks | Project-wide safety rules |
| `commands/` | Slash commands you invoke manually | Repeatable workflows (`/review-code`) |
| `agents/` | Sub-agents Claude delegates to automatically | Specialized tasks (CSV editing, testing) |
| `hooks/validators/` | Python scripts that validate work | Deterministic checks (CSV structure, JSON schema) |

### Scope Priority

Claude looks for `.claude/` in multiple places (highest priority first):

1. `--agents` CLI flag (session only)
2. `.claude/` in current project (this project)
3. `~/.claude/` in home directory (all projects)
4. Plugin's `agents/` directory

**Recommendation:** Put project-specific agents in `.claude/agents/` and commit to version control.

---

## Hooks: The Three Types

Hooks are scripts that fire at specific points in Claude's workflow.

### 1. PreToolUse

**When:** Before Claude uses a tool (Read, Write, Edit, Bash)

**Use for:** Blocking dangerous operations before they happen

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/block-dangerous-commands.sh"
```

**Example:** Block `rm -rf`, `sudo`, force pushes

### 2. PostToolUse

**When:** After Claude uses a tool, before it processes the result

**Use for:** Validating output immediately after an action

```yaml
hooks:
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/csv-validator.py"
```

**Example:** Validate CSV structure after reading a CSV file

### 3. Stop

**When:** When the agent finishes its work

**Use for:** Final validation before completing

```yaml
hooks:
  Stop:
    - type: command
      command: "python .claude/hooks/validators/final-check.py"
```

**Example:** Run linter on all modified files before completing

### Hook Exit Codes

Your validation script communicates back to Claude via exit codes:

| Exit Code | Meaning | What Happens |
|-----------|---------|--------------|
| 0 | Success | Claude continues normally |
| 2 | Blocking error | Claude receives stderr and MUST fix the issue |
| Other | Non-blocking error | User sees error, Claude continues |

### Hook Response Format (JSON)

For more control, your script can output JSON:

```python
# Block and tell Claude why
print(json.dumps({
    "decision": "block",
    "reason": "CSV validation failed:\n- Missing 'date' column\n- Invalid balance format"
}))
```

```python
# Allow and continue
print(json.dumps({}))
```

---

## Sub-Agents: Specialized Workers

Sub-agents are specialized versions of Claude that handle specific tasks.

### Why Sub-Agents?

> "A focused agent with one purpose outperforms an unfocused agent with many purposes." — IndyDevDan

- **Context isolation:** Each sub-agent has its own context window
- **Tool restriction:** Limit what a sub-agent can do (safety)
- **Parallelization:** Run multiple sub-agents simultaneously
- **Specialization:** Focused prompts for specific tasks

### Sub-Agent File Format

`.claude/agents/csv-editor.md`:

```markdown
---
name: csv-editor
description: Edit and validate CSV files. Use when working with CSV data.
tools: Read, Write, Edit, Grep
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/csv-validator.py"
    - matcher: "Write"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/csv-validator.py"
---

You are a CSV editing specialist. Your job is to read, modify, and validate CSV files.

When editing CSVs:
1. Preserve existing column order
2. Validate data types match existing patterns
3. Report any anomalies found

You have access to a CSV validator that runs automatically after reads and writes.
If validation fails, fix the issue before proceeding.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique ID (lowercase, hyphens only) |
| `description` | Yes | When Claude should use this agent |
| `tools` | No | Tools allowed (defaults to all) |
| `disallowedTools` | No | Tools to block |
| `model` | No | sonnet, opus, haiku, inherit |
| `hooks` | No | Hooks scoped to this agent only |
| `skills` | No | Preload other skills/knowledge |
| `permissionMode` | No | default, acceptEdits, plan, etc. |

### Automatic vs Manual Delegation

Claude automatically delegates based on the `description` field. To encourage proactive use:

```yaml
description: Expert code reviewer. Use proactively after any code changes.
```

Or request explicitly:
```
Use the csv-editor sub-agent to fix the malformed data in exports/january.csv
```

---

## Commands: User-Invokable Prompts

Commands are slash commands you invoke manually (like `/review-finances`).

### Command File Format

`.claude/commands/review-code.md`:

```markdown
---
description: Review code for quality and security issues
argument-hint: <file_or_directory>
hooks:
  Stop:
    - type: command
      command: "python .claude/hooks/validators/lint-check.py"
---

Review the code at $ARGUMENTS for:

1. **Security issues:** SQL injection, XSS, exposed secrets
2. **Code quality:** Readability, naming, duplication
3. **Best practices:** Error handling, type hints, documentation

Provide feedback organized by severity:
- CRITICAL: Must fix before merge
- WARNING: Should fix
- SUGGESTION: Consider improving
```

### Variables in Commands

| Variable | Value |
|----------|-------|
| `$ARGUMENTS` | Everything after the command name |
| `$CLAUDE_PROJECT_DIR` | Path to project root |

---

## The Nested Relationship

This is how the pieces fit together:

```
User invokes: /review-finances february.csv
        │
        ▼
┌─────────────────────────────────────────────────┐
│  COMMAND: review-finances.md                     │
│  - Defines the workflow                          │
│  - Has Stop hook: html-validator.py              │
│                                                  │
│  Workflow:                                       │
│  1. Normalize CSVs → calls normalize-csv-agent   │
│  2. Categorize → calls categorize-csv-agent      │
│  3. Generate graphs → calls graph-agent          │
│  4. Build dashboard → calls ui-agent             │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  SUB-AGENT: normalize-csv-agent.md              │
│  - Specialized for CSV normalization            │
│  - Has PostToolUse hook: csv-validator.py       │
│  - Has Stop hook: balance-validator.py          │
│                                                  │
│  Every time this agent reads/writes a CSV,      │
│  the validator runs automatically.              │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  VALIDATOR: csv-validator.py                     │
│  - Pure Python, deterministic                    │
│  - Checks: columns exist, dates valid, etc.     │
│  - Returns: {} (pass) or {"decision":"block"}   │
└─────────────────────────────────────────────────┘
```

### The Key Insight

- **Commands** define WHAT to do (the workflow)
- **Sub-agents** define HOW to do specific tasks (specialized workers)
- **Hooks** ensure VALIDATION happens (deterministic checks)
- **Validators** are the actual CHECK logic (Python scripts)

---

## Creating Templates

IndyDevDan uses code snippets (templates) to quickly scaffold new agents and commands.

### The Template Philosophy

Instead of writing each agent from scratch, create templates you can invoke:

1. **Agentic Prompt Template (AGP):** Base structure for any prompt
2. **Sub-Agent Template:** Structure for sub-agents
3. **Validator Template:** Structure for validation scripts

### Template: Sub-Agent

Save as a snippet or reference file:

```markdown
---
name: [agent-name]
description: [When Claude should delegate to this agent. Be specific.]
tools: [Read, Write, Edit, Bash, Grep, Glob]
model: [sonnet|opus|haiku|inherit]
hooks:
  PostToolUse:
    - matcher: "[Read|Write|Edit]"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/[validator-name].py"
  Stop:
    - type: command
      command: "python .claude/hooks/validators/[final-validator].py"
---

You are a [role] specialist.

## Purpose
[One sentence: what this agent does]

## Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Output Format
[How results should be formatted]
```

### Template: Validator Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]  # Add what you need
# ///

"""
[Validator Name]

Validates [what it validates] for [which agent/command].

Exit codes:
- 0: Validation passed
- 2: Validation failed (blocks agent, returns stderr)
"""

import json
import sys
from pathlib import Path

def validate(file_path: Path) -> list[str]:
    """
    Validate the file and return list of errors.
    Empty list = validation passed.
    """
    errors = []

    # Your validation logic here
    # Example:
    # if not file_path.exists():
    #     errors.append(f"File not found: {file_path}")

    return errors

def main():
    # Get file path from args or stdin
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
    else:
        # Read from stdin (hook passes context as JSON)
        stdin_data = sys.stdin.read()
        if stdin_data.strip():
            hook_input = json.loads(stdin_data)
            # Extract file path from hook context
            target = Path(hook_input.get("tool_input", {}).get("file_path", "."))
        else:
            target = Path(".")

    errors = validate(target)

    if errors:
        # Block and tell Claude what to fix
        print(json.dumps({
            "decision": "block",
            "reason": "Validation failed:\n" + "\n".join(f"- {e}" for e in errors)
        }))
        sys.exit(2)
    else:
        # Pass
        print(json.dumps({}))
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Template: Command

```markdown
---
description: [What this command does - shown in /help]
argument-hint: <required_arg> [optional_arg]
hooks:
  Stop:
    - type: command
      command: "python .claude/hooks/validators/[final-validator].py"
---

# [Command Name]

## Purpose
[What this command accomplishes]

## Arguments
- `$ARGUMENTS`: [What the user should provide]

## Workflow
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Validation
This command validates its output using [validator name].
If validation fails, fix the issues before completing.

## Example
```
/[command-name] path/to/file.csv
```
```

---

## Examples

### Example 1: CSV Validator Sub-Agent

`.claude/agents/csv-validator.md`:

```markdown
---
name: csv-validator
description: Validate and fix CSV files. Use when reading or modifying any CSV.
tools: Read, Write, Edit
model: sonnet
hooks:
  PostToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "python .claude/hooks/validators/csv-structure.py"
---

You are a CSV validation specialist.

## Purpose
Ensure CSV files are well-formed and consistent.

## When Invoked
1. Check the CSV structure (headers, row counts, data types)
2. Identify any malformed rows
3. Fix issues or report what needs manual attention

## Validation Rules
- All rows must have same number of columns as header
- No empty headers allowed
- Dates should be ISO 8601 (YYYY-MM-DD)
- Numbers should not have currency symbols

Your PostToolUse hook validates CSV structure automatically.
If validation fails, you'll receive specific errors to fix.
```

### Example 2: Git Safety Hook

`.claude/hooks/validators/git-safety.py`:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""Block dangerous git operations."""

import json
import sys
import re

BLOCKED_PATTERNS = [
    r"git\s+push\s+.*--force",
    r"git\s+push\s+-f",
    r"git\s+reset\s+--hard",
    r"git\s+clean\s+-fd",
    r"git\s+checkout\s+\.",  # Discard all changes
]

def main():
    stdin_data = sys.stdin.read()
    if not stdin_data.strip():
        print(json.dumps({}))
        sys.exit(0)

    hook_input = json.loads(stdin_data)
    command = hook_input.get("tool_input", {}).get("command", "")

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            print(json.dumps({
                "decision": "block",
                "reason": f"Blocked dangerous git command: {command}\n\nIf you really need to do this, ask the user for explicit confirmation."
            }))
            sys.exit(2)

    print(json.dumps({}))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Common Questions

### Q: Where do I put the .claude/ directory?
**A:** In your project root, next to your README.md. Commit it to version control so your team shares the same agents.

### Q: How do I test a hook without running Claude?
**A:** Run the validator script directly:
```bash
echo '{"tool_input": {"file_path": "test.csv"}}' | python .claude/hooks/validators/csv-validator.py
```

### Q: Can I have project-specific AND global agents?
**A:** Yes. Put global agents in `~/.claude/agents/`. Project agents override global ones with the same name.

### Q: How do I see which hooks fired?
**A:** Add logging to your validators. IndyDevDan logs to a `logs/` directory with timestamps.

### Q: What if my validator is slow?
**A:** Hooks run synchronously. Keep validators fast (<1 second). For heavy validation, consider running only on Stop hook instead of PostToolUse.

### Q: Can hooks call other hooks?
**A:** No. Hooks are flat. But a command can invoke sub-agents, and each sub-agent can have its own hooks.

### Q: How do I debug when Claude ignores my agent?
**A:** Check the `description` field. Claude uses this to decide when to delegate. Make it very specific about when to use the agent.

---

## Resources

### Official Documentation
- [Claude Code Sub-Agents](https://code.claude.com/docs/en/sub-agents)
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code Custom Commands](https://code.claude.com/docs/en/custom-commands)

### IndyDevDan's Repos (Pattern Examples)
- [agentic-finance-review](https://github.com/disler/agentic-finance-review) - Full pipeline with self-validating agents
- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - All 8 hook types demonstrated
- [single-file-agents](https://github.com/disler/single-file-agents) - Compact agent patterns

### Video Reference
- [The Claude Code Feature Senior Engineers KEEP MISSING](https://youtu.be/u5GkG71PkR0) - IndyDevDan's walkthrough

---

## Next Steps

1. **Start simple:** Create one validator (csv-validator.py)
2. **Wire it up:** Create one sub-agent that uses the validator
3. **Test it:** Break a CSV and watch the hook catch it
4. **Expand:** Add more agents as you identify patterns

Remember: The goal is **deterministic validation**, not more prompting. If you can check it with code, check it with code.

---

*Created: 2026-01-20*
*Source: IndyDevDan patterns + Claude Code official docs*
