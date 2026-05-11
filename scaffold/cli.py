"""
CLI for Project Scaffolding automation system
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Optional

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import click
from dotenv import load_dotenv
from rich.console import Console



def get_version() -> str:
    """Read version from pyproject.toml."""
    try:
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        if pyproject_path.exists():
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                return data.get("project", {}).get("version", "0.1.0")
    except Exception:
        pass
    return "0.1.0"


# Load environment variables from .env
load_dotenv()

console = Console(force_terminal=False)


@click.group()
@click.version_option(version=get_version())
def cli() -> None:
    """Project Scaffolding - Health Checks & Multi-AI Review System"""
    pass


@cli.command()
@click.option(
    "--type",
    "review_type",
    type=click.Choice(["document", "code"]),
    required=True,
    help="Type of review to run"
)
@click.option(
    "--input",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Path to document or code to review"
)
@click.option(
    "--round",
    "round_number",
    type=int,
    default=1,
    help="Review round number"
)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory (defaults to docs/reviews/ or docs/code_reviews/)"
)
@click.option(
    "--openai-key",
    envvar="SCAFFOLDING_OPENAI_KEY",
    help="OpenAI API key (or set SCAFFOLDING_OPENAI_KEY env var)"
)
@click.option(
    "--anthropic-key",
    envvar="SCAFFOLDING_ANTHROPIC_KEY",
    help="Anthropic API key (or set SCAFFOLDING_ANTHROPIC_KEY env var)"
)
@click.option(
    "--google-key",
    envvar="SCAFFOLDING_GOOGLE_KEY",
    help="Google AI API key (or set SCAFFOLDING_GOOGLE_KEY env var)"
)
@click.option(
    "--deepseek-key",
    envvar="SCAFFOLDING_DEEPSEEK_KEY",
    help="DeepSeek API key (or set SCAFFOLDING_DEEPSEEK_KEY env var)"
)
@click.option(
    "--ollama-model",
    envvar="SCAFFOLDING_OLLAMA_MODEL",
    default="llama3.2",
    help="Ollama model to use for local reviews (default: llama3.2)"
)
@click.option(
    "--ollama-host",
    envvar="SCAFFOLDING_OLLAMA_HOST",
    default="http://localhost:11434",
    help="Ollama host URL (default: http://localhost:11434)"
)
def review(
    review_type: str,
    input_path: Path,
    round_number: int,
    output_dir: Optional[Path],
    openai_key: Optional[str],
    anthropic_key: Optional[str],
    google_key: Optional[str],
    deepseek_key: Optional[str],
    ollama_model: str,
    ollama_host: str,
) -> None:
    """Run multi-AI review on a document or code.

    Example:
        scaffold review --type document --input docs/PRD.md
        scaffold review --type code --input src/main.py --round 2
    """
    from scaffold.review import create_orchestrator

    # Set output directory based on review type
    if output_dir is None:
        if review_type == "document":
            output_dir = Path("docs/reviews")
        else:
            output_dir = Path("docs/code_reviews")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Load review configurations
    prompt_dir = Path(__file__).parent / "prompts" / review_type
    if not prompt_dir.exists():
        console.print(f"[yellow]Skipping review: no prompts found for review type '{review_type}'[/yellow]")
        console.print(f"[yellow]Expected directory: {prompt_dir}[/yellow]")
        return

    configs = _load_review_configs(
        prompt_dir,
        openai_key,
        anthropic_key,
        google_key,
        deepseek_key,
        ollama_model
    )

    if not configs:
        console.print("[red]Error: No review configurations could be loaded (missing API keys?)[/red]")
        return

    console.print(f"\n[bold]Running {review_type} review (Round {round_number})[/bold]")
    console.print(f"  Input: {input_path}")
    console.print(f"  Output: {output_dir}")
    console.print(f"  Reviewers: {len(configs)}\n")

    # Run reviews
    orchestrator = create_orchestrator(configs, ollama_host)

    try:
        content = input_path.read_text()
        results = asyncio.run(orchestrator.run_reviews(content, round_number))

        # Save results
        for result in results:
            safe_name = result.reviewer_name.lower().replace(" ", "_")
            output_file = output_dir / f"round_{round_number}_{safe_name}.md"
            output_file.write_text(result.content)
            console.print(f"  [green]✓[/green] {result.reviewer_name} → {output_file}")

        # Calculate cost estimate
        total_tokens = sum(r.tokens_used for r in results if r.tokens_used)
        estimated_cost = total_tokens * 0.00001  # Rough estimate

        # Summary
        next_round = round_number + 1
        if round_number < 3:
            console.print("\n[bold yellow]Next steps:[/bold yellow]")
            console.print(f"  1. Review feedback in {output_dir}/")
            console.print("  2. Revise document based on feedback")
            console.print(f"  3. Run Round {next_round}:")
            console.print(f"     [cyan]scaffold review --type {review_type} --input {input_path} --round {next_round}[/cyan]")
            console.print(f"     Estimated cost: [green]${estimated_cost:.2f}[/green]\n")
        else:
            console.print("\n[bold green]Review process complete![/bold green]")
            console.print(f"  Total rounds: {round_number}")
            console.print(f"  Reviews saved to: {output_dir}\n")

    except Exception as e:
        console.print(f"[red]Error running review: {e}[/red]")
        raise


def _load_review_configs(
    prompt_dir: Path,
    openai_key: Optional[str],
    anthropic_key: Optional[str],
    google_key: Optional[str],
    deepseek_key: Optional[str],
    ollama_model: str
) -> List:
    """Load review configurations from prompt directory"""
    from scaffold.review import ReviewConfig
    configs = []

    # Map prompt names to API and model
    default_mapping = {
        "security": ("deepseek", "deepseek-chat", "Security Reviewer"),
        "performance": ("deepseek", "deepseek-chat", "Performance Reviewer"),
        "architecture": ("ollama", ollama_model, "Architecture Reviewer"),
        "quality": ("deepseek", "deepseek-chat", "Code Quality Reviewer"),
    }

    for prompt_file in sorted(prompt_dir.glob("*.md")):
        name_parts = prompt_file.stem.split("_")
        prefix = name_parts[0]

        if prefix in default_mapping:
            api, model, display_name = default_mapping[prefix]
        else:
            api = "openai"
            model = "gpt-4o"
            display_name = f"{prefix.title()} Reviewer"

        if api == "openai" and not openai_key:
            console.print(f"[red]✗ {display_name} requires OpenAI API key (SCAFFOLDING_OPENAI_KEY)[/red]")
            continue
        if api == "anthropic" and not anthropic_key:
            console.print(f"[red]✗ {display_name} requires Anthropic API key (SCAFFOLDING_ANTHROPIC_KEY)[/red]")
            continue
        if api == "google" and not google_key:
            console.print(f"[red]✗ {display_name} requires Google API key (SCAFFOLDING_GOOGLE_KEY)[/red]")
            continue
        if api == "deepseek" and not deepseek_key:
            console.print(f"[red]✗ {display_name} requires DeepSeek API key (SCAFFOLDING_DEEPSEEK_KEY)[/red]")
            continue

        configs.append(ReviewConfig(
            name=display_name,
            api=api,
            model=model,
            prompt_path=prompt_file
        ))

    return configs


# ---------------------------------------------------------------------------
# Locked Hygiene Contract — install / sync
# ---------------------------------------------------------------------------


def _print_project_result(result, apply: bool) -> None:
    """Render a ProjectResult to the console."""
    if result.error:
        console.print(f"[red]ERROR {result.project.name}: {result.error}[/red]")
        return
    if result.skipped:
        console.print(f"[dim]SKIP  {result.project.name} — {result.skip_reason}[/dim]")
        return
    if not result.has_changes:
        console.print(f"[green]OK    {result.project.name} (no changes needed)[/green]")
        return

    label = "WRITE" if apply else "PLAN "
    console.print(f"[yellow]{label} {result.project.name}[/yellow]")
    for change in result.changes:
        if change.is_noop:
            console.print(f"   [dim]·  {change.path.name}: {change.note}[/dim]")
            continue
        if change.note.startswith("REFUSED"):
            console.print(f"   [red]✗  {change.path.name}: {change.note}[/red]")
            continue
        marker = "✓" if apply else "→"
        console.print(f"   [cyan]{marker}  {change.path.name}: {change.note}[/cyan]")
        if not apply:
            diff = change.unified_diff()
            if diff:
                # Indent each diff line for readability.
                for line in diff.splitlines():
                    console.print(f"      {line}")


@cli.command("install-hygiene")
@click.argument(
    "targets",
    nargs=-1,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "--all",
    "all_projects",
    is_flag=True,
    default=False,
    help="Sweep every project under PROJECTS_ROOT (filtered by PROTECTED_PROJECTS).",
)
@click.option(
    "--apply",
    "apply",
    is_flag=True,
    default=False,
    help="Actually write changes. Default is dry-run (planning only).",
)
def install_hygiene(targets: tuple[Path, ...], all_projects: bool, apply: bool) -> None:
    """Install the locked-hygiene contract into one or more projects.

    Default mode is DRY-RUN — the command shows the planned diff and exits
    without touching the filesystem. Pass ``--apply`` to write.

    Examples:
        scaffold install-hygiene ~/projects/some-repo
        scaffold install-hygiene --all
        scaffold install-hygiene --all --apply
    """
    from scaffold import hygiene

    if not targets and not all_projects:
        console.print("[red]Provide a target directory or --all.[/red]")
        raise click.Abort()

    projects = hygiene.iter_projects(targets, all_projects)
    if not projects:
        console.print("[yellow]No projects matched.[/yellow]")
        return

    mode = "APPLY" if apply else "DRY-RUN"
    console.print(f"\n[bold]scaffold install-hygiene — {mode}[/bold] ({len(projects)} project(s))\n")

    summary: dict[str, int] = {"changes": 0, "ok": 0, "skipped": 0, "error": 0, "refused": 0}
    refused_projects: list[str] = []

    for project in projects:
        result = hygiene.plan_for_project(project)
        _print_project_result(result, apply=apply)
        if hygiene.is_refused(result):
            summary["refused"] += 1
            refused_projects.append(project.name)
            continue
        summary[result.status] += 1
        if apply and result.has_changes:
            hygiene.apply_result(result)

    console.print("\n[bold]Summary[/bold]")
    console.print(f"  changes : {summary['changes']}")
    console.print(f"  ok      : {summary['ok']}")
    console.print(f"  skipped : {summary['skipped']}")
    console.print(f"  refused : {summary['refused']}")
    console.print(f"  errors  : {summary['error']}")

    if refused_projects:
        console.print(
            "\n[red]Refused (manual cleanup):[/red] " + ", ".join(refused_projects)
        )

    if not apply and summary["changes"] > 0:
        console.print(
            "\n[yellow]Dry-run — no files written. Re-run with --apply to commit.[/yellow]"
        )


@cli.command("sync")
@click.argument(
    "targets",
    nargs=-1,
    type=click.Path(exists=True, file_okay=False, path_type=Path),
)
@click.option(
    "--all",
    "all_projects",
    is_flag=True,
    default=True,
    help="Scan every project under PROJECTS_ROOT (default).",
)
@click.option(
    "--apply",
    "apply",
    is_flag=True,
    default=False,
    help="Refresh out-of-date fragments. Default is detection-only (no writes).",
)
def sync(targets: tuple[Path, ...], all_projects: bool, apply: bool) -> None:
    """Detect and (optionally) refresh hygiene-fragment drift across the portfolio.

    Compares the marker-delimited block in every installed CLAUDE.md /
    AGENTS.md against the canonical template. By default reports drift only;
    pass ``--apply`` to rewrite drifted blocks.

    Examples:
        scaffold sync                  # report drift across the portfolio
        scaffold sync --apply          # refresh drifted blocks
        scaffold sync ~/projects/foo   # check one project
    """
    from scaffold import hygiene

    if targets:
        projects = [t.resolve() for t in targets]
    else:
        projects = hygiene.discover_projects()

    if not projects:
        console.print("[yellow]No projects matched.[/yellow]")
        return

    mode = "APPLY" if apply else "REPORT"
    console.print(f"\n[bold]scaffold sync — {mode}[/bold] ({len(projects)} project(s))\n")

    drift_count = 0
    refused_count = 0
    refreshed_count = 0

    for project in projects:
        reports = hygiene.detect_drift(project)
        if not reports:
            continue  # project has no CLAUDE.md/AGENTS.md to compare
        any_drift = any(r.drift for r in reports)
        if not any_drift:
            console.print(f"[green]OK    {project.name}[/green]")
            continue
        drift_count += 1
        console.print(f"[yellow]DRIFT {project.name}[/yellow]")
        for r in reports:
            if r.drift:
                console.print(f"   [yellow]·  {r.file.name}: {r.detail}[/yellow]")
        if apply:
            result = hygiene.plan_for_project(project)
            if hygiene.is_refused(result):
                refused_count += 1
                console.print(f"   [red]✗  refused — manual cleanup required[/red]")
                continue
            written = hygiene.apply_result(result)
            for change in written:
                console.print(f"   [cyan]✓  refreshed {change.path.name}[/cyan]")
            if written:
                refreshed_count += 1
        else:
            # Show a diff per drifted file.
            result = hygiene.plan_for_project(project)
            for change in result.changes:
                if change.is_noop or change.note.startswith("REFUSED"):
                    continue
                diff = change.unified_diff()
                if diff:
                    for line in diff.splitlines():
                        console.print(f"      {line}")

    console.print("\n[bold]Summary[/bold]")
    console.print(f"  drift     : {drift_count}")
    console.print(f"  refreshed : {refreshed_count}")
    console.print(f"  refused   : {refused_count}")

    if not apply and drift_count > 0:
        console.print(
            "\n[yellow]Detection-only — re-run with --apply to refresh.[/yellow]"
        )


if __name__ == "__main__":
    cli()
