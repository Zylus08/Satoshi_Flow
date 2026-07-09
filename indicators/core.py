import pandas as pd
import numpy as np

def calculate_sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=window).mean()

def calculate_ema(series: pd.Series, window: int) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=window, adjust=False).mean()

def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index."""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    # Fill initial NaNs or infs
    rsi = rsi.replace([np.inf, -np.inf], 100) 
    return rsi

def calculate_atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """Average True Range."""
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    
    return true_range.rolling(window=window).mean()

def calculate_rolling_volatility(series: pd.Series, window: int = 20) -> pd.Series:
    """Rolling Volatility (Standard Deviation of log returns)."""
    log_ret = calculate_log_returns(series)
    return log_ret.rolling(window=window).std()

def calculate_log_returns(series: pd.Series) -> pd.Series:
    """Log Returns."""
    return np.log(series / series.shift(1))

def calculate_rolling_max(series: pd.Series, window: int) -> pd.Series:
    """Rolling Maximum."""
    return series.rolling(window=window).max()

def calculate_rolling_min(series: pd.Series, window: int) -> pd.Series:
    """Rolling Minimum."""
    return series.rolling(window=window).min()

def calculate_zscore(series: pd.Series, window: int = 20) -> pd.Series:
    """Z-score."""
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    return (series - rolling_mean) / rolling_std

def calculate_volume_spike(volume_series: pd.Series, window: int = 20, multiplier: float = 2.0) -> pd.Series:
    """
    Volume Spike Indicator. 
    Returns boolean Series True if current volume > moving average volume * multiplier.
    """
    vol_sma = calculate_sma(volume_series, window)
    return volume_series > (vol_sma * multiplier)
