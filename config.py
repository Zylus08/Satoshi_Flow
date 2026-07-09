import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Data Settings
SYMBOL = "BTC-USD"
DATA_START_DATE = "2019-01-01"
DATA_END_DATE = "2023-12-31"
CSV_FILE_PATH = DATA_DIR / "btc_usd.csv"

# Backtest Settings
INITIAL_CAPITAL = 1000.0
BROKERAGE_FEE = 0.0015  # 0.15%

# Logging Settings
LOG_LEVEL = "INFO"
