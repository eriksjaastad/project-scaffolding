# Claude Code Templates

This directory contains templates for setting up Claude Code hooks and sub-agents in your projects.

## Quick Start

1. **Copy the `.claude/` directory to your project root:**
   ```bash
   cp -r templates/claude-code/.claude /path/to/your-project/
   ```

2. **Customize `settings.json`** for your project's permissions

3. **Copy and rename agent/command templates** as needed

4. **Create validators** for your specific validation needs

## Directory Structure

```
.claude/
├── settings.json           # Permissions + global hooks
├── agents/                 # Sub-agents (Claude delegates to these)
│   └── _template.md        # Copy and rename for new agents
├── commands/               # Slash commands (you invoke these)
│   └── _template.md        # Copy and rename for new commands
└── hooks/
    └── validators/         # Python validation scripts
        └── _template.py    # Copy and rename for new validators
```

## Usage

### Creating a New Sub-Agent

1. Copy `agents/_template.md` to `agents/my-agent.md`
2. Update the frontmatter (name, description, tools, hooks)
3. Write the system prompt
4. Create any validators it references

### Creating a New Command

1. Copy `commands/_template.md` to `commands/my-command.md`
2. Update the frontmatter (description, argument-hint, hooks)
3. Write the command instructions
4. Test with `/my-command <args>`

### Creating a New Validator

1. Copy `hooks/validators/_template.py` to `hooks/validators/my-validator.py`
2. Implement your validation logic in the `validate()` function
3. Test directly: `echo '{}' | python .claude/hooks/validators/my-validator.py`

## Reference

See `Documents/reference/CLAUDE_CODE_HOOKS_AND_SUBAGENTS.md` for full documentation.
