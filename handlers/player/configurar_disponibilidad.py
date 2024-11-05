from telebot import TeleBot
from telebot.types import Message
from model.api_conection import ApiConection
import os
from utils.language import get_language

def handle_configure_availability(message: Message, bot: TeleBot):
    api_conection = ApiConection("http://" + os.getenv('SERVICE_HOST') + ":" + os.getenv('SERVICE_PORT'))
    language = get_language(os.getenv('LANGUAGE'))
    text = message.text
    # mensaje vacio retorna ayuda
    if text.strip() == "/configurar_disponibilidad":
        bot.reply_to(message, language["MESSAGE_HELP_AVAILABILITY"])
        return
    number = text.split(' ')[1]
    # mensaje con valor numerico
    if number.isdigit():
        number = int(number)
        id_telegram = message.from_user.username # revisar si este es el ID
        _a = api_conection.set_availability(number, id_telegram)
        print(_a)
        response_to_user = 'OK'
        bot.reply_to(message, response_to_user)
        return
    # mensaje sin valor numerica valido
    bot.reply_to(message, language["MESSAGE_INVALID_VALUE"])