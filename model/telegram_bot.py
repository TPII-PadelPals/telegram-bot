from model.language_manager import LanguageManager
from telebot import TeleBot
import logging
from core.config import settings
from model.telegram_bot_ui import TelegramBotUI

class TelegramBot(TeleBot):
    def __init__(self):
        super().__init__(settings.TELEGRAM_BOT_TOKEN)
        self.log = self._setup_logging()
        self.language_manager = LanguageManager(settings.TELEGRAM_BOT_LANGUAGE)
        self.ui = TelegramBotUI(self)

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s][%(threadName)s] %(levelname)s: %(message)s"
        )
        log = logging.getLogger(__name__)
        return log

    def start(self):
        self.log.info("Telegram bot Initialized")
        self.log.info(f"Using Language: {settings.TELEGRAM_BOT_LANGUAGE}")
        self.polling(none_stop=True)
