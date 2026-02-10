"""Example RSI strategy"""

from tophy.strategy.base_strategy import BaseStrategy
from tophy.strategy.indicators import calculate_rsi, calculate_sma


class RSIStrategy(BaseStrategy):
    """Simple RSI-based trading strategy"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rsi_period = 14
        self.rsi_upper = 70
        self.rsi_lower = 30

    def populate_indicators(self) -> None:
        """Add technical indicators"""
        if self.dataframe is None:
            return

        self.dataframe["rsi"] = calculate_rsi(self.dataframe, period=self.rsi_period)
        self.dataframe["sma_20"] = calculate_sma(self.dataframe, period=20)
        self.dataframe["sma_50"] = calculate_sma(self.dataframe, period=50)

    def populate_entry_signals(self) -> None:
        """Generate buy signals"""
        if self.dataframe is None:
            return

        self.dataframe["buy_signal"] = False
        self.dataframe["sell_signal"] = False

        # Buy signal: RSI crosses below 30 (oversold) and price above SMA20
        rsi = self.dataframe["rsi"]
        sma_20 = self.dataframe["sma_20"]
        sma_50 = self.dataframe["sma_50"]
        close = self.dataframe["close"]

        buy_condition = (rsi < self.rsi_lower) & (close > sma_20) & (sma_20 > sma_50)

        self.dataframe.loc[buy_condition, "buy_signal"] = True

        # Sell signal: RSI crosses above 70 (overbought)
        sell_condition = rsi > self.rsi_upper
        self.dataframe.loc[sell_condition, "sell_signal"] = True

    def populate_exit_signals(self) -> None:
        """Generate exit signals"""
        if self.dataframe is None:
            return

        # Exit when RSI is overbought
        self.dataframe["exit_signal"] = self.dataframe["rsi"] > self.rsi_upper
