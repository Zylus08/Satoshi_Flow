import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from pathlib import Path

class Plotter:
    """
    Generates institutional-quality performance visualizations.
    """
    
    @staticmethod
    def set_style():
        sns.set_theme(style="whitegrid", palette="muted")
        plt.rcParams.update({'font.size': 12, 'figure.figsize': (12, 6)})

    @staticmethod
    def plot_performance(portfolio_df: pd.DataFrame, trades_df: pd.DataFrame, save_dir: str):
        Plotter.set_style()
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Equity Curve
        plt.figure()
        plt.plot(portfolio_df.index, portfolio_df['Portfolio_Value'], label='Strategy Equity', linewidth=2)
        plt.title('Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value ($)')
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_dir / 'equity_curve.png', dpi=300)
        plt.close()
        
        # 2. Underwater Plot (Drawdown)
        rolling_max = portfolio_df['Portfolio_Value'].cummax()
        drawdown = (portfolio_df['Portfolio_Value'] - rolling_max) / rolling_max
        plt.figure()
        plt.fill_between(drawdown.index, drawdown, 0, color='crimson', alpha=0.4)
        plt.plot(drawdown.index, drawdown, color='crimson', linewidth=1)
        plt.title('Underwater Plot (Drawdown)')
        plt.xlabel('Date')
        plt.ylabel('Drawdown (%)')
        plt.tight_layout()
        plt.savefig(save_dir / 'underwater.png', dpi=300)
        plt.close()
        
        # 3. Monthly Returns Heatmap
        # Resample daily returns to monthly
        monthly_returns = portfolio_df['Daily_Return'].resample('ME').apply(lambda x: (1 + x).prod() - 1)
        if not monthly_returns.empty:
            monthly_returns.index = pd.to_datetime(monthly_returns.index)
            heatmap_data = monthly_returns.groupby([monthly_returns.index.year, monthly_returns.index.month]).sum().unstack()
            heatmap_data.columns = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][:len(heatmap_data.columns)]
            
            plt.figure(figsize=(10, 6))
            sns.heatmap(heatmap_data, annot=True, fmt=".2%", cmap="RdYlGn", center=0, cbar_kws={'label': 'Return'})
            plt.title('Monthly Returns Heatmap')
            plt.ylabel('Year')
            plt.tight_layout()
            plt.savefig(save_dir / 'monthly_heatmap.png', dpi=300)
            plt.close()
            
        # 4. Rolling Sharpe Ratio (6-month)
        rolling_return = portfolio_df['Daily_Return'].rolling(window=180).mean()
        rolling_std = portfolio_df['Daily_Return'].rolling(window=180).std()
        rolling_sharpe = (rolling_return / rolling_std) * np.sqrt(365)
        
        plt.figure()
        plt.plot(rolling_sharpe.index, rolling_sharpe, color='darkorange', linewidth=1.5)
        plt.axhline(0, color='black', linestyle='--')
        plt.title('180-Day Rolling Sharpe Ratio')
        plt.xlabel('Date')
        plt.ylabel('Sharpe Ratio')
        plt.tight_layout()
        plt.savefig(save_dir / 'rolling_sharpe.png', dpi=300)
        plt.close()
