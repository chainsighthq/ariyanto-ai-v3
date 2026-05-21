#!/usr/bin/env python3
"""
ARIYANTO AI v3 - Simple Backtesting Engine
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict

class SimpleBacktester:
    def __init__(self, initial_balance: float = 10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trades = []
        self.position = None
    
    def run_simple_ma_strategy(self, symbol: str = "BTCUSDT", days: int = 30):
        """
        Simple Moving Average Crossover Strategy (contoh)
        """
        print(f"📊 Running Backtest: {symbol} | {days} days")
        print(f"💰 Initial Balance: ${self.initial_balance:,.2f}")
        print("-" * 50)
        
        # Simulasi data harga (dummy data)
        # Di production nanti bisa pakai data real dari exchange
        import random
        random.seed(42)
        
        prices = [70000 + random.gauss(0, 2000) for _ in range(days)]
        
        short_ma = 5
        long_ma = 20
        
        for i in range(long_ma, len(prices)):
            short_avg = sum(prices[i-short_ma:i]) / short_ma
            long_avg = sum(prices[i-long_ma:i]) / long_ma
            
            price = prices[i]
            date = datetime.now() - timedelta(days=len(prices)-i)
            
            # Buy signal
            if short_avg > long_avg and self.position is None:
                self.position = {
                    "entry_price": price,
                    "entry_date": date,
                    "size": self.balance * 0.95 / price
                }
                print(f"🟢 BUY  @ ${price:,.2f} | {date.strftime('%Y-%m-%d')}")
            
            # Sell signal
            elif short_avg < long_avg and self.position is not None:
                exit_price = price
                pnl = (exit_price - self.position["entry_price"]) * self.position["size"]
                self.balance += pnl
                
                self.trades.append({
                    "entry": self.position["entry_price"],
                    "exit": exit_price,
                    "pnl": pnl,
                    "return_pct": (pnl / (self.position["entry_price"] * self.position["size"])) * 100
                })
                
                print(f"🔴 SELL @ ${exit_price:,.2f} | PnL: ${pnl:+,.2f}")
                self.position = None
        
        # Close position if still open
        if self.position:
            final_price = prices[-1]
            pnl = (final_price - self.position["entry_price"]) * self.position["size"]
            self.balance += pnl
            print(f"🔴 CLOSE @ ${final_price:,.2f} | PnL: ${pnl:+,.2f}")
        
        self._print_summary()
    
    def _print_summary(self):
        print("-" * 50)
        print(f"💰 Final Balance : ${self.balance:,.2f}")
        print(f"📈 Total Return  : {((self.balance/self.initial_balance)-1)*100:+.2f}%")
        print(f"🔄 Total Trades  : {len(self.trades)}")
        
        if self.trades:
            wins = sum(1 for t in self.trades if t["pnl"] > 0)
            winrate = (wins / len(self.trades)) * 100
            print(f"✅ Win Rate      : {winrate:.1f}%")

if __name__ == "__main__":
    bt = SimpleBacktester(initial_balance=10000)
    bt.run_simple_ma_strategy(symbol="BTCUSDT", days=60)
