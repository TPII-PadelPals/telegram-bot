from handlers.player.matchups.utils import MatchupAction, ReserveStatus
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.users_service import UsersService
from services.matches_service import MatchesService


def handle_reply_one_matchup_callback(call: CallbackQuery, bot: TelegramBot):
    users_service = UsersService()
    matches_service = MatchesService()

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
    player_reserve_status = ReserveStatus.OUTSIDE
    if matchup_action == MatchupAction.CONFIRM:
        player_reserve_status = ReserveStatus.INSIDE

    if (not match_public_id) or (not player_reserve_status):
        bot.reply_to(call.message, bot.language_manager.get(
            "ERROR_SET_MATCH_PLAYER_STATUS"))
        return

    response = matches_service.update_match_player_status(
        user_public_id=user.public_id, match_public_id=match_public_id, status=player_reserve_status)

    if response:
        text = bot.language_manager.get("MESSAGE_MATCH_PLAYER_REJECT")
        payment_keyboard = None
        if player_reserve_status == 'inside':
            pay_url = response["pay_url"]
            text = bot.language_manager.get(
                "MESSAGE_MATCH_PLAYER_CONFIRMATION")
            buttons = [
                {'text': '👉 Ir a MercadoPago', 'url': pay_url},
            ]
            payment_keyboard = bot.ui.create_inline_keyboard(
                buttons=buttons, row_width=1)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=payment_keyboard
        )
    else:
        bot.reply_to(call.message, bot.language_manager.get(
            "ERROR_SET_MATCH_PLAYER_STATUS"))
