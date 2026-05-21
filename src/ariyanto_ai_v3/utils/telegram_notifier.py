import os
import asyncio
from loguru import logger

try:
    from telegram import Bot
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False

class TelegramNotifier:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        self.enabled = bool(self.bot_token and self.chat_id and TELEGRAM_AVAILABLE)

        if self.enabled:
            self.bot = Bot(token=self.bot_token)
            logger.info("Telegram Notifier enabled")
        else:
            logger.warning("Telegram Notifier disabled (token/chat_id kosong)")

    async def send(self, message: str):
        if not self.enabled:
            logger.debug(f"[Telegram OFF] {message}")
            return False
        try:
            full_msg = f"🤖 <b>ARIYANTO AI v3</b>\n{message}"
            await self.bot.send_message(chat_id=self.chat_id, text=full_msg, parse_mode="HTML")
            logger.info(f"Telegram sent: {message[:60]}...")
            return True
        except Exception as e:
            logger.error(f"Telegram error: {e}")
            return False

    def send_sync(self, message: str):
        try:
            asyncio.run(self.send(message))
        except Exception as e:
            logger.error(f"Telegram sync error: {e}")
