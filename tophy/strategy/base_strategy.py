"""Base strategy class"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
import pandas as pd

from tophy.utils.logger import get_logger
from tophy.utils.models import OrderSide


logger = get_logger(__name__)


class BaseStrategy(ABC):
    """Base class for trading strategies"""

    def __init__(
        self,
        name: str,
        pair: str,
        timeframe: str = "1h",
        stake_amount: float = 100.0,
        stop_loss: float = -0.05,
        take_profit: float = 0.10,
    ):
        """Initialize strategy"""
        self.name = name
        self.pair = pair
        self.timeframe = timeframe
        self.stake_amount = stake_amount
        self.stop_loss = stop_loss
        self.take_profit = take_profit

        self.dataframe: Optional[pd.DataFrame] = None
        self.current_idx: int = 0

    def set_dataframe(self, dataframe: pd.DataFrame) -> None:
        """Set the dataframe for analysis"""
        self.dataframe = dataframe

    def populate_indicators(self) -> None:
        """
        Populate technical indicators.
        This should be overridden by subclasses.
        """
        pass

    @abstractmethod
    def populate_entry_signals(self) -> None:
        """
        Populate entry signals.
        Must set 'entry_signal' column to True/False
        """
        pass

    @abstractmethod
    def populate_exit_signals(self) -> None:
        """
        Populate exit signals.
        Must set 'exit_signal' column to True/False
        """
        pass

    def get_entry_signal(self, idx: int) -> Optional[OrderSide]:
        """Get entry signal at index"""
        if self.dataframe is None:
            return None

        if idx >= len(self.dataframe):
            return None

        current_row = self.dataframe.iloc[idx]

        if current_row.get("buy_signal"):
            return OrderSide.BUY
        elif current_row.get("sell_signal"):
            return OrderSide.SELL

        return None

    def get_exit_signal(self, idx: int) -> bool:
        """Get exit signal at index"""
        if self.dataframe is None:
            return False

        if idx >= len(self.dataframe):
            return False

        current_row = self.dataframe.iloc[idx]
        return bool(current_row.get("exit_signal", False))

    def analyze(self) -> None:
        """Main analysis method"""
        if self.dataframe is None:
            logger.error("No dataframe set for analysis")
            return

        self.populate_indicators()
        self.populate_entry_signals()
        self.populate_exit_signals()

    def get_entry_price(self, idx: int) -> float:
        """Get entry price"""
        if self.dataframe is None or idx >= len(self.dataframe):
            return 0.0
        return float(self.dataframe.iloc[idx]["close"])

    def get_exit_price(self, idx: int) -> float:
        """Get exit price"""
        if self.dataframe is None or idx >= len(self.dataframe):
            return 0.0
        return float(self.dataframe.iloc[idx]["close"])
