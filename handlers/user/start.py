import time
from typing import Callable
from model.telegram_bot import TelegramBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from services.users_service import UsersService
from requests.exceptions import ConnectionError


LOGIN_CALLBACK_TIME = 8
LOGIN_POST_DISCLAIMER_TIME = 2


def filter_fn(call: CallbackQuery):
    return call.data.startswith("start")


def handle_start(message: Message, bot: TelegramBot, users_service: UsersService = UsersService()):
    chat_id = message.chat.id
    try:
        result = users_service.get_user_info(chat_id)
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
    except ConnectionError:
        bot.reply_to(
            message,
            "Ha ocurrido un error. Por favor, intenta de nuevo más tarde.")


def ask_login_method(message: Message, bot: TelegramBot):
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
                          bot: TelegramBot,
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
        fn_sleep(LOGIN_CALLBACK_TIME)
        bot.send_message(
            chat_id,
            "Te has registrado correctamente.\nPara encontrar matches, por favor, configura tu ubicación y disponibilidad.")
        send_disclaimer(chat_id, bot, fn_sleep)
    elif call.data == "start_user_pass":
        bot.reply_to(
            call.message,
            "Esta opción no esta disponible actualmente. Por favor, intenta de nuevo más tarde.")


def send_disclaimer(
        chat_id: int,
        bot: TelegramBot,
        fn_sleep: Callable[[float], None] = time.sleep):
    fn_sleep(LOGIN_POST_DISCLAIMER_TIME)
    bot.send_message(
        chat_id,
        bot.language_manager.get("MESSAGE_DISCLAIMER")
    )