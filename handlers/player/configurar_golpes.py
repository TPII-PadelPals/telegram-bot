from model.telegram_bot import TelegramBot
from telebot.types import Message

from utils.get_from_env import get_from_env_api


# ["configurar_golpes", lista de golpes, habilidad]
EXPECTED_INFORMATION = 3
SEPARATOR_OF_STROKES = ','
POSITION_OF_HABILITY = 2
POSITION_OF_STROKES = 1
MAX_VALUE_FOR_STROKE = 16
DEFINITION_OF_HABILITY = ["beginner", "intermediate", "advanced"]
DEFINITION_OF_STROKE = {
    "serve": "",
    "forehand_ground": "",
    "background_ground": "",
    "forehand_back_wall": "",
    "backhand_back_wall": "",
    "forehand_side_wall": "",
    "backhand_side_wall": "",
    "forehand_double_walls": "",
    "backhand_double_walls": "",
    "forehand_counter_wall": "",
    "backhand_counter_wall": "",
    "forehand_volley": "",
    "backhand_volley": "",
    "lob": "",
    "smash": "",
    "bandeja": ""
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

def handle_configure_strokes(message: Message, bot: TelegramBot, get_api=get_from_env_api):
    text = message.text
    api_conection = get_api()
    language_manager = bot.language_manager

    info_list = text.split()
    # mensaje vacio retorna ayuda
    if text.strip() == "/configurar_golpes" or len(info_list) != EXPECTED_INFORMATION:
        bot.reply_to(message, language_manager.get("MESSAGE_HELP_STROKE"))
        return
    hability = info_list[POSITION_OF_HABILITY].lower()
    # caso de error en habilidad
    if not hability in language_manager.get("STROKE_HABILITY"):
        bot.reply_to(message, language_manager.get("MESSAGE_INCORRECT_HABILITY"))
        return
    # obtengo el listado de golpes a configurar
    if info_list[POSITION_OF_STROKES].lower() == language_manager.get("ALL").lower():
        strokes_list = list(range(1, MAX_VALUE_FOR_STROKE + 1))
    else:
        strokes_list_str = info_list[POSITION_OF_STROKES].split(SEPARATOR_OF_STROKES)
        try:
            strokes_list = []
            for number_of_stroke_str in strokes_list_str:
                number_of_stroke = int(number_of_stroke_str)
                if number_of_stroke == 0 or number_of_stroke > MAX_VALUE_FOR_STROKE:
                    continue
                strokes_list.append(number_of_stroke)
            # strokes_list = [int(number_of_stroke) for number_of_stroke in strokes_list_str]
        # caso donde un valor no sea numerico
        except ValueError:
            bot.reply_to(message, language_manager.get("MESSAGE_INVALID_VALUE"))
            return
    # creo el mensaje para la api y el de respuesta para el usuario
    id_telegram = message.from_user.username
    response_to_user = language_manager.get("MESSAGE_STROKES_UPDATED")
    response_to_user += hability
    response_to_user += "\n"
    number_for_stroke_to_response = language_manager.get("NUMBER_FOR_STROKE")
    strokes_body = DEFINITION_OF_STROKE
    position_of_definition_hability = language_manager.get("SENDER_POSITION_STROKE_HABILITY")
    for number_of_stroke in strokes_list:
        strokes_body[NUMBER_FOR_STROKE[number_of_stroke]] = DEFINITION_OF_HABILITY[position_of_definition_hability[hability]]
        # agrego el golpe a la respuesta del usuario
        response_to_user += number_for_stroke_to_response[str(number_of_stroke)]
        response_to_user += "\n"
    # envio el mensaje a la api
    _result = api_conection.put_strokes(id_telegram, strokes_body)
    bot.reply_to(message, response_to_user)
