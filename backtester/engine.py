import pandas as pd
import logging
from signals.generator import Signal
from portfolio.accounting import PortfolioAccountant
from portfolio.risk import RiskManager

class BacktestEngine:
    """
    Event-driven simulation loop for backtesting.
    """
    def __init__(self, df: pd.DataFrame, initial_capital: float, fee_rate: float):
        self.df = df
        self.accountant = PortfolioAccountant(initial_capital=initial_capital)
        self.risk_manager = RiskManager(max_exposure=1.0, risk_per_trade=0.02)
        self.fee_rate = fee_rate
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def run(self):
        """Runs the simulation bar by bar."""
        self.logger.info("Starting backtest simulation...")
        
        stop_loss_price = None
        
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            date = row.name if isinstance(row.name, pd.Timestamp) else row.get('Date')
            
            # If Date is a column but not index, fallback to index
            if not isinstance(date, pd.Timestamp) and 'Date' in self.df.columns:
                 date = row['Date']
            
            current_price = row['Close']
            signal = row.get('Signal', Signal.HOLD)
            atr = row.get('ATR_14', 0.0)
            
            # Check stop loss if we have holdings
            if self.accountant.holdings > 0 and stop_loss_price:
                if current_price <= stop_loss_price:
                    self.logger.debug(f"{date} - Stop Loss Triggered at {current_price}")
                    self.accountant.execute_sell(date, current_price, self.accountant.holdings, self.fee_rate)
                    stop_loss_price = None
                    signal = Signal.HOLD # Cancel any other signals for this bar
                    
            # Process Signals
            if signal == Signal.BUY and self.accountant.holdings == 0:
                units = self.risk_manager.calculate_position_size(
                    cash=self.accountant.cash, 
                    current_price=current_price, 
                    atr=atr if not pd.isna(atr) else None
                )
                
                if units > 0:
                    self.accountant.execute_buy(date, current_price, units, self.fee_rate)
                    # Set initial stop loss
                    stop_loss_price = self.risk_manager.calculate_stop_loss(
                        entry_price=current_price, 
                        atr=atr if not pd.isna(atr) else None
                    )
                    
            elif signal == Signal.SELL and self.accountant.holdings > 0:
                self.accountant.execute_sell(date, current_price, self.accountant.holdings, self.fee_rate)
                stop_loss_price = None
                
            # Update Trailing Stop (simplified: using current price as highest since entry for simplicity of this loop)
            # In a full system, you track the highest price since entry.
            if self.accountant.holdings > 0 and stop_loss_price:
                new_stop = self.risk_manager.calculate_trailing_stop(
                     highest_price_since_entry=current_price, 
                     atr=atr if not pd.isna(atr) else None
                )
                if new_stop > stop_loss_price:
                    stop_loss_price = new_stop
                    
            # End of day accounting
            self.accountant.record_daily_state(date, current_price)
            
        self.logger.info("Backtest simulation complete.")
        return self.accountant
