from model.telegram_bot import TelegramBot
from telebot.types import Message

# saludar exit ver_fmt
COMMANDS = ["/start", "/help", "/registrarse", "/configurar_disponibilidad", "/ver_emparejamientos", "/configurar_golpes", "/ver_reservas", "/encuesta_jugador", "/configurar_ubicacion"]
SEPARATOR_OF_DATA = ": "

def handle_help(message: Message, bot: TelegramBot):
    data_language = bot.language_manager.get("MESSAGE_HELP_GENERAL")
    message_to_help = ""
    for command in COMMANDS:
        message_to_help += command + SEPARATOR_OF_DATA + data_language[command] + "\n"
    bot.reply_to(
        message,
        message_to_help)
