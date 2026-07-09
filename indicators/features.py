import pandas as pd
import numpy as np
from .core import (
    calculate_ema, calculate_rsi, calculate_atr, calculate_log_returns, 
    calculate_rolling_volatility, calculate_sma
)

class FeatureEngineer:
    """
    Constructs features from base indicators. Designed to avoid lookahead bias.
    """
    
    @staticmethod
    def build_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Adds engineered features to the provided OHLCV DataFrame in-place.
        """
        df = df.copy()
        
        df['EMA_20'] = calculate_ema(df['Close'], 20)
        df['EMA_50'] = calculate_ema(df['Close'], 50)
        df['Trend_Strength'] = (df['EMA_20'] - df['EMA_50']) / df['EMA_50']
        
        df['RSI_14'] = calculate_rsi(df['Close'], 14)
        
        df['Vol_20'] = calculate_rolling_volatility(df['Close'], 20)
        df['Vol_100'] = calculate_rolling_volatility(df['Close'], 100)
        df['Vol_Regime'] = df['Vol_20'] / df['Vol_100']
        
        df['Dist_From_EMA_20'] = (df['Close'] - df['EMA_20']) / df['EMA_20']
        
        df['ATR_14'] = calculate_atr(df, 14)
        df['ATR_Norm'] = df['ATR_14'] / df['Close']
        
        df['Vol_SMA_20'] = calculate_sma(df['Volume'], 20)
        df['Volume_Change'] = df['Volume'] / df['Vol_SMA_20']
        
        df['Return_5d'] = df['Close'] / df['Close'].shift(5) - 1
        
        df['SMA_20'] = calculate_sma(df['Close'], 20)
        df['Price_Momentum'] = df['Close'] / df['SMA_20']
        
        df.ffill(inplace=True)

        return df
