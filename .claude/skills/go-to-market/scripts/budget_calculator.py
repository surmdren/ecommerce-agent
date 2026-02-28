#!/usr/bin/env python3
"""
GTM Budget Calculator

Calculate budget allocation and ROI projections for go-to-market plans.

Usage:
    python budget_calculator.py --budget 50000 --duration 12 --channels "独立站,阿里国际站,展会"

Output:
    - Budget breakdown by category
    - Monthly cash flow projection
    - ROI scenarios (P70/P50/P30)
"""

import argparse
import json
from datetime import datetime, timedelta

# Channel cost templates (monthly average)
CHANNEL_COSTS = {
    "阿里国际站": {
        "setup": 5000,  # Annual fee amortized
        "monthly_fixed": 417,  # $5000/12
        "monthly_variable": 500,  # P4P advertising
        "roi_multiplier": (3, 6, 10)  # Conservative, Base, Optimistic
    },
    "独立站": {
        "setup": 5000,
        "monthly_fixed": 200,  # Hosting + tools
        "monthly_variable": 800,  # SEO/Ads
        "roi_multiplier": (2, 5, 15)
    },
    "展会": {
        "setup": 0,
        "monthly_fixed": 0,
        "monthly_variable": 2500,  # $15K/year ÷ 6 events
        "roi_multiplier": (2, 5, 10)
    },
    "亚马逊": {
        "setup": 3000,
        "monthly_fixed": 40,
        "monthly_variable": 1500,  # Inventory + ads
        "roi_multiplier": (1.2, 2, 4)
    },
}

def calculate_budget_allocation(total_budget, duration_months, channels):
    """Calculate budget breakdown."""

    # Calculate total setup costs
    setup_costs = sum(CHANNEL_COSTS[ch]["setup"] for ch in channels if ch in CHANNEL_COSTS)

    # Remaining budget for operations
    operational_budget = total_budget - setup_costs
    monthly_budget = operational_budget / duration_months

    # Allocate by channel
    allocation = {}
    for channel in channels:
        if channel in CHANNEL_COSTS:
            monthly_cost = (
                CHANNEL_COSTS[channel]["monthly_fixed"] +
                CHANNEL_COSTS[channel]["monthly_variable"]
            )
            allocation[channel] = {
                "setup": CHANNEL_COSTS[channel]["setup"],
                "monthly": monthly_cost,
                "total": CHANNEL_COSTS[channel]["setup"] + monthly_cost * duration_months
            }

    # Add other categories
    content_budget = operational_budget * 0.15
    personnel_budget = operational_budget * 0.20
    contingency = operational_budget * 0.15

    result = {
        "total_budget": total_budget,
        "duration_months": duration_months,
        "setup_costs": setup_costs,
        "operational_budget": operational_budget,
        "monthly_budget": monthly_budget,
        "channels": allocation,
        "other_costs": {
            "content_creation": content_budget,
            "personnel": personnel_budget,
            "contingency": contingency
        }
    }

    return result

def calculate_roi_projections(budget_allocation, channels):
    """Calculate ROI scenarios."""

    total_investment = budget_allocation["total_budget"]

    scenarios = {}
    for scenario_name, percentile in [("Conservative", 0), ("Base", 1), ("Optimistic", 2)]:
        total_return = 0
        for channel in channels:
            if channel in CHANNEL_COSTS and channel in budget_allocation["channels"]:
                channel_investment = budget_allocation["channels"][channel]["total"]
                multiplier = CHANNEL_COSTS[channel]["roi_multiplier"][percentile]
                channel_return = channel_investment * multiplier
                total_return += channel_return

        scenarios[scenario_name] = {
            "total_return": total_return,
            "roi_multiplier": total_return / total_investment if total_investment > 0 else 0,
            "profit": total_return - total_investment
        }

    return scenarios

def generate_cash_flow(budget_allocation):
    """Generate monthly cash flow projection."""

    duration = budget_allocation["duration_months"]
    monthly_ops = budget_allocation["monthly_budget"]

    cash_flow = []
    for month in range(1, duration + 1):
        if month == 1:
            # Include setup costs in first month
            outflow = budget_allocation["setup_costs"] + monthly_ops
        else:
            outflow = monthly_ops

        # Simple revenue ramp: 0 for first 2 months, then linear growth
        if month <= 2:
            inflow = 0
        else:
            # Assume reaching break-even around month 6-8
            inflow = (month - 2) * (budget_allocation["total_budget"] / duration) * 0.3

        cash_flow.append({
            "month": month,
            "outflow": round(outflow, 2),
            "inflow": round(inflow, 2),
            "net": round(inflow - outflow, 2)
        })

    return cash_flow

def main():
    parser = argparse.ArgumentParser(description="GTM Budget Calculator")
    parser.add_argument("--budget", type=float, required=True, help="Total budget in USD")
    parser.add_argument("--duration", type=int, required=True, help="Duration in months")
    parser.add_argument("--channels", type=str, required=True, help="Comma-separated channel names")
    parser.add_argument("--output", type=str, default="budget-breakdown.json", help="Output JSON file")

    args = parser.parse_args()

    channels = [ch.strip() for ch in args.channels.split(",")]

    # Calculate allocation
    allocation = calculate_budget_allocation(args.budget, args.duration, channels)

    # Calculate ROI
    roi_scenarios = calculate_roi_projections(allocation, channels)

    # Generate cash flow
    cash_flow = generate_cash_flow(allocation)

    # Combine results
    result = {
        "generated_at": datetime.now().isoformat(),
        "budget_allocation": allocation,
        "roi_scenarios": roi_scenarios,
        "cash_flow": cash_flow
    }

    # Save to JSON
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)

    # Print summary
    print(f"\n=== GTM Budget Analysis ===")
    print(f"Total Budget: ${allocation['total_budget']:,.0f}")
    print(f"Duration: {allocation['duration_months']} months")
    print(f"\nChannels: {', '.join(channels)}")
    print(f"\nSetup Costs: ${allocation['setup_costs']:,.0f}")
    print(f"Monthly Operational Budget: ${allocation['monthly_budget']:,.0f}")
    print(f"\n=== ROI Projections ===")
    for scenario, data in roi_scenarios.items():
        print(f"{scenario}: ${data['total_return']:,.0f} ({data['roi_multiplier']:.1f}x ROI)")
    print(f"\nDetailed breakdown saved to: {args.output}")

if __name__ == "__main__":
    main()
