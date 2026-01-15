#!/usr/bin/env python3
"""
delegate.py - CLI for delegating tasks to cheaper models

Usage:
    python scripts/delegate.py --model gemini-flash --prompt "Write a function that validates emails"
    python scripts/delegate.py --model deepseek-r1 --prompt "Explain this code" --file src/main.py
    python scripts/delegate.py --model qwen3:14b --prompt "Write tests for this"

Hierarchy:
    Opus (you're talking to) → delegates to → Gemini Flash or Ollama

Environment:
    GEMINI_API_KEY - Required for gemini-flash model
"""
import argparse
import subprocess
import sys
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Available models
GEMINI_MODELS = ["gemini-flash", "gemini-pro"]
OLLAMA_MODELS = ["deepseek-r1", "qwen3:14b", "llama3.1:8b", "codellama:13b"]


def call_gemini(prompt: str, model: str = "gemini-1.5-flash") -> str:
    """Call Gemini API."""
    try:
        import google.generativeai as genai
    except ImportError:
        logger.error("google-generativeai not installed. Run: pip install google-generativeai")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable not set")
        sys.exit(1)

    genai.configure(api_key=api_key)

    model_name = "gemini-1.5-flash" if model == "gemini-flash" else "gemini-1.5-pro"
    gen_model = genai.GenerativeModel(model_name)

    try:
        response = gen_model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        sys.exit(1)


def call_ollama(model: str, prompt: str, timeout: int = 300) -> str:
    """Call local Ollama model."""
    # Check if ollama is available
    if not subprocess.run(["which", "ollama"], capture_output=True).returncode == 0:
        logger.error("Ollama not found. Is it installed?")
        sys.exit(1)

    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode != 0:
            logger.error(f"Ollama error: {result.stderr}")
            sys.exit(1)
        return result.stdout
    except subprocess.TimeoutExpired:
        logger.error(f"Ollama timeout after {timeout}s")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Delegate tasks to cheaper models (Gemini or Ollama)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --model gemini-flash --prompt "Write a Python function to parse JSON"
    %(prog)s --model deepseek-r1 --prompt "Review this code" --file main.py
    %(prog)s --model qwen3:14b --prompt "Write unit tests" --timeout 600
        """
    )

    all_models = GEMINI_MODELS + OLLAMA_MODELS
    parser.add_argument(
        "--model", "-m",
        default="gemini-flash",
        choices=all_models,
        help=f"Model to use. Gemini: {GEMINI_MODELS}, Ollama: {OLLAMA_MODELS}"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="The prompt to send to the model"
    )
    parser.add_argument(
        "--file", "-f",
        help="Optional file to include as context (contents prepended to prompt)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=300,
        help="Timeout in seconds for Ollama models (default: 300)"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress info messages, only output model response"
    )

    args = parser.parse_args()

    if args.quiet:
        logging.disable(logging.INFO)

    # Build the full prompt
    full_prompt = args.prompt
    if args.file:
        if not os.path.exists(args.file):
            logger.error(f"File not found: {args.file}")
            sys.exit(1)
        with open(args.file, 'r') as f:
            file_content = f.read()
        full_prompt = f"File: {args.file}\n```\n{file_content}\n```\n\n{args.prompt}"

    # Route to appropriate model
    if args.model in GEMINI_MODELS:
        logger.info(f"Delegating to Gemini ({args.model})...")
        response = call_gemini(full_prompt, args.model)
    else:
        logger.info(f"Delegating to Ollama ({args.model})...")
        response = call_ollama(args.model, full_prompt, args.timeout)

    print(response)


if __name__ == "__main__":
    main()
