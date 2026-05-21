#!/usr/bin/env python3
"""
ARIYANTO AI v3 - Full Telegram Bot
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent / "src"))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from ariyanto_ai_v3.agents.supervisor_agent import SupervisorAgent
from ariyanto_ai_v3.core.models import Task

load_dotenv()
supervisor = SupervisorAgent(simulation=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *ARIYANTO AI v3*\n\n"
        "Kirim perintah apapun, saya akan routing ke agent yang tepat.\n\n"
        "Contoh: `Long BTC 10x`, `Check portfolio risk`, `Find SOL arbitrage`",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    
    if len(user_input) < 3:
        await update.message.reply_text("❌ Perintah terlalu pendek. Minimal 3 karakter.")
        return
    
    await update.message.reply_text("⏳ Processing...")
    
    try:
        task = Task(user_input=user_input, source="telegram")
        result = supervisor.run(task)
        
        if result.success:
            response = f"✅ *Routed to:* `{result.result_data.get('routed_to', 'N/A')}`\n\n{result.message}"
        else:
            response = f"❌ Error: {result.error}"
        
        await update.message.reply_text(response, parse_mode="Markdown")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Terjadi kesalahan: {str(e)}")

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN tidak ditemukan di .env")
        return
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 ARIYANTO AI v3 Telegram Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
