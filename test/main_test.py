import os
import unittest
from unittest.mock import patch, MagicMock
from unittest.mock import Mock, patch
from telebot.types import Message

from handlers.player import handle_respond_to_matchmaking_accept, handle_respond_to_matchmaking_reject, \
    handle_survey_to_player
from handlers.player.configurar_disponibilidad import process_time_step
from handlers.player.configurar_zona import handle_configure_zone, KM_STEERING_SEPARATOR
from handlers.player.configurar_golpes import handle_configure_strokes
from handlers.player.ver_reservas import handle_see_reserves
from model.language_manager import LanguageManager


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
        self.api_mock.put_survey_to_player = unittest.mock.create_autospec(
            lambda id_telegram, other_player, rating: None, return_value={"result": True, "message": "3"})
        self.api_mock.get_reserves = unittest.mock.create_autospec(lambda x: None, return_value=[])
        self.api_mock.respond_to_matchmaking = unittest.mock.create_autospec(lambda id_telegram, info, accept: None, return_value="")

        self.bot = MagicMock()
        self.bot.reply_to = unittest.mock.create_autospec(
            lambda x, y: None, return_value=None)


    @patch('handlers.player.configurar_disponibilidad.get_from_env_api')
    def test_availability_process_time_step(self, mock_get_from_env_api):
        self.bot.language_manager.get.return_value = [{"text": "Button1", "callback_data": "1"}, {"text": "Button2", "callback_data": "2"}]
        message = MagicMock()
        message.text = "Button1"
        message.from_user.username = "test_user"

        process_time_step(message, self.bot)

        api_conection = mock_get_from_env_api()
        api_conection.set_availability.assert_called_once_with("1", "test_user")
        self.bot.reply_to.assert_called_once()
        self.bot.send_message.assert_called_once()
        self.bot.register_next_step_handler.assert_called_once()

    def test_send_ubicacion_help(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_ZONE"
        message = MagicMock()
        message.text = '/configurar_zona'
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_ZONE")

    def test_send_ubicacion_help_border_case(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_ZONE"
        message = MagicMock()
        message.text = '/configurar_zona   '
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_ZONE")

    def test_send_ubicacion_only_km(self):
        self.bot.language_manager.get.return_value = "MESSAGE_ZONE_UPDATED_KM"
        message = MagicMock()
        message.text = '/configurar_zona 54'
        message.from_user.username = "123456"
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_KM: 54.")

    def test_send_ubicacion_only_zone(self):
        self.bot.language_manager.get.return_value = "MESSAGE_ZONE_UPDATED_LOCATION"
        message = MagicMock()
        message.text = '/configurar_zona CABA'
        message.from_user.username = "123456"
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_LOCATION: CABA.")

    def test_send_ubicacion_all(self):
        self.bot.language_manager.get.side_effect = [
            "MESSAGE_ZONE_UPDATED_LOCATION",
            "MESSAGE_ZONE_UPDATED_KM"
        ]
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + '82'
        message.from_user.username = "123456"
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_LOCATION: CABA.\nMESSAGE_ZONE_UPDATED_KM: 82.")

    def test_send_ubicacion_error_in_km(self):
        self.bot.language_manager.get.return_value = "MESSAGE_INVALID_VALUE"
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + 'asd'
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_INVALID_VALUE")

    def test_configure_strokes_help(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_STROKE"
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.put_strokes.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_STROKE"
        )

    def test_configure_strokes_invalid_for_minor_items(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_STROKE"
        message = MagicMock()
        message.text = '/ver_emparejamientos asd'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.put_strokes.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_STROKE"
        )

    def test_configure_strokes_invalid_for_mayor_items(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_STROKE"
        message = MagicMock()
        message.text = '/ver_emparejamientos asd asd wwww'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.put_strokes.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_STROKE"
        )

    def test_configure_strokes_invalid_for_hability_incorrect(self):
        self.bot.language_manager.get.return_value = "MESSAGE_INCORRECT_HABILITY"
        message = MagicMock()
        message.text = '/ver_emparejamientos all asd'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.put_strokes.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_INCORRECT_HABILITY"
        )

    def test_configure_strokes_invalid_for_number_of_stroke_incorrect(self):
        self.bot.language_manager.get.return_value = "MESSAGE_INVALID_VALUE"
        message = MagicMock()
        message.text = '/ver_emparejamientos s principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.api_mock.put_strokes.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_INVALID_VALUE"
        )

    def test_configure_strokes_2_and_5(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_STROKE"
        message = MagicMock()
        message.text = '/ver_emparejamientos 2,5 principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once()

    def test_configure_strokes_all(self):
        self.bot.language_manager.get.return_value = "MESSAGE_HELP_STROKE"
        message = MagicMock()
        message.text = '/ver_emparejamientos all principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once()

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

    def test_respond_to_matchmaking_accept_few_values_2(self):
        self.bot.language_manager.get.return_value = "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        message = MagicMock()
        message.text = '/ver_emparejamientos asd asd '
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_reject_few_values_0(self):
        self.bot.language_manager.get.return_value = "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_reject(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_accept_many_values_4(self):
        self.bot.language_manager.get.return_value = "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora extra'
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_reject_many_values_5(self):
        self.bot.language_manager.get.return_value = "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora extra hola'
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_accept(self):
        self.bot.language_manager.get.return_value = "MESSAGE_RESPOND_TO_MATCHMAKING"
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora'
        message.from_user.username = "aaa_jugador"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock)
        self.api_mock.respond_to_matchmaking.assert_called_once_with(
            "aaa_jugador",
            {
                "player_id_1": "aaa_jugador",
                "player_id_2": "oponente",
                "paddle_court_name": "cancha",
                "time_availability": "hora",
            },
            True
        )
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING"
        )

    def test_respond_to_matchmaking_reject(self):
        self.bot.language_manager.get.return_value = "MESSAGE_RESPOND_TO_MATCHMAKING"
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora'
        message.from_user.username = "zzz_jugador"
        handle_respond_to_matchmaking_reject(message, self.bot, lambda: self.api_mock)
        self.api_mock.respond_to_matchmaking.assert_called_once_with(
            "zzz_jugador",
            {
                "player_id_1": "oponente",
                "player_id_2": "zzz_jugador",
                "paddle_court_name": "cancha",
                "time_availability": "hora",
            },
            False
        )
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING"
        )

    def test_handle_survey_to_player_empty(self):
        message = MagicMock()
        message.text = '/encuesta_jugador'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_SURVEY_PLAYER"
        )

    def test_handle_survey_to_player_many_info(self):
        message = MagicMock()
        message.text = '/encuesta_jugador asd asd asd'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_SURVEY_PLAYER"
        )

    def test_handle_survey_to_player_other_player_and_rating_minnor(self):
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador 0'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "RATING_ERROR"
        )

    def test_handle_survey_to_player_other_player_and_rating_mayor(self):
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador 6'
        handle_survey_to_player(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "RATING_ERROR"
        )

    def test_handle_survey_to_player_other_player_and_rating_invalid(self):
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador asd'
        # message.from_user.username = "zzz_jugador"
        handle_survey_to_player(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_INVALID_VALUE"
        )

    def test_handle_survey_to_player_other_player_and_rating_valid(self):
        message = MagicMock()
        message.text = '/encuesta_jugador otro_jugador 3'
        message.from_user.username = "zzz_jugador"
        handle_survey_to_player(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "ANSWER_SURVEY_PLAYER3"
        )
        # la respuesta de la API esta hardcodeada a 3
        self.api_mock.put_survey_to_player.assert_called_once_with(
            "zzz_jugador",
            "otro_jugador",
            3
        )


if __name__ == '__main__':
    unittest.main()