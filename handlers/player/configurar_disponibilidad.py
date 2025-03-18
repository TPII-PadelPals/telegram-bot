import uuid
from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery
from services.players_service import PlayersService
from services.users_service import UsersService


AVAILABILITY_CONFIGURATION_COMMAND = "configurar_disponibilidad"

CALLBACK_STRING_SEPARATOR = ":"
TIME = "time"
DAY = "day"
INLINE_KEYBOARD_ROW_WIDTH = 2


def filter_fn(call: CallbackQuery):
    return call.data.startswith(AVAILABILITY_CONFIGURATION_COMMAND)


def generate_callback_string(data: str):
    return f"{AVAILABILITY_CONFIGURATION_COMMAND}{CALLBACK_STRING_SEPARATOR}{data}"


def availability_callback(call: CallbackQuery, bot: TelegramBot, users_service=UsersService):
    telegram_id = call.from_user.id

    response = users_service().get_user_info(telegram_id)
    user_public_id = response.get("data")[0].get("public_id") if response.get("data") else None

    type = call.data.split(CALLBACK_STRING_SEPARATOR)[1]
    if type == TIME:
        process_time_step(call, bot, user_public_id)
    elif type == DAY:
        process_day_step(call, bot, user_public_id)
    else:
        bot.send_message(
            call.message.chat.id,
            "Se ha producido un error",
        )

def generate_markup_options(bot: TelegramBot, callback_type: str, language_manager_msg: str):
    buttons = [
        {
            "text": x["text"],
            "callback_data": generate_callback_string(
                f"{callback_type}{CALLBACK_STRING_SEPARATOR}{x['callback_data']}"
            ),
        }
        for x in bot.language_manager.get(language_manager_msg)
    ]
    return bot.ui.create_inline_keyboard(buttons, row_width=INLINE_KEYBOARD_ROW_WIDTH)


def handle_configure_availability(message: Message, bot: TelegramBot):
    time_options = generate_markup_options(bot, TIME, "AVAILABILITY_TIME_BUTTONS")
    
    bot.send_message(
        message.chat.id,
        bot.language_manager.get("AVAILABLE_TIME_MESSAGE"),
        reply_markup=time_options,
    )


def process_time_step(
        call: CallbackQuery,
        bot: TelegramBot,
        user_public_id: uuid.UUID,
        players_service=PlayersService,
    ):
    callback_data = call.data
    
    if not user_public_id:
        bot.answer_callback_query(call.id, bot.language_manager.get("ERROR_USER_NOT_FOUND"))
        return

    time_id = int(callback_data.split(CALLBACK_STRING_SEPARATOR)[-1])

    if time_id is None:
        bot.reply_to(call.message, bot.language_manager.get("ERROR_SET_AVAILABILITY"))
        return
    
    partial_player = {
        "time_availability": time_id
    }

    response = players_service().update_partial_player(user_public_id, partial_player)

    if response:
        day_options = generate_markup_options(bot, DAY, "AVAILABILITY_DAY_BUTTONS")
        bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=bot.language_manager.get("AVAILABLE_DAYS_MESSAGE"),
        reply_markup=day_options,
        )
    else:
        bot.reply_to(call.id, bot.language_manager.get("ERROR_SET_AVAILABILITY"))


def process_day_step(
        call: CallbackQuery,
        bot: TelegramBot,
        user_public_id: uuid.UUID,
        players_service=PlayersService,
    ):
    callback_data = call.data

    if not user_public_id:
        bot.answer_callback_query(call.id, bot.language_manager.get("ERROR_USER_NOT_FOUND"))
        return


    week_day = int(callback_data.split(CALLBACK_STRING_SEPARATOR)[-1])

    if not week_day:
        bot.reply_to(call.message, bot.language_manager.get("ERROR_SET_AVAILABILITY"))

    availability_days = {
        "available_days": [
            {"week_day": week_day, "is_available": True},
        ]
    }

    response = players_service().update_availability(user_public_id, availability_days)


    if response:
        bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=bot.language_manager.get("SUCCESSFUL_AVAILABILITY_CONFIGURATION"),
        )
    else:
        bot.reply_to(call.id, bot.language_manager.get("ERROR_SET_AVAILABILITY"))
