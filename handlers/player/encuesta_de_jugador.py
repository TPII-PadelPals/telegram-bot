from telebot.types import Message

from model.telegram_bot import TelegramBot
from utils.get_from_env import get_from_env_api

INFO_FOR_SET_SURVEY_TO_PLAYER = 3
POSITION_RATING = 2
POSITION_OTHER_PLAYER = 1
DEFAULT_PLAYER = 'francoMartinDiMaria'
ANSWER_TO_QUESTION_RATING = ["1", "2", "3", "4", "5"]
MAX_RATING = 5
MIN_RATING = 1

def handle_survey_to_player(message: Message, bot: TelegramBot, get_api=get_from_env_api):
    text = message.text
    api_conection = get_api()
    language_manager = bot.language_manager

    # mensaje vacio retorna ayuda
    if text.strip() == "/encuesta_jugador":
        bot.reply_to(message, language_manager.get("MESSAGE_HELP_SURVEY_PLAYER"))
        return
    info = text.split(" ")
    n_info = len(info)
    if n_info == INFO_FOR_SET_SURVEY_TO_PLAYER:
        str_rating = info[POSITION_RATING]
        if not str_rating.isdigit():
            bot.reply_to(message, language_manager.get("MESSAGE_INVALID_VALUE"))
            return
        rating = int(str_rating)
        if rating < MIN_RATING or rating > MAX_RATING:
            bot.reply_to(message, language_manager.get("RATING_ERROR"))
            return
        other_player = info[POSITION_OTHER_PLAYER]
        id_telegram = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER
        respond = api_conection.put_survey_to_player(id_telegram, other_player, rating)
        if respond["result"]:
            message_to_user = language_manager.get("ANSWER_SURVEY_PLAYER") + str(respond["message"])
            bot.reply_to(message, message_to_user)
    else:
        bot.reply_to(message, language_manager.get("MESSAGE_HELP_SURVEY_PLAYER"))
    return
