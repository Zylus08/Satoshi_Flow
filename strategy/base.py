import pandas as pd
import logging
from signals.generator import SignalGenerator, Signal
from indicators.features import FeatureEngineer

class Strategy:
    """
    Base Strategy Class to combine feature engineering and signal generation.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the strategy logic on a historical dataset.
        Returns the dataframe with features and a new 'Signal' column.
        """
        self.logger.info("Building features...")
        df_features = FeatureEngineer.build_features(df)
        
        self.logger.info("Generating signals...")
        signals = SignalGenerator.generate_signals(df_features)
        df_features['Signal'] = signals
        
        return df_features
