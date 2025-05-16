import unittest
from unittest.mock import MagicMock

from utils.message_processing import MessageProcessing


class TestMessageProcessing(unittest.TestCase):
    def setUp(self):
        self.language = {
            "MESSAGE_SURVEY_PLAYER_ALLOWED": "MESSAGE_SURVEY_PLAYER_ALLOWED:",
            "MESSAGE_NEW_MATCHES": "MESSAGE_NEW_MATCHES"
        }
        self.message_processing = MessageProcessing()
        self.request = MagicMock()
        self.request.chat_id = "123456"

    def test_message_processing_with_out_order(self):
        message = "HOLA MUNDO"
        self.request.message = message
        result = self.message_processing.message_processing(self.language, self.request)
        self.assertEqual(result["message"], message)
        self.assertEqual(result["chat_id"], "123456")

    def test_message_processing_with_survey_player_order(self):
        message = "survey_player#HOLA;MUNDO"
        self.request.message = message
        result = self.message_processing.message_processing(self.language, self.request)
        self.assertEqual(result["message"], "MESSAGE_SURVEY_PLAYER_ALLOWED:HOLA, MUNDO")
        self.assertEqual(result["chat_id"], "123456")

    def test_message_processing_new_matches(self):
        message = "NEW_MATCH"
        self.request.message = message
        result = self.message_processing.message_processing(self.language, self.request)
        self.assertEqual(result["message"], "MESSAGE_NEW_MATCHES")
        self.assertEqual(result["chat_id"], "123456")


if __name__ == '__main__':
    unittest.main()
