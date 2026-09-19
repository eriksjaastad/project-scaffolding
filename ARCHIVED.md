# ARCHIVED — 2026-09-19

**Why archived:** Function absorbed by agent-runtime-config (hygiene/instruction writing) and project-tracker (EXTERNAL_RESOURCES.yaml, REVIEWS_AND_GOVERNANCE_PROTOCOL.md). Decommission spine #6833–#6839 completed: `scaffold sync` / `install-hygiene` CLI removed, portfolio hygiene ads stripped, Claude `/scaffold` + `/init-project` retired, templates/`sync_mcp` left in-tree for archive (seat-fit void per #6533/#6838).

**Why kept, not deleted:** (1) Git history and forensic notes. (2) **model-bench** still imports the seats.v1 validator from `scaffold/seats.py` + `templates/seats.schema.v1.md` — path must resolve under `_archive/project-scaffolding` until model-bench is repointed or the validator is rehomed. (3) Template/docs corpus may still be useful for resurrection or citation.

**If resurrecting:** read `FORENSIC_AUDIT_2026-09-18.md`, `PROGRESS.md` if present, and decommission cards #6833–#6839 notes on the project-scaffolding board (Done). Verify agent-runtime-config owns hygiene before restoring any CLI. Do not re-enable `scaffold sync --apply`.

**Resource disposition:**
| Resource | Disposition |
|---|---|
| Local tree | `~/projects/_archive/project-scaffolding/` |
| GitHub `eriksjaastad/project-scaffolding` | Archive read-only (Step 7) |
| Doppler `project-scaffolding` | Present — leave until secrets confirmed unused; do not delete blindly |
| launchd / cron | None found |
| Vercel / Railway | None for this repo |
| EXTERNAL_RESOURCES.yaml | Entry remains in project-tracker; mark archived |
| Claude `/scaffold`, `/init-project` | Retired stubs in `~/.claude/commands/` (#6837) |

## Inbound reference triage (2026-09-19)

### Fixed or already repointed
- EXTERNAL_RESOURCES + REVIEWS protocol live in `project-tracker/` (PRs #178 etc.).
- Hygiene blocks portfolio-wide: scaffold CLI ads stripped (#6836).
- `~/.claude/commands/scaffold.md` + `init-project.md`: RETIRED stubs.

### Load-bearing — must follow up (card / PR, not silently ignored)
- `_tools/model-bench/model_bench/seats.py` (+ tests/README): hard-coded `projects_root / "project-scaffolding"`. Update to `_archive/project-scaffolding` or rehome validator.
- `~/projects/AGENT_QUICK_REFERENCE.md`: many script/template paths under `project-scaffolding/` — rewrite to archive path or delete obsolete rows.
- `project-tracker/EXTERNAL_RESOURCES.yaml`: `project-scaffolding:` registry rows + DEEPSEEK note — mark archived / update paths.

### Cosmetic / historical — leave or card later
- Dated reviews, `_docs_archive`, PROGRESS.md mentions, image-workflow doc links, trading-copilot generated protocol header, twitter-growth seats.schema mention, job-search audit notes.
- `~/.claude/file-history/**`, session jsonl, hook logs — do-not-clean (dated/agent state).
- Unpushed local branch `fix/drop-rebase-from-hygiene-template` (`04b590e`) abandoned at archive time (hygiene template decommissioned; not landed).

### Internal stale refs
Frozen with the tree. Not rewritten.
