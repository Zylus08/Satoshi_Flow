import pandas as pd
from signals.generator import Signal
from indicators.core import calculate_ema

class BuyAndHoldStrategy:
    """
    Buys on the first available bar and holds.
    """
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        signals = [Signal.HOLD] * len(df)
        if len(signals) > 0:
            signals[0] = Signal.BUY
        df['Signal'] = signals
        return df

class EMACrossoverStrategy:
    """
    Simple EMA Crossover (Fast vs Slow).
    """
    def __init__(self, fast_window=20, slow_window=50):
        self.fast_window = fast_window
        self.slow_window = slow_window
        
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['EMA_Fast'] = calculate_ema(df['Close'], self.fast_window)
        df['EMA_Slow'] = calculate_ema(df['Close'], self.slow_window)
        
        signals = []
        for i in range(len(df)):
            row = df.iloc[i]
            
            if pd.isna(row.get('EMA_Fast')) or pd.isna(row.get('EMA_Slow')):
                signals.append(Signal.HOLD)
                continue
                
            if row['EMA_Fast'] > row['EMA_Slow']:
                signals.append(Signal.BUY)
            elif row['EMA_Fast'] < row['EMA_Slow']:
                signals.append(Signal.SELL)
            else:
                signals.append(Signal.HOLD)
                
        df['Signal'] = signals
        return df
