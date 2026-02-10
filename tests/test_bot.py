"""Unit tests for the trading bot"""

from datetime import datetime

import pandas as pd
import pytest

from strategies.rsi_strategy import RSIStrategy
from tophy.strategy.indicators import calculate_macd, calculate_rsi, calculate_sma
from tophy.utils.models import OrderSide, OrderType, Trade, TradeState


@pytest.fixture
def sample_dataframe():
    """Create sample OHLCV data"""
    dates = pd.date_range(start="2023-01-01", periods=100, freq="1h")
    data = {
        "open": [100 + i * 0.5 for i in range(100)],
        "high": [101 + i * 0.5 for i in range(100)],
        "low": [99 + i * 0.5 for i in range(100)],
        "close": [100.5 + i * 0.5 for i in range(100)],
        "volume": [1000] * 100,
    }
    df = pd.DataFrame(data, index=dates)
    return df


def test_calculate_sma(sample_dataframe):
    """Test SMA calculation"""
    sma = calculate_sma(sample_dataframe, period=20)
    assert len(sma) == len(sample_dataframe)
    assert pd.isna(sma.iloc[19]) == False


def test_calculate_rsi(sample_dataframe):
    """Test RSI calculation"""
    rsi = calculate_rsi(sample_dataframe, period=14)
    assert len(rsi) == len(sample_dataframe)
    assert rsi[rsi.notna()].min() >= 0
    assert rsi[rsi.notna()].max() <= 100


def test_calculate_macd(sample_dataframe):
    """Test MACD calculation"""
    macd, signal, histogram = calculate_macd(sample_dataframe)
    assert len(macd) == len(sample_dataframe)
    assert len(signal) == len(sample_dataframe)
    assert len(histogram) == len(sample_dataframe)


def test_rsi_strategy(sample_dataframe):
    """Test RSI strategy"""
    strategy = RSIStrategy(
        name="test_rsi",
        pair="BTC/USDT",
        stake_amount=100,
    )
    strategy.set_dataframe(sample_dataframe)
    strategy.analyze()

    assert "rsi" in strategy.dataframe.columns
    assert "buy_signal" in strategy.dataframe.columns
    assert "exit_signal" in strategy.dataframe.columns


def test_trade_pnl():
    """Test trade PnL calculation"""
    trade = Trade(
        id="TEST-1",
        symbol="BTC/USDT",
        entry_time=datetime.now(),
        entry_price=50000.0,
        quantity=0.1,
        side=OrderSide.BUY,
        strategy="test",
    )

    # Simulate profitable trade
    trade.exit_price = 55000.0
    trade.exit_time = datetime.now()
    trade.state = TradeState.CLOSED
    trade.calculate_pnl()

    assert trade.pnl == 500.0
    assert trade.pnl_percent == 10.0


if __name__ == "__main__":
    pytest.main([__file__])
