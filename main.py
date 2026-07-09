import logging
from config import CSV_FILE_PATH, DATA_START_DATE, DATA_END_DATE, INITIAL_CAPITAL, BROKERAGE_FEE, SLIPPAGE_RATE, REPORTS_DIR, LOG_LEVEL
from utils.data_loader import DataLoader
from strategy.base import Strategy
from strategy.benchmarks import BuyAndHoldStrategy, EMACrossoverStrategy
from backtester.engine import BacktestEngine
from utils.metrics import MetricsCalculator
from utils.plots import Plotter
from utils.reporter import Reporter
from research.robustness import RobustnessTester
from research.validation import Validator

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")

def run_backtest(df, strategy_obj, name):
    logger = logging.getLogger(name)
    logger.info(f"Running Backtest for {name}...")
    df_signals = strategy_obj.generate_signals(df)
    engine = BacktestEngine(df=df_signals, initial_capital=INITIAL_CAPITAL, fee_rate=BROKERAGE_FEE, slippage_rate=SLIPPAGE_RATE)
    accountant = engine.run()
    
    portfolio_df = accountant.get_history_df()
    trades_df = accountant.get_trade_log_df()
    metrics = MetricsCalculator.calculate_metrics(portfolio_df, trades_df, INITIAL_CAPITAL)
    return portfolio_df, trades_df, metrics

def main():
    logger = logging.getLogger("SatoshiFlow_V2")
    logger.info("Initializing SatoshiFlow V2 Research Pipeline...")
    
    # 1. Load Data
    try:
        df = DataLoader.load_csv(CSV_FILE_PATH, start_date=DATA_START_DATE, end_date=DATA_END_DATE)
    except FileNotFoundError:
        logger.error(f"Data file not found at {CSV_FILE_PATH}. Please run scripts/download_data.py first.")
        return
        
    # 2. Main Strategy
    main_port, main_trades, main_metrics = run_backtest(df, Strategy(), "Main_Strategy")
    
    # 3. Benchmarks
    bnh_port, _, bnh_metrics = run_backtest(df, BuyAndHoldStrategy(), "Buy_and_Hold")
    ema_port, _, ema_metrics = run_backtest(df, EMACrossoverStrategy(), "EMA_Crossover")
    
    logger.info(f"--- Benchmark Comparison ---")
    logger.info(f"Main Strategy CAGR: {main_metrics.get('CAGR',0):.2%}, Max DD: {main_metrics.get('Max Drawdown',0):.2%}")
    logger.info(f"Buy & Hold CAGR: {bnh_metrics.get('CAGR',0):.2%}, Max DD: {bnh_metrics.get('Max Drawdown',0):.2%}")
    logger.info(f"EMA Crossover CAGR: {ema_metrics.get('CAGR',0):.2%}, Max DD: {ema_metrics.get('Max Drawdown',0):.2%}")
    
    # 4. Visualization & Reporting
    logger.info("Generating Visualizations...")
    Plotter.plot_performance(main_port, main_trades, str(REPORTS_DIR))
    
    logger.info("Generating Research Report...")
    report_path = Reporter.generate_markdown_report(main_metrics, str(REPORTS_DIR))
    logger.info(f"Report generated successfully at {report_path}")
    
    # 5. Robustness Testing
    robust_df = RobustnessTester.run_sensitivity_analysis(df, INITIAL_CAPITAL, BROKERAGE_FEE, SLIPPAGE_RATE)
    robust_df.to_csv(REPORTS_DIR / 'robustness_results.csv', index=False)
    
    # 6. Validation (OOS & Walk-Forward)
    Validator.run_oos_test(df, INITIAL_CAPITAL, BROKERAGE_FEE, SLIPPAGE_RATE)
    wf_trades = Validator.run_walk_forward(df, INITIAL_CAPITAL, BROKERAGE_FEE, SLIPPAGE_RATE)
    if not wf_trades.empty:
         wf_trades.to_csv(REPORTS_DIR / 'walk_forward_trades.csv', index=False)
         
    logger.info("Research Pipeline Completed Successfully.")

if __name__ == "__main__":
    main()
