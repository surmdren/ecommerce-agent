#!/usr/bin/env python3
"""
Risk management calculator for arbitrage trading.
Calculates position sizing, stop loss, and portfolio risk metrics.
"""

from typing import Dict, List
import json


class RiskCalculator:
    def __init__(self, total_capital: float, risk_per_trade_pct: float = 2.0):
        """
        Initialize risk calculator.

        Args:
            total_capital: Total trading capital
            risk_per_trade_pct: Maximum risk per trade as percentage (default 2%)
        """
        self.total_capital = total_capital
        self.risk_per_trade_pct = risk_per_trade_pct
        self.max_risk_amount = total_capital * (risk_per_trade_pct / 100)

    def calculate_position_size(
        self,
        entry_price: float,
        stop_loss_price: float,
        risk_amount: float = None
    ) -> Dict:
        """
        Calculate position size based on stop loss.

        Args:
            entry_price: Entry price per share
            stop_loss_price: Stop loss price per share
            risk_amount: Custom risk amount (uses max_risk_amount if not provided)

        Returns:
            Dictionary with position sizing details
        """
        if risk_amount is None:
            risk_amount = self.max_risk_amount

        risk_per_share = abs(entry_price - stop_loss_price)
        if risk_per_share == 0:
            return {"error": "Entry price and stop loss cannot be the same"}

        shares = int(risk_amount / risk_per_share)
        position_value = shares * entry_price
        position_pct = (position_value / self.total_capital) * 100

        return {
            "shares": shares,
            "position_value": round(position_value, 2),
            "position_percent": round(position_pct, 2),
            "risk_amount": round(risk_amount, 2),
            "risk_per_share": round(risk_per_share, 2),
            "entry_price": entry_price,
            "stop_loss": stop_loss_price
        }

    def calculate_stop_loss(
        self,
        entry_price: float,
        volatility_pct: float = None,
        atr_value: float = None,
        custom_pct: float = None
    ) -> Dict:
        """
        Calculate stop loss levels using different methods.

        Args:
            entry_price: Entry price
            volatility_pct: Historical volatility percentage
            atr_value: Average True Range value
            custom_pct: Custom percentage below entry

        Returns:
            Dictionary with stop loss levels
        """
        results = {"entry_price": entry_price}

        if volatility_pct:
            sl_volatility = entry_price * (1 - volatility_pct / 100)
            results["volatility_based"] = round(sl_volatility, 2)

        if atr_value:
            sl_atr = entry_price - (2 * atr_value)  # 2x ATR
            results["atr_based"] = round(sl_atr, 2)

        if custom_pct:
            sl_custom = entry_price * (1 - custom_pct / 100)
            results["custom_pct_based"] = round(sl_custom, 2)

        return results

    def calculate_portfolio_correlation(
        self,
        positions: List[Dict[str, float]]
    ) -> Dict:
        """
        Simplified portfolio diversification check.

        Args:
            positions: List of {symbol, value, sector} dicts

        Returns:
            Portfolio concentration metrics
        """
        total_value = sum(p["value"] for p in positions)
        sector_exposure = {}

        for pos in positions:
            sector = pos.get("sector", "Unknown")
            sector_exposure[sector] = sector_exposure.get(sector, 0) + pos["value"]

        sector_pct = {
            sector: round((value / total_value) * 100, 2)
            for sector, value in sector_exposure.items()
        }

        max_sector = max(sector_pct, key=sector_pct.get)
        concentration_risk = sector_pct[max_sector]

        return {
            "total_portfolio_value": round(total_value, 2),
            "sector_exposure_pct": sector_pct,
            "max_sector": max_sector,
            "concentration_risk_pct": concentration_risk,
            "diversification_score": round(100 - concentration_risk, 2)
        }

    def risk_reward_ratio(
        self,
        entry_price: float,
        stop_loss: float,
        take_profit: float
    ) -> Dict:
        """Calculate risk/reward ratio."""
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)

        if risk == 0:
            return {"error": "Risk cannot be zero"}

        rr_ratio = reward / risk

        return {
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_amount": round(risk, 2),
            "reward_amount": round(reward, 2),
            "risk_reward_ratio": round(rr_ratio, 2),
            "recommendation": "Good" if rr_ratio >= 2 else "Reconsider" if rr_ratio >= 1 else "High Risk"
        }


if __name__ == "__main__":
    # Example usage
    calc = RiskCalculator(total_capital=100000, risk_per_trade_pct=2)

    # Position sizing
    print("=== Position Sizing ===")
    position = calc.calculate_position_size(entry_price=150, stop_loss_price=145)
    print(json.dumps(position, indent=2))

    # Stop loss calculation
    print("\n=== Stop Loss Levels ===")
    stop_levels = calc.calculate_stop_loss(
        entry_price=150,
        volatility_pct=5,
        atr_value=3,
        custom_pct=3
    )
    print(json.dumps(stop_levels, indent=2))

    # Risk/Reward
    print("\n=== Risk/Reward Analysis ===")
    rr = calc.risk_reward_ratio(entry_price=150, stop_loss=145, take_profit=165)
    print(json.dumps(rr, indent=2))
