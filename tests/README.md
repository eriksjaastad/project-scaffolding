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

### **test_kiro.py** - Kiro Integration Tests
Tests for Kiro CLI and spec generation.

```bash
# Fast tests only (skip API calls)
pytest tests/test_kiro.py -v -m "not slow"

# All tests (includes API calls)
pytest tests/test_kiro.py -v
```

Tests:
- ✅ Kiro CLI exists and is logged in
- ✅ Kiro spec generator creates directory structure
- ✅ Templates are copied correctly
- ✅ API calls work (slow tests)
- ✅ Full workflow (generate → review)

**Run time:** 
- Fast: ~10 seconds
- Full: ~2-3 minutes (API calls)

---

### **test_review.py** - Review Orchestrator Tests
Tests for multi-AI review system (DeepSeek + Kiro).

```bash
# Fast tests only
pytest tests/test_review.py -v -m "not slow"

# All tests
pytest tests/test_review.py -v
```

Tests:
- ✅ Orchestrator creation
- ✅ DeepSeek review works
- ✅ Kiro review works
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

- `@pytest.mark.slow` - Tests that call external APIs (DeepSeek, Kiro)
- `@pytest.mark.integration` - End-to-end integration tests
- `@pytest.mark.asyncio` - Async tests (for review orchestrator)

---

## Requirements

Tests require:
- ✅ Python 3.11+
- ✅ Virtual environment activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Kiro CLI installed (`brew install kiro-cli`)
- ✅ Logged into Kiro (`kiro-cli login`)
- ✅ DeepSeek API key in `.env` (for API tests)

---

## Environment Variables

For full test suite, set:

```bash
# Required for API tests
DEEPSEEK_API_KEY=sk-...

# Optional (will skip tests if not set)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
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

**"Kiro CLI not found"**
```bash
brew install kiro-cli
```

**"Not logged in"**
```bash
kiro-cli login
```

**"DeepSeek API key not found"**
```bash
echo "DEEPSEEK_API_KEY=sk-..." >> .env
```

**"Import errors"**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

**Last Updated:** December 23, 2025  
**Status:** Test suite complete! 🧪

