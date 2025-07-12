from handlers.player.matchups.handle_reply_one_matchup_confirm import handle_reply_one_matchup_confirm
from handlers.player.matchups.handle_reply_one_matchup_reject import handle_reply_one_matchup_reject
from handlers.player.matchups.utils import MatchupAction
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.users_service import UsersService


def handle_reply_one_matchup_callback(call: CallbackQuery, bot: TelegramBot):
    users_service = UsersService()

    chat_id = call.from_user.id
    users = users_service.get_user_info(chat_id)

    if not users:
        bot.send_message(chat_id, bot.language_manager.get(
            "ERROR_USER_NOT_FOUND"))
        return
    user = users[0]

    params = call.data.split(':')
    match_public_id = params.pop()
    matchup_action = params.pop()

    response = None
    if matchup_action == MatchupAction.REJECT:
        response = handle_reply_one_matchup_reject(
            call, bot, user.public_id, match_public_id)
    elif matchup_action == MatchupAction.CONFIRM:
        response = handle_reply_one_matchup_confirm(
            call, bot, user.public_id, match_public_id)

    if (not match_public_id) or (not response):
        bot.reply_to(call.message, bot.language_manager.get(
            "ERROR_SET_MATCH_PLAYER_STATUS"))
        return
