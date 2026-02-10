# Tophy Bot - Quick Start Guide

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd tophy-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your exchange API credentials:
```
EXCHANGE_API_KEY=your_key
EXCHANGE_API_SECRET=your_secret
```

3. Update `config/default.json` with your trading preferences:
- `pair`: Trading pair (e.g., BTC/USDT)
- `stake_amount`: Amount per trade
- `max_open_trades`: Maximum concurrent trades
- `stop_loss`: Stop loss percentage (e.g., -0.05 for -5%)
- `take_profit`: Take profit percentage (e.g., 0.10 for +10%)

## Usage

### Run in Dry-Run Mode (Simulator)
```bash
python main.py dry-run --strategy rsi --config config/default.json
```

### Run in Live Mode (Real Trading)
⚠️ **WARNING**: Use with caution! Start with small amounts.
```bash
python main.py live --strategy rsi --config config/default.json
```

### Backtest a Strategy
```bash
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31
```

## Creating Custom Strategies

1. Create a new file in `strategies/` directory:
```python
from tophy.strategy.base_strategy import BaseStrategy
from tophy.strategy.indicators import calculate_sma, calculate_rsi

class MyStrategy(BaseStrategy):
    def populate_indicators(self):
        self.dataframe["sma_20"] = calculate_sma(self.dataframe, period=20)
        self.dataframe["rsi"] = calculate_rsi(self.dataframe, period=14)
    
    def populate_entry_signals(self):
        # Define your buy/sell logic here
        self.dataframe["buy_signal"] = <your_condition>
        self.dataframe["sell_signal"] = <your_condition>
    
    def populate_exit_signals(self):
        self.dataframe["exit_signal"] = <your_condition>
```

2. Register the strategy in `main.py`:
```python
STRATEGY_MAP = {
    "rsi": RSIStrategy,
    "macd": MACDStrategy,
    "my_strategy": MyStrategy,  # Add this line
}
```

3. Run your strategy:
```bash
python main.py backtest --strategy my_strategy
```

## Available Technical Indicators

The bot includes these pre-built indicators in `tophy/strategy/indicators.py`:
- SMA (Simple Moving Average)
- EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- ATR (Average True Range)
- Stochastic Oscillator

## Project Structure

```
tophy-bot/
├── tophy/
│   ├── exchange/          # Exchange connectors (CCXT-based)
│   ├── strategy/          # Strategy base classes and indicators
│   ├── backtest/          # Backtesting engine
│   ├── trader/            # Main bot and position management
│   └── utils/             # Utilities, logging, models
├── strategies/            # User-defined strategies
├── config/                # Configuration files
├── tests/                 # Unit tests
├── main.py               # CLI entry point
└── README.md
```

## Supported Exchanges

The bot uses CCXT and supports 100+ exchanges:
- Binance
- Kraken
- Coinbase
- Bybit
- Kucoin
- And many more...

## Testing

Run unit tests:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=tophy
```

## Risk Management Features

- **Stop Loss**: Automatically closes losing trades
- **Take Profit**: Automatically closes winning trades
- **Max Open Trades**: Limits concurrent positions
- **Dry-Run Mode**: Test strategies with virtual money
- **Position Size**: Configurable stake amount per trade

## Logging

All bot activities are logged to:
- Console (real-time)
- `logs/` directory (persistent)

## Performance Metrics

Backtest results include:
- Total trades and win rate
- Profit factor and total PnL
- Average trade duration
- Sharpe ratio estimation

## Common Workflows

### Backtest Before Live Trading
```bash
# Test your strategy on historical data
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31

# Paper trade in dry-run mode
python main.py dry-run --strategy rsi

# Monitor logs in logs/tophy.trader.bot.log

# Once satisfied, go live
python main.py live --strategy rsi
```

### Optimize Strategy Parameters
1. Edit strategy in `strategies/`
2. Run multiple backtests with different parameters
3. Compare results in logs
4. Deploy best-performing strategy

## Troubleshooting

**ImportError on startup**:
```bash
pip install -r requirements.txt
```

**API connection errors**:
- Verify API keys in `.env`
- Check exchange sandbox mode setting
- Ensure internet connection

**No data in backtest**:
- Verify the trading pair is correct
- Check the date range
- Ensure exchange has historical data

## Support

For issues, questions, or contributions, please check:
1. Logs in `logs/` directory
2. CCXT documentation: https://docs.ccxt.com/
3. Strategy examples in `strategies/`

## License

MIT License
