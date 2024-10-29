import telebot
from model.api_conection import ApiConection
from telebot.util import extract_arguments
from languaje import get_languaje

from dotenv import load_dotenv
import os

# Carga el archivo .env
load_dotenv()
# obtiene el token del bot
token_bot = os.getenv('TOKEN_BOT_TELEGRAM')
# carga diccionario de idiomas
languaje = get_languaje(os.getenv('LANGUAGE'))
# obtiene la direccion del back end
api_conection = ApiConection(os.getenv('URL') + ":" + os.getenv('PORT'))
# creacion del bot
bot = telebot.TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, languaje["MESSAGE_START"])


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, '/start /help /ver_fmt /saludar /exit /registrarse /configurar_disponibilidad')


@bot.message_handler(commands=['saludar'])
def hello_world(message):
    hi_name = extract_arguments(message.text)
    # api_conection = ApiConection()
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


# Para todos los mensajes (esto es para pruebas borrarlo)
@bot.message_handler(func=lambda _message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.message_handler(commands=['configurar_disponibilidad'])
def set_availability(message):
    text = message.text
    # mensaje vacio retorna ayuda
    if text == "/configurar_disponibilidad":
        # text_base = 'Indicanos los horarios que suelas tener disponibles:\n'
        # text_definition_of_hour = '- Mañana de 8hs hasta 12hs.\n- Tarde de 12hs hasta 18hs.\n- Noche de 18hs hasta 00hs.\n'
        # text_options_allowed = '1: Mañana\n2: Tarde\n3: Noche\n4: Mañana y tarde\n5: Mañana y noche\n6: Tarde y noche\n7: Todos\n'
        # text_example = 'Asignación: /configurar_disponibilidad <Numero>'
        # response_to_user = text_base + text_definition_of_hour + text_options_allowed + text_example
        # bot.reply_to(message, response_to_user)
        bot.reply_to(message, languaje["MESSAGE_HELP_AVAILABILITY"])
        return
    number = text.split(' ')[1]
    # mensaje con valor numerico
    if number.isdigit():
        number = int(number)
        # api_conection = ApiConection()
        # el resultado de la api conection debe ser probado por separado
        _ = api_conection.set_availability(number)
        response_to_user = 'OK'
        bot.reply_to(message, response_to_user)
        return
    # mensaje sin valor numerica valido
    # response_to_user = "No es un valor valido"
    # bot.reply_to(message, response_to_user)
    bot.reply_to(message, languaje["MESSAGE_INVALID_VALUE"])

if __name__ == '__main__':
    print("BOT INICIADO")
    bot.polling(none_stop=True)

