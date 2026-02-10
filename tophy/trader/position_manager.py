"""Position management"""

from typing import List, Optional
from datetime import datetime

from tophy.utils.logger import get_logger
from tophy.utils.models import Trade, TradeState, OrderSide


logger = get_logger(__name__)


class PositionManager:
    """Manages open positions"""

    def __init__(self, max_open_trades: int = 3):
        """Initialize position manager"""
        self.max_open_trades = max_open_trades
        self.open_trades: List[Trade] = []

    def open_trade(self, trade: Trade) -> bool:
        """Open a new trade"""
        if len(self.open_trades) >= self.max_open_trades:
            logger.warning(
                f"Maximum open trades ({self.max_open_trades}) reached"
            )
            return False

        self.open_trades.append(trade)
        logger.info(
            f"Opened trade: {trade.symbol} @ {trade.entry_price} "
            f"(Q: {trade.quantity})"
        )
        return True

    def close_trade(self, trade: Trade, exit_price: float) -> bool:
        """Close an open trade"""
        if trade not in self.open_trades:
            logger.warning(f"Trade not found in open trades")
            return False

        trade.exit_price = exit_price
        trade.exit_time = datetime.now()
        trade.state = TradeState.CLOSED
        trade.calculate_pnl()

        self.open_trades.remove(trade)

        logger.info(
            f"Closed trade: {trade.symbol} @ {exit_price} "
            f"(PnL: {trade.pnl:.2f} / {trade.pnl_percent:.2f}%)"
        )
        return True

    def get_open_trades(self, symbol: Optional[str] = None) -> List[Trade]:
        """Get open trades"""
        if symbol:
            return [t for t in self.open_trades if t.symbol == symbol]
        return self.open_trades

    def get_trade_count(self) -> int:
        """Get number of open trades"""
        return len(self.open_trades)

    def check_stop_loss(self, current_price: float) -> List[Trade]:
        """Check for stop loss hits"""
        triggered = []
        for trade in self.open_trades:
            if trade.stop_loss and current_price <= trade.stop_loss:
                triggered.append(trade)
        return triggered

    def check_take_profit(self, current_price: float) -> List[Trade]:
        """Check for take profit hits"""
        triggered = []
        for trade in self.open_trades:
            if trade.take_profit and current_price >= trade.take_profit:
                triggered.append(trade)
        return triggered
