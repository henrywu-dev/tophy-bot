# Tophy Bot - Project Index & Getting Started

Welcome to Tophy Bot - a full-featured cryptocurrency trading bot similar to Freqtrade!

## 📚 Documentation

1. **[README.md](README.md)** - Project overview and features
2. **[QUICKSTART.md](QUICKSTART.md)** - Quick setup and basic usage guide
3. **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Complete technical documentation

## 🚀 Quick Start in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Exchange (Optional for Testing)
Edit `config/default.json` with your Binance API keys:
```json
{
  "exchange": {
    "api_key": "your_key_here",
    "api_secret": "your_secret_here"
  }
}
```

### 3. Run in Dry-Run Mode (Simulated)
```bash
python main.py dry-run --strategy rsi
```

### 4. Backtest a Strategy
```bash
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31
```

## 📁 Project Structure

```
tophy-bot/
├── tophy/              # Main bot package
│   ├── exchange/       # Exchange API connector (CCXT-based)
│   ├── strategy/       # Strategy framework + indicators
│   ├── backtest/       # Backtesting engine
│   ├── trader/         # Trading bot + position management
│   └── utils/          # Utilities, logging, models
├── strategies/         # User-defined trading strategies
├── config/             # Configuration files
├── tests/              # Unit tests
├── main.py             # CLI entry point
├── requirements.txt    # Python dependencies
├── setup.py            # Package setup
├── Dockerfile          # Docker configuration
└── docker-compose.yml  # Docker Compose setup
```

## 🎯 Key Features

✅ **Multi-Exchange Support** - Trade on 100+ exchanges (Binance, Kraken, Bybit, etc.)  
✅ **Strategy Framework** - Easy-to-use base classes for custom strategies  
✅ **Built-in Strategies** - RSI and MACD example strategies included  
✅ **Backtesting Engine** - Test strategies on historical data  
✅ **Risk Management** - Stop-loss, take-profit, position sizing  
✅ **Live Trading** - Live mode with dry-run testing  
✅ **Comprehensive Logging** - Detailed logs and performance tracking  
✅ **Technical Indicators** - SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic  

## 📖 Core Components

### Exchange Module (`tophy/exchange/base.py`)
- Connect to any CCXT-supported exchange
- Fetch market data (OHLCV, ticker)
- Place and manage orders
- Check balances and positions

### Strategy Framework (`tophy/strategy/`)
- **BaseStrategy**: Abstract base class for all strategies
- **Built-in Indicators**: 7 pre-implemented technical indicators
- Example Strategies: RSI and MACD strategies included

### Backtesting Engine (`tophy/backtest/engine.py`)
- Test strategies on historical data
- Calculate performance metrics
- Analyze win rate and profit factor
- Compare different strategies

### Trading Bot (`tophy/trader/bot.py`)
- Main bot with market monitoring
- Entry/exit signal processing
- Risk management (SL/TP)
- Portfolio tracking

### Position Manager (`tophy/trader/position_manager.py`)
- Track open trades
- Apply stop-loss and take-profit
- Enforce max concurrent trades
- Calculate trade statistics

## 🛠️ Creating Your First Strategy

1. Create `strategies/my_strategy.py`:
```python
from tophy.strategy.base_strategy import BaseStrategy
from tophy.strategy.indicators import calculate_sma, calculate_rsi

class MyStrategy(BaseStrategy):
    def populate_indicators(self):
        # Add indicators to dataframe
        self.dataframe["rsi"] = calculate_rsi(self.dataframe)
        self.dataframe["sma"] = calculate_sma(self.dataframe)
    
    def populate_entry_signals(self):
        # Define buy/sell conditions
        self.dataframe["buy_signal"] = (
            (self.dataframe["rsi"] < 30) & 
            (self.dataframe["close"] > self.dataframe["sma"])
        )
        self.dataframe["sell_signal"] = self.dataframe["rsi"] > 70
    
    def populate_exit_signals(self):
        # Define exit conditions
        self.dataframe["exit_signal"] = self.dataframe["rsi"] > 70
```

2. Register in `main.py`:
```python
from strategies.my_strategy import MyStrategy

STRATEGY_MAP = {
    "rsi": RSIStrategy,
    "macd": MACDStrategy,
    "my_strategy": MyStrategy,  # Add this
}
```

3. Test it:
```bash
python main.py backtest --strategy my_strategy
```

## 🎮 Usage Examples

### Run in Dry-Run Mode (Simulated Trading)
```bash
python main.py dry-run --strategy rsi --config config/default.json
```

### Backtest Strategy
```bash
python main.py backtest --strategy rsi --from 2023-01-01 --to 2023-12-31
```

### Live Trading (⚠️ Use with caution!)
```bash
python main.py live --strategy rsi --config config/default.json
```

