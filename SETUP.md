# Tophy Bot - Setup Guide

## ✅ Installation Fixed!

Your dependencies are now installed and ready to use.

### Virtual Environment

The project uses Python virtual environment to manage dependencies:

```bash
# Virtual environment location
./venv/

# To activate venv:
source venv/bin/activate     # On macOS/Linux
source venv/Scripts/activate # On Windows (Git Bash)
```

After activation, your terminal will show `(venv)` prefix.

### Installed Packages

All required packages are installed:

```
ccxt               4.5.37    # Exchange API connector
pandas             3.0.0     # Data manipulation
numpy              2.4.2     # Numerical computing
black              26.1.0    # Code formatter
flake8             7.3.0     # Linter
pylint             4.0.4     # Code analyzer
mypy               1.19.1    # Type checker
isort              7.0.0     # Import organizer
pytest             9.0.2     # Testing framework
```

## 🚀 Getting Started

### 1. Enter Virtual Environment

```bash
source venv/bin/activate
```

### 2. Run the Bot

**Dry-run (simulated trading):**
```bash
python main.py dry-run --strategy rsi
```

**Backtest:**
```bash
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31
```

**List available strategies:**
```bash
python main.py --help
```

### 3. Code Quality

**Check code quality:**
```bash
./scripts/lint.sh
```

**Auto-fix issues:**
```bash
./scripts/lint-fix.sh
```

### 4. Run Tests

```bash
pytest tests/
pytest tests/ --cov=tophy  # With coverage
```

## 📋 File Structure

```
tophy-bot/
├── venv/                    # Virtual environment (activate this!)
├── tophy/                   # Main bot package
├── strategies/              # Trading strategies
├── config/                  # Configuration files
├── tests/                   # Unit tests
├── scripts/                 # Helper scripts
├── main.py                  # CLI entry point
└── requirements.txt         # Dependencies
```

## 🔧 Next Steps

1. **Read the docs:**
   - INDEX.md - Quick references
   - QUICKSTART.md - 5-minute setup
   - README.md - Features overview

2. **Test the bot:**
   ```bash
   source venv/bin/activate
   python main.py dry-run --strategy rsi
   ```

3. **Create your strategy:**
   - Copy an example from `strategies/`
   - Modify the logic
   - Test with backtest

4. **Configure for trading:**
   - Edit `config/default.json`
   - Add your exchange API keys
   - Test with dry-run first

## ⚙️ Configuration

Edit `config/default.json`:

```json
{
  "exchange": {
    "name": "binance",
    "api_key": "YOUR_KEY",
    "api_secret": "YOUR_SECRET",
    "is_sandbox": true
  },
  "trading": {
    "pair": "BTC/USDT",
    "stake_amount": 100,
    "max_open_trades": 3
  }
}
```

## 🐛 Troubleshooting

**Virtual env not working?**
```bash
# Deactivate
deactivate

# Reactivate
source venv/bin/activate
```

**Package import errors?**
```bash
# Reinstall all packages
pip install -r requirements.txt --force-reinstall
```

**Need to add a new package?**
```bash
# Install it
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

## 📚 Available Commands

| Command | Purpose |
|---------|---------|
| `source venv/bin/activate` | Activate virtual environment |
| `deactivate` | Exit virtual environment |
| `python main.py dry-run --strategy rsi` | Run in simulation |
| `python main.py backtest --strategy rsi` | Test on historical data |
| `./scripts/lint.sh` | Check code quality |
| `./scripts/lint-fix.sh` | Auto-fix code issues |
| `pytest tests/` | Run unit tests |

## 🎯 Ready to Trade!

Your Tophy Bot is now set up and ready to use. Start with:

```bash
source venv/bin/activate
python main.py dry-run --strategy rsi
```

Happy trading! 🚀
