---
trigger: always_on
---

# Security: Default-Deny Command Policy (Allowlist)

## Goal
Minimize blast radius. The agent should behave as if it is in a hostile environment by default.

## Default stance
- Default: DO NOT auto-run terminal commands.
- Prefer "ask me first" over "guess if safe".
- If a task needs risky commands, pause and ask with the exact command + why.

## Allowed (low-risk, read-only) commands
Only inside the repo root:
- `pwd`
- `ls`
- `cat <repo-file>`
- `head|tail <repo-file>`
- `rg <pattern> <path>`
- `git status`
- `git diff`
- `git log -n <small-number>`

## Approval required (ok, but only with review)
- Running tests / linters / formatters:
  - `pytest`, `ruff`, `npm/pnpm/yarn test`, `go test`, `cargo test`, etc.
- Any command that writes files (even in-repo)
- Anything that changes git state:
  - `git add/commit/push`, `git reset`, `git clean`

## Forbidden / never auto-run
- Privilege escalation: `sudo`, `su`, `doas`
- Destructive filesystem: `mkfs`, `dd`, `shutdown`, `reboot`
- File deletion: Use `trash <file>` instead (enforced at shell level)
- Network download/execute: `curl|sh`, `wget ... | bash`
- Secrets/credential access: `~/.ssh`, keychains, `.env` dumps, `env | printenv`
- Interactive shells/REPLs: `bash`, `zsh`, `fish`, `python -i`, `node`, etc.

## Extra safety rules
- Never read or print secrets.
- Never write outside the repo.
- If a command touches the network, always request approval first.

---
*Synced from project-scaffolding governance templates*
