#!/usr/bin/env python3
"""
Test DeepSeek quality vs Claude Sonnet

Each project will get its own DeepSeek API key.
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI

DOTENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=DOTENV_PATH, override=False)
DOTENV_VALUES = dotenv_values(DOTENV_PATH)

@pytest.mark.slow
@pytest.mark.integration
def test_deepseek() -> None:
    """Test DeepSeek with a real coding task (integration; costs tokens)."""
    deepseek_key = (
        os.getenv("SCAFFOLDING_DEEPSEEK_KEY")
        or os.getenv("DEEPSEEK_API_KEY")
        or DOTENV_VALUES.get("SCAFFOLDING_DEEPSEEK_KEY")
        or DOTENV_VALUES.get("DEEPSEEK_API_KEY")
    )
    if not deepseek_key:
        pytest.skip("SCAFFOLDING_DEEPSEEK_KEY not set")
    
    client = OpenAI(
        api_key=deepseek_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    # Typical Tier 2 task
    prompt = """
Write a Python function that:
1. Takes a list of user objects (dicts with 'id', 'name', 'email')
2. Validates email format using regex
3. Removes duplicates based on email (keep first occurrence)
4. Returns sorted list by name (case-insensitive)
5. Include type hints, docstring, and error handling

Make it production-ready.
"""
    
    print("Testing DeepSeek V3...")
    print("=" * 80)
    print("Prompt:", prompt)
    print("=" * 80)
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful coding assistant. Write clean, production-ready code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        cost = tokens * 0.00000027  # $0.27 per 1M input + output
        
        print("\nDeepSeek Response:")
        print("=" * 80)
        print(content)
        print("=" * 80)
        print("\n📊 Stats:")
        print(f"   Tokens: {tokens:,}")
        print(f"   Cost: ${cost:.6f}")
        print("   Model: deepseek-chat")
        
        # Calculate what this would cost with Claude Sonnet
        claude_cost = tokens * 0.000003  # Rough avg of input/output
        savings = ((claude_cost - cost) / claude_cost) * 100
        
        print("\n💰 Comparison:")
        print(f"   DeepSeek cost: ${cost:.6f}")
        print(f"   Claude Sonnet (est): ${claude_cost:.6f}")
        print(f"   Savings: {savings:.1f}%")
        
        assert content and len(content) > 50
        assert tokens > 0
        assert cost >= 0
    
    except Exception as e:
        pytest.fail(f"DeepSeek call failed: {e}")

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python3 scripts/test_deepseek.py")
        print("Requires DEEPSEEK_API_KEY environment variable.")
        sys.exit(0)
    success = test_deepseek()
    sys.exit(0 if success else 1)

