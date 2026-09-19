# project-scaffolding forensic audit

**Date:** 2026-09-18 ~23:10 ET (America/New_York)  
**Machine:** Erik's MacBook (`20a4703f-f707-4ee4-91d3-5c820d987498`)  
**Path:** `/Users/eriksjaastad/projects/project-scaffolding`  
**Git:** `https://github.com/eriksjaastad/project-scaffolding.git` @ `ceeff02` (2026-09-13), dirty: `EXTERNAL_RESOURCES.yaml` (+71/-8 uncommitted)

---

## 1. Executive verdict

**Do not archive or delete yet.** Nothing is *running* (no PATH install, LaunchAgent, cron, or process), but three **load-bearing portfolio assets** still live inside this repo and are referenced live:

1. `EXTERNAL_RESOURCES.yaml` (~1222 lines) — canonical registry; `pt info external_resources_doc` still points here. project-tracker's local copy is a 21-line stub.
2. `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` — still cited as canonical by `~/.claude/skills/intake/SKILL.md` (and historically by code-reviewer / many CLAUDE.md forks).
3. Locked hygiene blocks in **~24 CLAUDE.md** and **~12 AGENTS.md** files that still tell agents to run `scaffold sync --apply` from project-scaffolding.

The board already has the right plan: **#6833 → #6838 then #6839 archive**. agent-runtime-config replaced the push/filler role; scaffolding is leftover infrastructure + stale docs + dangerous-if-someone-runs-sync CLI.

**Mac Mini was not involved.** This tree is on the MacBook. An earlier worker failed because it only had the Linux box FS, not because of Mini vs Book.

---

## 2. What still runs or is wired

| Item | Status | Evidence |
| --- | --- | --- |
| `scaffold` on PATH | **Not installed** | `which scaffold` → not found; not in uv-tool/pipx; not in ~/bin or Homebrew bin |
| LaunchAgents / crontab / pgrep | **Clear** | no matches |
| Shell rc aliases | **Clear** | no hits in ~/.zshrc etc. |
| CLI still callable from repo | **Yes (manual)** | `cd …/project-scaffolding && uv run python scaffold_cli.py --help` → commands: `install-hygiene`, `review`, `seats`, `sync` |
| Auto sync | **None** | card #6833 notes + this audit: nothing schedules sync |
| `pt` project record | **Present** | `pt status project-scaffolding` — last modified 2026-09-13; description still "Health checks, multi-AI review…" |
| Dirty working tree | **Yes** | uncommitted edits to `EXTERNAL_RESOURCES.yaml` |

---

## 3. External references

### Live dependency (would break or strand data if archived blindly)

| Ref | Class | Evidence |
| --- | --- | --- |
| `pt info external_resources_doc` → `~/projects/project-tracker/EXTERNAL_RESOURCES.yaml` | **LIVE** | `pt info get external_resources_doc`; file 1222 lines vs PT stub 21 lines |
| `~/.claude/skills/strategy/SKILL.md` reads that YAML | **LIVE** | Pre-flight step 1 |
| `~/.claude/skills/intake/SKILL.md` cites governance protocol path | **LIVE pointer** | "Canonical governance doc: `$PROJECTS_ROOT/project-tracker/REVIEWS_AND_GOVERNANCE_PROTOCOL.md`" |
| Hygiene blocks in ~24 CLAUDE.md / ~12 AGENTS.md | **LIVE docs / latent footgun** | find+grep `scaffold sync --apply`; still instruct agents to run sync from this repo |
| `~/.claude/commands/scaffold.md` + `init-project.md` | **LIVE commands** | `uv run scaffold_cli.py apply …` against this repo |
| `~/.claude/agents/card-factory.md` | **LIVE mention** | lists `project-scaffolding` (templates) |
| `~/projects/CLAUDE.md` + `AGENTS.md` | **LIVE portfolio docs** | name `scaffold sync (project-scaffolding)` |
| GitHub remote | **Exists** | origin still active; last merge 2026-09-13 |

### Stale / nostalgia (safe to strip; scripts missing)

