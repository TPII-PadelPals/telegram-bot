from model.telegram_bot import TelegramBot
from telebot.types import Message

from utils.get_from_env import get_from_env_api, get_from_env_lang

AMOUNT_OF_INFORMATION_EXPECTED = 3 # otro jugador + cancha + hora
TEMPLATE_INFO = {
    "player_id_1": "",
    "player_id_2": "",
    "paddle_court_name": "",
    "time_availability": "",
}
POSITION_OF_OPONENT = 1
POSITION_OF_COURT = 2
POSITION_OF_TIME = 3

def handle_respond_to_matchmaking_accept(message: Message, bot: TelegramBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    return _respond_to_matchmaking(message, bot, True, get_api, get_len)

def handle_respond_to_matchmaking_reject(message: Message, bot: TelegramBot, get_api=get_from_env_api, get_len=get_from_env_lang):
    return _respond_to_matchmaking(message, bot, False, get_api, get_len)

def _respond_to_matchmaking(message: Message, bot: TelegramBot, accept: bool, get_api=get_from_env_api, get_len=get_from_env_lang):
    text = message.text
    api_conection = get_api()
    language = get_len()

    info_list = text.split()
    len_info = len(info_list)
    # mensaje vacio retorna ayuda
    if len_info != AMOUNT_OF_INFORMATION_EXPECTED + 1: # la informacion esperada 3 + el comando de ejecucion
        bot.reply_to(message, language["MESSAGE_RESPOND_TO_MATCHMAKING_HELP"])
        return
    id_telegram = message.from_user.username
    info = TEMPLATE_INFO
    player_id_1, player_id_2 = sorted((id_telegram, info_list[POSITION_OF_OPONENT]))
    info["player_id_1"] = player_id_1
    info["player_id_2"] = player_id_2
    info["paddle_court_name"] = info_list[POSITION_OF_COURT]
    info["time_availability"] = info_list[POSITION_OF_TIME]
    result = api_conection.respond_to_matchmaking(id_telegram, info, accept)
    response_to_user = language["MESSAGE_RESPOND_TO_MATCHMAKING"] + result
    bot.reply_to(message, response_to_user)
    return