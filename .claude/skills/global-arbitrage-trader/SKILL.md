---
name: global-arbitrage-trader
description: "Systematically identify and execute arbitrage opportunities across global financial markets using information asymmetry. Covers cross-market arbitrage (A-shares/H-shares/US ADRs), time-based arbitrage (news events, earnings), regulatory policy differences, and market sentiment gaps. Supports stocks, ETFs, futures, options, bonds, forex, and crypto. Includes risk management (position sizing, stop loss, correlation analysis) and semi-automated trade execution with mandatory pre-trade confirmation. Use when (1) analyzing cross-market price discrepancies, (2) monitoring overnight news impact on related markets, (3) evaluating policy-driven arbitrage opportunities, (4) performing short-term trading based on information gaps, (5) managing risk for arbitrage positions, (6) generating arbitrage opportunity dashboards."
---

# Global Arbitrage Trader

Systematically identify and profit from global financial information asymmetry through structured arbitrage strategies.

## Overview

This skill enables个人投资者 (retail traders) to systematically discover and execute arbitrage opportunities across global financial markets by leveraging information gaps. It provides:

1. **Cross-Market Arbitrage Scanner**: Find price discrepancies for the same asset across different exchanges (US/HK/A-shares)
2. **Time-Based Opportunity Monitor**: Track overnight news and earnings announcements that create temporary mispricings
3. **Risk Management Framework**: Position sizing, stop-loss calculation, and portfolio correlation analysis
4. **Trade Execution Workflow**: Semi-automated execution with mandatory pre-trade confirmation

**Target Users**: Individual traders doing short-term trading (短线交易) with moderate capital ($10k-$500k)

## Workflow Decision Tree

Start here to determine your workflow:

```
User Request → Classify Intent:

├─ "Show me arbitrage opportunities" → [Scan for Opportunities]
├─ "Monitor [Company] cross-market spread" → [Track Specific Pair]
├─ "Calculate position size for [Trade]" → [Risk Calculation]
├─ "Execute trade on [Symbol]" → [Trade Execution]
└─ "Generate dashboard" → [Dashboard Generation]
```

## Step 1: Scan for Arbitrage Opportunities

### 1.1 Cross-Market Arbitrage

Identify price discrepancies for the same company listed on multiple exchanges.

**Common Pairs**:
- Alibaba: BABA (US) vs 9988.HK (Hong Kong)
- Baidu: BIDU (US) vs 9888.HK
- JD.com: JD (US) vs 9618.HK

**Execution**:
```python
from scripts.fetch_market_data import MarketDataFetcher

fetcher = MarketDataFetcher()
opportunities = fetcher.compare_cross_market({
    "Alibaba": ["BABA", "9988.HK"],
    "Baidu": ["BIDU", "9888.HK"]
})

# Opportunity structure:
# {
#   "Alibaba": {
#     "quotes": {...},
#     "opportunity": {
#       "buy_market": "9988.HK",
#       "buy_price": 75.30,
#       "sell_market": "BABA",
#       "sell_price": 78.50,
#       "spread_percent": 4.25
#     }
#   }
# }
```

**Threshold**: Only consider opportunities with spread > 2% (to cover transaction costs)

### 1.2 Time-Based Arbitrage

Monitor overnight news that affects related markets with time lag.

**Common Scenarios**:
- US Fed rate decision → China financial stocks next day
- US semiconductor stocks down → A-share chip stocks open lower
- Apple earnings miss → Apple supply chain stocks in Asia

**Workflow**:
1. Monitor US market close (9:30pm ET = 10:30am Beijing next day)
2. Identify significant moves (>3% on major stocks/indices)
3. Map to related A-share/H-share tickers
4. Prepare orders before Asian market open

**Information Sources**:
- Yahoo Finance for real-time US quotes
- Web search for breaking news
- See `references/arbitrage_strategies.md` for detailed strategy library

## Step 2: Risk Management Calculation

Before executing any trade, calculate proper position sizing and stop-loss levels.

### 2.1 Position Sizing

```python
from scripts.risk_calculator import RiskCalculator

# Initialize with your capital and risk tolerance
calc = RiskCalculator(
    total_capital=100000,  # $100k total
    risk_per_trade_pct=2.0  # Risk max 2% per trade
)

# Calculate position size
position = calc.calculate_position_size(
    entry_price=150.00,
    stop_loss_price=145.00  # 3.3% stop loss
)

# Returns:
# {
#   "shares": 400,
#   "position_value": 60000,
#   "position_percent": 60%,
#   "risk_amount": 2000  # 2% of capital
# }
```

### 2.2 Stop Loss Calculation

```python
# Multiple methods for stop loss
stop_levels = calc.calculate_stop_loss(
    entry_price=150.00,
    volatility_pct=5,  # Historical volatility
    atr_value=3.0,     # Average True Range
    custom_pct=3       # Custom percentage
)

# Returns different stop loss levels:
# {
#   "volatility_based": 142.50,
#   "atr_based": 144.00,
#   "custom_pct_based": 145.50
# }
```

### 2.3 Risk/Reward Analysis

```python
# Check if trade has favorable risk/reward ratio
rr = calc.risk_reward_ratio(
    entry_price=150.00,
    stop_loss=145.00,
    take_profit=165.00
)

# Returns:
# {
#   "risk_amount": 5.00,
#   "reward_amount": 15.00,
#   "risk_reward_ratio": 3.0,
#   "recommendation": "Good"  # >= 2.0 is good
# }
```

