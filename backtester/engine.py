import pandas as pd
import logging
from signals.generator import Signal
from portfolio.accounting import PortfolioAccountant
from portfolio.risk import RiskManager

class BacktestEngine:
    """
    Event-driven simulation loop for backtesting.
    """
    def __init__(self, df: pd.DataFrame, initial_capital: float, fee_rate: float, slippage_rate: float = 0.0):
        self.df = df
        self.accountant = PortfolioAccountant(initial_capital=initial_capital)
        self.risk_manager = RiskManager(max_exposure=1.0, risk_per_trade=0.02)
        self.fee_rate = fee_rate
        self.slippage_rate = slippage_rate
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def run(self):
        """Runs the simulation bar by bar."""
        self.logger.info("Starting backtest simulation (V2)...")
        
        stop_loss_price = None
        pending_signal = Signal.HOLD
        pending_atr = None
        
        # Optimize iteration using itertuples
        for row in self.df.itertuples():
            # row attributes are capitalized if they were in the df columns
            date = getattr(row, 'Date', row.Index)
            if isinstance(row.Index, pd.Timestamp) and not hasattr(row, 'Date'):
                date = row.Index
                
            open_price = row.Open
            high_price = row.High
            low_price = row.Low
            current_close = row.Close
            
            # 1. Execute Pending Signals at the OPEN price of current bar (t+1)
            # Apply Slippage: Buy higher, Sell lower
            if pending_signal == Signal.BUY and self.accountant.holdings == 0:
                exec_price = open_price * (1 + self.slippage_rate)
                units = self.risk_manager.calculate_position_size(
                    cash=self.accountant.cash, 
                    current_price=exec_price, 
                    atr=pending_atr
                )
                
                if units > 0:
                    self.accountant.execute_buy(date, exec_price, units, self.fee_rate)
                    stop_loss_price = self.risk_manager.calculate_stop_loss(
                        entry_price=exec_price, 
                        atr=pending_atr
                    )
            
            elif pending_signal == Signal.SELL and self.accountant.holdings > 0:
                exec_price = open_price * (1 - self.slippage_rate)
                self.accountant.execute_sell(date, exec_price, self.accountant.holdings, self.fee_rate)
                stop_loss_price = None
                
            pending_signal = Signal.HOLD
            pending_atr = None
            
            # 2. Intra-bar Stop Loss Check
            if self.accountant.holdings > 0 and stop_loss_price:
                # If low price drops below stop loss, execute sell at stop_loss_price (assuming a stop market order)
                # Apply slippage on the stop execution as well
                if low_price <= stop_loss_price:
                    exec_price = min(open_price, stop_loss_price) * (1 - self.slippage_rate) # gap down open
                    self.logger.debug(f"{date} - Stop Loss Triggered at {exec_price}")
                    self.accountant.execute_sell(date, exec_price, self.accountant.holdings, self.fee_rate)
                    stop_loss_price = None
            
            # 3. Process Signals Generated at the CLOSE of the current bar (to be executed next bar)
            signal = getattr(row, 'Signal', Signal.HOLD)
            atr = getattr(row, 'ATR_14', 0.0)
            
            if signal != Signal.HOLD:
                pending_signal = signal
                pending_atr = atr if not pd.isna(atr) else None
                
            # 4. Update Trailing Stop based on current Close
            if self.accountant.holdings > 0 and stop_loss_price:
                new_stop = self.risk_manager.calculate_trailing_stop(
                     highest_price_since_entry=current_close, 
                     atr=atr if not pd.isna(atr) else None
                )
                if new_stop > stop_loss_price:
                    stop_loss_price = new_stop
                    
            # 5. End of day accounting (mark to market using Close price)
            self.accountant.record_daily_state(date, current_close)
            
        self.logger.info("Backtest simulation complete.")
        return self.accountant
