import time
from typing import Callable
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from services.users_service import UsersService


def filter_fn(call: CallbackQuery):
    return call.data.startswith("start")


def handle_start(message: Message, bot: TeleBot, users_service: UsersService = UsersService()):
    chat_id = message.chat.id
    result = users_service.get_user_info(chat_id)
    if result:
        users_count = result["count"]
        if users_count == 0:
            ask_login_method(message, bot)
            return
        users = result["data"]
        user = users[0]
        bot.reply_to(
            message,
            f"Bienvenido de nuevo, {user['name']}!")
        return
    bot.reply_to(
        message,
        "Ha ocurrido un error. Por favor, intenta de nuevo más tarde.")


def ask_login_method(message: Message, bot: TeleBot):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(
            "Registrarse con Usuario y Contraseña",
            callback_data="start_user_pass"),
        InlineKeyboardButton(
            "Registrarse con Google",
            callback_data="start_google"))
    bot.reply_to(
        message,
        "Bienvenido a PaddlePals! Por favor seleccione un método de registro:",
        reply_markup=markup)


def handle_callback_query(call: CallbackQuery,
                          bot: TeleBot,
                          users_service: UsersService = UsersService(),
                          fn_sleep: Callable[[float], None] = time.sleep):
    chat_id = call.message.chat.id
    if call.data == "start_google":
        auth_url = users_service.generate_google_auth_url(chat_id)
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton(
                "Registrarse con Google",
                url=auth_url))
        bot.edit_message_text(
            "¡Bienvenido! Por favor, regístrate con Google para continuar.",
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=markup)
        fn_sleep(8)
        bot.send_message(
            chat_id,
            "Te has registrado correctamente.\nPara encontrar matches, por favor, configura tu ubicación y disponibilidad.")
    elif call.data == "start_user_pass":
        bot.reply_to(
            call.message,
            "Esta opción no esta disponible actualmente. Por favor, intenta de nuevo más tarde.")
