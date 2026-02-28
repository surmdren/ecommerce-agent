#!/usr/bin/env python3
"""
Multi-source market data fetcher for arbitrage trading.
Supports Yahoo Finance (free) for quick start.
"""

import requests
import json
from datetime import datetime
from typing import Dict, List

class MarketDataFetcher:
    def __init__(self):
        self.base_url = "https://query1.finance.yahoo.com/v7/finance/quote"

    def fetch_quotes(self, symbols: List[str]) -> Dict:
        """Fetch real-time quotes from Yahoo Finance."""
        try:
            params = {"symbols": ",".join(symbols)}
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            results = {}
            for quote in data.get("quoteResponse", {}).get("result", []):
                symbol = quote.get("symbol")
                results[symbol] = {
                    "price": quote.get("regularMarketPrice"),
                    "change_percent": quote.get("regularMarketChangePercent"),
                    "volume": quote.get("regularMarketVolume"),
                    "exchange": quote.get("fullExchangeName"),
                    "timestamp": datetime.now().isoformat()
                }
            return results
        except Exception as e:
            return {"error": str(e)}

    def compare_cross_market(self, company_symbols: Dict[str, List[str]]) -> Dict:
        """
        Compare prices across markets for arbitrage opportunities.

        Example:
            compare_cross_market({
                "Alibaba": ["BABA", "9988.HK"],
                "Baidu": ["BIDU", "9888.HK"]
            })
        """
        results = {}
        for company, symbols in company_symbols.items():
            quotes = self.fetch_quotes(symbols)
            if "error" in quotes:
                results[company] = quotes
                continue

            prices = {s: q["price"] for s, q in quotes.items() if q.get("price")}
            if len(prices) >= 2:
                min_sym = min(prices, key=prices.get)
                max_sym = max(prices, key=prices.get)
                spread_pct = ((prices[max_sym] - prices[min_sym]) / prices[min_sym]) * 100

                results[company] = {
                    "quotes": quotes,
                    "opportunity": {
                        "buy_market": min_sym,
                        "buy_price": prices[min_sym],
                        "sell_market": max_sym,
                        "sell_price": prices[max_sym],
                        "spread_percent": round(spread_pct, 2)
                    }
                }
        return results

if __name__ == "__main__":
    fetcher = MarketDataFetcher()
    result = fetcher.compare_cross_market({
        "Alibaba": ["BABA", "9988.HK"],
        "Baidu": ["BIDU", "9888.HK"]
    })
    print(json.dumps(result, indent=2))
