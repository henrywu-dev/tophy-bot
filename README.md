# Tophy Bot - Cryptocurrency Trading Bot

A powerful and flexible cryptocurrency trading bot, built in Python.

## Features

- **Multi-Exchange Support**: Connect to Binance, Kraken, Bybit, and other exchanges via CCXT
- **Strategy Framework**: Easy-to-use strategy framework for developing trading strategies
- **Backtesting**: Test your strategies on historical data
- **Risk Management**: Built-in stop-loss, take-profit, and position sizing
- **Configuration-Based**: Simple JSON/YAML configuration files
- **Dry-Run Mode**: Test strategies without real money
- **Logging & Monitoring**: Comprehensive logging for all trades and events

## Architecture

- **Exchange Connector**: Handles communication with trading exchanges
- **Strategy Framework**: Base classes and utilities for creating custom strategies
- **Backtesting Engine**: Historical data analysis and strategy performance
- **Trader Core**: Main trading logic and position management
- **Utils**: Helper functions and data utilities

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

1. Configure your exchange API keys in `config/exchange.json`
2. Create a strategy in `strategies/`
3. Run the bot:

```bash
python -m tophy.trader --strategy my_strategy --mode live
```

Or backtest:

```bash
python -m tophy.backtest --strategy my_strategy --from 2023-01-01 --to 2023-12-31
```

## Project Structure

```
tophy-bot/
├── tophy/                 # Main package
│   ├── exchange/         # Exchange connectors
│   ├── strategy/         # Strategy framework
│   ├── backtest/         # Backtesting engine
│   ├── trader/           # Main trading logic
│   └── utils/            # Utilities
├── strategies/           # User-defined strategies
├── config/               # Configuration files
├── tests/                # Unit tests
└── docs/                 # Documentation
```

## Development

Run tests:
```bash
pytest tests/
```

## License

MIT License
