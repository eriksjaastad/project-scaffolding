"""
Locked Hygiene Contract installer.

Phase E of the locked-hygiene umbrella (project-tracker card #6118): installs
the portfolio-wide hygiene fragment into every project under PROJECTS_ROOT.

Responsibilities
----------------
- Maintain the canonical hygiene fragment (text inserted into each project's
  CLAUDE.md / AGENTS.md between sentinel markers).
- Add ``.scratch/`` to each project's ``.gitignore`` (line-additive only).
- Provide idempotent install + drift detection so re-running is a no-op when
  the fragment is already current.

Cross-references
----------------
The fragment documents the hygiene contract enforced by:

- Phase B: ``~/.claude/hooks/branch-on-first-edit.py`` (PreToolUse Edit/Write
  gate while HEAD is ``main``/``master``/``trunk``; bypass via
  ``PT_ALLOW_MAIN_EDIT=1``; any path containing ``.scratch/`` passes
  unconditionally).
- ``~/.claude/hooks/stale-workspace-reporter.py`` (non-blocking Stop reminder
  for stale branches/stashes, throttled to once per day per repo). This
  replaced the former Phase C ``locked-session-end-gate.py``, which was removed:
  ``Stop`` fires after every turn (not at session end), so a *blocking* gate
  there trapped any dirty repo in a per-turn loop. Visibility, not enforcement.
- Phase D: ``pt handoff create | list | resolve | show`` (project-tracker).
- Phase F: ``pt migration start | finish | list`` (project-tracker).

Design decisions (from coordinator)
-----------------------------------
1. Fragment is bounded by HTML-comment markers so ``scaffold sync`` can refresh
   the block without disturbing surrounding content. Appended to EOF if missing.
2. ``.gitignore`` is line-additive; never re-ordered.
3. Project discovery for ``--all`` uses ``PROJECTS_ROOT.iterdir()`` filtered to
   directories with a ``.git/``, minus ``PROTECTED_PROJECTS``.
4. Dry-run is the default; ``--apply`` is required to mutate files.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from scaffold.constants import PROJECTS_ROOT, PROTECTED_PROJECTS

# Sentinel markers used to delimit the managed block.
BEGIN_MARKER = "<!-- BEGIN scaffold:hygiene -->"
END_MARKER = "<!-- END scaffold:hygiene -->"

# Generated-mirror header for AGENTS.md (#6680).
#
# FORMAT OWNER: agent-runtime-config's `runtime_doctor/compile/instructions.py`
# (GENERATED_PREFIX / INSTRUCTION_LINE). It is duplicated here rather than
# imported because these are separate repos with no dependency between them.
# The bytes MUST stay identical: runtime-doctor's `_is_managed_agents` keys
# off the first line, and monitor reports a mismatch as `agents_unmanaged`.
# `test_agents_mirror_matches_runtime_doctor_format` pins the exact strings.
AGENTS_GENERATED_PREFIX = "<!-- GENERATED FROM:"
AGENTS_INSTRUCTION_LINE = (
    "<!-- DO NOT EDIT DIRECTLY. "
    "Edit CLAUDE.md and re-run ~/.claude/scripts/sync-claude-md-to-agents-md.sh -->"
)

# Regex finds the managed block (greedy across newlines). Used for both
# extraction and replacement. Capture group 1 is the *inner* body between
# markers, exclusive of leading/trailing newlines on the marker lines.
_BLOCK_RE = re.compile(
    re.escape(BEGIN_MARKER) + r"\n(.*?)\n" + re.escape(END_MARKER),
    re.DOTALL,
)

# Files we mirror the fragment into when they exist alongside each other.
DOC_FILENAMES = ("CLAUDE.md", "AGENTS.md")

# Line we add to .gitignore. Matched by the regex below for idempotency.
GITIGNORE_LINE = ".scratch/"
_GITIGNORE_RE = re.compile(r"^\.scratch/?$", re.MULTILINE)


def fragment_body() -> str:
    """
    Canonical hygiene contract body.

    This is the *content* between the markers — markers themselves are added
    by ``render_fragment``. Keep this string stable; ``scaffold sync`` uses
    byte-for-byte comparison to detect drift.
    """
    return (
        "## Locked Hygiene Contract\n"
        "\n"
        "This project participates in the portfolio-wide locked hygiene contract\n"
        "installed by `scaffold install-hygiene`. The contract is enforced by user-scope\n"
        "hooks in `~/.claude/` and by `pt` CLI commands in project-tracker. **Do not edit\n"
        "this block by hand** — `scaffold sync` rewrites it. Add project-specific notes\n"
        "outside the markers.\n"
        "\n"
        "### What the contract requires\n"
        "\n"
        "1. **No direct edits on `main`/`master`/`trunk`.** A PreToolUse hook blocks\n"
        "   `Edit`/`Write`/`MultiEdit`/`NotebookEdit` on tracked files while HEAD is the\n"
        "   default branch. Work happens on feature branches; PRs are how changes land.\n"
        "2. **Stale branches and stashes are surfaced, not blocked.** A non-blocking\n"
        "   reminder flags merged-but-undeleted branches and leftover stashes (at most\n"
        "   once per day per repo). Run `/cleanup` to clear them. Nothing ever blocks a\n"
        "   session from ending — visibility, not enforcement.\n"
        "3. **Audit trail for bulk changes.** Multi-file refactors, renames, and doc\n"
        "   reorgs run inside `pt migration start <name>` … `pt migration finish <name>`\n"
        "   so they are reversible (`--revert` uses `git restore` for tracked paths and\n"
        "   `send2trash` for untracked — never raw `rm`).\n"
        "4. **Handoffs for work in progress.** If a session ends mid-task (mid-rebase,\n"
        "   mid-investigation), record it: `pt handoff create <card-pk> --branch <b>\n"
        "   --intent <s> --status <s> --next <s> --guidance preserve|discard` so the next\n"
        "   session or machine can pick it up cleanly.\n"
        "\n"
        "### Safety valves\n"
        "\n"
        "- **`.scratch/`** — every project has a gitignored `.scratch/` at its repo root.\n"
        "  The branch-on-first-edit hook lets edits under any `.scratch/` subdir through\n"
        "  unconditionally. Use it for throwaway notes, probe scripts, and reading-mode\n"
        "  poking. Files there never reach a PR. If `.scratch/` work turns into real work,\n"
        "  move it out before committing.\n"
        "- **`PT_ALLOW_MAIN_EDIT=1`** — one-shot env var to bypass the main-edit hook.\n"
        "  Use sparingly; intended for emergency fixes and tooling that must touch the\n"
        "  default branch.\n"
        "- **`pt handoff`** — durable record of in-progress work, carried across\n"
        "  sessions and machines.\n"
        "\n"
        "### Quick reference\n"
        "\n"
        "| Action                          | Command                                       |\n"
        "| ------------------------------- | --------------------------------------------- |\n"
        "| Start a recorded bulk migration | `pt migration start <name>`                   |\n"
        "| Finish + write `MIGRATIONS.md`  | `pt migration finish <name>`                  |\n"
        "| Revert a migration              | `pt migration finish <name> --revert`         |\n"
        "| Open a handoff                  | `pt handoff create <card-pk> --branch <b> …`  |\n"
        "| List open handoffs              | `pt handoff list`                             |\n"
        "| Resolve a handoff               | `pt handoff resolve <id>`                     |\n"
        "| Refresh this block portfolio-wide | `scaffold sync --apply` (from project-scaffolding) |\n"
    )


def render_fragment() -> str:
    """Return the full marker-wrapped block."""
    return f"{BEGIN_MARKER}\n{fragment_body()}{END_MARKER}\n"


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def discover_projects(root: Path | None = None) -> list[Path]:
    """
    Return the set of project directories eligible for the hygiene contract.

    Eligible = direct child of ``root`` AND has a ``.git/`` subdir AND is not
    listed in PROTECTED_PROJECTS (the union of ``ignore_projects`` and
    ``protected_projects`` from ``config/scan_config.yaml``).
    """
    base = root or PROJECTS_ROOT
    if not base.exists():
        return []
    found = []
    for child in sorted(base.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name in PROTECTED_PROJECTS:
            continue
        if not (child / ".git").exists():
            continue
        found.append(child)
    return found


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


@dataclass
class FileChange:
    """One file's planned change. ``before`` is empty for newly created files."""

    path: Path
    before: str
    after: str
    note: str = ""

    @property
    def is_noop(self) -> bool:
        return self.before == self.after

    def unified_diff(self) -> str:
        before_lines = self.before.splitlines(keepends=True) if self.before else []
        after_lines = self.after.splitlines(keepends=True)
        return "".join(
            difflib.unified_diff(
                before_lines,
                after_lines,
                fromfile=str(self.path) + " (current)",
                tofile=str(self.path) + " (planned)",
                n=2,
            )
        )


