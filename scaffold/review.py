"""
Multi-AI Review Orchestrator

Dispatches document/code reviews to multiple AI models in parallel,
tracks costs, and collects responses.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional

from anthropic import AsyncAnthropic
from openai import AsyncOpenAI, APIError, APIConnectionError, RateLimitError
from send2trash import send2trash
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)

# Setup logging for retry attempts
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

console = Console()


def safe_slug(text: str, base_path: Optional[Path] = None) -> str:
    """Sanitizes string for use in filenames and prevents path traversal.

    If base_path is provided, the resolved target path must stay within that base.
    """
    # Lowercase and replace non-alphanumeric with underscores
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    
    # Industrial Hardening: Prevent directory traversal attempts
    if ".." in slug or slug.startswith("/") or slug.startswith("~"):
        logger.warning(f"Potential path traversal attempt in slug: {text}")
        slug = slug.replace("..", "").replace("/", "").replace("~", "")

    if base_path:
        base_path = base_path.resolve()
        target_path = (base_path / slug).resolve()
        if not target_path.is_relative_to(base_path):
            raise ValueError("Security Alert: Path Traversal detected.")

    return slug


def save_atomic(path: Path, content: str) -> None:
    """Atomic write using temp file and rename"""
    temp_dir = path.parent
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    with tempfile.NamedTemporaryFile(mode='w', dir=temp_dir, delete=False) as tf:
        tf.write(content)
        temp_name = tf.name
    
    try:
        os.replace(temp_name, path)
    except Exception as e:
        logger.error(f"Atomic write failed for {path}: {e}")
        if os.path.exists(temp_name):
            try:
                send2trash(temp_name)
            except Exception as cleanup_err:
                logger.warning(f"Failed to trash temp file {temp_name}: {cleanup_err}")
        raise


@dataclass
class ReviewConfig:
    """Configuration for a single reviewer"""
    name: str
    api: str  # "openai", "anthropic", "google", "deepseek", "ollama"
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
        deepseek_key: Optional[str] = None,
        ollama_host: Optional[str] = None
    ) -> None:
        self.openai_client = AsyncOpenAI(api_key=openai_key) if openai_key else None
        self.anthropic_client = AsyncAnthropic(api_key=anthropic_key) if anthropic_key else None
        self.google_key = google_key  # Will implement Google AI if needed
        self.deepseek_client = AsyncOpenAI(
            api_key=deepseek_key,
            base_url="https://api.deepseek.com/v1"
        ) if deepseek_key else None
        self.ollama_host = ollama_host
        
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
        # Read document with size limit (Industrial Hardening H4/S2)
        MAX_FILE_SIZE = 500 * 1024  # 500KB
        if document_path.stat().st_size > MAX_FILE_SIZE:
            raise ValueError(
                f"Document {document_path.name} is too large ({document_path.stat().st_size / 1024:.1f}KB). "
                f"Max size allowed is {MAX_FILE_SIZE / 1024:.1f}KB to protect context window limits."
            )
        
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
                    timestamp=datetime.now(UTC).isoformat(),
                    error=str(result)
                ))
            else:
                review_results.append(result)
        
        # Save results
        for result in review_results:
            if not result.error:
                # Standardize filename: CODE_REVIEW_{safe_slug}.md
                slug_name = safe_slug(result.reviewer_name, base_path=round_dir)
                output_file = (round_dir / f"CODE_REVIEW_{slug_name.upper()}.md").resolve()
                
                # Security: Ensure path stays within round_dir (H4)
                if not output_file.is_relative_to(round_dir.resolve()):
                    logger.error(f"Security Alert: Path traversal detected in reviewer name: {result.reviewer_name}")
                    continue
                    
                save_atomic(output_file, result.content)
        
        # Create summary
        summary = ReviewSummary(
            round_number=round_number,
            document_path=document_path,
            results=review_results,
            total_cost=sum(r.cost for r in review_results),
            total_duration=max(r.duration_seconds for r in review_results),
            timestamp=datetime.now(UTC).isoformat()
        )
        
        # Save cost summary atomically
        cost_file = round_dir / "COST_SUMMARY.json"
        save_atomic(cost_file, json.dumps(summary.to_dict(), indent=2))
        
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
        elif config.api == "ollama":
            result = await self._call_ollama(config.model, full_prompt)
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
            timestamp=datetime.now(UTC).isoformat()
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((APIError, APIConnectionError, RateLimitError, asyncio.TimeoutError)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
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
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
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
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True
    )
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
    
    async def _call_ollama(self, model: str, prompt: str) -> Dict[str, Any]:
        """Call Ollama CLI for local review"""
        try:
            env = os.environ.copy()
            if self.ollama_host:
                env["OLLAMA_HOST"] = self.ollama_host
                
            # Industrial Hardening: subprocess with timeout and check
            result = subprocess.run(
                ["ollama", "run", model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=300,  # Local models can be slow
                check=True,
                env=env
            )
            
            return {
                "content": result.stdout.strip(),
                "cost": 0.0,  # Local usage is free
                "tokens": 0   # Hard to estimate tokens without extra dependencies
            }
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Ollama timed out after 300 seconds for model {model}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Ollama execution failed: {e.stderr}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error calling Ollama: {e}")

    def _display_summary(self, summary: ReviewSummary, output_dir: Path) -> None:
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
    deepseek_key: Optional[str] = None,
    ollama_host: Optional[str] = None
) -> ReviewOrchestrator:
    """Factory function to create a review orchestrator"""
    return ReviewOrchestrator(
        openai_key=openai_key,
        anthropic_key=anthropic_key,
        google_key=google_key,
        deepseek_key=deepseek_key,
        ollama_host=ollama_host
    )

