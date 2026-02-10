#!/bin/bash

# Tophy Bot - Auto-Fix Linting Issues
# This script automatically fixes code style issues

set -e

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║      Tophy Bot - Auto-Fix Linting Issues                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_PATH="."
PYTHON_FILES=$(find "$PROJECT_PATH" -name "*.py" -not -path "*/venv/*" -not -path "*/__pycache__/*" | tr '\n' ' ')

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_section() {
    echo -e "\n${BLUE}▶ $1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 1. isort - Sort imports (auto-fix)
print_section "Fixing imports with isort"
isort $PYTHON_FILES --profile black --line-length 100
echo -e "${GREEN}✓ Imports sorted${NC}"

# 2. Black - Format code (auto-fix)
print_section "Formatting code with Black"
black $PYTHON_FILES --line-length 100
echo -e "${GREEN}✓ Code formatted${NC}"

# 3. autopep8 - Additional PEP8 fixes
print_section "Fixing PEP8 issues with autopep8"
autopep8 --in-place --aggressive --aggressive $PYTHON_FILES --max-line-length 100
echo -e "${GREEN}✓ PEP8 issues fixed${NC}"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo -e "║      ${GREEN}✓ All Auto-Fixes Applied!${NC}                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Review the changes: ${BLUE}git diff${NC}"
echo "  2. Run full lint check: ${BLUE}./scripts/lint.sh${NC}"
echo "  3. Run tests: ${BLUE}pytest tests/${NC}"
echo ""
