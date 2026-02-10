"""Backtesting engine"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd

from tophy.utils.logger import get_logger
from tophy.utils.models import Trade, TradeState, OrderSide
from tophy.strategy.base_strategy import BaseStrategy
from tophy.exchange.base import BaseExchange


logger = get_logger(__name__)


class BacktestEngine:
    """Backtesting engine for strategy evaluation"""

    def __init__(
        self,
        strategy: BaseStrategy,
        exchange: BaseExchange,
        initial_balance: float = 10000.0,
    ):
        """Initialize backtesting engine"""
        self.strategy = strategy
        self.exchange = exchange
        self.initial_balance = initial_balance
        self.balance = initial_balance

        self.trades: List[Trade] = []
        self.open_trades: List[Trade] = []

    def fetch_historical_data(
        self,
        symbol: str,
        timeframe: str = "1h",
        days: int = 30,
    ) -> pd.DataFrame:
        """Fetch historical data for backtesting"""
        try:
            # Fetch data in chunks due to API limits
            all_data = []
            current_date = datetime.now()

            for i in range(0, days, 100):
                try:
                    data = self.exchange.get_ohlcv(
                        symbol,
                        timeframe=timeframe,
                        limit=min(100, days - i),
                    )
                    all_data.append(data)
                except Exception as e:
                    logger.warning(f"Error fetching data chunk: {e}")
                    break

            if not all_data:
                logger.error("No historical data fetched")
                return pd.DataFrame()

            df = pd.concat(all_data)
            df = df.sort_index()
            df = df[~df.index.duplicated(keep="first")]

            logger.info(f"Fetched {len(df)} candles for {symbol}")
            return df

        except Exception as e:
            logger.error(f"Failed to fetch historical data: {e}")
            raise

    def run(
        self,
        data: pd.DataFrame,
        symbol: str,
    ) -> Dict[str, Any]:
        """Run backtest"""
        logger.info("Starting backtest...")

        self.strategy.set_dataframe(data)
        self.strategy.analyze()

        # Simulate trading
        for idx in range(len(data)):
            self._process_bar(idx, data.iloc[idx])

        # Close any remaining open trades
        for trade in self.open_trades:
            self._close_trade(trade, data.iloc[-1]["close"])

        results = self._calculate_results(data)
        logger.info("Backtest completed")

        return results

    def _process_bar(self, idx: int, bar: pd.Series) -> None:
        """Process a bar of data"""
        # Check exit signals
        exit_signal = self.strategy.get_exit_signal(idx)

        if exit_signal and self.open_trades:
            trade_to_close = self.open_trades[0]
            self._close_trade(trade_to_close, bar["close"])

        # Check entry signals
        entry_signal = self.strategy.get_entry_signal(idx)

        if entry_signal and not self.open_trades:
            # Check if we have enough balance
            entry_price = bar["close"]
            quantity = self.strategy.stake_amount / entry_price

            if quantity > 0 and self.balance >= self.strategy.stake_amount:
                trade = Trade(
                    id=f"BT-{len(self.trades) + 1}",
                    symbol=self.strategy.pair,
                    entry_time=bar.name,
                    entry_price=entry_price,
                    quantity=quantity,
                    side=entry_signal,
                    strategy=self.strategy.name,
                    stop_loss=entry_price * (1 + self.strategy.stop_loss),
                    take_profit=entry_price * (1 + self.strategy.take_profit),
                )

                self.open_trades.append(trade)
                self.balance -= self.strategy.stake_amount
                logger.debug(f"Entry trade at {entry_price}")

        # Check stop loss and take profit
        for trade in self.open_trades[:]:
            if trade.stop_loss and bar["close"] <= trade.stop_loss:
                self._close_trade(trade, trade.stop_loss)
            elif trade.take_profit and bar["close"] >= trade.take_profit:
                self._close_trade(trade, trade.take_profit)

    def _close_trade(self, trade: Trade, exit_price: float) -> None:
        """Close a trade"""
        trade.exit_price = exit_price
        trade.exit_time = datetime.now()
        trade.state = TradeState.CLOSED
        trade.calculate_pnl()

        self.balance += trade.quantity * exit_price

        self.trades.append(trade)
        self.open_trades.remove(trade)

        logger.debug(f"Exit trade at {exit_price}, PnL: {trade.pnl:.2f}")

    def _calculate_results(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate backtest results"""
        if not self.trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0.0,
                "total_pnl": 0.0,
                "total_pnl_percent": 0.0,
                "avg_trade_duration": 0,
                "sharpe_ratio": 0.0,
            }

        winning_trades = len([t for t in self.trades if t.pnl > 0])
        losing_trades = len([t for t in self.trades if t.pnl <= 0])
        win_rate = winning_trades / len(self.trades) if self.trades else 0

        total_pnl = sum(t.pnl for t in self.trades)
        total_pnl_percent = (total_pnl / self.initial_balance) * 100

        # Average trade duration
        durations = [
            (t.exit_time - t.entry_time).total_seconds()
            for t in self.trades
            if t.exit_time
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_trades": len(self.trades),
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "win_rate": win_rate,
            "total_pnl": total_pnl,
            "total_pnl_percent": total_pnl_percent,
            "avg_trade_duration": avg_duration,
            "final_balance": self.balance,
            "profit_factor": self._calculate_profit_factor(),
        }

    def _calculate_profit_factor(self) -> float:
        """Calculate profit factor"""
        gross_profit = sum(t.pnl for t in self.trades if t.pnl > 0)
        gross_loss = abs(sum(t.pnl for t in self.trades if t.pnl < 0))

        if gross_loss == 0:
            return 0.0

        return gross_profit / gross_loss