@dataclass
class ProjectResult:
    """Aggregate plan/result for one project."""

    project: Path
    changes: list[FileChange] = field(default_factory=list)
    skipped: bool = False
    skip_reason: str = ""
    error: str = ""

    @property
    def has_changes(self) -> bool:
        return any(not c.is_noop for c in self.changes)

    @property
    def status(self) -> str:
        if self.error:
            return "error"
        if self.skipped:
            return "skipped"
        if self.has_changes:
            return "changes"
        return "ok"


# ---------------------------------------------------------------------------
# Per-file planners
# ---------------------------------------------------------------------------


def _plan_gitignore(project: Path) -> FileChange:
    gi = project / ".gitignore"
    before = gi.read_text() if gi.exists() else ""
    if _GITIGNORE_RE.search(before):
        return FileChange(path=gi, before=before, after=before, note=".scratch/ already ignored")
    # Append; preserve trailing newline discipline.
    if before and not before.endswith("\n"):
        after = before + "\n" + GITIGNORE_LINE + "\n"
    else:
        after = before + GITIGNORE_LINE + "\n"
    return FileChange(path=gi, before=before, after=after, note="add .scratch/")


def _plan_doc(doc_path: Path, project_name: str) -> FileChange | None:
    """
    Plan the CLAUDE.md / AGENTS.md update for one project.

    Returns ``None`` if the file should be skipped (e.g., multiple marker pairs
    — refuse to auto-merge). Returns a no-op FileChange when the block is
    already current.

    Behavior:

    * No file → create with a minimal ``# CLAUDE.md - <name>`` header plus the
      fragment.
    * File without markers → append fragment at EOF (with separating blank
      line).
    * File with exactly one marker pair → replace block in-place.
    * File with multiple marker pairs → return change with note and after=before
      (caller treats this as an error needing manual cleanup).
    """
    fragment = render_fragment()

    if not doc_path.exists():
        header = f"# CLAUDE.md - {project_name}\n\n"
        after = header + fragment
        return FileChange(path=doc_path, before="", after=after, note="create file")

    before = doc_path.read_text()
    matches = list(_BLOCK_RE.finditer(before))

    if len(matches) > 1:
        # Refuse to auto-merge corrupted state.
        return FileChange(
            path=doc_path,
            before=before,
            after=before,
            note=f"REFUSED: {len(matches)} marker pairs found — manual cleanup required",
        )

    if len(matches) == 1:
        # Replace the existing block (markers + body) with the canonical render.
        # ``fragment`` includes both markers and a trailing newline.
        start, end = matches[0].span()
        # Strip the trailing newline of fragment to avoid double-newline if the
        # following character is already a newline.
        replacement = fragment.rstrip("\n")
        after = before[:start] + replacement + before[end:]
        if after == before:
            return FileChange(path=doc_path, before=before, after=before, note="fragment current")
        return FileChange(path=doc_path, before=before, after=after, note="refresh fragment")

    # No markers — append at EOF with a separating blank line.
    sep = "" if before.endswith("\n\n") else ("\n" if before.endswith("\n") else "\n\n")
    after = before + sep + fragment
    return FileChange(path=doc_path, before=before, after=after, note="append fragment")


