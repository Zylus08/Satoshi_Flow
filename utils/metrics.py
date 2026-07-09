import pandas as pd
import numpy as np
import scipy.stats as stats

class MetricsCalculator:
    """
    Calculates advanced strategy performance metrics for institutional research.
    """
    
    @staticmethod
    def calculate_metrics(portfolio_df: pd.DataFrame, trades_df: pd.DataFrame, initial_capital: float, risk_free_rate: float = 0.0) -> dict:
        if portfolio_df.empty:
             return {}
             
        # Extract series
        portfolio_value = portfolio_df['Portfolio_Value']
        daily_returns = portfolio_df['Daily_Return']
        
        # 1. Total Return & CAGR
        total_return = (portfolio_value.iloc[-1] / initial_capital) - 1
        days = (portfolio_df.index[-1] - portfolio_df.index[0]).days
        years = days / 365.25 if days > 0 else 1
        cagr = (portfolio_value.iloc[-1] / initial_capital) ** (1 / years) - 1 if years > 0 else 0
        
        # 2. Volatility (Annualized)
        volatility = daily_returns.std() * np.sqrt(365)
        
        # 3. Sharpe & Sortino (Annualized)
        excess_returns = daily_returns - (risk_free_rate / 365)
        sharpe_ratio = (excess_returns.mean() / daily_returns.std()) * np.sqrt(365) if daily_returns.std() != 0 else 0
        
        downside_returns = daily_returns[daily_returns < 0]
        downside_deviation = np.sqrt((downside_returns ** 2).mean()) * np.sqrt(365) if not downside_returns.empty else 0
        sortino_ratio = (excess_returns.mean() * 365) / downside_deviation if downside_deviation != 0 else 0
        
        # 4. Drawdowns, Calmar, Ulcer Index
        rolling_max = portfolio_value.cummax()
        drawdown = (portfolio_value - rolling_max) / rolling_max
        max_drawdown = drawdown.min()
        
        calmar_ratio = cagr / abs(max_drawdown) if max_drawdown != 0 else float('inf')
        ulcer_index = np.sqrt((drawdown ** 2).mean())
        
        # 5. Higher Moments
        skewness = stats.skew(daily_returns.dropna())
        kurtosis = stats.kurtosis(daily_returns.dropna())
        
        # 6. Trade Statistics
        total_trades = 0
        win_rate = 0.0
        profit_factor = 0.0
        avg_trade_return = 0.0
        expectancy = 0.0
        recovery_factor = 0.0
        
        if not trades_df.empty:
            sells = trades_df[trades_df['Action'] == 'SELL']
            total_trades = len(sells)
            
            if total_trades > 0:
                winning_trades = sells[sells['PnL'] > 0]
                losing_trades = sells[sells['PnL'] <= 0]
                
                win_rate = len(winning_trades) / total_trades
                loss_rate = 1 - win_rate
                
                avg_win = winning_trades['PnL'].mean() if not winning_trades.empty else 0
                avg_loss = abs(losing_trades['PnL'].mean()) if not losing_trades.empty else 0
                
                gross_profit = winning_trades['PnL'].sum()
                gross_loss = abs(losing_trades['PnL'].sum())
                
                profit_factor = gross_profit / gross_loss if gross_loss != 0 else float('inf')
                avg_trade_return = sells['PnL'].mean()
                
                expectancy = (win_rate * avg_win) - (loss_rate * avg_loss)
                recovery_factor = total_return * initial_capital / abs(max_drawdown * initial_capital) if max_drawdown != 0 else float('inf')

        # 7. Exposure Time
        exposure = len(portfolio_df[portfolio_df['Holdings'] > 0]) / len(portfolio_df) if len(portfolio_df) > 0 else 0

        return {
            "Total Return": total_return,
            "CAGR": cagr,
            "Volatility (Ann)": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Sortino Ratio": sortino_ratio,
            "Calmar Ratio": calmar_ratio,
            "Max Drawdown": max_drawdown,
            "Ulcer Index": ulcer_index,
            "Skewness": skewness,
            "Kurtosis": kurtosis,
            "Total Trades": total_trades,
            "Win Rate": win_rate,
            "Profit Factor": profit_factor,
            "Expectancy": expectancy,
            "Recovery Factor": recovery_factor,
            "Avg Trade PnL": avg_trade_return,
            "Market Exposure": exposure
        }
