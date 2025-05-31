from model.telegram_bot import TelegramBot
from telebot.types import Message

# saludar exit ver_fmt
COMMANDS = ["/start", "/help", "/configurar_ubicacion",
            "/configurar_disponibilidad", "/configurar_golpes",  "/ver_emparejamientos"]
SEPARATOR_OF_DATA = ": "


def handle_help(message: Message, bot: TelegramBot):
    generate_message = generate_message_help(bot)
    bot.reply_to(
        message,
        generate_message)


def generate_message_help(bot: TelegramBot):
    data_language = bot.language_manager.get("MESSAGE_HELP_GENERAL")
    message_to_help = ""
    for command in COMMANDS:
        message_to_help += command + SEPARATOR_OF_DATA + \
            data_language[command] + "\n"
    return message_to_help
