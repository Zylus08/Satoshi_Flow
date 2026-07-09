import pandas as pd
from pathlib import Path
from datetime import datetime

class Reporter:
    """
    Generates a Markdown performance report.
    """
    
    @staticmethod
    def generate_markdown_report(metrics: dict, save_dir: str):
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        report_path = save_dir / 'report.md'
        
        lines = [
            f"# SatoshiFlow Backtest Report",
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Strategy Overview",
            "This strategy utilizes a combination of **Trend** (EMA 20 > EMA 50), **Momentum** (RSI > 55), ",
            "and **Volatility** (ATR < 20-day median ATR), supported by a **Volume Spike** confirmation filter.",
            "It is designed to capture trend continuations while avoiding extremely volatile, unconfirmed breakouts.",
            "",
            "## Risk Management",
            "- **Position Sizing:** ATR-based sizing, risking 2% of capital per trade.",
            "- **Stop Loss:** Trailing stop based on ATR.",
            "- **Brokerage Fee:** 0.15% per executed trade (buy and sell).",
            "",
            "## Performance Metrics",
            "| Metric | Value |",
            "| --- | --- |",
            f"| Total Return | {metrics.get('Total Return', 0):.2%} |",
            f"| CAGR | {metrics.get('CAGR', 0):.2%} |",
            f"| Annualized Volatility | {metrics.get('Volatility (Ann)', 0):.2%} |",
            f"| Sharpe Ratio | {metrics.get('Sharpe Ratio', 0):.2f} |",
            f"| Sortino Ratio | {metrics.get('Sortino Ratio', 0):.2f} |",
            f"| Max Drawdown | {metrics.get('Max Drawdown', 0):.2%} |",
            f"| Win Rate | {metrics.get('Win Rate', 0):.2%} |",
            f"| Profit Factor | {metrics.get('Profit Factor', 0):.2f} |",
            f"| Total Trades | {metrics.get('Total Trades', 0)} |",
            f"| Market Exposure | {metrics.get('Market Exposure', 0):.2%} |",
            "",
            "## Visualizations",
            "![Equity Curve](equity_curve.png)",
            "![Drawdown](drawdown.png)",
            "![Trades](trades.png)",
            "![Returns Distribution](returns_dist.png)",
            "![Rolling Sharpe](rolling_sharpe.png)",
            "",
            "## Strengths & Weaknesses",
            "**Strengths:**",
            "- Strict risk management limits drawdown during bear markets.",
            "- Avoids lookahead bias, providing realistic trade execution.",
            "",
            "**Weaknesses:**",
            "- Trend-following can suffer in choppy, sideways markets.",
            "- Only trades long, missing out on downside capture.",
            "",
            "## Future Improvements",
            "- Add shorting capabilities.",
            "- Implement Walk-Forward Optimization for parameters.",
            "- Enhance trailing stop logic to protect profits more aggressively."
        ]
        
        with open(report_path, 'w') as f:
            f.write("\n".join(lines))
            
        return report_path
