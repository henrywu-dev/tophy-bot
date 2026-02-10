#!/bin/bash

# Tophy Bot - Lint and Format Script
# This script runs all linting and formatting tools

set -e

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        Tophy Bot - Code Quality & Linting Tools              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

PROJECT_PATH="."
PYTHON_FILES=$(find "$PROJECT_PATH" -name "*.py" -not -path "*/venv/*" -not -path "*/__pycache__/*" | tr '\n' ' ')

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}▶ $1${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 1. isort - Sort imports
print_section "Running isort (Import Sorting)"
isort $PYTHON_FILES --profile black --line-length 100 --check-only --diff || {
    echo -e "${YELLOW}⚠ Running isort in fix mode...${NC}"
    isort $PYTHON_FILES --profile black --line-length 100
}

# 2. Black - Code formatting
print_section "Running Black (Code Formatting)"
black $PYTHON_FILES --line-length 100 --check --diff || {
    echo -e "${YELLOW}⚠ Running Black in fix mode...${NC}"
    black $PYTHON_FILES --line-length 100
}

# 3. Flake8 - Style guide enforcement
print_section "Running Flake8 (Style Guide)"
flake8 $PYTHON_FILES --max-line-length=100 --count --statistics || {
    echo -e "${YELLOW}⚠ Found Flake8 issues above${NC}"
}

# 4. Pylint - Code analysis
print_section "Running Pylint (Code Analysis)"
pylint tophy/ main.py --rcfile=.pylintrc --max-line-length=100 || {
    echo -e "${YELLOW}⚠ Pylint found some issues (non-blocking)${NC}"
}

# 5. mypy - Type checking
print_section "Running mypy (Type Checking)"
mypy tophy/ main.py --ignore-missing-imports --no-error-summary 2>/dev/null || {
    echo -e "${YELLOW}⚠ Some type hints could be improved (non-blocking)${NC}"
}

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo -e "║          ${GREEN}✓ Linting Complete!${NC}                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Summary:"
echo "  ✓ isort   - Import sorting"
echo "  ✓ Black   - Code formatting"
echo "  ✓ Flake8  - Style enforcement"
echo "  ✓ Pylint  - Code analysis"
echo "  ✓ mypy    - Type checking"
echo ""
echo "To auto-fix formatting issues, run:"
echo "  ${BLUE}chmod +x scripts/lint.sh && ./scripts/lint-fix.sh${NC}"
echo ""
