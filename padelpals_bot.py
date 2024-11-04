import telebot
from model.api_conection import ApiConection
from telebot.util import extract_arguments
from language import get_language
import logging

from dotenv import load_dotenv
import os

KM_STEERING_SEPARATOR = ';' # separador de direccion km en especificacion de ubicacion (no puede ser espacio)

# todo refactorizar para enviar esto afuera del archivo y poder mockearlo
# Carga el archivo .env
load_dotenv(override=True)
# obtiene el token del bot
token_bot = os.getenv('TOKEN_BOT_TELEGRAM')
# carga diccionario de idiomas
print(f"lenguaje: {os.getenv('LANGUAGE')}")
language = get_language(os.getenv('LANGUAGE'))
# obtiene la direccion del back end
api_conection = ApiConection("http://" + os.getenv('URL') + ":" + os.getenv('PORT'))
# creacion del bot
bot = telebot.TeleBot(token_bot)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,            # Nivel de log
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato del mensaje de log
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info(f'Received message from {message.chat.id}: {message.text}')
    logging.info(f'Complete Received message: {message.chat}')
    bot.reply_to(message, language["MESSAGE_START"])


@bot.message_handler(commands=['help'])
def send_help(message):
    print(message.from_user.username)
    bot.reply_to(message, '/start /help /ver_fmt /saludar /exit /registrarse /configurar_disponibilidad /configurar_zona')


@bot.message_handler(commands=['saludar'])
def hello_world(message):
    hi_name = extract_arguments(message.text)
    result = api_conection.get_hi_name(hi_name)
    bot.reply_to(message, f'{result}')


@bot.message_handler(commands=['registrarse'])
def register(message):
    bot.reply_to(message, 'asd')


# esto es para pruebas borrarlo
@bot.message_handler(commands=['ver_fmt'])
def send_format(message):
    print(message)
    bot.reply_to(message, str(message))


# detiene el bot, solo para pruebas todo borrar
@bot.message_handler(commands=['exit'])
def receive_exit(_message):
    bot.stop_bot()
    return


@bot.message_handler(commands=['configurar_disponibilidad'])
def set_availability(message):
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


@bot.message_handler(commands=['configurar_zona'])
def set_zone(message):
    text = message.text
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
        text_response = language["MESSAGE_ZONE_UPDATED_LOCATION"] + ": " + direction + "."
    # caso de dos o mas valores solo toma dos en orden
    else:
        km = info_list[1]
        if not km.isdigit():
            bot.reply_to(message, language["MESSAGE_INVALID_VALUE"])
            return
        direction = info_list[0]
        text_response = language["MESSAGE_ZONE_UPDATED_LOCATION"] + ": " + direction + ".\n"
        text_response += language["MESSAGE_ZONE_UPDATED_KM"] + ": " + km + "."
    id_telegram = message.from_user.username # revisar si este es el ID
    # todo verificar lo que devuelve el api
    _a = api_conection.set_zone(direction, km, id_telegram)
    print(_a)
    bot.reply_to(message, text_response)
    return



# Para todos los mensajes (esto es para pruebas borrarlo)
# @bot.message_handler(func=lambda _message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)


if __name__ == '__main__':
    logging.info("BOT Iniciado")
    bot.polling(none_stop=True)

