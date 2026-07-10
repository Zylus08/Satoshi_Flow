import pandas as pd
import numpy as np
from .core import (
    calculate_ema, calculate_rsi, calculate_atr, calculate_log_returns, 
    calculate_rolling_volatility, calculate_sma
)

class FeaturePipeline:
    """
    Constructs features from base indicators using a fit/transform ML workflow.
    Designed to avoid lookahead bias and support future ML model pipelines.
    """
    def __init__(self, lookback_window: int = 100):
        self.lookback_window = lookback_window
        self.history = None

    def fit(self, df: pd.DataFrame):
        """
        Fits the pipeline. For purely causal indicators, this simply stores the 
        tail of the training data to prevent indicator burn-in (NaNs) in the test set.
        """
        if len(df) > 0:
            self.history = df.tail(self.lookback_window).copy()
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the dataframe, adding engineered features.
        """
        is_test = False
        if self.history is not None and len(df) > 0:
            # Check if this is a test set that needs warm-up data
            # Assumes index is sorted and time-based
            if df.index[0] > self.history.index[-1]:
                is_test = True
                combined = pd.concat([self.history, df])
            else:
                combined = df.copy()
        else:
            combined = df.copy()
            
        combined = self._compute_features(combined)
        
        if is_test:
            # Return only the portion corresponding to the requested df
            return combined.loc[df.index].copy()
        return combined

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.fit(df)
        return self.transform(df)

    def _compute_features(self, df: pd.DataFrame) -> pd.DataFrame:
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
