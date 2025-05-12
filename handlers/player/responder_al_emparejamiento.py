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
        response.get("data")[0].get(
            "public_id") if response.get("data") else None
    )

    if not user_public_id:
        bot.send_message(chat_id, bot.language_manager.get(
            "ERROR_USER_NOT_FOUND"))
        return

    params = call.data.split(':')
    match_public_id = params.pop()
    player_reserve_status = params.pop()

    if (not match_public_id) or (not player_reserve_status):
        bot.reply_to(call.message, bot.language_manager.get(
            "ERROR_SET_MATCH_PLAYER_STATUS"))
        return

    response = matches_service.update_match_player_status(
        user_public_id=user_public_id, match_public_id=match_public_id, status=player_reserve_status)

    if response:
        text = bot.language_manager.get("MESSAGE_MATCH_PLAYER_REJECT")
        if player_reserve_status == 'inside':
            pay_url = response["pay_url"]
            text = bot.language_manager.get(
                "MESSAGE_MATCH_PLAYER_CONFIRMATION")
            text = text.format(pay_url)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
        )
    else:
        bot.reply_to(call.message, bot.language_manager.get(
            "ERROR_SET_MATCH_PLAYER_STATUS"))
