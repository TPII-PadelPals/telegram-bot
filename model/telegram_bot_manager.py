from handlers import MESSAGE_HANDLERS, CALLBACK_HANDLERS
from model.telegram_bot import TelegramBot

class TelegramBotManager():
    def __init__(self):
        self.bot = TelegramBot()
        self.register_handlers()

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
        self.bot.start()