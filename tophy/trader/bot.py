"""Main trading bot"""

import time
from typing import Optional, Dict, Any, List
from datetime import datetime

from tophy.utils.logger import get_logger
from tophy.utils.models import Trade, TradeState, OrderSide, Portfolio
from tophy.exchange.base import BaseExchange
from tophy.strategy.base_strategy import BaseStrategy
from tophy.trader.position_manager import PositionManager


logger = get_logger(__name__)


class TrophyBot:
    """Main trading bot class"""

    def __init__(
        self,
        exchange: BaseExchange,
        strategy: BaseStrategy,
        config: Optional[Dict[str, Any]] = None,
    ):
        """Initialize trading bot"""
        self.exchange = exchange
        self.strategy = strategy
        self.config = config or {}

        self.position_manager = PositionManager(
            max_open_trades=self.config.get("max_open_trades", 3)
        )
        self.portfolio = Portfolio()
        self.closed_trades: List[Trade] = []

        # Configuration
        self.is_running = False
        self.mode = self.config.get("mode", "dry-run")  # dry-run or live
        self.check_interval = self.config.get("check_interval", 60)  # seconds

        logger.info(f"Initialized TrophyBot in {self.mode} mode")

    def start(self) -> None:
        """Start the bot"""
        logger.info("Starting TrophyBot...")
        self.is_running = True

        # Initialize portfolio
        self._update_portfolio()

        try:
            while self.is_running:
                self._trading_loop()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
            self.stop()
        except Exception as e:
            logger.error(f"Bot error: {e}")
            self.stop()

    def stop(self) -> None:
        """Stop the bot"""
        logger.info("Stopping TrophyBot...")
        # Close all open trades at market price
        for trade in self.position_manager.get_open_trades():
            try:
                ticker = self.exchange.get_ticker(trade.symbol)
                self.position_manager.close_trade(trade, ticker.close)
                self.closed_trades.append(trade)
            except Exception as e:
                logger.error(f"Failed to close trade: {e}")

        self.is_running = False
        logger.info("TrophyBot stopped")

    def _trading_loop(self) -> None:
        """Main trading loop"""
        try:
            # Fetch current data
            df = self.exchange.get_ohlcv(
                self.strategy.pair,
                timeframe=self.strategy.timeframe,
                limit=100,
            )

            if df.empty:
                logger.warning("No OHLCV data received")
                return

            # Analyze with strategy
            self.strategy.set_dataframe(df)
            self.strategy.populate_indicators()
            self.strategy.populate_entry_signals()
            self.strategy.populate_exit_signals()

            # Get latest candle
            latest_idx = len(df) - 1
            latest_price = df.iloc[latest_idx]["close"]

            # Check exit signals
            exit_signal = self.strategy.get_exit_signal(latest_idx)
            if exit_signal:
                self._handle_exit_signal(latest_price)

            # Check entry signals
            entry_signal = self.strategy.get_entry_signal(latest_idx)
            if entry_signal:
                self._handle_entry_signal(entry_signal, latest_price)

            # Check stop loss and take profit
            self._check_risk_management(latest_price)

            # Update portfolio
            self._update_portfolio()

        except Exception as e:
            logger.error(f"Error in trading loop: {e}")

    def _handle_entry_signal(self, side: OrderSide, price: float) -> None:
        """Handle entry signal"""
        if len(self.position_manager.get_open_trades()) >= self.position_manager.max_open_trades:
            logger.info("Max open trades reached, skipping entry")
            return

        if self.portfolio.balance < self.strategy.stake_amount:
            logger.warning("Insufficient balance for trade entry")
            return

        trade = Trade(
            id=f"TRADE-{datetime.now().timestamp()}",
            symbol=self.strategy.pair,
            entry_time=datetime.now(),
            entry_price=price,
            quantity=self.strategy.stake_amount / price,
            side=side,
            strategy=self.strategy.name,
            stop_loss=price * (1 + self.strategy.stop_loss),
            take_profit=price * (1 + self.strategy.take_profit),
        )

        if self.mode == "live":
            try:
                self.exchange.create_order(
                    symbol=self.strategy.pair,
                    order_type="market",
                    side=side,
                    amount=trade.quantity,
                )
                logger.info(f"Created market order: {side.value} {trade.quantity}")
            except Exception as e:
                logger.error(f"Failed to create order: {e}")
                return

        self.position_manager.open_trade(trade)
        self.portfolio.balance -= self.strategy.stake_amount
        self.portfolio.open_trades = len(self.position_manager.get_open_trades())

    def _handle_exit_signal(self, price: float) -> None:
        """Handle exit signal"""
        open_trades = self.position_manager.get_open_trades()
        if not open_trades:
            return

        trade = open_trades[0]

        if self.mode == "live":
            try:
                # Determine sell side based on entry side
                sell_side = OrderSide.SELL if trade.side == OrderSide.BUY else OrderSide.BUY
                self.exchange.create_order(
                    symbol=self.strategy.pair,
                    order_type="market",
                    side=sell_side,
                    amount=trade.quantity,
                )
                logger.info(f"Created exit order: {sell_side.value} {trade.quantity}")
            except Exception as e:
                logger.error(f"Failed to create exit order: {e}")
                return

        self.position_manager.close_trade(trade, price)
        self.closed_trades.append(trade)
        self.portfolio.balance += trade.quantity * price

    def _check_risk_management(self, current_price: float) -> None:
        """Check stop loss and take profit"""
        # Check stop loss
        stop_loss_hits = self.position_manager.check_stop_loss(current_price)
        for trade in stop_loss_hits:
            logger.info(f"Stop loss triggered for {trade.symbol}")
            self._handle_exit_signal(current_price)

        # Check take profit
        take_profit_hits = self.position_manager.check_take_profit(current_price)
        for trade in take_profit_hits:
            logger.info(f"Take profit triggered for {trade.symbol}")
            self._handle_exit_signal(current_price)

    def _update_portfolio(self) -> None:
        """Update portfolio information"""
        try:
            balance = self.exchange.get_balance()
            # Assuming the first balance is the main currency
            main_balance = list(balance.values())[0] if balance else 0

            self.portfolio.balance = main_balance
            self.portfolio.open_trades = len(self.position_manager.get_open_trades())
            self.portfolio.closed_trades = len(self.closed_trades)
            self.portfolio.total_pnl = sum(t.pnl for t in self.closed_trades)
            self.portfolio.total_pnl_percent = (
                (self.portfolio.total_pnl / 10000) * 100
                if self.config.get("initial_balance")
                else 0
            )

        except Exception as e:
            logger.warning(f"Failed to update portfolio: {e}")

    def get_portfolio_stats(self) -> Dict[str, Any]:
        """Get portfolio statistics"""
        return {
            "balance": self.portfolio.balance,
            "open_trades": self.portfolio.open_trades,
            "closed_trades": self.portfolio.closed_trades,
            "total_pnl": self.portfolio.total_pnl,
            "total_pnl_percent": self.portfolio.total_pnl_percent,
        }
