from telebot import TeleBot
from telebot.types import Message

def handle_help(message: Message, bot: TeleBot):
    bot.stop_bot()
    return