### Run with Docker
```bash
docker-compose up
```

## 📊 Available Technical Indicators

All in `tophy/strategy/indicators.py`:

- **SMA** - Simple Moving Average
- **EMA** - Exponential Moving Average
- **RSI** - Relative Strength Index
- **MACD** - Moving Average Convergence Divergence
- **Bollinger Bands** - Upper, middle, lower bands
- **ATR** - Average True Range
- **Stochastic** - Stochastic Oscillator

Example usage:
```python
from tophy.strategy.indicators import calculate_rsi, calculate_sma

dataframe["rsi"] = calculate_rsi(dataframe, period=14)
dataframe["sma"] = calculate_sma(dataframe, period=20)
```

## ⚙️ Configuration

Edit `config/default.json`:

```json
{
  "exchange": {
    "name": "binance",
    "api_key": "your_key",
    "api_secret": "your_secret",
    "is_sandbox": true
  },
  "trading": {
    "mode": "dry-run",
    "pair": "BTC/USDT",
    "timeframe": "1h",
    "stake_amount": 100,
    "max_open_trades": 3,
    "check_interval": 60
  },
  "risk_management": {
    "stop_loss": -0.05,
    "take_profit": 0.10
  }
}
```

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
pytest tests/ --cov=tophy  # With coverage report
```

## 📝 Data Models

### Trade
```python
trade = Trade(
    id="TRADE-001",
    symbol="BTC/USDT",
    entry_time=datetime.now(),
    entry_price=45000.0,
    quantity=0.1,
    side=OrderSide.BUY,
    strategy="rsi",
    stop_loss=42750.0,
    take_profit=49500.0
)
```

### Order
```python
order = Order(
    id="ORD-001",
    symbol="BTC/USDT",
    side=OrderSide.BUY,
    type=OrderType.MARKET,
    price=45000.0,
    quantity=0.1,
    timestamp=datetime.now()
)
```

### Ticker
```python
ticker = exchange.get_ticker("BTC/USDT")
# Properties: symbol, timestamp, open, high, low, close, volume
```

## 🔒 Security

1. Never commit API keys - use `.env` file
2. Use sandbox mode for testing
3. Start with small amounts
4. Monitor bot logs actively
5. Enable IP whitelisting on exchange
6. Use 2FA on exchange account

## 🐛 Troubleshooting

**API Connection Error**
- Verify API keys in `config/default.json`
- Check exchange API permissions
- Ensure IP is whitelisted

**No Data in Backtest**
- Verify trading pair exists
- Check date range validity
- Try shorter timeframe

**Strategy Not Triggering**
- Check logs for errors
- Verify indicators calculate correctly
- Test entry conditions

## 📚 Learning Path

1. **Understand the Architecture** - Read IMPLEMENTATION.md
2. **Install & Configure** - Follow QUICKSTART.md
3. **Test Dry-Run** - Run with built-in strategies
4. **Backtest** - Test strategies on historical data
5. **Create Strategy** - Build your own strategy
6. **Paper Trade** - Use dry-run mode
7. **Go Live** - Start with small amounts

## 🔗 Supported Exchanges

Via CCXT, supports 100+ exchanges:
- Binance
- Kraken
- Coinbase
- Bybit
- Kucoin
- FTX
- Huobi
- OKX
- Poloniex
- Gemini
- [And 100+ more...](https://docs.ccxt.com/)

## 📦 Dependencies

- **ccxt**: Exchange API integration
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **ta**: Technical analysis indicators
- **requests**: HTTP requests
- **pyyaml**: Configuration files
- **plotly**: Data visualization

## 🤝 Contributing

Feel free to:
- Create new strategies
- Add more indicators
- Improve backtesting
- Fix bugs
- Optimize performance

## 📄 License

MIT License - Use freely and modify as needed

## 🎓 Next Steps

1. Install: `pip install -r requirements.txt`
2. Configure: Edit `config/default.json`
3. Test: `python main.py dry-run --strategy rsi`
4. Create: Build your first strategy
5. Backtest: Test before going live
6. Trade: Start with small amounts

---

## 📞 Support

For detailed information:
- General questions → [QUICKSTART.md](QUICKSTART.md)
- Technical details → [IMPLEMENTATION.md](IMPLEMENTATION.md)
- API reference → [CCXT Docs](https://docs.ccxt.com/)

## ⚠️ Disclaimer

**Cryptocurrency trading involves significant risk.** Always:
- Start with small amounts
- Use stop-loss on every trade
- Test thoroughly before live trading
- Never trade money you can't afford to lose
- Monitor your bot regularly

---

**Ready to start?** → Run `python main.py dry-run --strategy rsi`

Happy Trading! 🚀
