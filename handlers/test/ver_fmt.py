from telebot import TeleBot
from telebot.types import Message

def handle_format(message: Message, bot: TeleBot):
    print(message)
    bot.reply_to(message, str(message))