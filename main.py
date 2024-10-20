import telebot


# hay que ocultar esto no deberia esta en github
TOKEN = '7733963832:AAG4HDHRc5KqNa6XqRT5JCQ9tUwFNMiSZ9M'


# ver si se puede mover
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Bienvenido a PadelPals')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, '/start /help /ver_fmt /exit /duplicar /registrarse')


@bot.message_handler(commands=['registrarse'])
def send_help(message):
    bot.reply_to(message, 'asd')


# esto es para pruebas borrarlo
@bot.message_handler(commands=['ver_fmt'])
def send_format(message):
    print(message)
    bot.reply_to(message, str(message))


# esto es para pruebas borrarlo
@bot.message_handler(commands=['duplicar'])
def send_double(message):
    print(message)
    text = message.text
    result = ""
    try:
        result += str(duplicar(text.split()[1]))
    except:
        result += "No es un valor valido"
    bot.reply_to(message, result)


# detiene el bot
@bot.message_handler(commands=['exit'])
def receive_exit(_message):
    bot.stop_bot()
    return


# Para todos los mensajes (esto es para pruebas borrarlo)
@bot.message_handler(func=lambda _message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


def duplicar(n):
    return n * 2


if __name__ == '__main__':
    print("BOT INICIADO")
    bot.polling(none_stop=True)

