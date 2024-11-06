from telebot import TeleBot
from telebot.types import Message

from utils.get_from_env import get_from_env_lang, get_from_env_api


def handle_configure_availability(message: Message, bot: TeleBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    api_conection = get_api()
    language = get_len()
    text = message.text
    # mensaje vacio retorna ayuda
    if text.strip() == "/configurar_disponibilidad":
        bot.reply_to(message, language["MESSAGE_HELP_AVAILABILITY"])
        return
    number = text.split(' ')[1]
    # mensaje con valor numerico
    if number.isdigit():
        number = int(number)
        id_telegram = message.from_user.username  # revisar si este es el ID
        _a = api_conection.set_availability(number, id_telegram)
        print(_a)
        response_to_user = 'OK'
        bot.reply_to(message, response_to_user)
        return
    # mensaje sin valor numerica valido
    bot.reply_to(message, language["MESSAGE_INVALID_VALUE"])
