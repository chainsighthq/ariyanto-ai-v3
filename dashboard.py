#!/usr/bin/env python3
"""
ARIYANTO AI v3 - Interactive Web Dashboard
"""

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ariyanto_ai_v3.agents.supervisor_agent import SupervisorAgent
from ariyanto_ai_v3.core.models import Task

app = FastAPI(title="ARIYANTO AI v3 Dashboard")
supervisor = SupervisorAgent(simulation=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ARIYANTO AI v3</title>
    <meta charset="utf-8">
    <style>
        body { font-family: system-ui; background: #0d1117; color: #c9d1d9; padding: 20px; max-width: 900px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .card { background: #161b22; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        input, button { padding: 12px; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; font-size: 16px; }
        input { width: 70%; }
        button { background: #238636; color: white; cursor: pointer; }
        button:hover { background: #2ea043; }
        .result { background: #0d1117; padding: 15px; border-radius: 6px; margin-top: 15px; white-space: pre-wrap; }
        .success { border-left: 4px solid #238636; }
        .error { border-left: 4px solid #da3633; }
        h1 { color: #58a6ff; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 ARIYANTO AI v3</h1>
        <p>Hierarchical Multi-Agent Trading System • 52+ Agents</p>
    </div>

    <div class="card">
        <h2>🧪 Test Agent</h2>
        <form action="/test" method="post">
            <input type="text" name="prompt" placeholder="Contoh: Long BTC 10x atau Check portfolio risk" required>
            <button type="submit">Run</button>
        </form>
        
        {% if result %}
        <div class="result {{ 'success' if result.success else 'error' }}">
            <strong>Routed to:</strong> {{ result.result_data.get('routed_to', 'N/A') }}<br><br>
            <strong>Message:</strong><br>
            {{ result.message }}
        </div>
        {% endif %}
    </div>

    <div class="card">
        <h2>📋 Quick Examples</h2>
        <ul>
            <li><code>Long BTC 10x</code> → FuturesSpecialist</li>
            <li><code>Check portfolio risk</code> → RiskManager</li>
            <li><code>Analyze XAGUSD with ICT</code> → ICTSMCAgent</li>
            <li><code>Find SOL arbitrage</code> → DEXSpecialist</li>
            <li><code>RWA investment options</code> → RWAAgent</li>
        </ul>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML.replace("{% if result %}", "").replace("{% endif %}", "")

@app.post("/test", response_class=HTMLResponse)
async def test_agent(prompt: str = Form(...)):
    task = Task(user_input=prompt, source="cli")
    result = supervisor.run(task)
    
    html_result = HTML.replace(
        "{% if result %}", 
        f'<div class="result {"success" if result.success else "error"}">'
    ).replace(
        "{% endif %}", 
        f"""
        <strong>Routed to:</strong> {result.result_data.get('routed_to', 'N/A')}<br><br>
        <strong>Message:</strong><br>
        {result.message}
        </div>
        """
    )
    
    return html_result

if __name__ == "__main__":
    print("🚀 ARIYANTO AI v3 Dashboard running at http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
