#!/usr/bin/env python3
"""
Head-to-head comparison: DeepSeek vs Claude Opus vs GPT models

Test the same Tier 2 task with multiple models and compare:
- Quality of output
- Code completeness
- Cost
- Response time
"""

import time
from openai import OpenAI
from anthropic import Anthropic

# Test prompt (typical Tier 2 refactoring task)
TEST_PROMPT = """
Refactor this messy Python function into clean, production-ready code:

def process(data):
    result = []
    for item in data:
        if item['status'] == 'active':
            x = item['value'] * 2
            if x > 100:
                result.append({'name': item['name'], 'score': x, 'tier': 'premium'})
            else:
                result.append({'name': item['name'], 'score': x, 'tier': 'standard'})
    return sorted(result, key=lambda k: k['score'], reverse=True)

Requirements:
- Add type hints
- Add docstring
- Extract magic numbers to constants
- Add error handling
- Use dataclasses if appropriate
- Make it more readable
"""

def test_deepseek(api_key: str):
    """Test with DeepSeek V3"""
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )
    
    start = time.time()
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a code refactoring expert. Write clean, production-ready Python code."},
            {"role": "user", "content": TEST_PROMPT}
        ],
        temperature=0.0
    )
    duration = time.time() - start
    
    return {
        "model": "DeepSeek V3",
        "response": response.choices[0].message.content,
        "tokens": response.usage.total_tokens,
        "cost": response.usage.total_tokens * 0.00000027,  # $0.27 per 1M
        "duration": duration
    }

def test_claude_opus(api_key: str):
    """Test with Claude Opus 4"""
    client = Anthropic(api_key=api_key)
    
    start = time.time()
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": TEST_PROMPT}
        ]
    )
    duration = time.time() - start
    
    input_cost = response.usage.input_tokens * 0.000015  # $15 per 1M
    output_cost = response.usage.output_tokens * 0.000075  # $75 per 1M
    
    return {
        "model": "Claude Opus 4",
        "response": response.content[0].text,
        "tokens": response.usage.input_tokens + response.usage.output_tokens,
        "cost": input_cost + output_cost,
        "duration": duration
    }

def test_gpt4o(api_key: str):
    """Test with GPT-4o"""
    client = OpenAI(api_key=api_key)
    
    start = time.time()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a code refactoring expert."},
            {"role": "user", "content": TEST_PROMPT}
        ],
        temperature=0.0
    )
    duration = time.time() - start
    
    return {
        "model": "GPT-4o",
        "response": response.choices[0].message.content,
        "tokens": response.usage.total_tokens,
        "cost": response.usage.total_tokens * 0.0000125,  # Avg of input/output
        "duration": duration
    }

def compare_results(results: list):
    """Print comparison table"""
    print("\n" + "="*100)
    print("MODEL COMPARISON - Tier 2 Refactoring Task")
    print("="*100)
    
    for result in results:
        print(f"\n{result['model']}")
        print("-" * 100)
        print(f"Response length: {len(result['response'])} chars")
        print(f"Tokens: {result['tokens']:,}")
        print(f"Cost: ${result['cost']:.6f}")
        print(f"Duration: {result['duration']:.2f}s")
        print(f"\nCode:\n{result['response'][:500]}...")  # First 500 chars
    
    # Find cheapest and fastest
    cheapest = min(results, key=lambda x: x['cost'])
    fastest = min(results, key=lambda x: x['duration'])
    
    print("\n" + "="*100)
    print("WINNER ANALYSIS")
    print("="*100)
    print(f"💰 Cheapest: {cheapest['model']} (${cheapest['cost']:.6f})")
    print(f"⚡ Fastest: {fastest['model']} ({fastest['duration']:.2f}s)")
    
    # Cost comparison
    print(f"\n💸 Cost Comparison:")
    baseline = results[0]['cost']
    for result in results:
        savings = ((baseline - result['cost']) / baseline * 100) if result['cost'] < baseline else 0
        print(f"   {result['model']:20s} ${result['cost']:.6f}  ({savings:+.1f}% vs baseline)")

if __name__ == "__main__":
    import os
    
    # Get API keys
    deepseek_key = os.getenv("DEEPSEEK_API_KEY") or "sk-ad40fd4d89ce45d2b184c2073a6a8c4a"
    anthropic_key = os.getenv("SCAFFOLDING_ANTHROPIC_KEY")
    openai_key = os.getenv("SCAFFOLDING_OPENAI_KEY")
    
    results = []
    
    # Test DeepSeek
    print("Testing DeepSeek...")
    results.append(test_deepseek(deepseek_key))
    
    # Test Claude Opus (if key available)
    if anthropic_key:
        print("Testing Claude Opus...")
        try:
            results.append(test_claude_opus(anthropic_key))
        except Exception as e:
            print(f"Claude Opus test failed: {e}")
    
    # Test GPT-4o (if key available)
    if openai_key:
        print("Testing GPT-4o...")
        try:
            results.append(test_gpt4o(openai_key))
        except Exception as e:
            print(f"GPT-4o test failed: {e}")
    
    # Compare
    compare_results(results)

