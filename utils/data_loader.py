import pandas as pd
import logging
from pathlib import Path
from typing import Union, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class DataLoader:
    """
    DataLoader is responsible for loading OHLCV data from CSV,
    parsing timestamps, sorting, handling missing values, and validating schemas.
    """
    
    REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]

    @staticmethod
    def load_csv(filepath: Union[str, Path], 
                 start_date: str = None, 
                 end_date: str = None) -> pd.DataFrame:
        """
        Loads CSV, validates schema, processes missing values, and returns a DataFrame.
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found at {filepath}")
        
        logging.info(f"Loading data from {filepath}")
        df = pd.read_csv(filepath)
        
        # Validate columns
        missing_cols = [col for col in DataLoader.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in dataset: {missing_cols}")
            
        # Parse timestamps
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort chronologically
        df.sort_values(by='Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # Filter by dates if provided
        if start_date:
            df = df[df['Date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['Date'] <= pd.to_datetime(end_date)]
            
        # Handle missing values
        # Forward fill first (carry forward last known price)
        df.ffill(inplace=True)
        # Backward fill just in case the first row has missing values
        df.bfill(inplace=True)
        
        logging.info(f"Data loaded successfully with shape {df.shape}")
        return df
