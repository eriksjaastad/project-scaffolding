#!/usr/bin/env bash
#
# Install git hooks from project-scaffolding templates
# Run this from a project's root directory
#
# Usage: bash /path/to/project-scaffolding/templates/git-hooks/install-hooks.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOKS_DIR=".git/hooks"

if [ ! -d ".git" ]; then
    echo "ERROR: Not in a git repository root"
    echo "Run this from your project's root directory"
    exit 1
fi

echo "Installing git hooks..."

# Install pre-push hook
if [ -f "$SCRIPT_DIR/pre-push" ]; then
    cp "$SCRIPT_DIR/pre-push" "$HOOKS_DIR/pre-push"
    chmod +x "$HOOKS_DIR/pre-push"
    echo "  Installed: pre-push"
fi

# Install pre-commit hook if exists
if [ -f "$SCRIPT_DIR/pre-commit" ]; then
    cp "$SCRIPT_DIR/pre-commit" "$HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"
    echo "  Installed: pre-commit"
fi

echo ""
echo "Done. Hooks installed in $HOOKS_DIR"
echo ""
echo "To test: make a change and try 'git push'"
echo "To bypass (emergency only): git push --no-verify"
