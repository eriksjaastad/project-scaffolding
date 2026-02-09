"""
CLI for Project Scaffolding automation system
"""

import asyncio
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

import click
from dotenv import load_dotenv
from rich.console import Console

from scaffold.alerts import send_discord_alert
from scaffold.constants import PROTECTED_PROJECTS


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
        "ROLE": "floor-manager",
        "DESCRIPTIVE_TITLE": "Task Implementation",
        "CRON_EXPRESSION": "0 0 * * *",
        "COMMAND": "python scripts/validate_project.py",
        "SERVICE_NAME": "GitHub",
        "DOC_PATH": "Documents/README.md",
        "LANGUAGE": "Python",
        "LANGUAGE_VERSION": "3.11+",
        "FRAMEWORKS": "None",
        "RUN_COMMAND": "python main.py",
        "SETUP_COMMAND": "pip install -r requirements.txt",
        "TEST_COMMAND": "pytest",
        "MAIN_CODE_DIR": "src",
        "CONSTRAINTS": "None",
        "AI_STRATEGY": "Local-First",
        "CONFIG_NAME": "default",
        "FILE_CONTENT": "",
        "PROJECT_DESCRIPTION": "Brief description of the project's purpose",
        "VENV_ACTIVATION": "source venv/bin/activate",
        "WAIT_TIME": "2",
        "CONSTRAINT_1": "None",
        "CONSTRAINT_2": "None",
    }


def _substitute_placeholders(content: str, context: Dict[str, str], filename: str) -> str:
    """Substitute {{VAR}} or {var} placeholders in content."""
    
    # Mandatory variables that MUST exist in context if found in {{VAR}} format
    MANDATORY_VARS = {
        "PROJECT_NAME", "PROJECT_DESCRIPTION", "DATE", "STATUS", "PHASE",
        "PHASE_NUMBER", "PHASE_NAME", "PREVIOUS_PHASE", "DATE_RANGE",
        "PREVIOUS_DATE", "TASK_GROUP_NAME", "AI_NAME", "MODEL", "ROLE",
        "CRON_EXPRESSION", "COMMAND", "SERVICE_NAME", "DOC_PATH",
        "LANGUAGE", "LANGUAGE_VERSION", "FRAMEWORKS", "RUN_COMMAND",
        "TEST_COMMAND", "MAIN_CODE_DIR", "CONSTRAINTS", "AI_STRATEGY",
        "VENV_ACTIVATION", "WAIT_TIME"
    }

    # 1. Substitute {{VAR}}
    def replace_double(match):
        var_name = match.group(1).upper()
        if var_name in context:
            return context[var_name]
        
        # Fail loud ONLY if it's a mandatory scaffolding variable
        if var_name in MANDATORY_VARS:
            raise click.ClickException(f"Error: No context value for mandatory placeholder '{{{{{var_name}}}}}' in {filename}")
        
        # Otherwise, keep as is (might be a project-specific placeholder)
        return match.group(0)

    # 2. Substitute {var} - Optional substitution, no failure if missing
    def replace_single(match):
        var_name = match.group(1).upper()
        if var_name in context:
            return context[var_name]
        return match.group(0) # Keep as is if not in context

    # Pattern for {{VAR}}
    double_pattern = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
    content = double_pattern.sub(replace_double, content)
    
    # Pattern for {var}
    single_pattern = re.compile(r"\{([a-z0-9_]+)\}")
    content = single_pattern.sub(replace_single, content)
    
    return content


