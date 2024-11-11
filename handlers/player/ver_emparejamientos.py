from telebot import TeleBot
from telebot.types import Message

from utils.get_from_env import get_from_env_lang, get_from_env_api

def handle_see_matches(message: Message, bot: TeleBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    api_conection = get_api()
    language = get_len()
    #text = message.text
    # obtengo los matches
    id_telegram = message.from_user.username
    matches = api_conection.get_matches(id_telegram)
    # caso sin emparejamiento
    if len(matches) == 0:
        text_response = language["MESSAGE_SEE_MATCHES_EMPTY"]
        bot.reply_to(message, text_response)
        return
    text_response = language["MESSAGE_SEE_MATCHES"]
    for match in matches:
        other_player = match["player_id_1"]
        if other_player == id_telegram:
            other_player = match["player_id_2"]
        text_response += (other_player + language["SEE_MATCHES_SEPARATOR"] + str(match["paddle_court_id"])
                          + language["SEE_MATCHES_SEPARATOR"] + str(match["time_availability"])) + "\n"

    bot.reply_to(message, text_response)