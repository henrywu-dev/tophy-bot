"""Data structures and models"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class OrderType(Enum):
    """Order types"""

    MARKET = "market"
    LIMIT = "limit"


class OrderSide(Enum):
    """Order side"""

    BUY = "buy"
    SELL = "sell"


class TradeState(Enum):
    """Trade state"""

    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


@dataclass
class Ticker:
    """Price ticker data"""

    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    @property
    def mid_price(self) -> float:
        """Get mid price"""
        return (self.high + self.low) / 2


@dataclass
class Order:
    """Order data"""

    id: str
    symbol: str
    side: OrderSide
    type: OrderType
    price: float
    quantity: float
    timestamp: datetime
    status: str = "pending"
    filled: float = 0.0
    fee: float = 0.0


@dataclass
class Trade:
    """Trade data"""

    id: str
    symbol: str
    entry_time: datetime
    entry_price: float
    quantity: float
    side: OrderSide
    strategy: str
    state: TradeState = TradeState.OPEN
    exit_time: Optional[datetime] = None
    exit_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    pnl: float = field(default=0.0, init=False)
    pnl_percent: float = field(default=0.0, init=False)

    def calculate_pnl(self) -> None:
        """Calculate PnL"""
        if self.state == TradeState.CLOSED and self.exit_price:
            if self.side == OrderSide.BUY:
                self.pnl = (self.exit_price - self.entry_price) * self.quantity
                self.pnl_percent = ((self.exit_price - self.entry_price) / self.entry_price) * 100
            else:
                self.pnl = (self.entry_price - self.exit_price) * self.quantity
                self.pnl_percent = ((self.entry_price - self.exit_price) / self.entry_price) * 100


@dataclass
class Portfolio:
    """Portfolio data"""

    balance: float = 0.0
    stake_amount: float = 0.0
    open_trades: int = 0
    closed_trades: int = 0
    total_pnl: float = 0.0
    total_pnl_percent: float = 0.0
