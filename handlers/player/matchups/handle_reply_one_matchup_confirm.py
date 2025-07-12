from uuid import UUID
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery
from services.payments_service import PaymentsService


def handle_reply_one_matchup_confirm(call: CallbackQuery, bot: TelegramBot, user_public_id: UUID, match_public_id: UUID):
    payments_service = PaymentsService()

    response = payments_service.create_payment(user_public_id, match_public_id)
    if response:
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

    return response
