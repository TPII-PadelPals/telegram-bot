from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.users_service import UsersService
from services.matches_service import MatchesService

def handle_player_response_match_callback(call: CallbackQuery, bot: TelegramBot):
    users_service = UsersService()
    matches_service = MatchesService()

    chat_id = call.from_user.id
    response = users_service.get_user_info(chat_id)
    user_public_id = (
        response.get("data")[0].get("public_id") if response.get("data") else None
    )

    if not user_public_id:
        bot.send_message(chat_id, bot.language_manager.get("ERROR_USER_NOT_FOUND"))
        return
    
    params = call.data.split(':')
    match_public_id = params.pop()
    player_reserve_status = params.pop()

    if (not match_public_id) or (not player_reserve_status):
        bot.reply_to(call.message, bot.language_manager.get("ERROR_SET_MATCH_PLAYER_STATUS"))
        return
    
    response = matches_service.update_match_player_status(user_public_id=user_public_id, match_public_id=match_public_id, status=player_reserve_status)

    if response:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=bot.language_manager.get("MESSAGE_MATCH_PLAYER_CONFIRMATION"),
        )
    else:
        bot.reply_to(call.message, bot.language_manager.get("ERROR_SET_MATCH_PLAYER_STATUS"))



# AMOUNT_OF_INFORMATION_EXPECTED = 3 # otro jugador + cancha + hora
# TEMPLATE_INFO = {
#     "player_id_1": "",
#     "player_id_2": "",
#     "paddle_court_name": "",
#     "time_availability": "",
# }
# POSITION_OF_OPONENT = 1
# POSITION_OF_COURT = 2
# POSITION_OF_TIME = 3

# def handle_respond_to_matchmaking_accept(message: Message, bot: TelegramBot, get_api=get_from_env_api):
#     return _respond_to_matchmaking(message, bot, True, get_api)

# def handle_respond_to_matchmaking_reject(message: Message, bot: TelegramBot, get_api=get_from_env_api):
#     return _respond_to_matchmaking(message, bot, False, get_api)

# def _respond_to_matchmaking(message: Message, bot: TelegramBot, accept: bool, get_api=get_from_env_api):
#     text = message.text
#     api_conection = get_api()

#     info_list = text.split()
#     len_info = len(info_list)
#     # mensaje vacio retorna ayuda
#     if len_info != AMOUNT_OF_INFORMATION_EXPECTED + 1: # la informacion esperada 3 + el comando de ejecucion
#         bot.reply_to(message, bot.language_manager.get("MESSAGE_RESPOND_TO_MATCHMAKING_HELP"))
#         return
#     id_telegram = message.from_user.username
#     info = TEMPLATE_INFO
#     player_id_1, player_id_2 = sorted((id_telegram, info_list[POSITION_OF_OPONENT]))
#     info["player_id_1"] = player_id_1
#     info["player_id_2"] = player_id_2
#     info["paddle_court_name"] = info_list[POSITION_OF_COURT]
#     info["time_availability"] = info_list[POSITION_OF_TIME]
#     result = api_conection.respond_to_matchmaking(id_telegram, info, accept)
#     response_to_user = bot.language_manager.get("MESSAGE_RESPOND_TO_MATCHMAKING") + result
#     bot.reply_to(message, response_to_user)
#     return