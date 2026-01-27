# Tests for Project Scaffolding

This directory contains tests for the project scaffolding system.

## Test Organization

### **test_smoke.py** - Quick Smoke Tests
Run these first! Fast tests that verify basic structure and imports.

```bash
pytest tests/test_smoke.py -v
```

Tests:
- ✅ Project structure (templates, scripts, docs exist)
- ✅ Python imports work
- ✅ Dependencies installed
- ✅ Configuration files present

**Run time:** ~5 seconds

---

### **test_review.py** - Review Orchestrator Tests
Tests for multi-AI review system (DeepSeek + Ollama).

```bash
# Fast tests only
pytest tests/test_review.py -v -m "not slow"

# All tests
pytest tests/test_review.py -v
```

Tests:
- ✅ Orchestrator creation
- ✅ DeepSeek review works
- ✅ Ollama local review works
- ✅ Multi-reviewer parallel execution
- ✅ CLI interface

**Run time:**
- Fast: ~5 seconds
- Full: ~3-5 minutes (multiple API calls)

---

## Running All Tests

### **Quick Check (Smoke Tests Only)**
```bash
pytest tests/test_smoke.py -v
```

### **Fast Tests (No API Calls)**
```bash
pytest tests/ -v -m "not slow"
```

### **Full Test Suite**
```bash
pytest tests/ -v
```

### **Integration Tests Only**
```bash
pytest tests/ -v -m integration
```

---

## Test Markers

Tests use pytest markers to categorize them:

- `@pytest.mark.slow` - Tests that call external APIs (DeepSeek, Ollama)
- `@pytest.mark.integration` - End-to-end integration tests
- `@pytest.mark.asyncio` - Async tests (for review orchestrator)

---

## Requirements

Tests require:
- ✅ Python 3.11+
- ✅ Virtual environment activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Ollama CLI installed and running (for local reviewer)
- ✅ DeepSeek API key in `.env` (for API tests)

---

## Environment Variables

For full test suite, set:

```bash
# Required for API tests
SCAFFOLDING_DEEPSEEK_KEY=sk-...

# Optional (will skip tests if not set)
SCAFFOLDING_ANTHROPIC_KEY=sk-ant-...
SCAFFOLDING_OPENAI_KEY=sk-...
```

---

## Continuous Integration

For CI/CD, run:

```bash
# Fast tests only (no API costs)
pytest tests/ -v -m "not slow" --maxfail=5

# Or with coverage
pytest tests/ -v -m "not slow" --cov=scaffold --cov-report=html
```

---

## Troubleshooting

**"Ollama CLI not found"**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**"DeepSeek API key not found"**
```bash
echo "SCAFFOLDING_DEEPSEEK_KEY=sk-..." >> .env
```

**"Import errors"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

**Last Updated:** December 23, 2025  
**Status:** Test suite complete! 🧪

## Related Documentation

- [Doppler Secrets Management](Documents/reference/DOPPLER_SECRETS_MANAGEMENT.md) - secrets management
- [Local Model Learnings](Documents/reference/LOCAL_MODEL_LEARNINGS.md) - local AI
- [Cost Management](Documents/reference/MODEL_COST_COMPARISON.md) - cost management
- [AI Team Orchestration](patterns/ai-team-orchestration.md) - orchestration
- [Project Scaffolding](../project-scaffolding/README.md) - Project Scaffolding
