from model.telegram_bot import TelegramBot
from telebot.types import Message


def handle_help(message: Message, bot: TelegramBot):
    bot.stop_bot()
    return
