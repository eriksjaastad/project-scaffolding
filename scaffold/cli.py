"""
CLI for Project Scaffolding automation system
"""

import asyncio
import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

import click
from dotenv import load_dotenv
from rich.console import Console

from scaffold.alerts import send_discord_alert

# from scaffold.review import ReviewConfig, create_orchestrator

# Load environment variables from .env
load_dotenv()

console = Console(force_terminal=False)


def _get_context(project_name: str) -> Dict[str, str]:
    """Derive context variables for template substitution."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Try to find existing context from 00_Index or project.yaml if we're updating
    # For now, we derive from project name and defaults
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": "Brief description of the project's purpose",
        "DATE": today,
        "STATUS": "Active",
        "PHASE": "Foundation",
        "PHASE_NUMBER": "1",
        "PHASE_NAME": "Initial Setup",
        "PREVIOUS_PHASE": "None",
        "DATE_RANGE": today,
        "PREVIOUS_DATE": today,
        "TASK_GROUP_NAME": "Core Implementation",
        "AI_NAME": "Claude",
        "MODEL": "Claude 3.5 Sonnet",
        "CRON_EXPRESSION": "0 0 * * *",
        "COMMAND": "python scripts/validate_project.py",
        "SERVICE_NAME": "GitHub",
        "DOC_PATH": "Documents/README.md",
        "LANGUAGE": "Python",
        "LANGUAGE_VERSION": "3.11+",
        "FRAMEWORKS": "None",
        "RUN_COMMAND": "python main.py",
        "TEST_COMMAND": "pytest",
        "MAIN_CODE_DIR": "src",
        "CONSTRAINTS": "None",
    }


def _substitute_placeholders(content: str, context: Dict[str, str], filename: str) -> str:
    """Substitute {{VAR}} placeholders in content."""
    def replace(match):
        var_name = match.group(1)
        if var_name in context:
            return context[var_name]
        
        # Fail loud if placeholder has no value
        raise click.ClickException(f"Error: No context value for placeholder '{{{{{var_name}}}}}' in {filename}")

    # Pattern for {{VAR}}
    pattern = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
    return pattern.sub(replace, content)


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """Project Scaffolding - Automated Multi-AI Review & Build System"""
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
    ollama_host: str
) -> None:
    """
    Run multi-AI review on document or code
    
    Example:
        scaffold review --type document --input docs/VISION.md --round 1
    """
    # Determine output directory
    if output_dir is None:
        if review_type == "document":
            output_dir = Path("docs/sprint_reviews")
        else:
            output_dir = Path("docs/code_reviews")
    
    # Check for Definition of Done (DoD) in input file
    try:
        content = input_path.read_text()
        if "Definition of Done" not in content and "DoD" not in content:
            console.print("[red]Error: Input file missing 'Definition of Done' or 'DoD' section.[/red]")
            console.print("[yellow]Standard: All code review requests MUST include a Definition of Done for tracking.[/yellow]")
            return
    except Exception as e:
        console.print(f"[red]Error reading input file: {e}[/red]")
        return
    
    # Get prompt directory
    prompt_base = Path("prompts/active")
    if review_type == "document":
        prompt_dir = prompt_base / "document_review"
    else:
        prompt_dir = prompt_base / "code_review"
    
    if not prompt_dir.exists():
        console.print(f"[red]Error: Prompt directory not found: {prompt_dir}[/red]")
        console.print("[yellow]Hint: Create prompts in prompts/active/[/yellow]")
        return
    
    # Import here to avoid dependency issues when running other commands
    from scaffold.review import ReviewConfig, create_orchestrator

    # Load review configurations
    configs = _load_review_configs(prompt_dir, openai_key, anthropic_key, google_key, deepseek_key, ollama_model)
    
    if not configs:
        console.print("[red]Error: No review configurations found[/red]")
        console.print(f"[yellow]Hint: Add prompt files to {prompt_dir}[/yellow]")
        return
    
    # Create orchestrator
    orchestrator = create_orchestrator(
        openai_key=openai_key,
        anthropic_key=anthropic_key,
        google_key=google_key,
        deepseek_key=deepseek_key,
        ollama_host=ollama_host
    )
    
    # Run review
    try:
        summary = asyncio.run(
            orchestrator.run_review(
                document_path=input_path,
                configs=configs,
                round_number=round_number,
                output_dir=output_dir
            )
        )
        
        # Ask if user wants to continue to next round
        if round_number < 3:  # Assume max 3 rounds
            next_round = round_number + 1
            estimated_cost = summary.total_cost * 1.05  # Assume similar cost
            
            console.print("\n[bold]Next Steps:[/bold]")
            console.print(f"  1. Review feedback in: {output_dir / f'round_{round_number}'}")
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


@cli.command()
@click.argument("project_name")
@click.option("--dry-run", is_flag=True, help="Print what would happen, don't change anything")
@click.option("--force", is_flag=True, help="Overwrite existing files (make .backup first)")
@click.option("--verify-only", is_flag=True, help="Just check for $SCAFFOLDING refs, no copies")
def apply(project_name: str, dry_run: bool, force: bool, verify_only: bool) -> None:
    """
    Apply scaffolding to a target project to make it standalone.
    
    Example:
        scaffold apply project-tracker
    """
    # 0. Protection Check
    PROTECTED_PROJECTS = {"ai-journal", "writing", "plugin-duplicate-detection", "plugin-find-names-chrome"}
    if project_name in PROTECTED_PROJECTS:
        console.print(f"[bold red]ERROR: {project_name} is a PROTECTED PROJECT.[/bold red]")
        console.print("[red]These projects are on the 'Do Not Touch' list and cannot be scaffolded or modified by automatic services.[/red]")
        return

    scaffold_root = Path(__file__).parent.parent
    
    # Target resolution: try direct, then hyphen-to-space, then in parent dir
    target_dir = Path(project_name)
    if not target_dir.exists():
        # Try in parent directory (standard project layout)
        target_dir = scaffold_root.parent / project_name
    
    if not target_dir.exists() and "-" in project_name:
        # Try with space instead of hyphen
        alt_name = project_name.replace("-", " ")
        alt_target = scaffold_root.parent / alt_name
        if alt_target.exists():
            target_dir = alt_target
            project_name = alt_name

    if not target_dir.exists():
        if not dry_run:
            console.print(f"[yellow]Creating directory: {target_dir}[/yellow]")
            target_dir.mkdir(parents=True, exist_ok=True)
        else:
            console.print(f"[yellow]Would create directory: {target_dir}[/yellow]")

    console.print(f"\n[bold]Applying scaffolding to {project_name}...[/bold]\n")
    if dry_run:
        console.print("[yellow]DRY RUN: No changes will be made.[/yellow]\n")

    # 1. Verification Only mode
    if verify_only:
        _verify_references(target_dir)
        return

    # 2. Copy scripts
    console.print("[bold]Copying scripts...[/bold]")
    scripts_to_copy = [
        "scripts/warden_audit.py",
        "scripts/validate_project.py"
    ]
    
    target_scripts_dir = target_dir / "scripts"
    if not dry_run:
        target_scripts_dir.mkdir(parents=True, exist_ok=True)

    for script in scripts_to_copy:
        src = scaffold_root / script
        dst = target_dir / script
        _copy_file(src, dst, dry_run, force)

    # Special case: pre_review_scan.sh
    pre_review_src = target_dir / "scripts/pre_review_scan.sh"
    _create_pre_review_scan(pre_review_src, project_name, dry_run, force)

    # 3. Copy docs
    console.print("\n[bold]Copying docs...[/bold]")
    docs_to_copy = [
        ("REVIEWS_AND_GOVERNANCE_PROTOCOL.md", "Documents/REVIEWS_AND_GOVERNANCE_PROTOCOL.md"),
        ("patterns/code-review-standard.md", "Documents/patterns/code-review-standard.md"),
        ("patterns/learning-loop-pattern.md", "Documents/patterns/learning-loop-pattern.md"),
        ("Documents/reference/LOCAL_MODEL_LEARNINGS.md", "Documents/reference/LOCAL_MODEL_LEARNINGS.md")
    ]
    
    for src_rel, dst_rel in docs_to_copy:
        src = scaffold_root / src_rel
        dst = target_dir / dst_rel
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
        _copy_file(src, dst, dry_run, force)

    # 4. Update/append templates OR create from template if missing
    console.print("\n[bold]Updating/creating from templates...[/bold]")

    # Marker to detect if template was already appended
    SCAFFOLD_MARKER = "<!-- project-scaffolding template appended -->"

    # Map files to their templates (None means no template available)
    files_with_templates = {
        "AGENTS.md": "templates/AGENTS.md.template",
        "CLAUDE.md": "templates/CLAUDE.md.template",
        "TODO.md": "templates/TODO.md.template",
        "README.md": "templates/README.md.template",
        ".cursorrules": "templates/.cursorrules.template",
        ".cursorignore": "templates/.cursorignore.template",
        ".gitignore": "templates/.gitignore.template",
    }

    context = _get_context(project_name)

    for filename, template_path in files_with_templates.items():
        file_path = target_dir / filename
        if file_path.exists():
            if template_path:
                # File exists AND template available - append template if not already done
                template_full_path = scaffold_root / template_path
                if template_full_path.exists():
                    existing_content = file_path.read_text()
                    if SCAFFOLD_MARKER in existing_content:
                        console.print(f"  ✅ {filename} - template already appended")
                        _update_file_references(file_path, dry_run)
                    else:
                        console.print(f"  📝 Appending template to {filename}...")
                        if not dry_run:
                            template_content = template_full_path.read_text()
                            # Perform substitution on template content before appending
                            substituted_template = _substitute_placeholders(template_content, context, str(template_path))
                            appended_content = f"{existing_content}\n\n{SCAFFOLD_MARKER}\n\n{substituted_template}"
                            file_path.write_text(appended_content)
                        _update_file_references(file_path, dry_run)
            else:
                # File exists but no template - just update references
                _update_file_references(file_path, dry_run)
        elif template_path:
            # File missing but template available - create from template
            template_full_path = scaffold_root / template_path
            if template_full_path.exists():
                console.print(f"  📝 Creating {filename} from template...")
                if not dry_run:
                    template_content = template_full_path.read_text()
                    # Perform substitution
                    substituted_content = _substitute_placeholders(template_content, context, str(template_path))
                    # Add marker so future runs know this was scaffolded
                    content_with_marker = f"{SCAFFOLD_MARKER}\n\n{substituted_content}"
                    file_path.write_text(content_with_marker)
                    # Also update references in the newly created file
                    _update_file_references(file_path, dry_run=False)
            else:
                console.print(f"  [yellow]⚠️  Template not found for {filename}[/yellow]")
        else:
            # No template available
            console.print(f"  ⏭️  Skipped {filename} (not found, no template)")

    # 5. Add version metadata
    console.print("\n[bold]Adding version metadata...[/bold]")
    _add_version_metadata(target_dir, dry_run)

    # 6. Final verification
    console.print("\n[bold]Verifying...[/bold]")
    _verify_references(target_dir)
    _verify_no_placeholders(target_dir)

    if not dry_run:
        console.print(f"\n[bold green]✅ {project_name} is standalone (scaffolding_version: 1.0.0)[/bold green]\n")


def _verify_no_placeholders(target_dir: Path) -> None:
    """Verify that no {{VAR}} placeholders remain in scaffolded files."""
    files_to_check = ["AGENTS.md", "CLAUDE.md", "TODO.md", "README.md", ".cursorrules"]
    found_any = False
    
    # Pattern for {{VAR}}
    pattern = re.compile(r"\{\{[A-Z0-9_]+\}\}")
    
    for filename in files_to_check:
        file_path = target_dir / filename
        if not file_path.exists():
            continue
            
        content = file_path.read_text()
        matches = pattern.findall(content)
        if matches:
            found_any = True
            for match in set(matches):
                console.print(f"  [red]Error: Unfilled placeholder {match} remains in {filename}[/red]")
    
    if found_any:
        msg = f"❌ **Scaffolding Failure** in project: `{project_name}`\nUnfilled placeholders remain in scaffolded files."
        send_discord_alert(msg)
        raise click.ClickException("Verification failed: Unfilled placeholders remain.")
    else:
        console.print("  ✅ No unfilled placeholders found")


def _copy_file(src: Path, dst: Path, dry_run: bool, force: bool) -> None:
    if not src.exists():
        console.print(f"  [red]error[/red] Source not found: {src}")
        return

    if dst.exists() and not force:
        console.print(f"  ⏭️  Skipped {dst.name} (already exists)")
        return

    action = "Copying" if not dst.exists() else "Overwriting"
    console.print(f"  {action} {dst.name}...")

    if not dry_run:
        if dst.exists() and force:
            backup = dst.with_suffix(dst.suffix + ".backup")
            shutil.copy2(dst, backup)
        shutil.copy2(src, dst)


def _create_pre_review_scan(dst: Path, project_name: str, dry_run: bool, force: bool) -> None:
    template = """#!/bin/bash
