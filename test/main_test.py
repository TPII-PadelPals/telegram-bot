import unittest
from unittest.mock import patch, MagicMock
from unittest.mock import patch

from handlers.player import handle_respond_to_matchmaking_accept, handle_respond_to_matchmaking_reject, \
    handle_survey_to_player
from handlers.player.configurar_disponibilidad import process_time_step
from handlers.player.configurar_golpes import handle_configure_strokes
from handlers.player.ver_reservas import handle_see_reserves


class TestTelegramBot(unittest.TestCase):

    def setUp(self):
        self.api_mock = MagicMock()
        self.api_mock.set_availability = unittest.mock.create_autospec(
            lambda x, y: None, return_value="")
        self.api_mock.set_available_day = unittest.mock.create_autospec(
            lambda x, y: None, return_value="")
        self.api_mock.set_zone = unittest.mock.create_autospec(
            lambda x, y, z: None, return_value="")
        self.api_mock.get_matches = unittest.mock.create_autospec(
            lambda x: None, return_value=[])
        self.api_mock.put_strokes = unittest.mock.create_autospec(
            lambda x, y: None, return_value="")
        self.result_of_survey_player = {"result": True, "message": "3"}
        self.api_mock.put_survey_to_player = unittest.mock.create_autospec(
            lambda id_telegram, other_player, rating: None, return_value=self.result_of_survey_player)
        self.api_mock.get_reserves = unittest.mock.create_autospec(lambda x: None, return_value=[])
        self.api_mock.respond_to_matchmaking = unittest.mock.create_autospec(lambda id_telegram, info, accept: None, return_value="")

        self.bot = MagicMock()
        self.bot.reply_to = unittest.mock.create_autospec(
            lambda x, y: None, return_value=None)


    def test_see_reserves_empty(self):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_RESERVES_EMPTY"
        message = MagicMock()
        message.text = '/ver_reservas'
        message.from_user.username = "123456"
        handle_see_reserves(message, self.bot, lambda: self.api_mock)
        self.api_mock.get_reserves.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_SEE_RESERVES_EMPTY")

    def test_see_reserves_not_empty(self):
        self.bot.language_manager.get.return_value = "MESSAGE_SEE_RESERVES"
        self.api_mock.get_reserves = unittest.mock.create_autospec(lambda x: None, return_value=[
            {
                "player_id_1": "test_40",
                "player_id_2": "test_48",
                "paddle_court_name": "1",
                "time_availability": "2",
                "player_id_1_response_accept": "true",
                "player_id_2_response_accept": "false",
                "begin_date_time": "2024-11-11"
            }
        ])
        message = MagicMock()
        message.text = '/ver_reservas'
        message.from_user.username = "test_40"
        handle_see_reserves(message, self.bot, lambda: self.api_mock)
        self.api_mock.get_reserves.assert_called_once()
        self.bot.reply_to.assert_called_once()

    def test_handle_survey_to_player_empty(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_SURVEY_PLAYER"
        message = MagicMock()
        message.text = '/encuesta_jugador'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_SURVEY_PLAYER"
        )

    def test_handle_survey_to_player_many_info(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_SURVEY_PLAYER"
        message = MagicMock()
        message.text = '/encuesta_jugador asd asd asd'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_SURVEY_PLAYER"
        )

    def test_handle_survey_to_player_other_player_and_rating_minnor(self):
        self.bot.language_manager.get.return_value = "RATING_OUT_OF_RANGE_ERROR"
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador 0'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "RATING_OUT_OF_RANGE_ERROR"
        )

    def test_handle_survey_to_player_other_player_and_rating_mayor(self):
        self.bot.language_manager.get.return_value = "RATING_OUT_OF_RANGE_ERROR"
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador 6'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "RATING_OUT_OF_RANGE_ERROR"
        )

    def test_handle_survey_to_player_other_player_and_rating_invalid(self):
        self.bot.language_manager.get.return_value = "MESSAGE_INVALID_VALUE"
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador asd'
        # message.from_user.username = "zzz_jugador"
        handle_survey_to_player(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_INVALID_VALUE"
        )

    def test_handle_survey_to_player_other_player_and_rating_valid(self):
        self.bot.language_manager.get.return_value = "ANSWER_SURVEY_PLAYER"
        expected_respond_rating = int(self.result_of_survey_player["message"])
        jugador = "zzz_jugador"
        otro_jugador = 'otro_jugador'
        message = MagicMock()
        message.text = '/encuesta_jugador ' + otro_jugador + ' ' + self.result_of_survey_player["message"]
        message.from_user.username = jugador
        handle_survey_to_player(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "ANSWER_SURVEY_PLAYER3"
        )
        # la respuesta de la API esta hardcodeada a 3
        self.api_mock.put_survey_to_player.assert_called_once_with(
            jugador,
            otro_jugador,
            expected_respond_rating
        )


if __name__ == '__main__':
    unittest.main()