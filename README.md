# ARIYANTO AI v3

Hierarchical Multi-Agent Trading System

## Features
- 9 Specialist Agents (Futures, Risk, ICT, DEX, dll)
- Smart Keyword Routing
- Production Ready (systemd + Telegram)

## Usage
```bash
PYTHONPATH=src python run.py "Long BTC 10x"
PYTHONPATH=src python run.py "Check portfolio risk"
sudo systemctl status ariyanto-ai
sudo systemctl restart ariyanto-ai
Agents
FuturesSpecialist (long, short, btc)
RiskManager (risk, drawdown)
ICTSMCAgent (ict, smc)
IntelligenceResearchAgent (analyze, news)
DEXSpecialist (dex, arbitrage)
TradingViewMCPAgent (tradingview, chart)
MoonshotSolanaAgent (moonshot, solana)
WalletManager (wallet, balance)
GeneralAnalysisAgent (fallback)
Built by @ariiyaantoo

---

## ⚠️ LIVE TRADING MODE

**DEFAULT: SIMULATION MODE** (safe, no real money)

To enable live trading:

```bash
# 1. Edit .env
EXECUTION_MODE=live
MAX_POSITION_SIZE_USD=500
REQUIRE_CONFIRMATION=true

# 2. Start with confirmation
EXECUTION_MODE=live python run.py "Long BTC 10x"
Safety Features:
Max position size limit
Explicit confirmation required
All actions logged to audit trail
Telegram alerts for all live actions
Automatic fallback to simulation on errors
Never run live mode without:
Understanding the risks
Testing thoroughly in simulation
Setting appropriate position limits