def _copy_agentsync_rules(
    template_dir: Path,
    target_dir: Path,
    context: Dict[str, str],
    dry_run: bool = False,
) -> List[str]:
    """
    Copy .agentsync/rules/ templates to target project with placeholder substitution.

    Args:
        template_dir: Path to project-scaffolding templates directory
        target_dir: Path to target project root
        context: Variables for placeholder substitution
        dry_run: Preview changes without writing

    Returns:
        List of actions taken (for logging)
    """
    actions = []

    agentsync_src = template_dir / ".agentsync" / "rules"
    agentsync_dst = target_dir / ".agentsync" / "rules"

    if not agentsync_src.exists():
        actions.append(f"[yellow]⚠️  No .agentsync/rules/ templates found at {agentsync_src}[/yellow]")
        return actions

    # Create target directory structure
    if not dry_run:
        agentsync_dst.mkdir(parents=True, exist_ok=True)
    actions.append(f"[dim]📁 Ensuring {agentsync_dst} exists[/dim]")

    # Find all template files
    templates = list(agentsync_src.glob("*.md.template")) + list(agentsync_src.glob("*.md"))

    for template_path in templates:
        # Determine output filename (strip .template suffix if present)
        out_name = template_path.name
        if out_name.endswith(".template"):
            out_name = out_name[:-9]  # Remove ".template"

        out_path = agentsync_dst / out_name

        # Read template and substitute placeholders
        template_content = template_path.read_text()
        try:
            substituted = _substitute_placeholders(template_content, context, template_path.name)
        except click.ClickException as e:
            actions.append(f"[red]❌ Error processing {template_path.name}: {e}[/red]")
            continue

        if dry_run:
            action = "Would update" if out_path.exists() else "Would create"
            actions.append(f"[cyan]📝 {action} {out_path} (from {template_path.name})[/cyan]")
        else:
            # Backup existing file before overwriting
            if out_path.exists():
                backup_path = out_path.with_suffix(out_path.suffix + ".backup")
                shutil.copy2(out_path, backup_path)
                actions.append(f"[yellow]💾 Backed up {out_path.name} → {backup_path.name}[/yellow]")

            out_path.write_text(substituted)
            action = "Updated" if out_path.exists() else "Created"
            actions.append(f"[green]✅ {action} {out_path}[/green]")

    return actions


