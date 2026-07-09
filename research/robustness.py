import pandas as pd
import logging
from strategy.base import Strategy
from backtester.engine import BacktestEngine
from utils.metrics import MetricsCalculator

class RobustnessTester:
    """
    Tests strategy against perturbations in parameters to prove it is not overfitted.
    """
    
    @staticmethod
    def run_sensitivity_analysis(df: pd.DataFrame, initial_capital: float, fee_rate: float, slippage_rate: float) -> pd.DataFrame:
        logger = logging.getLogger("RobustnessTester")
        logger.info("Starting Sensitivity Analysis...")
        
        # We will perturb Slippage and Brokerage to see the impact on CAGR and Sharpe
        results = []
        
        slippage_scenarios = [0.0, 0.0005, 0.001] # 0%, 0.05%, 0.10%
        brokerage_scenarios = [0.0015, 0.0025, 0.005] # 0.15%, 0.25%, 0.50%
        
        strategy = Strategy()
        df_signals = strategy.generate_signals(df)
        
        for slip in slippage_scenarios:
            for fee in brokerage_scenarios:
                logger.info(f"Testing Scenario - Slippage: {slip*100}%, Fee: {fee*100}%")
                
                engine = BacktestEngine(df=df_signals, initial_capital=initial_capital, fee_rate=fee, slippage_rate=slip)
                accountant = engine.run()
                
                metrics = MetricsCalculator.calculate_metrics(
                    accountant.get_history_df(), 
                    accountant.get_trade_log_df(), 
                    initial_capital
                )
                
                results.append({
                    'Slippage': slip,
                    'Brokerage': fee,
                    'CAGR': metrics.get('CAGR', 0),
                    'Sharpe': metrics.get('Sharpe Ratio', 0),
                    'Max Drawdown': metrics.get('Max Drawdown', 0)
                })
                
        results_df = pd.DataFrame(results)
        logger.info("Sensitivity Analysis Complete.")
        return results_df
