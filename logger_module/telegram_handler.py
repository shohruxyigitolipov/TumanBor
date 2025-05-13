# logger_module/telegram_handler.py

import logging
import requests

class TelegramLogHandler(logging.Handler):
    def __init__(self, bot_token: str, chat_id: str, level: int = logging.NOTSET):
        super().__init__(level)
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def emit(self, record):
        try:
            log_entry = self.format(record)
            payload = {
                "chat_id": self.chat_id,
                "text": f"🛑 <b>Log:</b>\n<pre>{log_entry}</pre>",
                "parse_mode": "HTML"
            }
            requests.post(self.api_url, data=payload, timeout=3)
        except Exception as e:
            print(f"[TelegramLogHandler] Ошибка: {e}")