# ---------------------------------------------------------------------------
# Public planner
# ---------------------------------------------------------------------------


def plan_for_project(project: Path) -> ProjectResult:
    """Build the full plan for one project (no writes)."""
    result = ProjectResult(project=project)
    if not project.exists() or not project.is_dir():
        result.error = f"not a directory: {project}"
        return result
    if not (project / ".git").exists():
        result.skipped = True
        result.skip_reason = "no .git/ (not a git repo)"
        return result
    if project.name in PROTECTED_PROJECTS:
        result.skipped = True
        result.skip_reason = "in PROTECTED_PROJECTS"
        return result

    # .gitignore
    result.changes.append(_plan_gitignore(project))

    # CLAUDE.md / AGENTS.md
    # Update CLAUDE.md if it exists OR AGENTS.md doesn't exist either (then we
    # create CLAUDE.md).
    claude = project / "CLAUDE.md"
    agents = project / "AGENTS.md"
    claude_change = None
    if claude.exists() or not agents.exists():
        claude_change = _plan_doc(claude, project.name)
        if claude_change is not None:
            result.changes.append(claude_change)

    if agents.exists():
        change = _plan_doc(agents, project.name)
        if change is not None:
            result.changes.append(change)
    elif claude_change is not None and not claude_change.note.startswith("REFUSED"):
        # #6680: create the mirror instead of silently excluding Codex.
        #
        # The REFUSED guard is load-bearing. `_plan_doc` returns a REFUSED
        # FileChange (never None — the docstring is wrong about that) when
        # CLAUDE.md carries multiple marker pairs, and `apply_result`
        # correctly declines to write it. Without this check the mirror was
        # still built from `claude_change.after`, which for a REFUSED change
        # equals the corrupted `before` — so `scaffold sync --apply` would
        # mint a brand-new AGENTS.md containing the very corruption the tool
        # had just refused to touch. Refusing to auto-merge has to mean
        # refusing to propagate.
        # Before this, AGENTS.md was updated only if it already existed, so
        # every rule synced into CLAUDE.md reached Claude and skipped Codex
        # — ai-memory had no AGENTS.md at all and Codex working there got no
        # project instructions whatsoever.
        #
        # Mirror from the PLANNED CLAUDE.md content, not what is on disk:
        # this pass may be inserting or updating the hygiene block, and a
        # mirror of the pre-change bytes would be stale the moment it lands.
        result.changes.append(_plan_agents_mirror(agents, claude, claude_change.after))

    return result


