from telebot import TeleBot
from telebot.types import Message


def handle_help(message: Message, bot: TeleBot):
    bot.reply_to(
        message,
        '/start /help /ver_fmt /saludar /exit /registrarse /configurar_disponibilidad /configurar_zona')
