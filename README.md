# SatoshiFlow V2: Institutional Research Framework

SatoshiFlow V2 is a rigorous quantitative research environment for backtesting and validating systematic trading strategies on BTC/USD.

## V2 Upgrades
- **Bias Prevention:** Exact execution timing (signals generated at Close are executed at the Open of the following bar) to eliminate lookahead bias.
- **Slippage Modeling:** Realistic slippage applied to market orders and stop losses.
- **Benchmark Comparison:** Integrated Buy & Hold and Simple EMA Crossover baselines.
- **Advanced Metrics:** Institutional metrics including Calmar Ratio, Ulcer Index, Skewness, Kurtosis, and Expectancy.
- **Robustness Testing:** Multi-dimensional parameter sensitivity analysis to prove generalization and avoid overfitting.
- **Validation Methods:** Out-of-Sample (OOS) data splits and Walk-Forward Validation loops.
- **Institutional Visualizations:** Seaborn-powered heatmaps and underwater charts.

## Project Structure
```
SatoshiFlow/
├── data/               # Historical OHLCV data
├── indicators/         # Raw indicators & feature pipelines
├── signals/            # Signal generation logic
├── strategy/           # Strategy rules and baselines (benchmarks.py)
├── backtester/         # Event-driven execution engine (slippage & timing aware)
├── portfolio/          # Position sizing, risk, and accounting
├── research/           # Robustness and validation methodologies
├── reports/            # Output metrics, heatmaps, and research_report.md
├── scripts/            # Data collection utilities
├── utils/              # Calculation, plotting, and markdown reporting
├── main.py             # Research pipeline execution
├── config.py           # Core settings (Brokerage, Slippage)
└── requirements.txt    # Dependencies (numpy, pandas, seaborn, statsmodels)
```

## Running the Research Pipeline
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the main research script:
   ```bash
   python main.py
   ```
3. Check the `reports/` directory for the comprehensive academic Markdown report, sensitivity tables, and visual analysis.
