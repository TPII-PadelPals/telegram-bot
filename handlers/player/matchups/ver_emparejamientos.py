
from handlers.player.matchups.handle_display_all_matchups import display_all_matchups, handle_display_all_matchups_callback
from handlers.player.matchups.handle_display_all_pay_methods import handle_display_all_pay_methods_callback
from handlers.player.matchups.handle_display_one_matchup import handle_display_one_matchup_callback
from handlers.player.matchups.handle_reply_one_matchup import handle_reply_one_matchup_callback
from handlers.player.matchups.utils import VIEW_PADDLE_MATCHUPS_COMMAND, MatchupAction, generate_callback_string
from model.telegram_bot import TelegramBot
from telebot.types import Message, CallbackQuery


def filter_fn(call: CallbackQuery):
    return call.data.startswith(VIEW_PADDLE_MATCHUPS_COMMAND)


def handle_matchups(message: Message, bot: TelegramBot):
    display_all_matchups(bot, message.chat.id)  # message.message_id


# Switch callbacks
def matchups_callback(call: CallbackQuery, bot: TelegramBot):
    data = call.data

    if data == generate_callback_string(MatchupAction.ALL):
        handle_display_all_matchups_callback(call, bot)

    elif data.startswith(generate_callback_string(MatchupAction.ONE)):
        handle_display_one_matchup_callback(call, bot)

    elif data.startswith(generate_callback_string(MatchupAction.PAY)):
        handle_display_all_pay_methods_callback(call, bot)

    elif (data.startswith(generate_callback_string(MatchupAction.CONFIRM)) or
          data.startswith(generate_callback_string(MatchupAction.REJECT))):
        handle_reply_one_matchup_callback(call, bot)

    else:
        raise ValueError("Callback not implemented")
