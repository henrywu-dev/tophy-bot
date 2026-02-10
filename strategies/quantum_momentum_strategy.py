"""
Quantum Momentum Strategy - A Creative Multi-Layer Trading Strategy

This strategy combines:
1. Volatility Regime Detection - identifies trending vs ranging markets
2. Momentum Divergence - detects hidden strength/weakness
3. Volume Wave Confirmation - validates moves with volume
4. Dynamic Risk Management - adaptive stop-loss/TP based on volatility

The strategy works by finding "confluence points" where multiple signals align,
creating high-probability trade setups.
"""

import pandas as pd
import numpy as np
from tophy.strategy.base_strategy import BaseStrategy
from tophy.strategy.indicators import calculate_rsi, calculate_sma, calculate_atr
from tophy.utils.models import OrderSide


class QuantumMomentumStrategy(BaseStrategy):
    """
    Advanced multi-layer momentum strategy with volatility awareness.
    
    Trading Logic:
    - Buy: Volatility increases + Momentum divergence + Volume confirms + Price breakout
    - Sell: Opposite conditions + Trend exhaustion signals
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Volatility parameters
        self.volatility_period = 20
        self.volatility_threshold = 1.2  # 20% above average
        
        # Momentum parameters
        self.rsi_period = 14
        self.rsi_extreme_low = 25
        self.rsi_extreme_high = 75
        self.divergence_lookback = 5
        
        # Volume parameters
        self.volume_period = 20
        self.volume_multiplier = 1.5
        
        # Trend parameters
        self.sma_fast = 9
        self.sma_medium = 21
        self.sma_slow = 55
        
    def populate_indicators(self) -> None:
        """Populate all technical indicators"""
        if self.dataframe is None:
            return
        
        df = self.dataframe
        
        # === VOLATILITY INDICATORS ===
        # Calculate ATR for volatility
        df["atr"] = calculate_atr(df, period=14)
        df["atr_sma"] = df["atr"].rolling(window=self.volatility_period).mean()
        df["volatility_ratio"] = df["atr"] / df["atr_sma"]
        df["high_volatility"] = df["volatility_ratio"] > self.volatility_threshold
        
        # Standard deviation for volatility bands
        df["std_dev"] = df["close"].rolling(window=20).std()
        df["mean"] = df["close"].rolling(window=20).mean()
        df["vol_upper"] = df["mean"] + (2 * df["std_dev"])
        df["vol_lower"] = df["mean"] - (2 * df["std_dev"])
        
        # === MOMENTUM INDICATORS ===
        df["rsi"] = calculate_rsi(df, period=self.rsi_period)
        df["momentum"] = df["close"].diff(period=3)
        df["momentum_ma"] = df["momentum"].rolling(window=10).mean()
        
        # === VOLUME INDICATORS ===
        df["volume_ma"] = df["volume"].rolling(window=self.volume_period).mean()
        df["volume_ratio"] = df["volume"] / df["volume_ma"]
        df["volume_increasing"] = df["volume_ratio"] > self.volume_multiplier
        
        # === PRICE ACTION INDICATORS ===
        df["sma_fast"] = calculate_sma(df, period=self.sma_fast)
        df["sma_medium"] = calculate_sma(df, period=self.sma_medium)
        df["sma_slow"] = calculate_sma(df, period=self.sma_slow)
        
        # Price position relative to SMAs
        df["price_vs_fast"] = df["close"] > df["sma_fast"]
        df["price_vs_medium"] = df["close"] > df["sma_medium"]
        df["price_vs_slow"] = df["close"] > df["sma_slow"]
        
        # === ADVANCED INDICATORS ===
        # Momentum strength
        df["momentum_strength"] = (df["momentum"] / df["close"]) * 100
        
        # Price acceleration (rate of change)
        df["roc"] = df["close"].pct_change(periods=5) * 100
        
        # Volume divergence (volume vs momentum direction)
        df["vol_momentum_divergence"] = (
            (df["momentum"] * df["volume_ratio"]).rolling(window=3).mean()
        )

    def populate_entry_signals(self) -> None:
        """Generate buy and sell signals"""
        if self.dataframe is None:
            return
        
        df = self.dataframe
        df["buy_signal"] = False
        df["sell_signal"] = False
        
        # === BUY SIGNAL CONDITIONS ===
        # Condition 1: Volatility Expansion (market waking up)
        volatility_expansion = df["high_volatility"] & (df["volume_increasing"])
        
        # Condition 2: Bullish Divergence (price recovers, momentum strengthens)
        price_near_lower_band = df["close"] < df["vol_lower"] + (0.5 * df["std_dev"])
        momentum_recovering = (df["rsi"] > self.rsi_extreme_low) & (df["rsi"].shift(1) < self.rsi_extreme_low)
        bullish_divergence = price_near_lower_band & momentum_recovering
        
        # Condition 3: Momentum Confirmation (positive momentum acceleration)
        positive_momentum = df["momentum"] > 0
        momentum_accelerating = df["momentum"] > df["momentum"].shift(1)
        momentum_strong = abs(df["momentum_strength"]) > 0.5
        momentum_confirmation = positive_momentum & momentum_accelerating & momentum_strong
        
        # Condition 4: Trend Alignment (price above key moving averages)
        trend_bullish = (df["price_vs_fast"] & df["price_vs_medium"])
        
        # Condition 5: Volume Wave (volume confirms the move)
        volume_wave = df["volume_ratio"] > 1.2
        
        # === COMPOSITE BUY SIGNAL ===
        # Strong setup: Volatility expansion + Momentum confirmation + Trend alignment
        buy_strong = (
            volatility_expansion & 
            momentum_confirmation & 
            trend_bullish &
            volume_wave
        )
        
        # Moderate setup: Divergence + Volume confirmation + Trend
        buy_moderate = (
            bullish_divergence &
            volume_wave &
            trend_bullish
        )
        
        df.loc[buy_strong | buy_moderate, "buy_signal"] = True
        
        # === SELL SIGNAL CONDITIONS ===
        # Condition 1: Bearish Divergence (price peaks, momentum weakens)
        price_near_upper_band = df["close"] > df["vol_upper"] - (0.5 * df["std_dev"])
        momentum_weakening = (df["rsi"] < self.rsi_extreme_high) & (df["rsi"].shift(1) > self.rsi_extreme_high)
        bearish_divergence = price_near_upper_band & momentum_weakening
        
        # Condition 2: Negative Momentum Acceleration
        negative_momentum = df["momentum"] < 0
        momentum_accelerating_down = df["momentum"] < df["momentum"].shift(1)
        momentum_weak = abs(df["momentum_strength"]) > 0.5
        momentum_weakened = negative_momentum & momentum_accelerating_down & momentum_weak
        
        # Condition 3: Trend Reversal (price crosses below medium SMA)
        trend_bearish = (df["close"] < df["sma_medium"]) & (df["close"].shift(1) > df["sma_medium"])
        
        # Condition 4: Volume Exhaustion (volume decreases on up move)
        volume_exhaustion = df["volume_ratio"] < 0.8 & negative_momentum
        
        # === COMPOSITE SELL SIGNAL ===
        sell_strong = (
            bearish_divergence &
            momentum_weakened &
            trend_bearish
        )
        
        sell_moderate = (
            trend_bearish &
            volume_exhaustion
        )
        
        df.loc[sell_strong | sell_moderate, "sell_signal"] = True

    def populate_exit_signals(self) -> None:
        """Generate exit signals for open trades"""
        if self.dataframe is None:
            return
        
        df = self.dataframe
        
        # Exit Condition 1: Extreme RSI (overbought/oversold)
        rsi_extreme = (df["rsi"] > 85) | (df["rsi"] < 15)
        
        # Exit Condition 2: Momentum reversal
        momentum_reversal = (
            (df["momentum"] * df["momentum"].shift(1)) < 0
        )
        
        # Exit Condition 3: Breaking below/above key support/resistance
        breaking_support = df["close"] < df["sma_slow"]
        
        # Exit Condition 4: Volatility collapse (trend ending)
        volatility_collapse = (df["volatility_ratio"] < 0.7)
        
        # Composite exit
        df["exit_signal"] = rsi_extreme | momentum_reversal | breaking_support | volatility_collapse
        
        # Smooth the signal to avoid multiple exits
        df["exit_signal"] = df["exit_signal"].rolling(window=2).max()

    def get_trade_strength(self, idx: int) -> float:
        """
        Calculate signal strength for position sizing
        Returns 0.0 to 1.0 indicating how strong the trade signal is
        """
        if self.dataframe is None or idx >= len(self.dataframe):
            return 0.0
        
        row = self.dataframe.iloc[idx]
        
        strength = 0.0
        
        # Volatility strength (0-0.2)
        if row.get("high_volatility"):
            strength += 0.2
        
        # Momentum strength (0-0.3)
        momentum_pct = abs(row.get("momentum_strength", 0))
        if momentum_pct > 1.0:
            strength += 0.3
        elif momentum_pct > 0.5:
            strength += 0.15
        
        # Trend alignment strength (0-0.3)
        trend_alignment = sum([
            row.get("price_vs_fast", False),
            row.get("price_vs_medium", False),
            row.get("price_vs_slow", False)
        ]) / 3.0
        strength += trend_alignment * 0.3
        
        # Volume confirmation (0-0.2)
        if row.get("volume_increasing"):
            strength += 0.2
        
        return min(strength, 1.0)
    
    def get_dynamic_stop_loss(self, entry_price: float, idx: int) -> float:
        """
        Calculate dynamic stop-loss based on volatility
        Wider stops in high volatility, tighter in low volatility
        """
        if self.dataframe is None or idx >= len(self.dataframe):
            return entry_price * (1 + self.stop_loss)
        
        row = self.dataframe.iloc[idx]
        atr = row.get("atr", 0)
        
        # Dynamic stop: 1.5 to 3 ATRs depending on volatility
        if row.get("high_volatility"):
            stop_distance = atr * 3
        else:
            stop_distance = atr * 1.5
        
        return entry_price - stop_distance
    
    def get_dynamic_take_profit(self, entry_price: float, idx: int) -> float:
        """
        Calculate dynamic take-profit based on volatility and momentum
        Targets are 2-4x the risk based on signal strength
        """
        if self.dataframe is None or idx >= len(self.dataframe):
            return entry_price * (1 + self.take_profit)
        
        row = self.dataframe.iloc[idx]
        atr = row.get("atr", 0)
        
        # Dynamic TP: 2-4 ATRs based on momentum strength
        momentum_pct = abs(row.get("momentum_strength", 0))
        if momentum_pct > 1.5:
            tp_distance = atr * 4
        elif momentum_pct > 0.5:
            tp_distance = atr * 3
        else:
            tp_distance = atr * 2
        
        return entry_price + tp_distance
