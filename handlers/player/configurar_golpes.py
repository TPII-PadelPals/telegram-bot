from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery
from services.player_service import PlayerService
from services.users_service import UsersService

# Constants
MAX_VALUE_FOR_STROKE = 16
SKILL_LEVELS = [1.0, 2.0, 3.0]
NUMBER_FOR_STROKE = {
    1: "serve",
    2: "forehand_ground",
    3: "background_ground",
    4: "forehand_back_wall",
    5: "backhand_back_wall",
    6: "forehand_side_wall",
    7: "backhand_side_wall",
    8: "forehand_double_walls",
    9: "backhand_double_walls",
    10: "forehand_counter_wall",
    11: "backhand_counter_wall",
    12: "forehand_volley",
    13: "backhand_volley",
    14: "lob",
    15: "smash",
    16: "bandeja",
}

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
    for number, stroke_name in NUMBER_FOR_STROKE.items():
        display_name = language_manager.get("NUMBER_FOR_STROKE").get(
            str(number), stroke_name
        )
        buttons.append(
            {
                "text": display_name,
                "callback_data": generate_callback_string(f"stroke:{number}"),
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
    stroke_id = stroke_data.split(":")[-1]

    skill_buttons = [
        {
            "text": language_manager.get("BEGINNER"),
            "callback_data": generate_callback_string(
                f"skill:{stroke_id}:0"
            ),  # 0 = principiante
        },
        {
            "text": language_manager.get("INTERMEDIATE"),
            "callback_data": generate_callback_string(
                f"skill:{stroke_id}:1"
            ),  # 1 = intermedio
        },
        {
            "text": language_manager.get("ADVANCED"),
            "callback_data": generate_callback_string(
                f"skill:{stroke_id}:2"
            ),  # 2 = avanzado
        },
        {
            "text": language_manager.get("BACK"),
            "callback_data": generate_callback_string(f"strokes_list"),
        },
    ]

    markup = bot.ui.create_inline_keyboard(skill_buttons, row_width=2)

    if stroke_id == "all":
        stroke_name = language_manager.get("ALL_STROKES")
    else:
        stroke_number = int(stroke_id)
        stroke_name = language_manager.get("NUMBER_FOR_STROKE").get(
            str(stroke_number), NUMBER_FOR_STROKE[stroke_number]
        )

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
    stroke_id = parts[2]
    level_idx = int(parts[3])

    telegram_id = call.from_user.id
    user_id = get_user_public_id(telegram_id, user_service)

    if user_id is None:
        bot.answer_callback_query(call.id, language_manager.get("ERROR_RECEIVE_DATA"))
        return

    api_connection = get_api()

    strokes_body = {}
    if stroke_id == "all":
        for number in range(1, MAX_VALUE_FOR_STROKE + 1):
            stroke_name = NUMBER_FOR_STROKE[number]
            strokes_body[stroke_name] = SKILL_LEVELS[level_idx]
    else:
        stroke_number = int(stroke_id)
        stroke_name = NUMBER_FOR_STROKE[stroke_number]
        strokes_body[stroke_name] = SKILL_LEVELS[level_idx]

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
