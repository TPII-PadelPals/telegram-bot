from model.telegram_bot import TelegramBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

import logging

logging.basicConfig(level=logging.INFO)
loger = logging.getLogger(__name__)


def handle_configure_ui_buttons(message: Message, bot: TelegramBot):

    main_menu = bot.ui.create_reply_keyboard([
        ["🍽️ Today's Menu", "📝 Place Order"],
        ["⭐ Special Offers", "📞 Contact Us"]
    ], resize_keyboard=True)

    msg = bot.reply_to(message, "Welcome to our Restaurant Bot! How can I help you today?", reply_markup=main_menu)
    bot.register_next_step_handler(msg, process_step_2, bot)
    loger.info("Se ha configurado ui_buttons")


def process_step_2(message: Message, bot: TelegramBot):

    disponible = message.text == "🍽️ Today's Menu"

    if not disponible:
        bot.reply_to(message, "Opción no disponible")
        return

    categories = bot.ui.create_reply_keyboard([
        ["🥗 Starters", "🍛 Main Course"],
        ["🍰 Desserts", "🥤 Drinks"],
        ["⬅️ Back to Main Menu"]
    ])

    msg = bot.send_message(message.chat.id, "Please select a category:", reply_markup=categories)

    bot.register_next_step_handler(msg, process_step3, bot)
    loger.info("Se ha configurado el process_step_2")


def process_step3(message: Message, bot: TelegramBot):

    bot.send_message(
        message.chat.id,
        "Selected!",
       )

    loger.info("Se ha configurado el dia correctamente")