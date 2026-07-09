import pandas as pd

class RiskManager:
    """
    Handles position sizing, stop loss, and risk limits.
    """
    
    def __init__(self, max_exposure: float = 1.0, risk_per_trade: float = 0.02):
        self.max_exposure = max_exposure
        self.risk_per_trade = risk_per_trade
        
    def calculate_position_size(self, cash: float, current_price: float, atr: float = None) -> float:
        """
        Calculates how much asset to buy. 
        If ATR is provided, sizes based on volatility. 
        Otherwise, uses standard risk per trade.
        """
        if cash <= 0:
            return 0.0
            
        capital_to_risk = cash * self.risk_per_trade
        
        if atr and atr > 0:
            # ATR based sizing: Risking 1 ATR distance
            units = capital_to_risk / atr
        else:
            # Default to using risk capital fully if no ATR
            units = capital_to_risk / current_price
            
        # Ensure we don't exceed max exposure
        max_investment = cash * self.max_exposure
        investment = units * current_price
        
        if investment > max_investment:
            units = max_investment / current_price
            
        return units

    def calculate_stop_loss(self, entry_price: float, atr: float, multiplier: float = 2.0) -> float:
        """
        Calculates an ATR-based stop loss for a long position.
        """
        if not atr or pd.isna(atr):
            return 0.0 # No stop loss if no ATR
        return entry_price - (atr * multiplier)

    def calculate_trailing_stop(self, highest_price_since_entry: float, atr: float, multiplier: float = 2.0) -> float:
        """
        Calculates an ATR-based trailing stop for a long position.
        """
        if not atr or pd.isna(atr):
            return 0.0 # No stop loss if no ATR
        return highest_price_since_entry - (atr * multiplier)
