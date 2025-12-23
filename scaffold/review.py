"""
Multi-AI Review Orchestrator

Dispatches document/code reviews to multiple AI models in parallel,
tracks costs, and collects responses.
"""

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import aiohttp
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


@dataclass
class ReviewConfig:
    """Configuration for a single reviewer"""
    name: str
    api: str  # "openai", "anthropic", "google", "deepseek"
    model: str
    prompt_path: Path
    

@dataclass
class ReviewResult:
    """Result from a single reviewer"""
    reviewer_name: str
    api: str
    model: str
    content: str
    cost: float
    tokens_used: int
    duration_seconds: float
    timestamp: str
    error: Optional[str] = None


@dataclass
class ReviewSummary:
    """Summary of all reviews in a round"""
    round_number: int
    document_path: Path
    results: List[ReviewResult]
    total_cost: float
    total_duration: float
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "round": self.round_number,
            "document": str(self.document_path),
            "results": [
                {
                    "reviewer": r.reviewer_name,
                    "api": r.api,
                    "model": r.model,
                    "cost": r.cost,
                    "tokens": r.tokens_used,
                    "duration": r.duration_seconds,
                    "error": r.error
                }
                for r in self.results
            ],
            "total_cost": self.total_cost,
            "total_duration": self.total_duration,
            "timestamp": self.timestamp
        }


