from telebot import TeleBot
from telebot.types import Message
from model.api_conection import ApiConection
import os
from telebot.util import extract_arguments

def handle_greet(message: Message, bot: TeleBot):
    api_conection = ApiConection("http://" + os.getenv('SERVICE_HOST') + ":" + os.getenv('SERVICE_PORT'))
    hi_name = extract_arguments(message.text)
    result = api_conection.get_hi_name(hi_name)
    bot.reply_to(message, f'{result}')