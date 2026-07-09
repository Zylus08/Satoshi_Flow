import logging
from config import CSV_FILE_PATH, DATA_START_DATE, DATA_END_DATE, INITIAL_CAPITAL, BROKERAGE_FEE, REPORTS_DIR, LOG_LEVEL
from utils.data_loader import DataLoader
from strategy.base import Strategy
from backtester.engine import BacktestEngine
from utils.metrics import MetricsCalculator
from utils.plots import Plotter
from utils.reporter import Reporter

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    logger = logging.getLogger("SatoshiFlow")
    logger.info("Initializing SatoshiFlow Backtest Pipeline...")
    
    # 1. Load Data
    try:
        df = DataLoader.load_csv(CSV_FILE_PATH, start_date=DATA_START_DATE, end_date=DATA_END_DATE)
    except FileNotFoundError:
        logger.error(f"Data file not found at {CSV_FILE_PATH}. Please run scripts/download_data.py first.")
        return
        
    # 2. Run Strategy (Feature Engineering + Signal Generation)
    strategy = Strategy()
    df_signals = strategy.generate_signals(df)
    
    # 3. Backtest Engine
    engine = BacktestEngine(df=df_signals, initial_capital=INITIAL_CAPITAL, fee_rate=BROKERAGE_FEE)
    accountant = engine.run()
    
    portfolio_df = accountant.get_history_df()
    trades_df = accountant.get_trade_log_df()
    
    # 4. Calculate Metrics
    logger.info("Calculating Performance Metrics...")
    metrics = MetricsCalculator.calculate_metrics(portfolio_df, trades_df, INITIAL_CAPITAL)
    
    for k, v in metrics.items():
        if isinstance(v, float) and 'Trades' not in k and 'Factor' not in k and 'Ratio' not in k:
            logger.info(f"{k}: {v:.2%}")
        elif isinstance(v, float):
             logger.info(f"{k}: {v:.2f}")
        else:
            logger.info(f"{k}: {v}")
            
    # 5. Visualization
    logger.info("Generating Visualizations...")
    Plotter.plot_performance(portfolio_df, trades_df, str(REPORTS_DIR))
    
    # 6. Report Generation
    logger.info("Generating Final Report...")
    report_path = Reporter.generate_markdown_report(metrics, str(REPORTS_DIR))
    logger.info(f"Report generated successfully at {report_path}")

if __name__ == "__main__":
    main()
