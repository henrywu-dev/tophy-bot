"""Technical indicators"""

import pandas as pd


def calculate_sma(dataframe: pd.DataFrame, column: str = "close", period: int = 20) -> pd.Series:
    """Calculate Simple Moving Average"""
    return dataframe[column].rolling(window=period).mean()


def calculate_ema(dataframe: pd.DataFrame, column: str = "close", period: int = 20) -> pd.Series:
    """Calculate Exponential Moving Average"""
    return dataframe[column].ewm(span=period).mean()


def calculate_rsi(dataframe: pd.DataFrame, column: str = "close", period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index"""
    delta = dataframe[column].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_macd(
    dataframe: pd.DataFrame,
    column: str = "close",
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> tuple:
    """Calculate MACD"""
    exp1 = dataframe[column].ewm(span=fast).mean()
    exp2 = dataframe[column].ewm(span=slow).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram


def calculate_bollinger_bands(
    dataframe: pd.DataFrame,
    column: str = "close",
    period: int = 20,
    std_dev: float = 2.0,
) -> tuple:
    """Calculate Bollinger Bands"""
    sma = dataframe[column].rolling(window=period).mean()
    std = dataframe[column].rolling(window=period).std()
    upper = sma + (std * std_dev)
    lower = sma - (std * std_dev)
    return upper, sma, lower


def calculate_atr(
    dataframe: pd.DataFrame,
    period: int = 14,
) -> pd.Series:
    """Calculate Average True Range"""
    high_low = dataframe["high"] - dataframe["low"]
    high_close = abs(dataframe["high"] - dataframe["close"].shift())
    low_close = abs(dataframe["low"] - dataframe["close"].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    atr = true_range.rolling(period).mean()
    return atr


def calculate_stochastic(
    dataframe: pd.DataFrame,
    period: int = 14,
    smoothing: int = 3,
) -> tuple:
    """Calculate Stochastic Oscillator"""
    low_min = dataframe["low"].rolling(window=period).min()
    high_max = dataframe["high"].rolling(window=period).max()

    k = 100 * ((dataframe["close"] - low_min) / (high_max - low_min))
    d = k.rolling(window=smoothing).mean()

    return k, d
