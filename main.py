"""CLI interface for the bot"""

import argparse
import json
from pathlib import Path

from tophy.utils.logger import get_logger
from tophy.utils.config import load_config
from tophy.exchange.base import BaseExchange
from tophy.trader.bot import TrophyBot
from tophy.backtest.engine import BacktestEngine
from strategies.rsi_strategy import RSIStrategy
from strategies.macd_strategy import MACDStrategy


logger = get_logger(__name__)


STRATEGY_MAP = {
    "rsi": RSIStrategy,
    "macd": MACDStrategy,
}


def main():
    parser = argparse.ArgumentParser(description="Tophy Bot - Crypto Trading Bot")
    parser.add_argument(
        "mode",
        choices=["live", "dry-run", "backtest"],
        help="Bot operating mode",
    )
    parser.add_argument(
        "--strategy",
        required=True,
        choices=list(STRATEGY_MAP.keys()),
        help="Trading strategy to use",
    )
    parser.add_argument(
        "--config",
        default="config/default.json",
        help="Configuration file path",
    )
    parser.add_argument(
        "--from",
        dest="from_date",
        help="Backtest start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--to",
        dest="to_date",
        help="Backtest end date (YYYY-MM-DD)",
    )

    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        return

    # Initialize exchange
    exchange_config = config["exchange"]
    exchange = BaseExchange(
        exchange_name=exchange_config["name"],
        api_key=exchange_config["api_key"],
        api_secret=exchange_config["api_secret"],
        is_sandbox=exchange_config.get("is_sandbox", True),
    )

    # Initialize strategy
    strategy_class = STRATEGY_MAP[args.strategy]
    trading_config = config["trading"]
    strategy = strategy_class(
        name=args.strategy,
        pair=trading_config["pair"],
        timeframe=trading_config.get("timeframe", "1h"),
        stake_amount=trading_config.get("stake_amount", 100),
        stop_loss=config["risk_management"]["stop_loss"],
        take_profit=config["risk_management"]["take_profit"],
    )

    if args.mode == "backtest":
        logger.info(f"Starting backtest with {args.strategy} strategy...")
        backtest_engine = BacktestEngine(
            strategy=strategy,
            exchange=exchange,
            initial_balance=config["backtest"]["initial_balance"],
        )

        try:
            data = backtest_engine.fetch_historical_data(
                symbol=trading_config["pair"],
                timeframe=trading_config.get("timeframe", "1h"),
                days=config["backtest"].get("days", 30),
            )

            if not data.empty:
                results = backtest_engine.run(data, trading_config["pair"])
                logger.info("Backtest Results:")
                for key, value in results.items():
                    logger.info(f"  {key}: {value}")
            else:
                logger.error("No data for backtest")

        except Exception as e:
            logger.error(f"Backtest failed: {e}")

    else:
        logger.info(f"Starting bot in {args.mode} mode with {args.strategy} strategy...")
        bot = TrophyBot(
            exchange=exchange,
            strategy=strategy,
            config={
                "mode": args.mode,
                **trading_config,
                **config["risk_management"],
            },
        )

        try:
            bot.start()
        except KeyboardInterrupt:
            logger.info("Bot interrupted")
        except Exception as e:
            logger.error(f"Bot error: {e}")


if __name__ == "__main__":
    main()
