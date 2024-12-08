from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery

from utils.get_from_env import get_from_env_lang, get_from_env_api

import logging

logging.basicConfig(level=logging.INFO)
loger = logging.getLogger(__name__)

DEFAULT_PLAYER = 'francoMartinDiMaria'

def get_callback_data(text, buttons):
    for button in buttons:
        if button["text"] == text:
            return button["callback_data"]
    return None

def handle_configure_availability(message: Message, bot: TeleBot):
    language = get_from_env_lang()
    
    markup = ReplyKeyboardMarkup(row_width=2)
    for button in language["AVAILABILITY_TIME_BUTTONS"]:
        markup.add(KeyboardButton(button["text"]))

    msg = bot.reply_to(message, language["AVAILABILITY_MESSAGE"], reply_markup=markup, parse_mode="Markdown")
    bot.register_next_step_handler(msg, process_time_step, bot)
    loger.info("Se ha configurado la disponibilidad")


def process_time_step(message: Message, bot: TeleBot):
    api_conection = get_from_env_api()
    language = get_from_env_lang()

    id_telegram = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER
    text = message.text.strip()

    number = get_callback_data(text, language["AVAILABILITY_TIME_BUTTONS"])
    loger.info(f"Se ha configurado la disponibilidad para el horario {number}")

    if number is None:
        bot.reply_to(message, 'No se pudo configurar la disponibilidad')

    api_conection.set_availability(number, id_telegram)
    bot.reply_to(message, 'Se ha configurado el horario correctamente')

    markup = ReplyKeyboardMarkup(row_width=2)
    for button in language["AVAILABILITY_DAY_BUTTONS"]:
        markup.add(KeyboardButton(button["text"]))

    msg = bot.send_message(message.chat.id, language["AVAILABLE_DAYS_MESSAGE"], reply_markup=markup)

    bot.register_next_step_handler(msg, process_day_step, bot)
    loger.info("Se ha configurado el horario correctamente")


def process_day_step(message: Message, bot: TeleBot):
    api_conection = get_from_env_api()
    language = get_from_env_lang()

    id_telegram = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER
    text = message.text.strip()

    number = get_callback_data(text, language["AVAILABILITY_DAY_BUTTONS"])
    loger.info(f"Se ha configurado la disponibilidad para el dia {number}")

    if number is None:
        bot.reply_to(message, 'No se pudo configurar la disponibilidad')

    api_conection.set_available_day(number, id_telegram)
    bot.reply_to(message, 'Se ha configurado el dia correctamente')


    bot.send_message(
        message.chat.id,
        "Ya tenes todo listo! Deseas ver los matches que tenes emparejados para vos? Utiliza el comando /ver_emparejamientos",
       )

    loger.info("Se ha configurado el dia correctamente")