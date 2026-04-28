#!/bin/bash
# pre_review_scan.sh - Run before code reviews or commits
# Usage: ./scripts/pre_review_scan.sh

set -e  # Exit on first error

echo "=== Pre-Review Scan ==="
echo ""

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "1. Running security tests..."
python -m pytest tests/test_security.py -v
SECURITY_EXIT=$?

echo ""
echo "2. Checking git hook template syntax..."
bash -n templates/git-hooks/pre-commit templates/git-hooks/pre-push templates/git-hooks/install-hooks.sh
HOOK_EXIT=$?

echo ""
echo "=== Scan Complete ==="

if [ $SECURITY_EXIT -ne 0 ] || [ $HOOK_EXIT -ne 0 ]; then
    echo "FAILED: One or more checks failed"
    exit 1
else
    echo "PASSED: All checks passed"
    exit 0
fi
