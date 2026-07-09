import sys
from pathlib import Path
import yfinance as yf
import logging

# Add parent dir to sys path to import config
sys.path.append(str(Path(__file__).resolve().parent.parent))
import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def download_data():
    logging.info(f"Downloading {config.SYMBOL} data from {config.DATA_START_DATE} to {config.DATA_END_DATE}...")
    
    # Download data using yfinance
    df = yf.download(
        tickers=config.SYMBOL,
        start=config.DATA_START_DATE,
        end=config.DATA_END_DATE,
        interval="1d",
        auto_adjust=False
    )
    
    if df.empty:
        logging.error("Failed to download data or empty dataframe returned.")
        return
    
    # Flatten MultiIndex columns if necessary (yfinance sometimes returns multi-index)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Reorder columns
    expected_cols = ["Open", "High", "Low", "Close", "Volume"]
    available_cols = [col for col in expected_cols if col in df.columns]
    df = df[available_cols]
    
    # Reset index so 'Date' becomes a column
    df.reset_index(inplace=True)
    
    # yfinance Date column might have timezone, remove it for simplicity
    if df['Date'].dt.tz is not None:
         df['Date'] = df['Date'].dt.tz_convert(None)

    # Save to CSV
    csv_path = config.CSV_FILE_PATH
    df.to_csv(csv_path, index=False)
    logging.info(f"Data saved to {csv_path} with shape {df.shape}")

if __name__ == "__main__":
    import pandas as pd
    download_data()
