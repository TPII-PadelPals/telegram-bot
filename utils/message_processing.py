from model.language_manager import LanguageManager
from utils.message_request import MessageRequest


class MessageProcessing:
    SEPARATOR_FOR_MESSAGE = ";"
    SEPARATOR_FOR_ORDER_IN_MESSAGE = "#"
    SEPARATOR_FOR_NAMES = ", "

    ORDER_SURVEY_PLAYER = "survey_player"

    def message_processing(self, language: LanguageManager, request: MessageRequest):
        split_message = request.message.split(self.SEPARATOR_FOR_ORDER_IN_MESSAGE)
        match split_message[0]:
            case self.ORDER_SURVEY_PLAYER:
                list_of_players = split_message[1].split(self.SEPARATOR_FOR_MESSAGE)
                message = language.get("MESSAGE_SURVEY_PLAYER_ALLOWED")
                message += self.SEPARATOR_FOR_NAMES.join(list_of_players)
            case _:
                message = request.message
        result = {"chat_id": request.chat_id, "message": message}
        return result