def _run_agentsync(
    project_name: str,
    dry_run: bool = False,
) -> tuple[bool, List[str]]:
    """
    Run agentsync to sync .agentsync/rules/ to IDE configs.

    Args:
        project_name: Name of the project to sync
        dry_run: Preview without running

    Returns:
        Tuple of (success, list of log messages)
    """
    actions = []

    # AgentSync lives in project-scaffolding/agentsync/ (same repo as this CLI)
    agentsync_script = Path(__file__).parent.parent / "agentsync" / "sync_rules.py"

    if not agentsync_script.exists():
        actions.append(f"[yellow]⚠️  AgentSync not found at {agentsync_script}[/yellow]")
        actions.append("[yellow]   Skipping agentsync (IDE configs won't be updated)[/yellow]")
        return False, actions

    if dry_run:
        actions.append(f"[cyan]🔄 Would run: uv run {agentsync_script} {project_name}[/cyan]")
        return True, actions

    # Run agentsync
    actions.append(f"[blue]🔄 Running agentsync for {project_name}...[/blue]")

    try:
        # Use uv run to ensure consistent Python environment
        result = subprocess.run(
            ["uv", "run", str(agentsync_script), project_name],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        if result.returncode == 0:
            actions.append("[green]✅ AgentSync completed successfully[/green]")
            if result.stdout.strip():
                for line in result.stdout.strip().split("\n"):
                    actions.append(f"[dim]   {line}[/dim]")
            return True, actions
        else:
            actions.append(f"[red]❌ AgentSync failed (exit code {result.returncode})[/red]")
            if result.stderr.strip():
                for line in result.stderr.strip().split("\n"):
                    actions.append(f"[red]   {line}[/red]")
            return False, actions

    except subprocess.TimeoutExpired:
        actions.append("[red]❌ AgentSync timed out after 60 seconds[/red]")
        return False, actions
    except FileNotFoundError:
        actions.append("[yellow]⚠️  'uv' command not found - skipping agentsync[/yellow]")
        actions.append("[yellow]   Install uv or run agentsync manually[/yellow]")
        return False, actions
    except Exception as e:
        actions.append(f"[red]❌ AgentSync error: {e}[/red]")
        return False, actions


@click.group()
@click.version_option(version=get_version())
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
@click.option("--dry-run", is_flag=True, help="Preview changes without writing anything")
@click.option("--verify-only", is_flag=True, help="Just check for $SCAFFOLDING refs, no copies")
def apply(project_name: str, dry_run: bool, verify_only: bool) -> None:
    """
    Apply scaffolding to a target project to make it standalone.
    
    Example:
        scaffold apply project-tracker
    """
    # 0. Protection Check
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

    # Check for existing version
    version_file = target_dir / ".scaffolding-version"
    current_version = get_version()
    rules_version = get_rules_version()
    if version_file.exists():
        try:
            import json
            data = json.loads(version_file.read_text())
            old_version = data.get("scaffolding_version", "0.0.0")
            old_rules_version = data.get("rules_version", "0.0.0")
            
            if old_version < current_version:
                console.print(f"[yellow]⚠️  Updating project from scaffolding version {old_version} to {current_version}[/yellow]")
            elif old_version > current_version:
                console.print(f"[red]⚠️  Warning: Project has newer scaffolding version ({old_version}) than this CLI ({current_version})[/red]")
            
            if old_rules_version < rules_version:
                console.print(f"[yellow]⚠️  Updating project from rules version {old_rules_version} to {rules_version}[/yellow]")
            elif old_rules_version > rules_version:
                console.print(f"[red]⚠️  Warning: Project has newer rules version ({old_rules_version}) than this CLI ({rules_version})[/red]")
                
            if old_version == current_version and old_rules_version == rules_version:
                console.print(f"[blue]ℹ️  Project is already at version {current_version} (rules: {rules_version})[/blue]")
        except Exception:
            pass

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
        _copy_file(src, dst, dry_run)

    # Special case: pre_review_scan.sh
    pre_review_src = target_dir / "scripts/pre_review_scan.sh"
    _create_pre_review_scan(pre_review_src, project_name, dry_run)

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
        _copy_file(src, dst, dry_run)

    # 4. Copy .agentsync/rules/ templates
    console.print("\n[bold]Copying .agentsync/rules/...[/bold]")
    context = _get_context(project_name)
    agentsync_actions = _copy_agentsync_rules(
        template_dir=scaffold_root / "templates",
        target_dir=target_dir,
        context=context,
        dry_run=dry_run,
    )
    for action in agentsync_actions:
        console.print(f"  {action}")

    # 5. Run agentsync to sync rules to IDE configs
    console.print("\n[bold]Running agentsync...[/bold]")
    agentsync_success, agentsync_logs = _run_agentsync(
        project_name=project_name,
        dry_run=dry_run,
    )
    for log in agentsync_logs:
        console.print(f"  {log}")

    # 6. Update templates with npm-like marker pattern
    # NOTE: CLAUDE.md and .cursorrules are managed by AgentSync (step 5)
    # Do NOT add templates for them here - it causes duplication
    console.print("\n[bold]Updating/creating from templates...[/bold]")

    # Markers for scaffold-owned sections (content outside these is preserved)
    # This follows the same pattern as agentsync for consistency
    SCAFFOLD_START = "<!-- SCAFFOLD:START - Do not edit between markers -->"
    SCAFFOLD_END = "<!-- SCAFFOLD:END - Custom content below is preserved -->"

    # Map files to their templates (None means no template available)
    # IMPORTANT: CLAUDE.md and .cursorrules are managed by AgentSync, not here
    files_with_templates = {
        "AGENTS.md": "templates/AGENTS.md.template",
        "DECISIONS.md": "templates/DECISIONS.md.template",
        "README.md": "templates/README.md.template",
        ".cursorignore": "templates/.cursorignore.template",
        ".gitignore": "templates/.gitignore.template",
    }

    for filename, template_path in files_with_templates.items():
        file_path = target_dir / filename
        template_full_path = scaffold_root / template_path if template_path else None

        if template_full_path and not template_full_path.exists():
            console.print(f"  [yellow]⚠️  Template not found for {filename}[/yellow]")
            continue

        if file_path.exists():
            if template_path:
                existing_content = file_path.read_text()
                template_content = template_full_path.read_text()

                # Perform substitution on template content
                substituted_template = _substitute_placeholders(template_content, context, str(template_path))

                # Check if file has our markers (npm-like update between markers)
                if SCAFFOLD_START in existing_content and SCAFFOLD_END in existing_content:
                    # UPDATE mode: Replace content between markers, preserve content outside
                    console.print(f"  🔄 Updating {filename} (between markers)...")
                    if not dry_run:
                        # Extract content before START marker
                        start_idx = existing_content.find(SCAFFOLD_START)
                        content_before = existing_content[:start_idx].rstrip()

                        # Extract content after END marker
                        end_idx = existing_content.find(SCAFFOLD_END)
                        content_after = existing_content[end_idx + len(SCAFFOLD_END):].lstrip('\n')

                        # Build new content: before + markers + template + after
                        new_content = f"{content_before}\n{SCAFFOLD_START}\n{substituted_template}\n{SCAFFOLD_END}"
                        if content_after:
                            new_content += f"\n{content_after}"

                        file_path.write_text(new_content)
                    _update_file_references(file_path, dry_run)
                else:
                    # Check for old-style marker to migrate
                    OLD_MARKER = "<!-- project-scaffolding template appended -->"
                    if OLD_MARKER in existing_content:
                        # MIGRATION mode: Convert old marker format to new
                        console.print(f"  🔄 Migrating {filename} to marker-based format...")
                        if not dry_run:
                            # Remove old marker and content after it
                            old_idx = existing_content.find(OLD_MARKER)
                            preserved_content = existing_content[:old_idx].rstrip()

                            # Build new content with proper markers
                            new_content = f"{SCAFFOLD_START}\n{substituted_template}\n{SCAFFOLD_END}\n\n{preserved_content}"
                            file_path.write_text(new_content)
                        _update_file_references(file_path, dry_run)
                    else:
                        # ADD mode: File exists without markers - add them (existing content becomes custom)
                        console.print(f"  📝 Adding markers to {filename} (preserving existing as custom)...")
                        if not dry_run:
                            # Existing content becomes "custom content" after END marker
                            new_content = f"{SCAFFOLD_START}\n{substituted_template}\n{SCAFFOLD_END}\n\n{existing_content}"
                            file_path.write_text(new_content)
                        _update_file_references(file_path, dry_run)
            else:
                # File exists but no template - just update references
                _update_file_references(file_path, dry_run)
        elif template_path:
            # File missing but template available - create from template with markers
            console.print(f"  📝 Creating {filename} from template...")
            if not dry_run:
                template_content = template_full_path.read_text()
                # Perform substitution
                substituted_content = _substitute_placeholders(template_content, context, str(template_path))
                # Create with markers so future runs can update
                content_with_markers = f"{SCAFFOLD_START}\n{substituted_content}\n{SCAFFOLD_END}"
                file_path.write_text(content_with_markers)
                # Also update references in the newly created file
                _update_file_references(file_path, dry_run=False)
        else:
            # No template available
            console.print(f"  ⏭️  Skipped {filename} (not found, no template)")

    # 7. Add version metadata
    console.print("\n[bold]Adding version metadata...[/bold]")
    _add_version_metadata(target_dir, dry_run)

    # 8. Final verification
    console.print("\n[bold]Verifying...[/bold]")
    _verify_references(target_dir)
    _verify_no_placeholders(target_dir, project_name)

    if not dry_run:
        console.print(f"\n[bold green]✅ {project_name} is standalone (scaffolding_version: 1.0.0)[/bold green]\n")


def _verify_no_placeholders(target_dir: Path, project_name: str) -> None:
    """Verify that no mandatory {{VAR}} placeholders remain in scaffolded files."""
    files_to_check = ["AGENTS.md", "CLAUDE.md", "README.md", ".cursorrules"]
    found_any = False
    
    # Mandatory variables that SHOULD NOT remain in scaffolded files
    MANDATORY_VARS = {
        "PROJECT_NAME", "PROJECT_DESCRIPTION", "DATE", "STATUS", "PHASE",
        "PHASE_NUMBER", "PHASE_NAME", "PREVIOUS_PHASE", "DATE_RANGE",
        "PREVIOUS_DATE", "TASK_GROUP_NAME", "AI_NAME", "MODEL", "ROLE",
        "CRON_EXPRESSION", "COMMAND", "SERVICE_NAME", "DOC_PATH",
        "LANGUAGE", "LANGUAGE_VERSION", "FRAMEWORKS", "RUN_COMMAND",
        "TEST_COMMAND", "MAIN_CODE_DIR", "CONSTRAINTS", "AI_STRATEGY",
        "VENV_ACTIVATION", "WAIT_TIME"
    }
    
    # Pattern for {{VAR}}
    pattern = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
    
    for filename in files_to_check:
        file_path = target_dir / filename
        if not file_path.exists():
            continue
            
        content = file_path.read_text()
        matches = pattern.findall(content)
        for match in matches:
            if match in MANDATORY_VARS:
                found_any = True
                console.print(f"  [red]Error: Mandatory placeholder {{{{{match}}}}} remains in {filename}[/red]")
    
    if found_any:
        msg = f"❌ **Scaffolding Failure** in project: `{project_name}`\nMandatory placeholders remain in scaffolded files."
        send_discord_alert(msg)
        raise click.ClickException("Verification failed: Mandatory placeholders remain.")
    else:
        console.print("  ✅ No mandatory placeholders found")


def _migrate_index(index_path: Path, context: Dict[str, str], dry_run: bool) -> None:
    """Ensure Index file has all required sections."""
    if not index_path.exists():
        return

    content = index_path.read_text()
    modified = False
    
    # 1. Check tags in frontmatter
    if "map/project" not in content:
        console.print(f"  🔄 Adding map/project tag to {index_path.name}...")
        if not dry_run:
            # Simple insertion after 'tags:'
            content = re.sub(r"(tags:\s*\n)", r"\1    - map/project\n", content)
            modified = True

    # 2. Check for required sections
    required_sections = [
        ("## Key Components", "\n## Key Components\n- **Component 1**: Description\n- **Component 2**: Description\n"),
        ("## Status", "\n## Status\nCurrent status and next steps.\n")
    ]
    
    for section_title, template in required_sections:
        if section_title not in content:
            console.print(f"  🔄 Adding {section_title} section to {index_path.name}...")
            if not dry_run:
                content = content.rstrip() + "\n" + template
                modified = True
    
    if modified and not dry_run:
        index_path.write_text(content)


def _copy_file(src: Path, dst: Path, dry_run: bool) -> None:
    if not src.exists():
        console.print(f"  [red]error[/red] Source not found: {src}")
        return

    # Skip if source and destination are the same file
    if src.resolve() == dst.resolve():
        console.print(f"  [blue]ℹ️  Skipping {dst.name} (source and destination are the same)[/blue]")
        return

    action = "Copying" if not dst.exists() else "Updating"
    console.print(f"  {action} {dst.name}...")

    if not dry_run:
        if dst.exists():
            backup = dst.with_suffix(dst.suffix + ".backup")
            shutil.copy2(dst, backup)
        shutil.copy2(src, dst)


def _create_pre_review_scan(dst: Path, project_name: str, dry_run: bool) -> None:
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

    action = "Creating" if not dst.exists() else "Updating"
    console.print(f"  {action} pre_review_scan.sh...")

    if not dry_run:
        if dst.exists():
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


def get_rules_version() -> str:
    """Read rules version from templates/.agentsync/RULES_VERSION."""
    try:
        rules_version_path = Path(__file__).parent.parent / "templates" / ".agentsync" / "RULES_VERSION"
        if rules_version_path.exists():
            return rules_version_path.read_text().strip()
    except Exception:
        pass
    return "1.0.0"


def _add_version_metadata(target_dir: Path, dry_run: bool) -> None:
    """Add version metadata to 00_Index and create .scaffolding-version file."""
    # 1. Update 00_Index
    index_files = list(target_dir.glob("00_Index_*.md"))
    current_version = get_version()
    rules_version = get_rules_version()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Context for migration
    context = {"DATE": today} # Minimal context for now

    if index_files:
        for index_file in index_files:
            # NEW: Migrate index to include required sections
            _migrate_index(index_file, context, dry_run)
            
            content = index_file.read_text()
            if "scaffolding_version:" in content:
                # Update existing version
                new_content = re.sub(r"scaffolding_version: .*", f"scaffolding_version: {current_version}", content)
                new_content = re.sub(r"scaffolding_date: .*", f"scaffolding_date: {today}", new_content)
                if new_content != content:
                    console.print(f"  ✅ Updated version in {index_file.name}")
                    if not dry_run:
                        index_file.write_text(new_content)
            else:
                # Add new version metadata
                metadata = f"\nscaffolding_version: {current_version}\nscaffolding_date: {today}\n"
                console.print(f"  ✅ Added version to {index_file.name}")
                if not dry_run:
                    with open(index_file, "a") as f:
                        f.write(metadata)
    else:
        console.print("  [yellow]⏭️  Skipped 00_Index version metadata (no 00_Index_*.md found)[/yellow]")

    # 2. Create .scaffolding-version JSON file
    version_file = target_dir / ".scaffolding-version"
    version_data = {
        "scaffolding_version": current_version,
        "applied_at": datetime.now().isoformat(),
        "rules_version": rules_version
    }
    
    if dry_run:
        console.print(f"  [cyan]Would create {version_file.name} with version {current_version} and rules {rules_version}[/cyan]")
    else:
        import json
        version_file.write_text(json.dumps(version_data, indent=2))
        console.print(f"  ✅ Created {version_file.name}")


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


@cli.command("sync-root")
@click.option("--dry-run", is_flag=True, help="Preview changes without writing anything")
def sync_root(dry_run: bool) -> None:
    """
    Sync root-level ecosystem files (CLAUDE.md, etc.) from templates.
    
    This updates the projects root directory with the latest templates.
    Unlike 'apply' which works on individual projects, this updates the
    ecosystem-wide root files.
    
    Example:
        scaffold sync-root
        scaffold sync-root --dry-run
    """
    scaffold_root = Path(__file__).parent.parent
    root_templates = scaffold_root / "templates" / "root"
    
    # Detect projects root (parent of project-scaffolding)
    projects_root = scaffold_root.parent
    
    console.print(f"\n[bold]Syncing root-level files to {projects_root}...[/bold]\n")
    if dry_run:
        console.print("[yellow]DRY RUN: No changes will be made.[/yellow]\n")
    
    if not root_templates.exists():
        console.print(f"[red]Error: Root templates directory not found: {root_templates}[/red]")
        return
    
    # Files to sync from templates/root/
    templates = list(root_templates.glob("*.template"))
    
    if not templates:
        console.print("[yellow]No root templates found in templates/root/[/yellow]")
        return
    
    for template_path in templates:
        # Determine output filename (strip .template suffix)
        out_name = template_path.name
        if out_name.endswith(".template"):
            out_name = out_name[:-9]
        
        target_path = projects_root / out_name
        template_content = template_path.read_text()
        
        if target_path.exists():
            existing_content = target_path.read_text()
            
            # Create backup before overwriting
            if not dry_run:
                backup_path = target_path.with_suffix(target_path.suffix + ".backup")
                backup_path.write_text(existing_content)
                console.print(f"  [yellow]💾 Backed up {out_name} → {backup_path.name}[/yellow]")
            
            console.print(f"  [green]✅ Updated {out_name}[/green]")
            if not dry_run:
                target_path.write_text(template_content)
        else:
            console.print(f"  [green]✅ Created {out_name}[/green]")
            if not dry_run:
                target_path.write_text(template_content)
    
    # Add version tracking
    version_file = projects_root / ".root-sync-version"
    current_version = get_version()
    
    if not dry_run:
        import json
        version_data = {
            "synced_version": current_version,
            "synced_at": datetime.now().isoformat()
        }
        version_file.write_text(json.dumps(version_data, indent=2))
        console.print(f"  [green]✅ Updated {version_file.name}[/green]")
    else:
        console.print(f"  [cyan]Would update {version_file.name}[/cyan]")
    
    console.print(f"\n[bold green]✅ Root sync complete (version {current_version})[/bold green]\n")


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

