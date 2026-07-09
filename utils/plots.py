import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

class Plotter:
    """
    Generates performance visualizations.
    """
    
    @staticmethod
    def plot_performance(portfolio_df: pd.DataFrame, trades_df: pd.DataFrame, save_dir: str):
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Plot 1: Equity Curve
        plt.figure(figsize=(10, 5))
        plt.plot(portfolio_df.index, portfolio_df['Portfolio_Value'], label='Portfolio Value', color='blue')
        plt.title('Equity Curve')
        plt.xlabel('Date')
        plt.ylabel('Value ($)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_dir / 'equity_curve.png')
        plt.close()
        
        # Plot 2: Drawdown Curve
        rolling_max = portfolio_df['Portfolio_Value'].cummax()
        drawdown = (portfolio_df['Portfolio_Value'] - rolling_max) / rolling_max
        plt.figure(figsize=(10, 5))
        plt.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.3)
        plt.plot(drawdown.index, drawdown, color='red', linewidth=1)
        plt.title('Drawdown Curve')
        plt.xlabel('Date')
        plt.ylabel('Drawdown')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_dir / 'drawdown.png')
        plt.close()
        
        # Plot 3: Price with Buy/Sell markers
        plt.figure(figsize=(12, 6))
        plt.plot(portfolio_df.index, portfolio_df['Price'], label='BTC/USD', color='black', alpha=0.5)
        
        if not trades_df.empty:
            buys = trades_df[trades_df['Action'] == 'BUY']
            sells = trades_df[trades_df['Action'] == 'SELL']
            plt.scatter(buys['Date'], buys['Price'], marker='^', color='green', label='Buy', alpha=1)
            plt.scatter(sells['Date'], sells['Price'], marker='v', color='red', label='Sell', alpha=1)
            
        plt.title('Price with Trades')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_dir / 'trades.png')
        plt.close()
        
        # Plot 4: Returns Distribution
        plt.figure(figsize=(10, 5))
        portfolio_df['Daily_Return'].hist(bins=50, alpha=0.7, color='purple')
        plt.title('Daily Returns Distribution')
        plt.xlabel('Daily Return')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_dir / 'returns_dist.png')
        plt.close()

        # Plot 5: Rolling Sharpe Ratio (6-month ~ 180 days)
        rolling_return = portfolio_df['Daily_Return'].rolling(window=180).mean()
        rolling_std = portfolio_df['Daily_Return'].rolling(window=180).std()
        rolling_sharpe = (rolling_return / rolling_std) * np.sqrt(365)
        
        plt.figure(figsize=(10, 5))
        plt.plot(rolling_sharpe.index, rolling_sharpe, label='180-Day Rolling Sharpe', color='orange')
        plt.axhline(0, color='black', linestyle='--')
        plt.title('Rolling Sharpe Ratio')
        plt.xlabel('Date')
        plt.ylabel('Sharpe Ratio')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_dir / 'rolling_sharpe.png')
        plt.close()
