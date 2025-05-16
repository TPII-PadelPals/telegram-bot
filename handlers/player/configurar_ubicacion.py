from model.telegram_bot import TelegramBot
from telebot.types import Message, ReplyKeyboardMarkup
from services.players_service import PlayersService
from services.users_service import UsersService
from uuid import UUID

players_service = PlayersService()
users_service = UsersService()


def handle_address_configuration(message: Message, bot: TelegramBot):
    chat_id = message.chat.id
    users = users_service.get_user_info(chat_id)
    user = users[0]
    # user_public_id = users["data"][0]["public_id"]

    msg = bot.send_message(
        chat_id, "Por favor, ingrese la ubicación donde desea jugar:")
    bot.register_next_step_handler(
        msg, process_address_step, bot, user.public_id)


def process_address_step(message: Message, bot: TelegramBot, user_public_id: UUID):
    chat_id = message.chat.id
    address = message.text
    player_partial_data = {
        "address": address,
    }

    response = players_service.update_partial_player(
        user_public_id, player_partial_data)
    if response:
        bot.send_message(
            chat_id, "¡Ubicación guardada con éxito! ¿Cuántos kilómetros está dispuesto a caminar hasta una cancha de pádel?")
        markup = ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('<5', '<10', '<15', '<20', '<25', '<30')
        msg = bot.send_message(chat_id, "Elija un radio:", reply_markup=markup)
        bot.register_next_step_handler(
            msg, process_radius_step, bot, user_public_id)
    else:
        bot.send_message(
            chat_id, "No se pudo guardar la ubicación. Por favor, inténtelo de nuevo.")


def process_radius_step(message: Message, bot: TelegramBot, user_public_id: str):
    chat_id = message.chat.id
    radius = message.text
    parsed_radius = int(radius.replace("<", ""))
    player_partial_data = {
        "search_range_km": parsed_radius,
    }

    response = players_service.update_partial_player(
        user_public_id, player_partial_data)
    if response:
        bot.send_message(chat_id, f"¡Radio de {radius} km guardado con éxito!")
    else:
        bot.send_message(
            chat_id, "No se pudo guardar el radio. Por favor, inténtelo de nuevo.")
