from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from services.user_service import UserService


def handle_start(message: Message, bot: TeleBot):
    chat_id = message.chat.id
    service = UserService()
    result = service.register_user(chat_id)
    if result:
        ask_login_method(message, bot)
    else:
        result = service.get_user_info(chat_id)
        if result:
            bot.reply_to(
                message,
                f"Bienvenido de nuevo, {result.get('name')}!")
        else:
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


def handle_callback_query(call: CallbackQuery, bot: TeleBot):
    chat_id = call.message.chat.id
    service = UserService()
    if call.data == "start_google":
        auth_url = service.generate_google_auth_url(chat_id)
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
    elif call.data == "start_user_pass":
        bot.reply_to(
            call.message,
            "Esta opción no esta disponible actualmente. Por favor, intenta de nuevo más tarde.")
