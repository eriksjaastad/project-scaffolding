"""
CLI for Project Scaffolding automation system
"""

import asyncio
import os
from pathlib import Path
from typing import List, Optional

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Confirm

from scaffold.review import ReviewConfig, create_orchestrator

# Load environment variables from .env
load_dotenv()

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
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
    envvar="DEEPSEEK_API_KEY",
    help="DeepSeek API key (or set DEEPSEEK_API_KEY env var)"
)
def review(
    review_type: str,
    input_path: Path,
    round_number: int,
    output_dir: Optional[Path],
    openai_key: Optional[str],
    anthropic_key: Optional[str],
    google_key: Optional[str],
    deepseek_key: Optional[str]
):
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
    
    # Load review configurations
    configs = _load_review_configs(prompt_dir, openai_key, anthropic_key, google_key, deepseek_key)
    
    if not configs:
        console.print("[red]Error: No review configurations found[/red]")
        console.print(f"[yellow]Hint: Add prompt files to {prompt_dir}[/yellow]")
        return
    
    # Create orchestrator
    orchestrator = create_orchestrator(
        openai_key=openai_key,
        anthropic_key=anthropic_key,
        google_key=google_key,
        deepseek_key=deepseek_key
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
            
            console.print(f"\n[bold]Next Steps:[/bold]")
            console.print(f"  1. Review feedback in: {output_dir / f'round_{round_number}'}")
            console.print(f"  2. Revise document based on feedback")
            console.print(f"  3. Run Round {next_round}:")
            console.print(f"     [cyan]scaffold review --type {review_type} --input {input_path} --round {next_round}[/cyan]")
            console.print(f"     Estimated cost: [green]${estimated_cost:.2f}[/green]\n")
        else:
            console.print(f"\n[bold green]Review process complete![/bold green]")
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
    deepseek_key: Optional[str]
) -> List[ReviewConfig]:
    """Load review configurations from prompt directory"""
    configs = []
    
    # Map prompt names to API and model
    # Format: {filename_prefix}: (api, model, display_name)
    default_mapping = {
        "security": ("deepseek", "deepseek-chat", "Security Reviewer"),
        "performance": ("deepseek", "deepseek-chat", "Performance Reviewer"),
        "architecture": ("kiro", "claude-sonnet-4", "Architecture Reviewer"),  # Tier 1: Kiro
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
        
        # Check if we have the API key
        if api == "openai" and not openai_key:
            console.print(f"[yellow]Skipping {display_name} (no OpenAI key)[/yellow]")
            continue
        if api == "anthropic" and not anthropic_key:
            console.print(f"[yellow]Skipping {display_name} (no Anthropic key)[/yellow]")
            continue
        if api == "google" and not google_key:
            console.print(f"[yellow]Skipping {display_name} (no Google key)[/yellow]")
            continue
        if api == "deepseek" and not deepseek_key:
            console.print(f"[yellow]Skipping {display_name} (no DeepSeek key)[/yellow]")
            continue
        if api == "kiro":
            # Check if Kiro CLI is available
            import shutil
            if not shutil.which("kiro-cli") and not os.path.exists("/Applications/Kiro CLI.app/Contents/MacOS/kiro-cli"):
                console.print(f"[yellow]Skipping {display_name} (Kiro CLI not installed)[/yellow]")
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

