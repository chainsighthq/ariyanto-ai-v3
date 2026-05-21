# 🤖 ARIYANTO AI v3

**Production-Grade Hierarchical Multi-Agent Trading System**

- **52+ Specialist Agents** (Futures, Risk, ICT/SMC, DEX, RWA, dll)
- **Smart Keyword Routing** — Otomatis pilih agent terbaik
- **Hybrid Memory** — Redis (fast) + SQLite (persistent + audit)
- **Production Ready** — Systemd, monitoring, backup, Telegram alerts
- **Safe by Default** — Simulation mode + live mode dengan proteksi

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test via CLI
PYTHONPATH=src python run.py "Long BTC 10x"
PYTHONPATH=src python run.py "Check portfolio risk"
PYTHONPATH=src python run.py "Find SOL arbitrage"

# 3. Run Dashboard
python dashboard.py
# Buka http://localhost:8080

# 4. Run Telegram Bot
python telegram_bot.py

# 5. Run Production (systemd)
sudo systemctl start ariyanto-ai
sudo systemctl start ariyanto-telegram-bot
📁 Project Structure
ariyanto-ai-v3/
├── src/ariyanto_ai_v3/
│   ├── agents/           # 50+ specialist agents
│   ├── core/             # Router, Models, Supervisor
│   ├── memory/           # Redis + SQLite hybrid
│   └── utils/            # Telegram, Rate Limiter, Metrics
├── dashboard.py          # Web monitoring
├── telegram_bot.py       # Telegram interface
├── backtest.py           # Simple backtesting engine
├── run_production.py     # Production runner
└── tests/                # 13 unit tests (100% pass)
🔒 Security Features
Simulation mode by default
Max position size limit
Rate limiting (Telegram)
Full audit logging
.env protected via .gitignore
📊 Monitoring
Dashboard: http://localhost:8080
Prometheus: http://localhost:8000/metrics
Grafana: http://localhost:3000
Logs: logs/ + journalctl -u ariyanto-ai
Built with ❤️ by @ariiyaantoo
