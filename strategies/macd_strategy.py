"""Example MACD strategy"""

import pandas as pd
from tophy.strategy.base_strategy import BaseStrategy
from tophy.strategy.indicators import calculate_macd, calculate_sma


class MACDStrategy(BaseStrategy):
    """MACD-based trading strategy"""

    def populate_indicators(self) -> None:
        """Add technical indicators"""
        if self.dataframe is None:
            return

        macd, signal, histogram = calculate_macd(self.dataframe)
        self.dataframe["macd"] = macd
        self.dataframe["macd_signal"] = signal
        self.dataframe["macd_histogram"] = histogram
        self.dataframe["sma_20"] = calculate_sma(self.dataframe, period=20)

    def populate_entry_signals(self) -> None:
        """Generate buy signals"""
        if self.dataframe is None:
            return

        self.dataframe["buy_signal"] = False
        self.dataframe["sell_signal"] = False

        macd = self.dataframe["macd"]
        signal = self.dataframe["macd_signal"]

        # Buy: MACD crosses above signal line
        buy_condition = (
            (macd > signal)
            & (macd.shift(1) <= signal.shift(1))
        )
        self.dataframe.loc[buy_condition, "buy_signal"] = True

        # Sell: MACD crosses below signal line
        sell_condition = (
            (macd < signal)
            & (macd.shift(1) >= signal.shift(1))
        )
        self.dataframe.loc[sell_condition, "sell_signal"] = True

    def populate_exit_signals(self) -> None:
        """Generate exit signals"""
        if self.dataframe is None:
            return

        # Exit when MACD is negative
        self.dataframe["exit_signal"] = self.dataframe["macd"] < 0
