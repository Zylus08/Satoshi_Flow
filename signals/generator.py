import pandas as pd
from enum import Enum
import numpy as np

class Signal(Enum):
    BUY = 1
    SELL = -1
    HOLD = 0

class SignalGenerator:
    """
    Generates trading signals based on engineered features.
    """
    
    @staticmethod
    def generate_signals(df: pd.DataFrame) -> pd.Series:
        """
        Calculates signal for each row in the DataFrame.
        Returns a Series of Signal enums.
        """
        # Calculate ATR rolling median for Volatility Filter
        # Using a 20-day rolling median of the 14-day ATR
        if 'ATR_14' in df.columns:
            atr_median = df['ATR_14'].rolling(window=20).median()
        else:
            atr_median = pd.Series(index=df.index, dtype=float)
            
        # Initialize signals to HOLD
        signals = pd.Series(Signal.HOLD, index=df.index)
        
        # Filters
        valid_rows = df['EMA_20'].notna() & df['EMA_50'].notna()
        trend_up = df['EMA_20'] > df['EMA_50']
        momentum_up = df['RSI_14'] > 55
        volatility_low = atr_median.notna() & (df['ATR_14'] < atr_median)
        volume_up = df['Volume_Change'] > 1.0
        
        # Simple Exit Logic: Trend reversal or momentum loss
        trend_down = df['EMA_20'] < df['EMA_50']
        momentum_down = df['RSI_14'] < 45
        
        buy_condition = valid_rows & trend_up & momentum_up & volatility_low & volume_up
        sell_condition = valid_rows & (trend_down | momentum_down)
        
        # We process SELL conditions first, then BUY (if both are true somehow, SELL overrides)
        signals[buy_condition] = Signal.BUY
        signals[sell_condition] = Signal.SELL
        
        return signals
