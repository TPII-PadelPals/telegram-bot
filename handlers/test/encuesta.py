from telebot import TeleBot
from telebot.types import Message

from model.player_survey.survey_generator import SurveyGenerator


AMOUNT_OF_INFORMATION_MIN = 4

def handle_survey_test(message: Message, bot: TeleBot):
    list_survey_info = message.text.split(" ")
    if len(list_survey_info) >= AMOUNT_OF_INFORMATION_MIN:
        # Pregunta de la encuesta
        question = list_survey_info[1]

        # Opciones de respuesta
        options = list_survey_info[2:]
    else:
        # Pregunta de la encuesta
        question = "¿Cuál es tu lenguaje de programación favorito?"

        # Opciones de respuesta
        options = ["Python", "JavaScript", "C++", "Otros"]
    survey = SurveyGenerator([question], [options])
    # Enviar encuesta al chat
    survey.send_survey(bot, message.chat.id, False)
