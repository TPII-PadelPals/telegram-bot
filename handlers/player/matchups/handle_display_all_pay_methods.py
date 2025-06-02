
from handlers.player.matchups.utils import MatchupAction, generate_callback_string
from model.telegram_bot import TelegramBot
from telebot.types import CallbackQuery


def handle_display_all_pay_methods_callback(call: CallbackQuery, bot: TelegramBot):
    match_public_id = call.data.split(":")[-1]

    text = bot.language_manager.get("MESSAGE_MATCH_PLAYER_CONFIRMATION")

    buttons = [
        {'text': '💳 Pagar con MercadoPago', 'callback_data': generate_callback_string(
            f"{MatchupAction.CONFIRM}:{match_public_id}")},
        {'text': '⬅', 'callback_data': generate_callback_string(
            f'{MatchupAction.ONE}:{match_public_id}')}
    ]
    keyboard = bot.ui.create_inline_keyboard(buttons=buttons, row_width=1)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=text,
        reply_markup=keyboard
    )
