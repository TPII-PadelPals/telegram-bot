from model.telegram_bot import TelegramBot
from telebot.types import Message, ReplyKeyboardMarkup
# from services.player_service import PlayerService
from services.player_service_backend import PlayerServiceBackEnd

DEFAULT_PLAYER = 'francoMartinDiMaria'

player_service = PlayerServiceBackEnd()

def handle_configure_location(message: Message, bot: TelegramBot):
    chat_id = message.chat.id

    msg = bot.send_message(chat_id, "Por favor, ingrese la ubicación donde desea jugar:")
    bot.register_next_step_handler(msg, process_location_step, bot)

def process_location_step(message: Message, bot: TelegramBot):
    chat_id = message.chat.id
    location = message.text
    nickname = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER

    response = player_service.update_location(nickname, location)
    if response:
        bot.send_message(chat_id, "¡Ubicación guardada con éxito! ¿Cuántos kilómetros está dispuesto a caminar hasta una cancha de pádel?")
        markup = ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('<5', '<10', '<15', '<20', '<25', '<30')
        msg = bot.send_message(chat_id, "Elija un radio:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_radius_step, bot, location)
    else:
        bot.send_message(chat_id, "No se pudo guardar la ubicación. Por favor, inténtelo de nuevo.")

def process_radius_step(message: Message, bot: TelegramBot, location: str):
    chat_id = message.chat.id
    radius = message.text
    nickname = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER

    parsed_radius = int(radius.replace("<", ""))

    response = player_service.update_radius(nickname, location, parsed_radius)
    if response:
        bot.send_message(chat_id, f"¡Radio de {radius} km guardado con éxito para la ubicación {location}!")
    else:
        bot.send_message(chat_id, "No se pudo guardar el radio. Por favor, inténtelo de nuevo.")
