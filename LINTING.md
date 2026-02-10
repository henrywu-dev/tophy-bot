# Code Quality & Linting Setup

This project includes comprehensive code quality tools and linting configured for Python development.

## 📦 Installed Tools

### Code Formatting
- **Black** (23.10.0) - Opinionated code formatter
- **isort** (5.12.0) - Import statement organizer
- **autopep8** (2.0.2) - Automatic PEP8 formatter

### Code Analysis
- **Flake8** (6.1.0) - PEP8, PyFlakes, McCabe complexity checker
- **Pylint** (3.0.0) - Code analysis and quality metrics
- **mypy** (1.6.0) - Static type checker

## 🚀 Quick Start

### Install Linting Tools
```bash
pip install -r requirements.txt
```

### Setup Development Environment
```bash
./scripts/setup-dev.sh
```

This will:
- Install all linting tools
- Set up pre-commit hooks
- Configure code quality checks

## 📋 Available Commands

### Automatic Formatting (Recommended First Step)
```bash
./scripts/lint-fix.sh
```

Automatically fixes:
- Import ordering (isort)
- Code formatting (Black + autopep8)
- PEP8 style issues

### Run All Lint Checks
```bash
./scripts/lint.sh
```

Runs (in order):
1. **isort** - Check import ordering
2. **Black** - Check code formatting
3. **Flake8** - Check style and complexity
4. **Pylint** - Analyze code quality
5. **mypy** - Check type hints

### Individual Tools

#### isort - Organize Imports
```bash
# Check only
isort tophy/ main.py --check-only --diff

# Auto-fix
isort tophy/ main.py --profile black --line-length 100
```

#### Black - Format Code
```bash
# Check only
black tophy/ main.py --check --diff

# Auto-fix
black tophy/ main.py --line-length 100
```

#### Flake8 - Style Checking
```bash
flake8 tophy/ main.py --max-line-length=100 --statistics
```

#### Pylint - Code Analysis
```bash
pylint tophy/ main.py --rcfile=.pylintrc
```

#### mypy - Type Checking
```bash
mypy tophy/ main.py --ignore-missing-imports
```

#### autopep8 - Auto-fix PEP8
```bash
autopep8 --in-place --aggressive --aggressive tophy/ main.py
```

## ⚙️ Configuration Files

### `.flake8`
Flake8 configuration:
- Max line length: 100
- Ignored checks: E203, W503
- Max complexity: 10

### `pyproject.toml`
Black, isort, mypy configuration:
- Line length: 100
- Target Python: 3.8+
- Type checking: enabled

### `.pylintrc`
Pylint configuration:
- Max line length: 100
- Attribute limit: 10
- Statement limit: 50
- Custom message control

## 🔄 Git Hooks (Pre-commit)

After running `./scripts/setup-dev.sh`, a pre-commit hook is installed that:
1. Checks staged Python files
2. Runs isort validation
3. Runs Black validation
4. Runs Flake8 checks
5. Blocks commit if issues found

**To bypass (not recommended):**
```bash
git commit --no-verify
```

## 🎯 Best Practices

### Before Committing
1. Run auto-fixes: `./scripts/lint-fix.sh`
2. Review changes: `git diff`
3. Run full lint: `./scripts/lint.sh`
4. Run tests: `pytest tests/`

### Development Workflow
```bash
# Make changes to your code
vim tophy/exchange/base.py

# Auto-fix formatting
./scripts/lint-fix.sh

# Review changes
git diff

# Run tests
pytest tests/

# Commit if all good
git add .
git commit -m "Your commit message"
```

### Code Style Guide

#### Line Length
- **Maximum:** 100 characters
- Use line continuation for readability

#### Imports
- Organized by: stdlib, third-party, local
- Alphabetically sorted
- Done automatically by isort

#### Naming
- Classes: `PascalCase` (e.g., `BaseStrategy`)
- Functions: `snake_case` (e.g., `calculate_sma`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TRADES`)
- Private: `_leading_underscore` (e.g., `_internal_method`)

#### Type Hints
- Use type hints for function arguments
- Use type hints for return values (except `None`)
- Example:
  ```python
  def calculate_sma(df: pd.DataFrame, period: int = 20) -> pd.Series:
      return df["close"].rolling(window=period).mean()
  ```

#### Docstrings
- Use triple quotes
- First line: brief description
- Rest: detailed explanation if needed
- Example:
  ```python
  def my_function(symbol: str) -> float:
      """Get the current price for a symbol.
      
      Args:
          symbol: Trading pair symbol (e.g., 'BTC/USDT')
      
      Returns:
          Current price as float
      """
  ```

## 🔍 Common Issues & Solutions

### isort Conflicts
If isort and Black disagree:
```bash
# isort respects Black's line-length with:
isort --profile black --line-length 100
```

### Flake8 Line Length
Some lines will exceed 100 chars naturally:
```python
# Use noqa comment to ignore specific line
very_long_function_name(param1, param2, param3)  # noqa: E501
```

### Type Checking Warnings
For external libraries without type hints:
```python
import ccxt  # type: ignore
```

### Pylint Disabling Rules
For specific violations:
```python
def function_with_many_args(a, b, c, d):  # pylint: disable=too-many-arguments
    pass
```

## 📊 Metrics & Reports

### Check Code Complexity
```bash
flake8 tophy/ --statistics
```

### Generate Coverage Report
```bash
pytest tests/ --cov=tophy --cov-report=html
open htmlcov/index.html
```

### Check Code Quality
```bash
pylint tophy/ --exit-zero  # Don't fail on exit
```

## 🔧 IDE Integration

### VS Code
Add to `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.python",
        "editor.formatOnSave": true
    }
}
```

### PyCharm
1. Settings → Editor → Code Style → Python
2. Scheme: Set to "Black"
3. Enable all inspections
4. Run linters on save

## ✅ Checklist Before Merging

- [ ] Code formatted with Black: `black tophy/ main.py`
- [ ] Imports sorted: `isort tophy/ main.py`
- [ ] Flake8 passes: `flake8 tophy/ main.py`
- [ ] Pylint score: `pylint tophy/ main.py | tail -5`
- [ ] Type hints: `mypy tophy/ main.py`
- [ ] Tests pass: `pytest tests/`
- [ ] Coverage acceptable: `pytest tests/ --cov=tophy`

## 📚 Resources

- Black: https://github.com/psf/black
- isort: https://pycqa.github.io/isort/
- Flake8: https://flake8.pycqa.org/
- Pylint: https://www.pylint.org/
- mypy: https://mypy.readthedocs.io/

## 🆘 Troubleshooting

**Q: lint.sh returns exit code 1**
```bash
# Run lint-fix.sh first to auto-correct
./scripts/lint-fix.sh

# Then run checks again
./scripts/lint.sh
```

**Q: Pre-commit hook blocks my commit**
```bash
# Review the issues
./scripts/lint.sh

# Auto-fix them
./scripts/lint-fix.sh

# Try commit again
git add .
git commit -m "message"
```

**Q: My changes look correct but linter complains**
```bash
# Check raw file
cat -A tophy/file.py | grep -n "^"

# Could be tabs vs spaces
# Fix with: autopep8 --in-place --aggressive tophy/file.py
```

## 🎓 Learning More

Read individual tool docs for advanced configuration:
- Detailed rules: `flake8 --extend-ignore=E,W`
- Type checking: `mypy --help`
- Code analysis: `pylint --long-help`

---

**Happy coding! Clean code is happy code.** ✨
