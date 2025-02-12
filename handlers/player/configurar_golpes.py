import copy

from model.language_manager import LanguageManager
from model.telegram_bot import TelegramBot
from telebot.types import Message
from model.validation import ValidateConfigStrokes
from services.player_service import PlayerService
from services.users_service import UsersService


# ["configurar_golpes", lista de golpes, habilidad]
SEPARATOR_OF_STROKES = ','
POSITION_OF_HABILITY = 2
POSITION_OF_STROKES = 1
MAX_VALUE_FOR_STROKE = 16
DEFINITION_OF_HABILITY = [1.0, 2.0, 3.0]
DEFINITION_OF_STROKE = {
    "serve": None,
    "forehand_ground": None,
    "background_ground": None,
    "forehand_back_wall": None,
    "backhand_back_wall": None,
    "forehand_side_wall": None,
    "backhand_side_wall": None,
    "forehand_double_walls": None,
    "backhand_double_walls": None,
    "forehand_counter_wall": None,
    "backhand_counter_wall": None,
    "forehand_volley": None,
    "backhand_volley": None,
    "lob": None,
    "smash": None,
    "bandeja": None
}
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
    16: "bandeja"
}

# TODO traducir NUMBER_FOR_STROKE y MESSAGE_HELP_STROKE del json

def handle_configure_strokes(message: Message, bot: TelegramBot, get_api=PlayerService):
    text = message.text
    api_conection = get_api()
    language_manager = bot.language_manager

    info_list = text.split()
    # validation
    validation = ValidateConfigStrokes(info_list)
    is_valid, respond = validation.validate(language_manager)
    if not is_valid:
        bot.reply_to(message, respond)
        return

    hability = info_list[POSITION_OF_HABILITY].lower()
    id_telegram = message.from_user.id
    user_id = _get_user_public_id(id_telegram)
    if user_id is None:
        bot.reply_to(message, language_manager.get("ERROR_RECIVE_DATA"))
        return
    # obtengo el listado de golpes a configurar
    strokes_list = _generate_stroke_list(info_list[POSITION_OF_STROKES], language_manager)
    strokes_body = copy.copy(DEFINITION_OF_STROKE)
    position_of_definition_hability = language_manager.get("SENDER_POSITION_STROKE_HABILITY")
    for number_of_stroke in strokes_list:
        strokes_body[NUMBER_FOR_STROKE[number_of_stroke]] = DEFINITION_OF_HABILITY[position_of_definition_hability[hability]]
    # envio el mensaje a la api
    result = api_conection.update_strokes(user_id, strokes_body)
    if result.status_code != 200:
        bot.reply_to(message, language_manager.get("ERROR_RECIVE_DATA"))
        return

    response_to_user = _generate_message(strokes_list, hability, language_manager)
    bot.reply_to(message, response_to_user)

def _generate_stroke_list(strokes_str: str, language_manager: LanguageManager) -> list[int]:
    if strokes_str.lower() == language_manager.get("ALL").lower():
        strokes_list = list(range(1, MAX_VALUE_FOR_STROKE + 1))
    else:
        strokes_list_str = strokes_str.split(SEPARATOR_OF_STROKES)
        strokes_list = []
        for number_of_stroke_str in strokes_list_str:
            number_of_stroke = int(number_of_stroke_str)
            if number_of_stroke == 0 or number_of_stroke > MAX_VALUE_FOR_STROKE:
                continue
            strokes_list.append(number_of_stroke)
    return strokes_list


def _get_user_public_id(id_telegram):
    service = UsersService()
    data = service.get_user_info(id_telegram)
    return data.get("public_id")


def _generate_message(strokes_list: list[int], hability: str, language_manager: LanguageManager) -> str:
    response_to_user = language_manager.get("MESSAGE_STROKES_UPDATED")
    response_to_user += hability
    response_to_user += "\n"
    number_for_stroke_to_response = language_manager.get("NUMBER_FOR_STROKE")
    for number_of_stroke in strokes_list:
        # agrego el golpe a la respuesta del usuario
        response_to_user += number_for_stroke_to_response[str(number_of_stroke)]
        response_to_user += "\n"
    return response_to_user