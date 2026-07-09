import pandas as pd
from pathlib import Path
from datetime import datetime

class Reporter:
    """
    Generates an Academic Markdown performance report.
    """
    
    @staticmethod
    def generate_markdown_report(metrics: dict, save_dir: str):
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        report_path = save_dir / 'research_report.md'
        
        lines = [
            f"# SatoshiFlow V2 Quantitative Research Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## 1. Abstract",
            "This report details the backtest results and robustness checks of a systematic trend-following strategy applied to BTC/USD. The strategy aims to capture multi-week momentum while severely restricting volatility drag via ATR-based position sizing and trailing stops.",
            "",
            "## 2. Research Motivation & Hypothesis",
            "Cryptocurrency markets exhibit heavy-tailed return distributions and persistent volatility clustering. The hypothesis is that a volatility-normalized trend-following system can outperform a Buy & Hold approach on a risk-adjusted basis (higher Sharpe, lower Max Drawdown).",
            "",
            "## 3. Methodology & Indicator Design",
            "- **Trend Filter:** Fast EMA (20) > Slow EMA (50)",
            "- **Momentum:** 14-day RSI > 55",
            "- **Volatility Regime:** Current ATR(14) < 20-day median ATR",
            "- **Volume Confirmation:** Volume > 20-day SMA",
            "",
            "## 4. Bias Prevention & Execution Model",
            "To prevent **lookahead bias**, signals generated at the close of time $t$ are executed at the `Open` price of time $t+1$. A slippage rate of 0.05% and brokerage of 0.15% are applied to every transaction.",
            "",
            "## 5. Performance Metrics",
            "| Metric | Value |",
            "| --- | --- |",
            f"| Total Return | {metrics.get('Total Return', 0):.2%} |",
            f"| CAGR | {metrics.get('CAGR', 0):.2%} |",
            f"| Annualized Volatility | {metrics.get('Volatility (Ann)', 0):.2%} |",
            f"| Sharpe Ratio | {metrics.get('Sharpe Ratio', 0):.2f} |",
            f"| Sortino Ratio | {metrics.get('Sortino Ratio', 0):.2f} |",
            f"| Calmar Ratio | {metrics.get('Calmar Ratio', 0):.2f} |",
            f"| Max Drawdown | {metrics.get('Max Drawdown', 0):.2%} |",
            f"| Ulcer Index | {metrics.get('Ulcer Index', 0):.4f} |",
            f"| Return Skewness | {metrics.get('Skewness', 0):.2f} |",
            f"| Return Kurtosis | {metrics.get('Kurtosis', 0):.2f} |",
            f"| Win Rate | {metrics.get('Win Rate', 0):.2%} |",
            f"| Profit Factor | {metrics.get('Profit Factor', 0):.2f} |",
            f"| Expectancy | {metrics.get('Expectancy', 0):.2%} |",
            f"| Recovery Factor | {metrics.get('Recovery Factor', 0):.2f} |",
            f"| Market Exposure | {metrics.get('Market Exposure', 0):.2%} |",
            "",
            "## 6. Visualizations",
            "![Equity Curve](equity_curve.png)",
            "![Underwater Plot](underwater.png)",
            "![Monthly Returns Heatmap](monthly_heatmap.png)",
            "![Rolling Sharpe](rolling_sharpe.png)",
            "",
            "## 7. Limitations & Future Directions",
            "The model trades strictly long, meaning it suffers from zero returns (though protected from drawdowns) during prolonged bear markets. Future research should evaluate adding short exposure and optimizing parameters using Walk-Forward methodologies."
        ]
        
        with open(report_path, 'w') as f:
            f.write("\n".join(lines))
            
        return report_path