class ReviewOrchestrator:
    """Orchestrates multi-AI reviews"""
    
    def __init__(
        self,
        openai_key: Optional[str] = None,
        anthropic_key: Optional[str] = None,
        google_key: Optional[str] = None,
        deepseek_key: Optional[str] = None
    ):
        self.openai_client = AsyncOpenAI(api_key=openai_key) if openai_key else None
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_key) if anthropic_key else None
        self.google_key = google_key  # Will implement Google AI if needed
        self.deepseek_client = AsyncOpenAI(
            api_key=deepseek_key,
            base_url="https://api.deepseek.com/v1"
        ) if deepseek_key else None
        
    async def run_review(
        self,
        document_path: Path,
        configs: List[ReviewConfig],
        round_number: int,
        output_dir: Path
    ) -> ReviewSummary:
        """
        Run reviews with multiple AI models in parallel
        
        Args:
            document_path: Path to document to review
            configs: List of reviewer configurations
            round_number: Which review round this is
            output_dir: Where to save results
            
        Returns:
            ReviewSummary with all results and costs
        """
        # Read document
        document_content = document_path.read_text()
        
        # Create output directory
        round_dir = output_dir / f"round_{round_number}"
        round_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(f"\n[bold cyan]Running Review Round {round_number}[/bold cyan]")
        console.print(f"Document: {document_path}")
        console.print(f"Reviewers: {len(configs)}\n")
        
        # Run reviews in parallel with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            tasks = []
            for config in configs:
                task_id = progress.add_task(
                    f"[cyan]{config.name} ({config.model})",
                    total=None
                )
                tasks.append(
                    self._run_single_review(
                        document_content,
                        config,
                        progress,
                        task_id
                    )
                )
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        review_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                config = configs[i]
                console.print(f"[red]Error in {config.name}: {str(result)}[/red]")
                review_results.append(ReviewResult(
                    reviewer_name=config.name,
                    api=config.api,
                    model=config.model,
                    content="",
                    cost=0.0,
                    tokens_used=0,
                    duration_seconds=0.0,
                    timestamp=datetime.utcnow().isoformat(),
                    error=str(result)
                ))
            else:
                review_results.append(result)
        
        # Save results
        for result in review_results:
            if not result.error:
                output_file = round_dir / f"{result.reviewer_name.lower().replace(' ', '_')}.md"
                output_file.write_text(result.content)
        
        # Create summary
        summary = ReviewSummary(
            round_number=round_number,
            document_path=document_path,
            results=review_results,
            total_cost=sum(r.cost for r in review_results),
            total_duration=max(r.duration_seconds for r in review_results),
            timestamp=datetime.utcnow().isoformat()
        )
        
        # Save cost summary
        cost_file = round_dir / "COST_SUMMARY.json"
        cost_file.write_text(json.dumps(summary.to_dict(), indent=2))
        
        # Display results
        self._display_summary(summary, round_dir)
        
        return summary
    
    async def _run_single_review(
        self,
        document: str,
        config: ReviewConfig,
        progress: Progress,
        task_id: Any
    ) -> ReviewResult:
        """Run a single review"""
        start_time = asyncio.get_event_loop().time()
        
        # Load prompt
        prompt_content = config.prompt_path.read_text()
        full_prompt = f"{prompt_content}\n\n---\n\nDocument to review:\n\n{document}"
        
        # Call appropriate API
        if config.api == "openai":
            result = await self._call_openai(config.model, full_prompt)
        elif config.api == "anthropic":
            result = await self._call_anthropic(config.model, full_prompt)
        elif config.api == "google":
            result = await self._call_google(config.model, full_prompt)
        elif config.api == "deepseek":
            result = await self._call_deepseek(config.model, full_prompt)
        else:
            raise ValueError(f"Unknown API: {config.api}")
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        progress.update(task_id, completed=True)
        
        return ReviewResult(
            reviewer_name=config.name,
            api=config.api,
            model=config.model,
            content=result["content"],
            cost=result["cost"],
            tokens_used=result["tokens"],
            duration_seconds=duration,
            timestamp=datetime.utcnow().isoformat()
        )
    
    async def _call_openai(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call OpenAI API"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a thorough, critical reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Calculate cost (approximate - update with actual pricing)
        tokens = response.usage.total_tokens
        if "gpt-4o" in model:
            cost = tokens * 0.000015  # $15 per 1M tokens (rough average)
        elif "gpt-4o-mini" in model:
            cost = tokens * 0.0000015  # $1.50 per 1M tokens
        else:
            cost = tokens * 0.00003  # Default to GPT-4 pricing
        
        return {
            "content": response.choices[0].message.content,
            "cost": cost,
            "tokens": tokens
        }
    
    async def _call_anthropic(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call Anthropic API"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        response = await self.anthropic_client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Calculate cost (approximate - update with actual pricing)
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        
        if "opus" in model:
            cost = (input_tokens * 0.000015) + (output_tokens * 0.000075)  # $15/$75 per 1M
        elif "sonnet" in model:
            cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)  # $3/$15 per 1M
        elif "haiku" in model:
            cost = (input_tokens * 0.00000025) + (output_tokens * 0.00000125)  # $0.25/$1.25 per 1M
        else:
            cost = (input_tokens * 0.000003) + (output_tokens * 0.000015)  # Default to Sonnet
        
        return {
            "content": response.content[0].text,
            "cost": cost,
            "tokens": input_tokens + output_tokens
        }
    
    async def _call_google(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call Google AI API (stub for now)"""
        # TODO: Implement Google AI if needed
        raise NotImplementedError("Google AI not yet implemented")
    
    async def _call_deepseek(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call DeepSeek API"""
        if not self.deepseek_client:
            raise ValueError("DeepSeek client not initialized")
        
        response = await self.deepseek_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a thorough, critical reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        
        # Calculate cost
        # DeepSeek pricing: $0.27 per 1M tokens (input + output combined)
        total_tokens = response.usage.total_tokens
        cost = total_tokens * 0.00000027
        
        return {
            "content": response.choices[0].message.content,
            "cost": cost,
            "tokens": total_tokens
        }
    
    def _display_summary(self, summary: ReviewSummary, output_dir: Path):
        """Display review summary in terminal"""
        console.print("\n[bold green]Review Complete![/bold green]\n")
        
        # Cost table
        table = Table(title="Cost Breakdown")
        table.add_column("Reviewer", style="cyan")
        table.add_column("Model", style="magenta")
        table.add_column("Tokens", justify="right", style="blue")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Duration", justify="right", style="yellow")
        
        for result in summary.results:
            if result.error:
                table.add_row(
                    result.reviewer_name,
                    result.model,
                    "ERROR",
                    "$0.00",
                    "N/A",
                    style="red"
                )
            else:
                table.add_row(
                    result.reviewer_name,
                    result.model,
                    f"{result.tokens_used:,}",
                    f"${result.cost:.4f}",
                    f"{result.duration_seconds:.1f}s"
                )
        
        table.add_section()
        table.add_row(
            "[bold]TOTAL[/bold]",
            "",
            "",
            f"[bold]${summary.total_cost:.4f}[/bold]",
            f"[bold]{summary.total_duration:.1f}s[/bold]"
        )
        
        console.print(table)
        console.print(f"\n[dim]Reviews saved to: {output_dir}[/dim]\n")


def create_orchestrator(
    openai_key: Optional[str] = None,
    anthropic_key: Optional[str] = None,
    google_key: Optional[str] = None,
    deepseek_key: Optional[str] = None
) -> ReviewOrchestrator:
    """Factory function to create a review orchestrator"""
    return ReviewOrchestrator(
        openai_key=openai_key,
        anthropic_key=anthropic_key,
        google_key=google_key,
        deepseek_key=deepseek_key
    )

