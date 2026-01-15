# Test Coverage Templates

Templates for adding test coverage to projects.

## Files

| File | Copy To | Purpose |
|------|---------|---------|
| `coveragerc.template` | `.coveragerc` (project root) | Coverage configuration |
| `run_coverage.py` | `scripts/tests/run_coverage.py` | Coverage runner script |

## Quick Setup

```bash
# From your project root
cp /path/to/project-scaffolding/templates/test-coverage/coveragerc.template .coveragerc
mkdir -p scripts/tests
cp /path/to/project-scaffolding/templates/test-coverage/run_coverage.py scripts/tests/

# Install requirements
pip install pytest pytest-cov coverage

# Run coverage
doppler run -- python scripts/tests/run_coverage.py
```

## Customization

### .coveragerc

Edit the `[run] source` directive to match your project structure:
- `source = scripts` for scripts-based projects
- `source = src` for src-based projects
- `source = .` for single-file tools

### run_coverage.py

Edit the `--cov=scripts` argument to match your source directory.

## Requirements

Add to your `requirements.txt`:

```bash
pytest>=7.0.0
pytest-cov>=4.0.0
coverage>=7.0.0
```

## Output

Coverage reports are generated in `scripts/tests/htmlcov/`:
- `index.html` - Main report (open in browser)
- `coverage.xml` - XML format (for CI integration)

## See Also

- `patterns/project-vs-tool-requirements.md` - When to use coverage
- `patterns/testing-patterns.md` - Test structure guidelines
