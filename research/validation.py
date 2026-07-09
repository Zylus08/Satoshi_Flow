import pandas as pd
import logging
from strategy.base import Strategy
from backtester.engine import BacktestEngine
from utils.metrics import MetricsCalculator

class Validator:
    """
    Handles Out-of-Sample and Walk-Forward Validation.
    """
    
    @staticmethod
    def run_oos_test(df: pd.DataFrame, initial_capital: float, fee_rate: float, slippage_rate: float):
        logger = logging.getLogger("Validator")
        logger.info("Starting Out-Of-Sample (OOS) Testing...")
        
        strategy = Strategy()
        # Compute features globally to prevent indicator burn-in during OOS periods
        df_signals = strategy.generate_signals(df)
        
        # Split: Train (2019-2021), Test (2022-2023)
        train_df = df_signals[(df_signals['Date'] >= '2019-01-01') & (df_signals['Date'] <= '2021-12-31')].copy()
        test_df = df_signals[(df_signals['Date'] >= '2022-01-01') & (df_signals['Date'] <= '2023-12-31')].copy()
        
        # Train
        engine_train = BacktestEngine(train_df, initial_capital, fee_rate, slippage_rate)
        acc_train = engine_train.run()
        metrics_train = MetricsCalculator.calculate_metrics(acc_train.get_history_df(), acc_train.get_trade_log_df(), initial_capital)
        
        # Test
        engine_test = BacktestEngine(test_df, initial_capital, fee_rate, slippage_rate)
        acc_test = engine_test.run()
        metrics_test = MetricsCalculator.calculate_metrics(acc_test.get_history_df(), acc_test.get_trade_log_df(), initial_capital)
        
        logger.info(f"Train CAGR: {metrics_train.get('CAGR',0):.2%}, Test CAGR: {metrics_test.get('CAGR',0):.2%}")
        logger.info(f"Train Sharpe: {metrics_train.get('Sharpe Ratio',0):.2f}, Test Sharpe: {metrics_test.get('Sharpe Ratio',0):.2f}")
        
        return metrics_train, metrics_test

    @staticmethod
    def run_walk_forward(df: pd.DataFrame, initial_capital: float, fee_rate: float, slippage_rate: float):
        logger = logging.getLogger("Validator")
        logger.info("Starting Walk-Forward Validation...")
        
        # Simple Walk-Forward: 
        # Window 1: Train 2019-2020, Test 2021
        # Window 2: Train 2020-2021, Test 2022
        # Window 3: Train 2021-2022, Test 2023
        
        windows = [
            ('2019-01-01', '2020-12-31', '2021-01-01', '2021-12-31'),
            ('2020-01-01', '2021-12-31', '2022-01-01', '2022-12-31'),
            ('2021-01-01', '2022-12-31', '2023-01-01', '2023-12-31')
        ]
        
        strategy = Strategy()
        # Compute features globally to prevent indicator burn-in during OOS periods
        df_signals = strategy.generate_signals(df)
        all_test_trades = []
        
        for train_start, train_end, test_start, test_end in windows:
            logger.info(f"Walk-Forward Window -> Train: {train_start} to {train_end} | Test: {test_start} to {test_end}")
            
            test_df = df_signals[(df_signals['Date'] >= test_start) & (df_signals['Date'] <= test_end)].copy()
            if test_df.empty:
                continue
                
            engine = BacktestEngine(test_df, initial_capital, fee_rate, slippage_rate)
            acc = engine.run()
            
            # Collect trades
            trades = acc.get_trade_log_df()
            if not trades.empty:
                all_test_trades.append(trades)
                
        if all_test_trades:
            combined_trades = pd.concat(all_test_trades)
            logger.info(f"Walk-Forward Validation Total Out-of-Sample Trades: {len(combined_trades)}")
            return combined_trades
        return pd.DataFrame()