| Ref | Class | Evidence |
| --- | --- | --- |
| `~/projects/AGENT_QUICK_REFERENCE.md` rows for sync_agent_configs, validate_agent_sync, reindex_projects, update_cursorrules, archive_reviews, Documents/*, templates as "start a new project" | **STALE** | those scripts/paths **do not exist** under `scripts/` or `agentsync/` (only `agentsync/sync_mcp.py` remains) |
| README "agentsync retired March 2026" | **Accurate history** | matches empty agentsync except sync_mcp.py |
| Project-workflow.md agentsync history | **Historical** | version notes only |

### Self / superseded

| Ref | Class | Evidence |
| --- | --- | --- |
| `scaffold/hygiene.py` emits the locked block text | **Source of footgun** | footer row still says `scaffold sync --apply (from project-scaffolding)` |
| agent-runtime-config `shared_blocks.py` | **Successor aware of legacy** | comments treat `scaffold:hygiene` as other-tool / legacy; ARC is the replacement instruction-writer |
| seats / model-bench | **Mostly inert** | model-bench discovers per-project `seats.yaml`; card #6533 (2026-08-06) says seat-fit program killed — do **not** rehome seats schema as if it were a live keystone |

### Tools that could not help

| Tool | Result |
| --- | --- |
| `grepai` | **Broken today** — Ollama 404 `nomic-embed-text` missing. Multi-method search used ripgrep + find + targeted reads instead. |

---

## 4. Useful extract candidates

| Asset | Move to | Why |
| --- | --- | --- |
| `EXTERNAL_RESOURCES.yaml` (+ uncommitted dirty edits — commit or diff-review first) | **project-tracker** (preferred: next to `pt`, already has stub + parser) **or** agent-runtime-config | Live `pt info` + strategy skill |
| `REVIEWS_AND_GOVERNANCE_PROTOCOL.md` | **agent-runtime-config** or fold into `~/.claude/agents/code-reviewer.md` | Intake + review protocol; avoid orphaning |
| `agentsync/sync_mcp.py` (if still used) | **_tools** or agent-runtime-config | Only remaining agentsync piece — verify callers before move |
| `templates/git-hooks/`, `templates/github-workflows/`, useful templates | **_tools** (optional) | Reference only; low urgency |
| `scaffold review` / multi-AI review | **Decide** keep as tiny _tools CLI or drop if unused | Callable but not on PATH; no evidence of scheduled use |
| `templates/seats.*` + `scaffold seats` | **Archive with project** (per #6533) | Seat-fit program void; model-bench does not need the schema rehomed |

---

## 5. Safe to unplug (after rehomes)

**Not yet.** Sequence already on the board:

1. **#6833** — neutralize or remove `scaffold sync --apply` (safety: can CREATE AGENTS.md in repos that lack one).
2. **#6834** — rehome EXTERNAL_RESOURCES.yaml + `pt info set external_resources_doc …`.
3. **#6835** — rehome governance protocol + repoint intake/code-reviewer.
4. **#6836** — strip scaffold-command advertising from hygiene blocks (or replace via ARC).
5. **#6837** — retire/repoint ~/.claude skills/commands (`/scaffold`, `/init-project` likely full retire).
6. **#6838** — templates fate (seats → archive-in-place per #6533).
7. **#6839** — move repo to `_archive`.

Also strip/rewrite **AGENT_QUICK_REFERENCE.md** and root CLAUDE/AGENTS mentions so agents stop being sent into a ghost toolkit.

---

## 6. Board card recommendations (21 Backlog + 6 Cancelled)

### Execute / keep (decommission spine)

| Card | Action |
| --- | --- |
| #6833–#6839 | **Keep & execute in order** — this *is* the retire plan |
| #6533 | **Align with #6838/#6839** — seats not a blocker; archive seats with project |

### Cancel or backlog-as-wontfix (scaffolding improvement work)

| Card | Action |
| --- | --- |
| #6792 AGENTS.md parity | Cancel or move to agent-runtime-config if still wanted |
| #6123 / #6122 binary artifact hygiene | Move to portfolio/_tools or project-tracker — not scaffolding-specific |
| #6067 Doppler pattern | Move to agent-runtime-config / portfolio docs |
| #6201 track() in review.py | Cancel if retiring review CLI; else tiny follow-up before archive |
| #6780 PROGRESS.md gitignore | Portfolio hygiene — move off this board |
| #6779 / #6778 / #6777 gha/hook bugs | Move to `_tools` / claude-user-config — not scaffolding |
| #6504 packaging drift | Only if keeping review CLI; else cancel with archive |
| #6462 / #6117 / #6116 scaffold guidance fixes | **Cancel** — superseded by decommission; don't invest in generator |

### Already Cancelled (leave)

#6096, #5548, #5111, #5110, #5210, #5204

---

## 7. Risks / unknowns

- Uncommitted `EXTERNAL_RESOURCES.yaml` diff may contain important registry edits — review before move/commit.
- Whether anything still *invokes* `scaffold review` interactively was not proven (no PATH, no hooks); absence of automation ≠ zero human use.
- code-reviewer.md no longer greps to the governance path in a quick scan; intake still does — confirm code-reviewer text before rehoming (#6835 notes may be slightly stale).
- grepai unavailable (missing embedding model) — semantic search gap; lexical search was thorough.
- Mac Mini not scanned; Erik believes this lives only on MacBook — consistent with this audit.

---

## 8. Suggested next actions (ordered)

1. **Do not run** `scaffold sync --apply` / `install-hygiene --apply` portfolio-wide.
2. Start **#6833** (disable or delete sync create behavior) — cheapest safety win.
3. Rehome **EXTERNAL_RESOURCES.yaml** → project-tracker + update `pt info` + strategy skill (#6834).
4. Rehome **REVIEWS_AND_GOVERNANCE_PROTOCOL.md** + repoint intake (#6835).
5. Strip hygiene advertising + retire `/scaffold` + `/init-project` (#6836–#6837).
6. Archive repo (#6839); cancel leftover "improve scaffolding" cards.
7. Optional: fix grepai Ollama model later — unrelated.

**No deletions performed in this audit.**
