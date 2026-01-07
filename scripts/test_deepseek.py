#!/usr/bin/env python3
"""
Test DeepSeek quality vs Claude Sonnet

Each project will get its own DeepSeek API key.
"""

from openai import OpenAI
import sys
import os

# Testing API key
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY")

def test_deepseek() -> bool:
    """Test DeepSeek with a real coding task"""
    if not DEEPSEEK_KEY:
        print("\n❌ Error: DEEPSEEK_API_KEY environment variable is not set")
        return False
    
    client = OpenAI(
        api_key=DEEPSEEK_KEY,
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
        print(f"\n📊 Stats:")
        print(f"   Tokens: {tokens:,}")
        print(f"   Cost: ${cost:.6f}")
        print(f"   Model: deepseek-chat")
        
        # Calculate what this would cost with Claude Sonnet
        claude_cost = tokens * 0.000003  # Rough avg of input/output
        savings = ((claude_cost - cost) / claude_cost) * 100
        
        print(f"\n💰 Comparison:")
        print(f"   DeepSeek cost: ${cost:.6f}")
        print(f"   Claude Sonnet (est): ${claude_cost:.6f}")
        print(f"   Savings: {savings:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python3 scripts/test_deepseek.py")
        print("Requires DEEPSEEK_API_KEY environment variable.")
        sys.exit(0)
    success = test_deepseek()
    sys.exit(0 if success else 1)

