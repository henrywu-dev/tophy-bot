#!/bin/bash

# Tophy Bot - Development Setup Script
# Sets up pre-commit hooks and development environment

set -e

echo "┌────────────────────────────────────────────────────────────────┐"
echo "│       Tophy Bot - Development Environment Setup                │"
echo "└────────────────────────────────────────────────────────────────┘"
echo ""

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Make scripts executable
chmod +x scripts/lint.sh scripts/lint-fix.sh 2>/dev/null || true

# Create a pre-commit hook
echo "Setting up pre-commit hooks..."
mkdir -p .git/hooks

cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo "Running pre-commit linting checks..."

# Get list of staged Python files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$')

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

# Run linting on staged files
isort $STAGED_FILES --check-only --profile black || {
    echo "⚠ Run 'isort' to fix import ordering"
    exit 1
}

black $STAGED_FILES --check --line-length 100 || {
    echo "⚠ Run 'black' to fix code formatting"
    exit 1
}

flake8 $STAGED_FILES --max-line-length=100 || {
    echo "⚠ Flake8 issues found"
    exit 1
}

echo "✓ Pre-commit checks passed"
exit 0
EOF

chmod +x .git/hooks/pre-commit
echo "✓ Pre-commit hook installed"

echo ""
echo "Development tools ready! Available commands:"
echo ""
echo "  Linting & Checking:"
echo "    ${BLUE}./scripts/lint.sh${NC}        - Run all linting checks"
echo "    ${BLUE}./scripts/lint-fix.sh${NC}    - Auto-fix all issues"
echo ""
echo "  Formatting:"
echo "    ${BLUE}black tophy/ main.py${NC}        - Format with Black"
echo "    ${BLUE}isort tophy/ main.py${NC}        - Sort imports"
echo ""
echo "  Code Analysis:"
echo "    ${BLUE}flake8 tophy/ main.py${NC}       - Check PEP8"
echo "    ${BLUE}pylint tophy/ main.py${NC}       - Analyze code"
echo "    ${BLUE}mypy tophy/ main.py${NC}         - Type checking"
echo ""
echo "  Testing:"
echo "    ${BLUE}pytest tests/${NC}               - Run all tests"
echo "    ${BLUE}pytest tests/ --cov=tophy${NC}   - With coverage"
echo ""
echo "✓ Setup complete!"
echo ""
