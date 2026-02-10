"""Base exchange class"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import ccxt
import pandas as pd

from tophy.utils.logger import get_logger
from tophy.utils.models import Order, OrderSide, OrderType, Ticker

logger = get_logger(__name__)


class BaseExchange:
    """Base class for exchange connectors"""

    def __init__(
        self,
        exchange_name: str,
        api_key: str,
        api_secret: str,
        is_sandbox: bool = False,
    ):
        """Initialize exchange connector"""
        self.exchange_name = exchange_name.lower()
        self.api_key = api_key
        self.api_secret = api_secret
        self.is_sandbox = is_sandbox

        # Initialize exchange
        self._init_exchange()

    def _init_exchange(self) -> None:
        """Initialize CCXT exchange"""
        try:
            exchange_class = getattr(ccxt, self.exchange_name)
            self.exchange = exchange_class(
                {
                    "apiKey": self.api_key,
                    "secret": self.api_secret,
                    "sandbox": self.is_sandbox,
                    "enableRateLimit": True,
                }
            )
            self.exchange.load_markets()
            logger.info(f"Initialized {self.exchange_name} exchange")
        except Exception as e:
            logger.error(f"Failed to initialize exchange: {e}")
            raise

    def get_ticker(self, symbol: str) -> Ticker:
        """Get current ticker for symbol"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return Ticker(
                symbol=symbol,
                timestamp=datetime.fromtimestamp(ticker["timestamp"] / 1000),
                open=ticker["open"],
                high=ticker["high"],
                low=ticker["low"],
                close=ticker["close"],
                volume=ticker["quoteVolume"],
            )
        except Exception as e:
            logger.error(f"Failed to fetch ticker for {symbol}: {e}")
            raise

    def get_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1h",
        limit: int = 100,
    ) -> pd.DataFrame:
        """Get OHLCV data"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv,
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df = df.set_index("timestamp")
            return df
        except Exception as e:
            logger.error(f"Failed to fetch OHLCV for {symbol}: {e}")
            raise

    def get_balance(self) -> Dict[str, float]:
        """Get account balance"""
        try:
            balance = self.exchange.fetch_balance()
            return balance["free"]
        except Exception as e:
            logger.error(f"Failed to fetch balance: {e}")
            raise

    def create_order(
        self,
        symbol: str,
        order_type: OrderType,
        side: OrderSide,
        amount: float,
        price: Optional[float] = None,
    ) -> Order:
        """Create an order"""
        try:
            order = self.exchange.create_order(
                symbol=symbol,
                type=order_type.value,
                side=side.value,
                amount=amount,
                price=price,
            )
            return self._parse_order(order)
        except Exception as e:
            logger.error(f"Failed to create order: {e}")
            raise

    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """Cancel an order"""
        try:
            self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Cancelled order {order_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel order: {e}")
            return False

    def get_order_status(self, order_id: str, symbol: str) -> str:
        """Get order status"""
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order["status"]
        except Exception as e:
            logger.error(f"Failed to fetch order status: {e}")
            raise

    def get_open_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """Get open orders"""
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            return [self._parse_order(order) for order in orders]
        except Exception as e:
            logger.error(f"Failed to fetch open orders: {e}")
            raise

    def get_my_trades(
        self,
        symbol: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """Get trade history"""
        try:
            trades = self.exchange.fetch_my_trades(symbol, limit=limit)
            return trades
        except Exception as e:
            logger.error(f"Failed to fetch trades: {e}")
            raise

    def _parse_order(self, order: Dict) -> Order:
        """Parse order from exchange response"""
        return Order(
            id=order["id"],
            symbol=order["symbol"],
            side=OrderSide(order["side"]),
            type=OrderType(order["type"]),
            price=order["price"],
            quantity=order["amount"],
            timestamp=datetime.fromtimestamp(order["timestamp"] / 1000),
            status=order["status"],
            filled=order["filled"],
            fee=order.get("fee", {}).get("cost", 0.0),
        )

    def get_symbols(self) -> List[str]:
        """Get available trading symbols"""
        return self.exchange.symbols
