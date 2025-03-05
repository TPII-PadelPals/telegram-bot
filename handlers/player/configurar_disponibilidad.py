from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery

from utils.get_from_env import get_from_env_api

DEFAULT_PLAYER = 'francoMartinDiMaria'

AVAILABILITY_CONFIGURATION_COMMAND = "configurar_disponibilidad"

CALLBACK_STRING_SEPARATOR = ':'
TIME = 'time'
DAY = 'day'

def filter_fn(call: CallbackQuery):
    return call.data.startswith(AVAILABILITY_CONFIGURATION_COMMAND)

def generate_callback_string(data: str):
    return f"{AVAILABILITY_CONFIGURATION_COMMAND}{CALLBACK_STRING_SEPARATOR}{data}"

def availability_callback(call: CallbackQuery, bot: TelegramBot):
    type = call.data.split(CALLBACK_STRING_SEPARATOR)[1]
    if type == TIME:
        process_time_step(call, bot)
    elif type == DAY:
        process_day_step(call, bot)
    else:
        bot.send_message(
            call.message.chat.id,
            "Se ha producido un error",
        )    

def handle_configure_availability(message: Message, bot: TelegramBot):
    buttons = [{'text': x["text"], 'callback_data': generate_callback_string(f"{TIME}{CALLBACK_STRING_SEPARATOR}{x['callback_data']}")} for x in bot.language_manager.get("AVAILABILITY_TIME_BUTTONS")]
    menu = bot.ui.create_inline_keyboard(buttons, row_width=2)
    bot.send_message(message.chat.id, bot.language_manager.get("AVAILABLE_TIME_MESSAGE"), reply_markup=menu)


def process_time_step(call: CallbackQuery, bot: TelegramBot):
    api_conection = get_from_env_api()

    callback_data = call.data
    telegram_id = call.message.chat.username if call.message.chat.username else DEFAULT_PLAYER
    time_id = int(callback_data.split(CALLBACK_STRING_SEPARATOR)[-1])

    if time_id is None:
        bot.reply_to(call.message, 'No se pudo configurar la disponibilidad')
        return

    api_conection.set_availability(time_id, telegram_id)

    buttons = [{'text': x["text"], 'callback_data': generate_callback_string(f"{DAY}{CALLBACK_STRING_SEPARATOR}{x['callback_data']}")} for x in bot.language_manager.get("AVAILABILITY_DAY_BUTTONS")]
    menu = bot.ui.create_inline_keyboard(buttons, row_width=2)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=bot.language_manager.get("AVAILABLE_DAYS_MESSAGE"), reply_markup=menu)


def process_day_step(call: CallbackQuery, bot: TelegramBot):
    api_conection = get_from_env_api()

    callback_data = call.data
    telegram_id = call.message.chat.username if call.message.chat.username else DEFAULT_PLAYER
    day_id = int(callback_data.split(CALLBACK_STRING_SEPARATOR)[-1])

    if day_id is None:
        bot.reply_to(call.message, 'No se pudo configurar la disponibilidad')

    api_conection.set_available_day(day_id, telegram_id)


    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Ya tenes todo listo! Deseas ver los matches que tenes emparejados para vos? Utiliza el comando /ver_emparejamientos")
