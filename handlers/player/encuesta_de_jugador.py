from telebot.types import Message

from model.telegram_bot import TelegramBot
from model.validation import ValidateSurveyPlayer
from utils.get_from_env import get_from_env_api

POSITION_RATING = 2
POSITION_OTHER_PLAYER = 1
DEFAULT_PLAYER = 'francoMartinDiMaria'

def handle_survey_to_player(message: Message, bot: TelegramBot, get_api=get_from_env_api):
    text = message.text
    api_conection = get_api()
    language_manager = bot.language_manager
    # mensaje vacio retorna ayuda
    if text.strip() == "/encuesta_jugador":
        bot.reply_to(message, language_manager.get("MESSAGE_HELP_SURVEY_PLAYER"))
        return
    info = text.split(" ")
    # validation
    validation = ValidateSurveyPlayer(info)
    is_valid, respond = validation.validate(language_manager)
    if not is_valid:
        bot.reply_to(message, respond)
        return
    # info is valid
    str_rating = info[POSITION_RATING]
    rating = int(str_rating)
    other_player = info[POSITION_OTHER_PLAYER]
    id_telegram = message.from_user.username if message.from_user.username is not None else DEFAULT_PLAYER
    respond = api_conection.put_survey_to_player(id_telegram, other_player, rating)
    if respond["result"]:
        message_to_user = language_manager.get("ANSWER_SURVEY_PLAYER") + str(respond["message"])
        bot.reply_to(message, message_to_user)
    return
