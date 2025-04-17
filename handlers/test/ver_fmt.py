from model.telegram_bot import TelegramBot
from telebot.types import Message


def handle_format(message: Message, bot: TelegramBot):
    print(message)
    bot.reply_to(message, str(message))
