# Tophy Bot - Complete Implementation Guide

## Project Overview

Tophy Bot is a full-featured cryptocurrency trading bot built in Python, similar to Freqtrade. It provides:

- **Multi-Exchange Support**: Trade on any exchange supported by CCXT (100+ exchanges)
- **Strategy Framework**: Easy-to-use base classes for creating custom trading strategies
- **Backtesting Engine**: Test strategies on historical data before live trading
- **Risk Management**: Built-in stop-loss, take-profit, and position sizing
- **Live Trading**: Real-time trading with dry-run and live modes
- **Comprehensive Logging**: Full activity tracking and performance monitoring

## Architecture

### Core Components

#### 1. **Exchange Connector** (`tophy/exchange/base.py`)
Handles all exchange interactions via CCXT library:
- Fetch market data (OHLCV, ticker)
- Place and cancel orders
- Manage balance and positions
- Support for sandbox/live modes

#### 2. **Strategy Framework** (`tophy/strategy/`)
- `base_strategy.py`: Abstract base class for strategies
- `indicators.py`: Pre-built technical indicators (SMA, EMA, RSI, MACD, etc.)

Strategy Structure:
```python
class MyStrategy(BaseStrategy):
    def populate_indicators(self):
        # Add technical indicators to dataframe
        
    def populate_entry_signals(self):
        # Define buy (buy_signal) and sell (sell_signal) conditions
        
    def populate_exit_signals(self):
        # Define exit conditions
```

#### 3. **Backtesting Engine** (`tophy/backtest/engine.py`)
Simulates trading on historical data:
- Fetches historical OHLCV data
- Executes strategy on each candle
- Tracks trades and calculates metrics
- Outputs performance statistics

Key Metrics:
- Win rate and profit factor
- Total PnL and PnL percentage
- Trade duration
- Final portfolio value

#### 4. **Trading Bot** (`tophy/trader/bot.py`)
Main bot logic:
- Market data monitoring
- Signal detection and execution
- Risk management (SL/TP)
- Portfolio tracking

#### 5. **Position Manager** (`tophy/trader/position_manager.py`)
Manages open trades:
- Track open positions
- Apply stop-loss and take-profit
- Enforce max concurrent trades limit

#### 6. **Utilities** (`tophy/utils/`)
- `logger.py`: Logging to console and files
- `config.py`: JSON/YAML configuration loading
- `models.py`: Data structures (Trade, Order, Ticker, etc.)

## Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Configuration
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
    "timeframe": "1h",
    "stake_amount": 100,
    "max_open_trades": 3
  }
}
```

### 3. Running the Bot

**Dry-Run (Simulated)**:
```bash
python main.py dry-run --strategy rsi
```

**Backtest**:
```bash
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31
```

**Live Trading**:
```bash
python main.py live --strategy rsi
```

## Built-in Strategies

### RSI Strategy
Entry: RSI crosses below 30 (oversold) + price above SMA20
Exit: RSI crosses above 70 (overbought)

### MACD Strategy
Entry: MACD crosses above signal line
Exit: MACD becomes negative

## Creating Custom Strategies

1. Create `strategies/my_strategy.py`:
```python
from tophy.strategy.base_strategy import BaseStrategy
from tophy.strategy.indicators import calculate_sma, calculate_rsi

class MyStrategy(BaseStrategy):
    def populate_indicators(self):
        self.dataframe["sma_20"] = calculate_sma(self.dataframe, period=20)
        self.dataframe["rsi"] = calculate_rsi(self.dataframe, period=14)
    
    def populate_entry_signals(self):
        self.dataframe["buy_signal"] = (
            (self.dataframe["rsi"] < 30) & 
            (self.dataframe["close"] > self.dataframe["sma_20"])
        )
        self.dataframe["sell_signal"] = self.dataframe["rsi"] > 70
    
    def populate_exit_signals(self):
        self.dataframe["exit_signal"] = self.dataframe["rsi"] > 70
```

2. Register in `main.py`:
```python
STRATEGY_MAP = {
    "rsi": RSIStrategy,
    "macd": MACDStrategy,
    "my_strategy": MyStrategy,
}
```

## Data Models

### Trade
Represents a single trade:
```python
class Trade:
    id: str              # Unique identifier
    symbol: str          # Trading pair
    entry_time: datetime # Entry timestamp
    entry_price: float   # Entry price
    quantity: float      # Trade quantity
    side: OrderSide      # BUY or SELL
    stop_loss: float     # SL price
    take_profit: float   # TP price
    pnl: float          # Profit/Loss
    pnl_percent: float  # PnL percentage
```

### Order
Represents a market order:
```python
class Order:
    id: str
    symbol: str
    side: OrderSide      # BUY or SELL
    type: OrderType      # MARKET or LIMIT
    price: float
    quantity: float
    timestamp: datetime
    status: str          # pending, open, closed
