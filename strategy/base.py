import pandas as pd
import logging
from signals.generator import SignalGenerator, Signal
from indicators.features import FeaturePipeline

class Strategy:
    """
    Base Strategy Class to combine feature engineering and signal generation.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.feature_pipeline = FeaturePipeline()
        
    def fit_transform_and_generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fits the feature pipeline, transforms the data, and generates signals.
        """
        self.logger.info("Building features (fit_transform)...")
        df_features = self.feature_pipeline.fit_transform(df)
        
        self.logger.info("Generating signals...")
        signals = SignalGenerator.generate_signals(df_features)
        df_features['Signal'] = signals
        
        return df_features

    def transform_and_generate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the data using a fitted pipeline and generates signals.
        """
        self.logger.info("Building features (transform)...")
        df_features = self.feature_pipeline.transform(df)
        
        self.logger.info("Generating signals...")
        signals = SignalGenerator.generate_signals(df_features)
        df_features['Signal'] = signals
        
        return df_features
        
    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Executes the strategy logic on a historical dataset.
        Backward compatibility wrapper that runs fit_transform.
        """
        return self.fit_transform_and_generate(df)
