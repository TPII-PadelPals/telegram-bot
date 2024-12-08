from telebot import TeleBot
from telebot.types import Message

from utils.get_from_env import get_from_env_api, get_from_env_lang

# separador de direccion km en especificacion de ubicacion (no puede ser
# espacio)
KM_STEERING_SEPARATOR = ';'
DEFAULT_PLAYER = 'francoMartinDiMaria'


def handle_configure_zone(message: Message, bot: TeleBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    text = message.text
    api_conection = get_api()
    language = get_len()

    # mensaje vacio retorna ayuda
    if text.strip() == "/configurar_zona":
        bot.reply_to(message, language["MESSAGE_HELP_ZONE"])
        return
    # verifico la cantidad de info dada por el usuario
    number_of_not_info_charactes = len("/configurar_zona") + 1
    info_field = text[number_of_not_info_charactes:]
    info_list = info_field.split(KM_STEERING_SEPARATOR)
    # no ocurrira nunca que haya cero valores por el if anterior
    # solo se dio un valor y son los KM
    if len(info_list) == 1 and info_list[0].isdigit():
        direction = None
        km = info_list[0]
        text_response = language["MESSAGE_ZONE_UPDATED_KM"] + ": " + km + "."
    # solo se dio un valor y es la ubicacion
    elif len(info_list) == 1 and not info_list[0].isdigit():
        direction = info_list[0]
        km = None
        text_response = language["MESSAGE_ZONE_UPDATED_LOCATION"] + \
            ": " + direction + "."
    # caso de dos o mas valores solo toma dos en orden
    else:
        km = info_list[1]
        if not km.isdigit():
            bot.reply_to(message, language["MESSAGE_INVALID_VALUE"])
            return
        direction = info_list[0]
        text_response = language["MESSAGE_ZONE_UPDATED_LOCATION"] + \
            ": " + direction + ".\n"
        text_response += language["MESSAGE_ZONE_UPDATED_KM"] + ": " + km + "."
    id_telegram = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER  # revisar si este es el ID
    # todo verificar lo que devuelve el api
    _a = api_conection.set_zone(direction, km, id_telegram)
    print(_a)
    bot.reply_to(message, text_response)
    return