```

### Ticker
Current market price data:
```python
class Ticker:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
```

## Configuration Options

### Exchange Settings
- `name`: Exchange name (binance, kraken, bybit, etc.)
- `api_key`: API key
- `api_secret`: API secret
- `is_sandbox`: Use sandbox mode (recommended for testing)

### Trading Settings
- `mode`: "live", "dry-run", or "backtest"
- `pair`: Trading pair (e.g., BTC/USDT)
- `timeframe`: Candle timeframe (1m, 5m, 15m, 1h, 4h, 1d)
- `stake_amount`: Amount per trade
- `max_open_trades`: Maximum concurrent open trades
- `check_interval`: Bot check interval in seconds

### Risk Management
- `stop_loss`: Stop loss percentage (e.g., -0.05 = -5%)
- `take_profit`: Take profit percentage (e.g., 0.10 = +10%)

## Available Indicators

All indicators are in `tophy/strategy/indicators.py`:

```python
calculate_sma(dataframe, period=20)           # Simple Moving Average
calculate_ema(dataframe, period=20)           # Exponential Moving Average
calculate_rsi(dataframe, period=14)           # Relative Strength Index
calculate_macd(dataframe, fast=12, slow=26)   # MACD
calculate_bollinger_bands(dataframe, period=20)  # Bollinger Bands
calculate_atr(dataframe, period=14)           # Average True Range
calculate_stochastic(dataframe, period=14)    # Stochastic Oscillator
```

## Trading Flow

### Live Trading Loop
1. Fetch latest OHLCV data
2. Calculate indicators
3. Check for entry signals
4. Check for exit signals
5. Apply risk management (SL/TP)
6. Execute trades (if enabled)
7. Update portfolio
8. Wait for next check interval

### Backtesting Flow
1. Fetch historical data
2. For each candle:
   - Calculate indicators
   - Check signals
   - Execute trades (simulated)
   - Apply SL/TP
3. Calculate performance metrics

## File Structure

```
tophy-bot/
├── tophy/                     # Main package
│   ├── __init__.py
│   ├── exchange/
│   │   ├── __init__.py
│   │   └── base.py           # CCXT-based exchange connector
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── base_strategy.py  # Abstract strategy base class
│   │   └── indicators.py     # Technical indicators
│   ├── backtest/
│   │   ├── __init__.py
│   │   └── engine.py         # Backtesting engine
│   ├── trader/
│   │   ├── __init__.py
│   │   ├── bot.py            # Main trading bot
│   │   └── position_manager.py  # Position management
│   └── utils/
│       ├── __init__.py
│       ├── logger.py         # Logging utilities
│       ├── config.py         # Configuration loader
│       └── models.py         # Data structures
├── strategies/               # User-defined strategies
│   ├── rsi_strategy.py       # Example RSI strategy
│   └── macd_strategy.py      # Example MACD strategy
├── config/
│   └── default.json         # Default configuration
├── tests/
│   └── test_bot.py          # Unit tests
├── logs/                    # Bot logs (created at runtime)
├── main.py                  # CLI entry point
├── setup.py                 # Package setup
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── QUICKSTART.md            # Quick start guide
├── .gitignore               # Git ignore patterns
└── .env.example             # Example environment variables
```

## Testing

Run unit tests:
```bash
pytest tests/
pytest tests/ --cov=tophy        # With coverage
pytest tests/test_bot.py::test_trade_pnl  # Specific test
```

Test Coverage:
- Indicator calculations
- Strategy functionality
- Trade PnL calculations
- Data model validation

## Performance Optimization

1. **Use appropriate timeframes**: Start with 1h or 4h
2. **Limit historical data**: Backtest on recent data first
3. **Optimize indicators**: Calculate only needed indicators
4. **Batch operations**: Process multiple strategies efficiently

## Logging

All activities are logged to:
- **Console**: Real-time display
- **Files**: `logs/` directory with detailed logs

Log levels: INFO, WARNING, ERROR

## Security Best Practices

1. **Never commit API keys**: Use `.env` file
2. **Use sandbox mode first**: Test before live trading
3. **Start with small amounts**: Test real trading gradually
4. **Monitor bot actively**: Watch logs and trades
5. **Use IP whitelisting**: On exchange API settings
6. **Enable 2FA**: On exchange account

## Supported Exchanges

Via CCXT, supports 100+ exchanges:
- Binance
- Kraken
- Coinbase
- Bybit
- Kucoin
- FTX
- Huobi
- OKX
- And many more...

## Common Use Cases

### Backtest → Dry-Run → Live Workflow
```bash
# 1. Backtest strategy
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31

# 2. Paper trade in dry-run
python main.py dry-run --strategy rsi

# 3. Monitor performance for a few days
# Check logs in logs/ directory

# 4. Go live with confidence
python main.py live --strategy rsi
```

### Strategy Optimization
```bash
# Test different parameters
# Edit strategies/my_strategy.py
# Change indicator periods, thresholds, etc.

python main.py backtest --strategy my_strategy

# Compare results in logs
# Deploy best-performing version
```

## Troubleshooting

**API Connection Error**:
- Verify API keys in `.env`
- Check exchange API key permissions
- Ensure IP is whitelisted

**No Data in Backtest**:
- Check trading pair exists on exchange
- Verify date range has data
- Try shorter timeframe

**Strategy Not Triggering**:
- Monitor logs for signal calculations
- Check dataframe columns have indicators
- Verify entry conditions are being met

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Configure exchange API keys in `config/default.json`
3. Test with dry-run mode
4. Create or modify a strategy
5. Backtest the strategy
6. Deploy to live trading (with caution!)

## Additional Resources

- CCXT Documentation: https://docs.ccxt.com/
- Freqtrade Reference: https://www.freqtrade.io/
- Strategy Ideas: Common technical analysis patterns

## License

MIT License - Feel free to use and modify!

---

**Happy Trading! Start small, backtest thoroughly, and always use proper risk management.**