**Rule**: Only execute trades with Risk/Reward >= 2:1

## Step 3: Trade Execution

**CRITICAL**: Before any automated trade execution, use `AskUserQuestion` to confirm:

```python
# MANDATORY PRE-TRADE CONFIRMATION
confirmation = AskUserQuestion(
    questions=[{
        "question": f"Execute trade: BUY {shares} shares of {symbol} at ${price}?",
        "header": "Trade Confirm",
        "multiSelect": false,
        "options": [
            {
                "label": "Confirm and Execute",
                "description": f"Buy {shares} @ ${price} | Stop Loss: ${stop_loss} | Risk: ${risk_amount}"
            },
            {
                "label": "Cancel",
                "description": "Do not execute this trade"
            }
        ]
    }]
)
```

**Execution Context** (what to tell user):
1. **Opportunity**: Why this trade makes sense (e.g., "4.2% spread between BABA US and 9988.HK")
2. **Risk**: How much capital at risk (e.g., "$2,000 max loss if stop hit")
3. **Expected Return**: Target profit (e.g., "$6,000 profit if spread converges")
4. **Timeline**: Expected holding period (e.g., "1-3 days for spread convergence")

### Broker API Integration

Currently **not implemented** - requires user-specific broker API setup.

**Supported Brokers** (user must configure):
- Futu Securities (富途证券): US/HK stocks
- Tiger Brokers (老虎证券): US/HK stocks
- Interactive Brokers: Global multi-asset

**Configuration**: Copy `assets/config_template.json` and fill in API keys.

## Step 4: Monitor and Exit

### Exit Conditions

1. **Target Hit**: Spread converges to historical mean
2. **Stop Loss**: Price hits stop loss level
3. **Time Stop**: Holding period exceeds N days without profit
4. **Event Risk**: Major news breaks that invalidates thesis

### Portfolio Correlation

```python
# Check portfolio diversification
portfolio = [
    {"symbol": "BABA", "value": 30000, "sector": "E-commerce"},
    {"symbol": "BIDU", "value": 25000, "sector": "Internet"},
    {"symbol": "PDD", "value": 20000, "sector": "E-commerce"}
]

metrics = calc.calculate_portfolio_correlation(portfolio)

# Returns:
# {
#   "total_portfolio_value": 75000,
#   "sector_exposure_pct": {
#     "E-commerce": 66.67,
#     "Internet": 33.33
#   },
#   "concentration_risk_pct": 66.67,
#   "diversification_score": 33.33
# }
```

**Warning**: If concentration_risk > 50%, consider diversifying.

## Common Usage Examples

### Example 1: Daily Morning Scan

```python
# 9:00am: Scan for opportunities before market open
fetcher = MarketDataFetcher()

# Check cross-market spreads
opportunities = fetcher.compare_cross_market({
    "Alibaba": ["BABA", "9988.HK"],
    "Baidu": ["BIDU", "9888.HK"],
    "JD": ["JD", "9618.HK"]
})

# Filter: only show spread > 2%
viable = {k: v for k, v in opportunities.items()
          if v.get("opportunity", {}).get("spread_percent", 0) > 2.0}

# Output to user as markdown table
```

### Example 2: News-Driven Arbitrage

```
User: "US semis down 5% yesterday, any A-share opportunities?"

Agent workflow:
1. Search news: Confirm US semiconductor selloff reason
2. Identify related A-share tickers (688981.SS, 002371.SZ, etc.)
3. Fetch A-share opening prices
4. Calculate expected gap and potential profit
5. Present opportunity with risk analysis
6. If user confirms, prepare trade execution
```

### Example 3: Position Sizing

```
User: "I want to buy Alibaba HK at 75, stop loss at 72, how many shares?"

Agent workflow:
1. Load user's total capital from config
2. Calculate position size with 2% risk rule
3. Present: "Buy 666 shares = $49,950 position (50% of capital)"
4. Show risk/reward if take profit at 81
5. Ask confirmation before execution
```

## Bundled Resources

### scripts/
- **fetch_market_data.py**: Multi-source market data fetcher (Yahoo Finance free API)
- **risk_calculator.py**: Position sizing, stop loss, risk/reward calculations

Run scripts directly:
```bash
python scripts/fetch_market_data.py
python scripts/risk_calculator.py
```

### references/
- **arbitrage_strategies.md**: Comprehensive strategy library covering 4 types of arbitrage with real examples, risk management rules, and data sources

Load when user asks about specific strategies:
```python
# Example: User asks "How does ADR arbitrage work?"
read_file("references/arbitrage_strategies.md")  # Section 1.1
```

### assets/
- **config_template.json**: Configuration template for capital, risk tolerance, monitored pairs, and broker API credentials

## Risk Warnings

1. **Transaction Costs**: Always account for commissions, exchange fees, and bid-ask spread
2. **Currency Risk**: Cross-border trades involve FX risk
3. **Execution Risk**: Prices may move between analysis and execution
4. **Regulatory Risk**: Cross-border trading subject to policy changes
5. **Liquidity Risk**: Some markets have low liquidity causing slippage

**Disclaimer**: This skill is for educational and research purposes. Trading involves significant risk. Past performance does not guarantee future results.
