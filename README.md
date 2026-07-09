# SatoshiFlow

SatoshiFlow is a modular, research-oriented quantitative trading backtesting framework for BTC/USD, built in Python.

## Project Overview
The framework implements a complete end-to-end pipeline from data loading, feature engineering, and signal generation to risk management, backtesting, and performance reporting. It is designed to be highly modular and extensible, mimicking an institutional-grade architecture.

## Architecture
```
SatoshiFlow/
├── data/               # Contains historical OHLCV data
├── indicators/         # Raw indicator implementations and feature pipeline
├── signals/            # Signal generation logic (BUY/SELL/HOLD)
├── strategy/           # Strategy rules wrapping features and signals
├── backtester/         # Event-driven backtesting loop
├── portfolio/          # Portfolio accounting and risk management
├── reports/            # Generated performance reports and plots
├── scripts/            # Helper scripts (e.g., data downloader)
├── utils/              # Metrics calculation, plotting, reporting
├── main.py             # Entry point
├── config.py           # Configuration parameters
└── requirements.txt    # Project dependencies
```

## Strategy Explanation
The current implemented strategy is a long-only trend-following system:
- **Trend Filter:** 20-day EMA > 50-day EMA
- **Momentum Filter:** 14-day RSI > 55
- **Volatility Filter:** 14-day ATR < 20-day median ATR
- **Volume Filter:** Current volume > 20-day volume moving average

**Risk Management:**
Positions are sized based on ATR (risking 2% of capital per 1 ATR). An ATR-based trailing stop is employed to lock in profits.

## Installation
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Download historical data:
   ```bash
   python scripts/download_data.py
   ```
2. Run the backtester:
   ```bash
   python main.py
   ```
3. View the generated metrics, visualizations, and `report.md` in the `reports/` directory.

## Limitations & Future Work
- **Limitations:** The strategy only trades long. It might suffer during extended bear markets or choppy sideways regimes. Slippage and market impact are currently not modeled.
- **Future Work:** Add short selling, Walk-Forward Validation, Slippage modeling, and multi-asset support.
