import telebot
import logging
from handlers import MESSAGE_HANDLERS, CALLBACK_HANDLERS
import os


class TelegramBot:
    def __init__(self):
        self.log = self.setup_logging()
        self.token_bot = os.getenv('TELEGRAM_BOT_TOKEN')
        self.bot = telebot.TeleBot(self.token_bot)
        self.register_handlers()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s][%(threadName)s] %(levelname)s: %(message)s"
        )
        log = logging.getLogger(__name__)
        return log

    def register_handlers(self):
        for handler in MESSAGE_HANDLERS:
            self.bot.register_message_handler(
                callback=handler["handler"], commands=[
                    handler["command"]], pass_bot=True)

        for handler in CALLBACK_HANDLERS:
            self.bot.register_callback_query_handler(
                callback=handler['handler'],
                func=handler['filter_fn'],
                pass_bot=True)

    def start(self):
        self.log.info("Telegram bot Initialized")
        self.log.info(f"Using Language: {os.getenv('TELEGRAM_BOT_LANGUAGE')}")
        self.bot.polling(none_stop=True)
