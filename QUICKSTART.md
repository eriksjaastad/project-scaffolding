# Multi-AI Review System - Quick Start

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Dependencies already installed
```

### 2. Set Up API Keys

Create a `.env` file:

```bash
cp .env.example .env
# Then edit .env with your actual keys
```

Or export them:

```bash
export SCAFFOLDING_OPENAI_KEY="sk-..."
export SCAFFOLDING_ANTHROPIC_KEY="sk-ant-..."
```

## Usage

### Run Document Review

```bash
# Round 1
python scaffold_cli.py review \
  --type document \
  --input docs/VISION.md \
  --round 1

# After revising based on feedback, run Round 2
python scaffold_cli.py review \
  --type document \
  --input docs/VISION.md \
  --round 2
```

### Output

Reviews will be saved to:
```
docs/sprint_reviews/
├── round_1/
│   ├── security_reviewer.md
│   ├── performance_reviewer.md
│   ├── architecture_reviewer.md
│   └── COST_SUMMARY.json
└── round_2/
    └── ...
```

### What You Get

- **3 parallel reviews** (Security, Performance, Architecture)
- **Real-time cost tracking** (per API, per reviewer)
- **Token usage** for each review
- **Duration** for each review
- **Structured feedback** (no sunshine!)

## Example Output

```
Running Review Round 1
Document: docs/VISION.md
Reviewers: 3

⠋ Security Reviewer (gpt-4o)
⠙ Performance Reviewer (claude-sonnet-4)
⠹ Architecture Reviewer (claude-sonnet-4)

Review Complete!

┌─────────────────────────────────────────────┐
│              Cost Breakdown                 │
├──────────────┬──────────┬────────┬─────────┤
│ Reviewer     │ Model    │ Tokens │ Cost    │
├──────────────┼──────────┼────────┼─────────┤
│ Security     │ gpt-4o   │ 12,450 │ $0.1868 │
│ Performance  │ sonnet-4 │ 15,200 │ $0.2280 │
│ Architecture │ sonnet-4 │ 14,800 │ $0.2220 │
├──────────────┴──────────┴────────┴─────────┤
│ TOTAL                            │ $0.6368 │
└──────────────────────────────────┴─────────┘

Reviews saved to: docs/sprint_reviews/round_1
```

## What's Next

1. **Read the reviews** in `docs/sprint_reviews/round_1/`
2. **Revise your document** based on feedback
3. **Run Round 2** to verify fixes
4. **Generate prompts** (coming soon)
5. **Start building** (task dispatch coming soon)

## Prompts

Prompts are in `prompts/active/document_review/`:
- `security.md` - Security-focused reviewer
- `performance.md` - Performance-focused reviewer
- `architecture.md` - Architecture-focused reviewer

These are **version 1**. As you learn what works, you'll create v2, v3, etc. in `prompts/versions/`.

## Cost Tracking

Every review round creates a `COST_SUMMARY.json`:

```json
{
  "round": 1,
  "total_cost": 0.6368,
  "breakdown": {
    "openai": {"cost": 0.1868, "tokens": 12450},
    "anthropic": {"cost": 0.4500, "tokens": 30000}
  }
}
```

This data feeds into the analytics system (coming soon).

## Next Components

- ✅ Multi-AI review orchestrator
- ⏳ Code review prompts
- ⏳ Task dispatch system
- ⏳ Cost monitoring dashboard
- ⏳ Prompt versioning CLI
- ⏳ Analytics & learning loop

---

**Status:** Week 1, Day 1 - Core review system working!  
**Next:** Test with real document, then build code review prompts

