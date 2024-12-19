from telebot import TeleBot
from telebot.types import Message

def handle_survey_test(message: Message, bot: TeleBot):
    # print(message)
    # Pregunta de la encuesta
    question = "¿Cuál es tu lenguaje de programación favorito?"

    # Opciones de respuesta
    options = ["Python", "JavaScript", "C++", "Otros"]

    # Enviar encuesta al chat
    bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        allows_multiple_answers=True,
        is_anonymous=False  # Encuesta no anónima
    )
    # bot.reply_to(message, str(message))