def render_agents_mirror(claude_path: Path, claude_text: str) -> str:
    """Render AGENTS.md as a generated mirror of CLAUDE.md (#6680).

    Shape is fixed by runtime-doctor (see AGENTS_GENERATED_PREFIX above):
    marker line, instruction line, blank line, then the CLAUDE.md body
    byte-for-byte. A plain copy would also "work" for Codex, but nothing
    could then distinguish a stale copy from a hand-authored file — which is
    exactly how the portfolio root AGENTS.md drifted for five weeks unnoticed.

    The marker path is rendered home-relative so the file is identical on
    every machine.

    One documented divergence from runtime-doctor's `_build_managed_bytes`:
    a CRLF source is normalized to LF here, because `claude_text` has been
    through `_plan_doc`'s text-mode read/write round trip, while
    runtime-doctor reads with `read_bytes()` and preserves CRLF verbatim.
    Pre-existing `_plan_doc` behavior, not introduced with the mirror, and
    inert on this all-POSIX portfolio — but "byte-for-byte" is not literally
    true for that one input.
    """
    try:
        rel = claude_path.resolve().relative_to(Path.home())
        source = f"~/{rel}"
    except ValueError:
        source = str(claude_path)
    return (
        f"{AGENTS_GENERATED_PREFIX} {source} -->\n"
        f"{AGENTS_INSTRUCTION_LINE}\n"
        "\n"
        f"{claude_text}"
    )


def _plan_agents_mirror(agents_path: Path, claude_path: Path, claude_text: str) -> FileChange:
    before = agents_path.read_text() if agents_path.exists() else ""
    after = render_agents_mirror(claude_path, claude_text)
    return FileChange(
        path=agents_path,
        before=before,
        after=after,
        note="create AGENTS.md mirror",
    )


# ---------------------------------------------------------------------------
# Drift detection (used by ``scaffold sync``)
# ---------------------------------------------------------------------------


@dataclass
class DriftReport:
    project: Path
    file: Path
    drift: bool
    detail: str = ""


def detect_drift(project: Path) -> list[DriftReport]:
    """
    Compare each project's hygiene block (between markers) against the canonical
    fragment. Returns one DriftReport per CLAUDE.md/AGENTS.md examined.

    A project with no markers at all is reported as drift (= "missing block").
    """
    reports: list[DriftReport] = []
    canonical = fragment_body()
    for fname in DOC_FILENAMES:
        doc = project / fname
        if not doc.exists():
            continue
        text = doc.read_text()
        matches = list(_BLOCK_RE.finditer(text))
        if not matches:
            reports.append(DriftReport(project=project, file=doc, drift=True, detail="no markers"))
            continue
        if len(matches) > 1:
            reports.append(
                DriftReport(
                    project=project,
                    file=doc,
                    drift=True,
                    detail=f"{len(matches)} marker pairs (manual cleanup)",
                )
            )
            continue
        body = matches[0].group(1) + "\n"
        if body != canonical:
            reports.append(DriftReport(project=project, file=doc, drift=True, detail="content drift"))
        else:
            reports.append(DriftReport(project=project, file=doc, drift=False))
    return reports


# ---------------------------------------------------------------------------
# Apply
# ---------------------------------------------------------------------------


def apply_result(result: ProjectResult) -> list[FileChange]:
    """
    Write the planned changes to disk. Returns the list of changes that were
    actually written (excludes no-ops and the "refused" sentinel). Refuses to
    write a FileChange whose ``note`` starts with ``REFUSED``.
    """
    written: list[FileChange] = []
    for change in result.changes:
        if change.is_noop:
            continue
        if change.note.startswith("REFUSED"):
            continue
        change.path.parent.mkdir(parents=True, exist_ok=True)
        change.path.write_text(change.after)
        written.append(change)
    return written


def is_refused(result: ProjectResult) -> bool:
    """True if any planned change is in the REFUSED state."""
    return any(c.note.startswith("REFUSED") for c in result.changes)


# ---------------------------------------------------------------------------
# Convenience
# ---------------------------------------------------------------------------


def iter_projects(
    targets: Iterable[Path] | None,
    all_projects: bool,
    root: Path | None = None,
) -> list[Path]:
    """Resolve CLI arguments into a concrete project list."""
    if all_projects:
        return discover_projects(root)
    return [t.resolve() for t in (targets or [])]