# pre_review_scan.sh - Run before code reviews or commits
# Usage: ./scripts/pre_review_scan.sh

set -e  # Exit on first error

echo "=== Pre-Review Scan ==="
echo ""

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "1. Running Warden Security Audit (fast mode)..."
python ./scripts/warden_audit.py --root . --fast
WARDEN_EXIT=$?

echo ""
echo "2. Running Project Validation..."
python ./scripts/validate_project.py {project_name}
VALIDATE_EXIT=$?

echo ""
echo "=== Scan Complete ==="

if [ $WARDEN_EXIT -ne 0 ] || [ $VALIDATE_EXIT -ne 0 ]; then
    echo "FAILED: One or more checks failed"
    exit 1
else
    echo "PASSED: All checks passed"
    exit 0
fi
"""
    content = template.replace("{project_name}", project_name)
    
    if dst.exists() and not force:
        console.print("  ⏭️  Skipped pre_review_scan.sh (already exists)")
        return

    action = "Creating" if not dst.exists() else "Overwriting"
    console.print(f"  {action} pre_review_scan.sh...")

    if not dry_run:
        if dst.exists() and force:
            backup = dst.with_suffix(dst.suffix + ".backup")
            dst.rename(backup)
        dst.write_text(content)
        dst.chmod(0o755)


def _update_file_references(file_path: Path, dry_run: bool) -> None:
    content = file_path.read_text()
    
    replacements = [
        (r"\$SCAFFOLDING/scripts/", "./scripts/"),
        (r"\$SCAFFOLDING/Documents/", "./Documents/"),
        (r"\$SCAFFOLDING/patterns/", "./Documents/patterns/"),
        (r"\$SCAFFOLDING/", "./"),
    ]
    
    new_content = content
    total_replacements = 0
    for pattern, replacement in replacements:
        new_content, count = re.subn(pattern, replacement, new_content)
        total_replacements += count
    
    if total_replacements > 0:
        console.print(f"  ✅ {file_path.name} - {total_replacements} replacements")
        if not dry_run:
            file_path.write_text(new_content)
    else:
        console.print(f"  ✅ {file_path.name} - 0 replacements (already clean)")


def _add_version_metadata(target_dir: Path, dry_run: bool) -> None:
    index_files = list(target_dir.glob("00_Index_*.md"))
    if not index_files:
        console.print("  [yellow]⏭️  Skipped version metadata (no 00_Index_*.md found)[/yellow]")
        return

    for index_file in index_files:
        content = index_file.read_text()
        if "scaffolding_version:" in content:
            console.print(f"  ⏭️  Skipped {index_file.name} (version already present)")
            continue
            
        today = datetime.now().strftime("%Y-%m-%d")
        metadata = f"\nscaffolding_version: 1.0.0\nscaffolding_date: {today}\n"
        
        console.print(f"  ✅ Added to {index_file.name}")
        if not dry_run:
            with open(index_file, "a") as f:
                f.write(metadata)


def _verify_references(target_dir: Path) -> None:
    files_to_check = ["AGENTS.md", "CLAUDE.md", ".cursorrules"]
    found_any = False
    
    for filename in files_to_check:
        file_path = target_dir / filename
        if not file_path.exists():
            continue
            
        content = file_path.read_text()
        if "$SCAFFOLDING" in content:
            found_any = True
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if "$SCAFFOLDING" in line:
                    console.print(f"  [red]Error: Found $SCAFFOLDING in {filename}:{i+1}[/red]")
                    console.print(f"    [dim]{line.strip()}[/dim]")
    
    if not found_any:
        console.print("  ✅ No $SCAFFOLDING references found")
    else:
        console.print("\n[red]Verification failed: $SCAFFOLDING references remain.[/red]")


def _load_review_configs(
    prompt_dir: Path,
    openai_key: Optional[str],
    anthropic_key: Optional[str],
    google_key: Optional[str],
    deepseek_key: Optional[str],
    ollama_model: str
) -> List:
    """Load review configurations from prompt directory"""
    # Import here to avoid dependency issues
    from scaffold.review import ReviewConfig
    configs = []
    
    # Map prompt names to API and model
    # Format: {filename_prefix}: (api, model, display_name)
    default_mapping = {
        "security": ("deepseek", "deepseek-chat", "Security Reviewer"),
        "performance": ("deepseek", "deepseek-chat", "Performance Reviewer"),
        "architecture": ("ollama", ollama_model, "Architecture Reviewer"),  # Local via Ollama
        "quality": ("deepseek", "deepseek-chat", "Code Quality Reviewer"),
    }
    
    # Find all .md files in prompt directory
    for prompt_file in sorted(prompt_dir.glob("*.md")):
        # Extract prefix (e.g., "security" from "security_v2.md")
        name_parts = prompt_file.stem.split("_")
        prefix = name_parts[0]
        
        # Get config from mapping or use defaults
        if prefix in default_mapping:
            api, model, display_name = default_mapping[prefix]
        else:
            # Default to OpenAI GPT-4o
            api = "openai"
            model = "gpt-4o"
            display_name = f"{prefix.title()} Reviewer"
        
        # Check if we have the API key (fail loud!)
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


if __name__ == "__main__":
    cli()

