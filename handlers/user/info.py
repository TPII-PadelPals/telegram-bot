from telebot import TeleBot
from services.users_service_backend import UsersServiceBackend
from telebot.types import Message
import requests


def handle_info(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    try:
        service = UsersServiceBackend()
        user_info = service.get_user_info(chat_id)
        if user_info:
            response = f"Nombre: {user_info['name']}\nEmail: {user_info['email']}"
            bot.reply_to(message, response)
        else:
            bot.reply_to(
                message,
                "No se encontró información del usuario. ¿Te has registrado con Google?")
    except requests.exceptions.RequestException:
        bot.reply_to(
            message,
            "Hubo un problema al obtener tu información. Por favor, intenta de nuevo más tarde.")
