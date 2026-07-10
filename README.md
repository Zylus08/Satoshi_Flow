# 📈 SatoshiFlow

> **An institutional-grade quantitative research framework for developing, backtesting, and validating systematic trading strategies on Bitcoin (BTC/USD).**

SatoshiFlow is a modular quantitative research environment designed to evaluate trading strategies under realistic market conditions. Rather than maximizing historical returns, the framework emphasizes **research integrity**, **reproducibility**, and **methodological correctness** by incorporating realistic execution assumptions, rigorous validation techniques, and institutional performance analytics.

---

# Overview

Many retail trading backtests produce attractive performance by unintentionally introducing methodological errors such as lookahead bias, unrealistic execution assumptions, ignored transaction costs, or weak validation procedures.

SatoshiFlow was built to address these issues by providing a clean, extensible research framework that prioritizes statistical credibility over optimistic backtest results.

The framework includes:

* Event-driven backtesting engine
* Strict prevention of lookahead bias
* Realistic transaction cost and slippage modeling
* ATR-based risk management
* Institutional performance metrics
* Out-of-Sample validation
* Rolling Walk-Forward validation
* Strategy benchmarking
* Automated reporting and visualization

---

# Research Objectives

The framework is designed to answer the following questions:

* Can a systematic BTC/USD strategy outperform passive Buy & Hold?
* Does the strategy remain profitable after accounting for realistic trading costs?
* Does performance generalize to unseen market data?
* Is the observed performance statistically credible rather than a result of overfitting?
* How does the strategy behave across different market environments?

---

# Key Features

## Institutional Backtesting

* Event-driven execution engine
* Mark-to-market portfolio accounting
* Cash and holdings reconciliation
* Position tracking
* Trade logging
* Realistic execution timing

Signals generated using information available at **Close(t)** are executed at **Open(t+1)**, preventing lookahead bias.

---

## Risk Management

* ATR-based position sizing
* ATR stop-loss
* Institutional trailing stop based on the highest price since entry
* Maximum exposure constraints
* Brokerage and slippage modeling

---

## Performance Analytics

Automatically computes:

### Return Metrics

* Total Return
* CAGR
* Average Trade PnL

### Risk Metrics

* Annualized Volatility
* Sharpe Ratio
* Sortino Ratio
* Calmar Ratio
* Maximum Drawdown
* Ulcer Index

### Trade Statistics

* Win Rate
* Profit Factor
* Expectancy
* Recovery Factor
* Market Exposure

### Distribution Statistics

* Skewness
* Kurtosis

---

## Research Validation

The framework supports multiple validation methodologies.

### Out-of-Sample Validation

Training Period

* 2019–2021

Testing Period

* 2022–2023

Performance is evaluated separately on unseen data.

---

### Rolling Walk-Forward Validation

Successive rolling windows are evaluated to approximate live trading performance.

This methodology helps estimate how the strategy would have behaved when continuously deployed through time without future information.

---

## Benchmark Comparison

Strategies are evaluated against standard baselines:

* Buy & Hold BTC
* EMA Crossover Strategy
* Primary SatoshiFlow Strategy

All benchmarks use identical assumptions regarding:

* Initial capital
* Brokerage
* Slippage
* Execution timing

ensuring fair comparison.

---

# System Architecture

```text
                 Historical OHLCV Data
                         │
                         ▼
                 Feature Engineering
                         │
                         ▼
                 Signal Generation
                         │
                         ▼
                 Risk Management
                         │
                         ▼
                Event-Driven Execution
                         │
                         ▼
               Portfolio Accounting
                         │
                         ▼
             Performance Evaluation
                         │
                         ▼
            Reports & Visualizations
```

---

# Project Structure

```text
SatoshiFlow/
│
├── backtester/
│   └── Event-driven execution engine
│
├── data/
│   └── Historical BTC/USD OHLCV data
│
├── indicators/
│   ├── Technical indicators
│   └── Feature engineering pipeline
│
├── portfolio/
│   ├── Portfolio accounting
│   └── Risk management
│
├── reports/
│   ├── Research report
│   ├── Performance charts
│   ├── Robustness analysis
│   └── Validation outputs
│
├── research/
│   ├── Out-of-sample validation
│   ├── Walk-forward validation
│   └── Robustness testing
│
├── scripts/
│   └── Data collection utilities
│
├── signals/
│   └── Trading signal generation
│
├── strategy/
│   ├── Primary strategy
│   └── Benchmark strategies
│
├── utils/
│   ├── Metrics
│   ├── Plotting
│   └── Report generation
│
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Research Pipeline

```text
Load Historical Data
          │
          ▼
Compute Technical Indicators
          │
          ▼
Generate Trading Signals
          │
          ▼
Apply Risk Management
          │
          ▼
Execute Orders
          │
          ▼
Update Portfolio
          │
          ▼
Compute Performance Metrics
          │
          ▼
Generate Research Report
```

---

# Execution Model

SatoshiFlow follows an event-driven execution model designed to eliminate lookahead bias.

```text
Close(t)

↓

Generate Signal

↓

Open(t+1)

↓

Execute Trade
```

Signals never use information from future observations.

---

# Trading Assumptions

| Parameter       |                     Value |
| --------------- | ------------------------: |
| Initial Capital |                     $1000 |
| Asset           |                   BTC/USD |
| Brokerage       |           0.15% per trade |
| Slippage        |              Configurable |
| Position Sizing |                 ATR-Based |
| Stop Loss       |                 ATR-Based |
| Trailing Stop   | Highest Price Since Entry |

---

# Generated Reports

Running the research pipeline automatically produces:

* Comprehensive research report
* Equity curve
* Drawdown analysis
* Underwater chart
* Monthly return heatmap
* Benchmark comparison
* Robustness analysis
* Walk-forward validation outputs
* Trade logs
* Performance summary

All outputs are saved in the `reports/` directory.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd SatoshiFlow
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the research pipeline:

```bash
python main.py
```

---

# Design Principles

The framework was developed around the following principles:

* Eliminate lookahead bias.
* Model realistic execution costs.
* Prevent hidden data leakage.
* Prefer robust methodology over optimistic backtests.
* Keep the architecture modular and extensible.
* Separate research logic from execution logic.
* Ensure reproducible experiments.

---

# Current Limitations

SatoshiFlow is intentionally focused on a single-asset, daily-frequency research workflow.

Current limitations include:

* Long-only trading
* Daily OHLCV data
* Single asset (BTC/USD)
* No limit order simulation
* No tick-level execution
* No portfolio optimization
* No machine learning strategies (yet)

These design choices keep the framework focused on methodological correctness while providing a strong foundation for future extensions.

---

# Future Work

Planned research directions include:

* Multi-asset portfolio support
* Intraday and tick-level backtesting
* Hidden Markov Model regime detection
* Dynamic portfolio allocation
* Reinforcement learning execution policies
* Bayesian parameter estimation
* Portfolio optimization
* Factor-based strategies
* Alternative data integration

---

# Lessons Learned

One of the key outcomes of this project was that improving **research methodology** often reduced reported performance while increasing confidence in the results.

During development, several important methodological issues were identified and corrected, including:

* Execution timing to eliminate lookahead bias
* Transaction cost accounting
* Benchmark implementation
* Validation pipeline design
* Institutional trailing-stop behavior

These changes produced more conservative—but substantially more credible—performance estimates, reinforcing the importance of rigorous quantitative research practices.

---

# Disclaimer

This project is intended for **research and educational purposes only**.

It is **not** financial advice and should not be interpreted as a recommendation to buy or sell any financial instrument.

Past backtest performance does not guarantee future results.
