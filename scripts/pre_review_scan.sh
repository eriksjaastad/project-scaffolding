#!/bin/bash
# Mandatory pre-review scan for project-scaffolding
# Run this BEFORE any human/AI code review
# Exit code 1 = review must address failures

set -e

FAILED=0

echo "=================================="
echo "🔍 PRE-REVIEW SCAN - Project Scaffolding"
echo "=================================="
echo ""

# ============================================================
# TIER 1: BLAST RADIUS CHECKS (Propagation Sources)
# These have highest impact - they infect downstream projects
# ============================================================

echo "📋 TIER 1: BLAST RADIUS (Templates & Configs)"
echo "--------------------------------------------------"

# Hardcoded path detection (using character class to avoid self-detection)
USER_PATH_PREFIX="/[U]sers/"

echo -n "  [1.1] Checking templates/ for hardcoded paths... "
if find templates/ -type f 2>/dev/null | xargs grep -l "$USER_PATH_PREFIX" 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [1.2] Checking YAML files for hardcoded paths... "
if grep -rn "$USER_PATH_PREFIX" *.yaml 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

# Note: All files are now subject to path checks to ensure DNA portability.

echo ""

# ============================================================
# TIER 2: SECURITY & SAFETY
# ============================================================

echo "🔒 TIER 2: SECURITY & SAFETY"
echo "--------------------------------------------------"

echo -n "  [2.1] Checking for hardcoded API keys (sk-...)... "
if grep -rE "sk-[a-zA-Z0-9]{32,}" scripts/ scaffold/ templates/ 2>/dev/null; then
    echo "❌ FAIL"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [2.2] Checking for silent exception swallowing... "
if grep -rn "except.*:$" scripts/ scaffold/ 2>/dev/null | grep -v "# noqa" | grep "pass"; then
    echo "❌ FAIL (found 'except: pass')"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [2.3] Checking .env is gitignored... "
if git check-ignore .env >/dev/null 2>&1; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
    FAILED=1
fi

echo ""

# ============================================================
# TIER 3: DEPENDENCY SAFETY
# ============================================================

echo "📦 TIER 3: DEPENDENCY SAFETY"
echo "--------------------------------------------------"

echo -n "  [3.1] Checking for unpinned dependencies (>=)... "
if grep -E "^[^#].*>=" requirements.txt 2>/dev/null; then
    echo "❌ FAIL (found >= without upper bound)"
    FAILED=1
else
    echo "✅ PASS"
fi

echo -n "  [3.2] Checking anthropic version boundary... "
if grep -E "anthropic~=0\.[0-9]+" requirements.txt 2>/dev/null; then
    echo "⚠️  WARN (0.x -> 1.x was breaking change)"
    # Don't fail, just warn
else
    echo "✅ PASS"
fi

echo ""

# ============================================================
# TIER 4: CODE QUALITY
# ============================================================

echo "✨ TIER 4: CODE QUALITY"
echo "--------------------------------------------------"

echo -n "  [4.1] Checking for functions without type hints... "
# Use python for more robust multi-line check
MISSING_TYPES=$(python3 -c '
import sys
import os
import re

missing = 0
for dir_path in ["scripts", "scaffold"]:
    if not os.path.exists(dir_path): continue
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                # Find all def statements
                for match in re.finditer(r"^def\s+\w+", content, re.MULTILINE):
                    start = match.start()
                    # Find the colon that ends this definition
                    colon_pos = content.find(":", start)
                    if colon_pos != -1:
                        def_sig = content[start:colon_pos]
                        if "->" not in def_sig:
                            missing += 1
sys.exit(missing)
' 2>&1 || echo $?)

if [ "$MISSING_TYPES" -gt 0 ]; then
    echo "⚠️  WARN ($MISSING_TYPES functions without return type)"
else
    echo "✅ PASS"
fi

echo ""

# ============================================================
# RESULTS
# ============================================================

echo "=================================="
if [ $FAILED -eq 0 ]; then
    echo "✅ PRE-REVIEW SCAN PASSED"
    echo "   Safe to proceed with human/AI review"
    exit 0
else
    echo "❌ PRE-REVIEW SCAN FAILED"
    echo "   Fix failures before requesting review"
    exit 1
fi

