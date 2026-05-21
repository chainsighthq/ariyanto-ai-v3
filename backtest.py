#!/usr/bin/env python3
"""
ARIYANTO AI v3 - Advanced Backtesting Engine (Realistic)
"""

import random
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Trade:
    entry_price: float
    exit_price: float
    size: float
    pnl: float
    return_pct: float
    entry_date: datetime
    exit_date: datetime

class RealisticBacktester:
    def __init__(self, initial_balance: float = 10000, fee_rate: float = 0.0006, slippage: float = 0.0005):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.fee_rate = fee_rate          # 0.06% fee (Hyperliquid typical)
        self.slippage = slippage          # 0.05% slippage
        self.trades: List[Trade] = []
        self.position = None
        self.max_drawdown = 0.0
        self.peak_balance = initial_balance

    def generate_realistic_prices(self, days: int = 60, volatility: float = 0.025) -> List[float]:
        """Generate realistic price movement"""
        prices = [70000.0]
        for _ in range(days - 1):
            change = random.gauss(0, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 30000))  # floor price
        return prices

    def run_ma_strategy(self, symbol: str = "BTCUSDT", days: int = 60):
        print(f"📊 Backtest: {symbol} | {days} days | Fee: {self.fee_rate*100:.2f}% | Slippage: {self.slippage*100:.2f}%")
        print(f"💰 Initial: ${self.initial_balance:,.2f}")
        print("-" * 60)

        prices = self.generate_realistic_prices(days)
        short_ma, long_ma = 7, 21

        for i in range(long_ma, len(prices)):
            short_avg = sum(prices[i-short_ma:i]) / short_ma
            long_avg = sum(prices[i-long_ma:i]) / long_ma
            price = prices[i]
            date = datetime.now() - timedelta(days=len(prices)-i)

            # Buy
            if short_avg > long_avg and self.position is None:
                entry_price = price * (1 + self.slippage)
                size = (self.balance * 0.95) / entry_price
                fee = entry_price * size * self.fee_rate
                self.balance -= fee

                self.position = {
                    "entry_price": entry_price,
                    "entry_date": date,
                    "size": size
                }
                print(f"🟢 BUY  @ ${entry_price:,.2f} | {date.strftime('%m/%d')} | Fee: ${fee:.2f}")

            # Sell
            elif short_avg < long_avg and self.position is not None:
                exit_price = price * (1 - self.slippage)
                gross_pnl = (exit_price - self.position["entry_price"]) * self.position["size"]
                fee = exit_price * self.position["size"] * self.fee_rate
                net_pnl = gross_pnl - fee
                self.balance += net_pnl

                trade = Trade(
                    entry_price=self.position["entry_price"],
                    exit_price=exit_price,
                    size=self.position["size"],
                    pnl=net_pnl,
                    return_pct=(net_pnl / (self.position["entry_price"] * self.position["size"])) * 100,
                    entry_date=self.position["entry_date"],
                    exit_date=date
                )
                self.trades.append(trade)

                # Update drawdown
                if self.balance > self.peak_balance:
                    self.peak_balance = self.balance
                dd = (self.peak_balance - self.balance) / self.peak_balance * 100
                if dd > self.max_drawdown:
                    self.max_drawdown = dd

                print(f"🔴 SELL @ ${exit_price:,.2f} | PnL: ${net_pnl:+.2f} | DD: {dd:.1f}%")
                self.position = None

        # Close final position
        if self.position:
            exit_price = prices[-1] * (1 - self.slippage)
            gross_pnl = (exit_price - self.position["entry_price"]) * self.position["size"]
            fee = exit_price * self.position["size"] * self.fee_rate
            net_pnl = gross_pnl - fee
            self.balance += net_pnl
            print(f"🔴 CLOSE @ ${exit_price:,.2f} | PnL: ${net_pnl:+.2f}")

        self._print_final_report()

    def _print_final_report(self):
        print("-" * 60)
        print(f"💰 Final Balance     : ${self.balance:,.2f}")
        print(f"📈 Total Return      : {((self.balance/self.initial_balance)-1)*100:+.2f}%")
        print(f"📉 Max Drawdown      : {self.max_drawdown:.2f}%")
        print(f"🔄 Total Trades      : {len(self.trades)}")

        if self.trades:
            wins = sum(1 for t in self.trades if t.pnl > 0)
            winrate = (wins / len(self.trades)) * 100
            avg_pnl = sum(t.pnl for t in self.trades) / len(self.trades)
            print(f"✅ Win Rate          : {winrate:.1f}%")
            print(f"💵 Avg PnL per trade : ${avg_pnl:+.2f}")

if __name__ == "__main__":
    random.seed(42)
    bt = RealisticBacktester(initial_balance=10000, fee_rate=0.0006, slippage=0.0005)
    bt.run_ma_strategy(days=90)
