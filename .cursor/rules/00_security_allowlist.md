# Security: Default-Deny Command Policy (Allowlist)

## Objective
Reduce blast radius. Agent may only execute a minimal, explicitly approved set of commands.
Everything else requires manual approval (or is forbidden).

## Defaults
- Default: **DENY** auto-run for all terminal commands.
- Require manual approval for any command that:
  - writes outside the repo
  - modifies git state (add/commit/push)
  - installs dependencies
  - touches secrets/credentials
  - uses the network
  - spawns an interactive shell / REPL

## Allowed Commands (Auto-Approved) — Read-only & Low-Risk
Only within the repository root:
- `pwd`
- `ls` (no recursive flags that dump huge trees)
- `cat <repo-file>`
- `rg <pattern> <path>`
- `sed -n ... <repo-file>` (print-only)
- `head|tail <repo-file>`
- `git status`
- `git diff`
- `git log -n <small-number>`

## Allowed Commands (Approval Required) — Build/Test/Format
Allowed only with:
- repo scope
- no network
- max runtime (e.g., 60–180s)
- no writing outside repo

Examples:
- `npm test` / `pnpm test` / `pytest`
- `npm run lint` / `ruff check`
- `prettier --check`
- formatters that write files **only** under repo (approval required)

## Forbidden Commands (Never Auto-Run; Preferably Block)
- Privilege escalation: `sudo`, `su`, `doas`
- Destructive filesystem: `mkfs`, `dd`, `shutdown`, `reboot`
- File deletion: Use `trash <file>` instead (enforced at shell level)
- Network download/execute: `curl|sh`, `wget ... | bash`
- Secret exfil / credential access: anything reading `~/.ssh`, keychains, env dumps
- Interactive shells / REPLs in auto-run: `bash`, `zsh`, `fish`, `python -i`, `node`, `rails c`, etc.
- Git mutation in auto-run: `git add`, `git commit`, `git push`, `git reset --hard`, `git clean -fd`

## Safety Requirements
- Never modify files in: `.env`, `.cursor`, `.git`, `~/.ssh`, keychain locations.
- Never write outside repo root.
- Never use network unless explicitly approved.
- Always show the exact command before execution when approval is required.

## Escalation
If a task requires forbidden operations:
1) explain why
2) propose a safer alternative
3) ask for explicit approval + exact command

---
*Synced from project-scaffolding governance templates*
