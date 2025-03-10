from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery
from services.player_service import PlayerService
from services.users_service import UsersService

SKILL_LEVELS = [1.0, 2.0, 3.0]
STROKES_CONFIGURATION_COMMAND = "configurar_golpes"


def filter_fn(call: CallbackQuery):
    return call.data.startswith(STROKES_CONFIGURATION_COMMAND)


def generate_callback_string(data: str):
    return f"{STROKES_CONFIGURATION_COMMAND}:{data}"


def callback_handler_fn(call: CallbackQuery, bot: TelegramBot):
    handlers = {
        "stroke": strokes_callback,
        "skill": skill_level_callback,
        "strokes_list": show_strokes_list_callback,
    }
    handler_key = call.data.split(":")[1]
    handler = handlers.get(handler_key)
    handler(call, bot)


def generate_strokes_markup(bot: TelegramBot):
    language_manager = bot.language_manager

    buttons = []
    strokes_names = language_manager.get("STROKES_NAMES")
    for key, value in strokes_names.items():
        buttons.append(
            {
                "text": value,
                "callback_data": generate_callback_string(f"stroke:{key}"),
            }
        )

    buttons.append(
        {
            "text": language_manager.get("ALL_STROKES"),
            "callback_data": generate_callback_string("stroke:all"),
        }
    )

    markup = bot.ui.create_inline_keyboard(buttons, row_width=2)
    return markup


def handle_configure_strokes(message: Message, bot: TelegramBot):
    """Show the list of strokes using inline buttons"""
    markup = generate_strokes_markup(bot)

    bot.send_message(
        message.chat.id,
        bot.language_manager.get("SELECT_STROKE_MESSAGE"),
        reply_markup=markup,
    )


def strokes_callback(call: CallbackQuery, bot: TelegramBot):
    """Handle the stroke selection and show skill level options"""
    language_manager = bot.language_manager

    stroke_data = call.data
    stroke_key = stroke_data.split(":")[-1]

    skill_buttons = [
        {
            "text": language_manager.get("BEGINNER"),
            "callback_data": generate_callback_string(
                f"skill:{stroke_key}:0"
            ),  # 0 = principiante
        },
        {
            "text": language_manager.get("INTERMEDIATE"),
            "callback_data": generate_callback_string(
                f"skill:{stroke_key}:1"
            ),  # 1 = intermedio
        },
        {
            "text": language_manager.get("ADVANCED"),
            "callback_data": generate_callback_string(
                f"skill:{stroke_key}:2"
            ),  # 2 = avanzado
        },
        {
            "text": language_manager.get("BACK"),
            "callback_data": generate_callback_string(f"strokes_list"),
        },
    ]

    markup = bot.ui.create_inline_keyboard(skill_buttons, row_width=2)
    strokes_names = language_manager.get("STROKES_NAMES")

    if stroke_key == "all":
        stroke_name = language_manager.get("ALL_STROKES")
    else:
        stroke_name = strokes_names.get(stroke_key)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=language_manager.get("SELECT_SKILL_LEVEL_FOR").format(stroke=stroke_name),
        reply_markup=markup,
    )


def skill_level_callback(
    call: CallbackQuery,
    bot: TelegramBot,
    get_api=PlayerService,
    user_service=UsersService,
):
    """Handle the skill level selection and update the player's stroke skill"""
    language_manager = bot.language_manager

    parts = call.data.split(":")
    stroke_key = parts[2]
    level_idx = int(parts[3])

    telegram_id = call.from_user.id
    user_id = get_user_public_id(telegram_id, user_service)

    if user_id is None:
        bot.answer_callback_query(call.id, language_manager.get("ERROR_RECEIVE_DATA"))
        return

    api_connection = get_api()
    strokes_names = language_manager.get("STROKES_NAMES")

    strokes_body = {}
    if stroke_key == "all":
        for key, _ in strokes_names.items():
            strokes_body[key] = SKILL_LEVELS[level_idx]
    else:
        strokes_body[stroke_key] = SKILL_LEVELS[level_idx]

    result = api_connection.update_strokes(user_id, strokes_body)

    if result.get("user_public_id") != str(user_id):
        bot.answer_callback_query(call.id, language_manager.get("ERROR_RECEIVE_DATA"))
        return

    bot.answer_callback_query(call.id, language_manager.get("STROKE_UPDATED_SUCCESS"))

    show_strokes_list_callback(call, bot)


def show_strokes_list_callback(call: CallbackQuery, bot: TelegramBot):
    markup = generate_strokes_markup(bot)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=bot.language_manager.get("SELECT_STROKE_MESSAGE"),
        reply_markup=markup,
    )


def get_user_public_id(telegram_id, user_service):
    service = user_service()
    data = service.get_user_info(telegram_id)
    return data.get("data")[0].get("public_id") if data.get("data") else None
