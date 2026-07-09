import pandas as pd
from typing import List, Dict

class PortfolioAccountant:
    """
    Tracks portfolio performance, trades, and PnL.
    """
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.holdings = 0.0
        self.average_entry_price = 0.0
        
        self.realized_pnl = 0.0
        self.trade_log: List[Dict] = []
        self.history: List[Dict] = []
        
    def get_portfolio_value(self, current_price: float) -> float:
        """Returns total portfolio value (cash + unrealized value)."""
        return self.cash + (self.holdings * current_price)
        
    def get_unrealized_pnl(self, current_price: float) -> float:
        if self.holdings == 0:
            return 0.0
        return (current_price - self.average_entry_price) * self.holdings

    def log_trade(self, date: pd.Timestamp, action: str, price: float, units: float, fee: float, pnl: float = 0.0):
        """Records a trade execution."""
        self.trade_log.append({
            'Date': date,
            'Action': action,
            'Price': price,
            'Units': units,
            'Fee': fee,
            'PnL': pnl
        })
        
    def record_daily_state(self, date: pd.Timestamp, current_price: float):
        """Records end-of-day portfolio state."""
        self.history.append({
            'Date': date,
            'Cash': self.cash,
            'Holdings': self.holdings,
            'Price': current_price,
            'Portfolio_Value': self.get_portfolio_value(current_price),
            'Unrealized_PnL': self.get_unrealized_pnl(current_price),
            'Realized_PnL': self.realized_pnl
        })
        
    def execute_buy(self, date: pd.Timestamp, price: float, units: float, fee_rate: float):
        cost = price * units
        fee = cost * fee_rate
        total_cost = cost + fee
        
        if total_cost > self.cash:
            # Adjust units to fit available cash (rare, but safety check)
            units = self.cash / (price * (1 + fee_rate))
            cost = price * units
            fee = cost * fee_rate
            total_cost = cost + fee
            
        # Update entry price (weighted average)
        total_value_held = self.holdings * self.average_entry_price
        self.holdings += units
        self.average_entry_price = (total_value_held + cost) / self.holdings
        
        # Track entry fees for PnL
        if not hasattr(self, 'accumulated_entry_fees'):
            self.accumulated_entry_fees = 0.0
        self.accumulated_entry_fees += fee
        
        self.cash -= total_cost
        self.log_trade(date, 'BUY', price, units, fee)

    def execute_sell(self, date: pd.Timestamp, price: float, units: float, fee_rate: float):
        if units > self.holdings:
            units = self.holdings # Can't sell more than we hold
            
        revenue = price * units
        fee = revenue * fee_rate
        net_revenue = revenue - fee
        
        # Proportion of entry fees assigned to this sell
        proportion_sold = units / self.holdings if self.holdings > 0 else 1.0
        entry_fees_for_this_trade = getattr(self, 'accumulated_entry_fees', 0.0) * proportion_sold
        
        # True Net PnL = Revenue - Cost - ExitFee - EntryFee
        pnl = (price - self.average_entry_price) * units - fee - entry_fees_for_this_trade
        self.realized_pnl += pnl
        
        self.holdings -= units
        self.cash += net_revenue
        
        # Reduce accumulated entry fees
        if hasattr(self, 'accumulated_entry_fees'):
            self.accumulated_entry_fees -= entry_fees_for_this_trade
        
        if self.holdings <= 1e-8: # floating point precision check
            self.holdings = 0.0
            self.average_entry_price = 0.0
            self.accumulated_entry_fees = 0.0
            
        self.log_trade(date, 'SELL', price, units, fee, pnl)

    def get_history_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.history)
        if not df.empty:
             df.set_index('Date', inplace=True)
             df['Daily_Return'] = df['Portfolio_Value'].pct_change().fillna(0.0)
        return df
        
    def get_trade_log_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.trade_log)
