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
            
        signals = []
        for i in range(len(df)):
            row = df.iloc[i]
            
            # Since rolling calculates based on past, we ensure no lookahead
            # If NaNs are present (early data), just HOLD
            if pd.isna(row.get('EMA_20')) or pd.isna(row.get('EMA_50')):
                signals.append(Signal.HOLD)
                continue
                
            # Filters
            trend_up = row['EMA_20'] > row['EMA_50']
            momentum_up = row['RSI_14'] > 55
            volatility_low = pd.notna(atr_median.iloc[i]) and row['ATR_14'] < atr_median.iloc[i]
            volume_up = row['Volume_Change'] > 1.0
            
            # Simple Exit Logic: Trend reversal or momentum loss
            trend_down = row['EMA_20'] < row['EMA_50']
            momentum_down = row['RSI_14'] < 45
            
            if trend_up and momentum_up and volatility_low and volume_up:
                signals.append(Signal.BUY)
            elif trend_down or momentum_down:
                signals.append(Signal.SELL)
            else:
                signals.append(Signal.HOLD)
                
        return pd.Series(signals, index=df.index)
