from telebot import TeleBot
from telebot.types import Message

from utils.get_from_env import get_from_env_lang

# saludar exit ver_fmt
COMMANDS = ["/start", "/help", "/registrarse", "/configurar_disponibilidad", "/configurar_zona", "/ver_emparejamientos", "/configurar_golpes", "/ver_reservas", "/aceptar_emparejamiento", "/rechazar_emparejamiento", "/encuesta_jugador"]
SEPARATOR_OF_DATA = ": "

def handle_help(message: Message, bot: TeleBot, get_len=get_from_env_lang):
    language = get_len()
    data_language = language["MESSAGE_HELP_GENERAL"]
    message_to_help = ""
    for command in COMMANDS:
        message_to_help += command + SEPARATOR_OF_DATA + data_language[command] + "\n"
    bot.reply_to(
        message,
        message_to_help)
