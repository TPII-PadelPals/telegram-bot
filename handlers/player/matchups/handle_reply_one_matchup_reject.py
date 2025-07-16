from uuid import UUID
from handlers.player.matchups.utils import ReserveStatus
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.matches_service import MatchesService


def handle_reply_one_matchup_reject(call: CallbackQuery, bot: TelegramBot, user_public_id: UUID, match_public_id: UUID):
    matches_service = MatchesService()

    response = matches_service.update_match_player_status(
        user_public_id=user_public_id, match_public_id=match_public_id, status=ReserveStatus.OUTSIDE)
    if response:
        text = bot.language_manager.get("MESSAGE_MATCH_PLAYER_REJECT")
        payment_keyboard = None
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=payment_keyboard
        )

    return response
