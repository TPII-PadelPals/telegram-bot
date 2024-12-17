from telebot import TeleBot
from telebot.types import Message
from model.api_conection import ApiConection
from telebot.util import extract_arguments
from core.config import settings

def handle_greet(message: Message, bot: TeleBot):
    api_conection = ApiConection(f"http://{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}")
    hi_name = extract_arguments(message.text)
    result = api_conection.get_hi_name(hi_name)
    bot.reply_to(message, f'{result}')
