import os
import unittest
from unittest.mock import patch, MagicMock
from unittest.mock import Mock, patch
from telebot.types import Message

from handlers.player import handle_respond_to_matchmaking_accept, handle_respond_to_matchmaking_reject
from handlers.player.configurar_disponibilidad import process_time_step
from handlers.player.configurar_zona import handle_configure_zone, KM_STEERING_SEPARATOR
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
        self.api_mock.get_reserves = unittest.mock.create_autospec(lambda x: None, return_value=[])
        self.api_mock.respond_to_matchmaking = unittest.mock.create_autospec(lambda id_telegram, info, accept: None, return_value="")
        self.leng_mock = {"MESSAGE_HELP_AVAILABILITY": "MESSAGE_HELP_AVAILABILITY",
                          "MESSAGE_HELP_ZONE": "MESSAGE_HELP_ZONE",
                          "MESSAGE_ZONE_UPDATED_LOCATION": "MESSAGE_ZONE_UPDATED_LOCATION",
                          "MESSAGE_ZONE_UPDATED_KM": "MESSAGE_ZONE_UPDATED_KM",
                          "MESSAGE_INVALID_VALUE": "MESSAGE_INVALID_VALUE",
                          "DAYS_NAMES": {"lunes": 0},
                          "MESSAGE_SEE_MATCHES": "MESSAGE_SEE_MATCHES",
                          "SEE_MATCHES_SEPARATOR": "|",
                          "MESSAGE_SEE_MATCHES_EMPTY": "MESSAGE_SEE_MATCHES_EMPTY",
                          "PLAYER": "PLAYER",
                          "COURT": "COURT",
                          "COURT_ID": "COURT_ID",
                          "TIME": "TIME",
                          "DATE": "Fecha",
                          "DATE_FMT": "%d/%m/%Y",
                          "TIME": "Horario",
                          "TIME_FMT": "%H:%M",
                          "ALL": "ALL",
                          "STROKE_HABILITY": ["principiante", "intermedio", "avanzado"],
                          "MESSAGE_HELP_STROKE": "MESSAGE_HELP_STROKE",
                          "MESSAGE_INCORRECT_HABILITY": "MESSAGE_INCORRECT_HABILITY",
                          "MESSAGE_STROKES_UPDATED": "MESSAGE_STROKES_UPDATED",
                          "NUMBER_FOR_STROKE": {"2": "2", "5": "5", "1": "1", "3": "3", "4": "4", "6": "6", "7": "7", "8": "8", "9": "8", "10": "8", "11": "8", "12": "8", "13": "8", "14": "8", "15": "8", "16": "8"},
                          "TIME_NAMES": {"2": "TIME_NAMES"},
                          "SENDER_POSITION_STROKE_HABILITY": {
                              "principiante": 0,
                              "intermedio": 1,
                              "avanzado": 2
                          },
                          "MESSAGE_SEE_RESERVES_EMPTY": "MESSAGE_SEE_RESERVES_EMPTY",
                          "DATE": "DATE",
                          "MESSAGE_SEE_RESERVES": "MESSAGE_SEE_RESERVES",
                          "MESSAGE_RESPOND_TO_MATCHMAKING_HELP": "MESSAGE_RESPOND_TO_MATCHMAKING_HELP",
                          "I_ACCEPT": "I_ACCEPT",
                          "ACCEPT": "ACCEPT",
                          "MESSAGE_RESPOND_TO_MATCHMAKING": "MESSAGE_RESPOND_TO_MATCHMAKING"
                        }
        self.bot = MagicMock()
        self.bot.reply_to = unittest.mock.create_autospec(
            lambda x, y: None, return_value=None)

    @patch('handlers.player.configurar_disponibilidad.get_from_env_api')
    @patch('handlers.player.configurar_disponibilidad.get_from_env_lang')
    def test_availability_process_time_step(self, mock_get_from_env_lang, mock_get_from_env_api):

        mock_get_from_env_lang.return_value = {
            "AVAILABILITY_TIME_BUTTONS": [
                {"text": "Morning", "callback_data": "1"},
                {"text": "Afternoon", "callback_data": "2"},
                {"text": "Evening", "callback_data": "3"}
            ],
            "AVAILABILITY_DAY_BUTTONS": [
                {"text": "Monday", "callback_data": "1"},
                {"text": "Tuesday", "callback_data": "2"}
            ],
            "AVAILABILITY_MESSAGE": "Please select a time",
            "AVAILABLE_DAYS_MESSAGE": "Please select a day"
        }

        mock_api = Mock()
        mock_get_from_env_api.return_value = mock_api

        message = Mock(spec=Message)
        type(message).from_user = Mock(username="test_user")
        message.chat = Mock()
        message.text = "Morning"
        message.chat.id = 12345

        bot = Mock()

        process_time_step(message, bot)

        mock_api.set_availability.assert_called_once_with("1", "test_user")
        bot.reply_to.assert_called_once_with(message, 'Se ha configurado el horario correctamente')
        bot.send_message.assert_called_once_with(12345, "Please select a day", reply_markup=bot.send_message.call_args[1]['reply_markup'])
        bot.register_next_step_handler.assert_called_once()

    def test_send_ubicacion_help(self):
        message = MagicMock()
        message.text = '/configurar_zona'
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_HELP_ZONE"])

    def test_send_ubicacion_help_border_case(self):
        message = MagicMock()
        message.text = '/configurar_zona   '
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_HELP_ZONE"])

    def test_send_ubicacion_only_km(self):
        message = MagicMock()
        message.text = '/configurar_zona 54'
        message.from_user.username = "123456"
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_KM: 54.")

    def test_send_ubicacion_only_zone(self):
        message = MagicMock()
        message.text = '/configurar_zona CABA'
        message.from_user.username = "123456"
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_LOCATION: CABA.")

    def test_send_ubicacion_all(self):
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + '82'
        message.from_user.username = "123456"
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_LOCATION: CABA.\nMESSAGE_ZONE_UPDATED_KM: 82.")

    def test_send_ubicacion_error_in_km(self):
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + 'asd'
        handle_configure_zone(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message, self.leng_mock["MESSAGE_INVALID_VALUE"])

    def test_configure_strokes_help(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_not_called()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_STROKE"
        )

    def test_configure_strokes_invalid_for_minor_items(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos asd'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_not_called()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_STROKE"
        )

    def test_configure_strokes_invalid_for_mayor_items(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos asd asd wwww'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_not_called()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_HELP_STROKE"
        )

    def test_configure_strokes_invalid_for_hability_incorrect(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos all asd'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_not_called()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_INCORRECT_HABILITY"
        )

    def test_configure_strokes_invalid_for_number_of_stroke_incorrect(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos s principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_not_called()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_INVALID_VALUE"
        )

    def test_configure_strokes_2_and_5(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos 2,5 principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_called_once()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once()

    def test_configure_strokes_all(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos all principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(
            message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_called_once()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once()

    def test_see_reserves_empty(self):
        message = MagicMock()
        message.text = '/ver_reservas'
        message.from_user.username = "123456"
        handle_see_reserves(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.get_reserves.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_SEE_RESERVES_EMPTY")

    def test_see_reserves_not_empty(self):
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
        handle_see_reserves(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.get_reserves.assert_called_once()
        # self.bot.reply_to.assert_called_once_with(
        #     message,
        #     "```\nMESSAGE_SEE_MATCHESPLAYER |COURT|TIME\ntest_48|1    |TIME_NAMES\n```")
        self.bot.reply_to.assert_called_once()

    def test_respond_to_matchmaking_accept_few_values_2(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos asd asd '
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_reject_few_values_0(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_reject(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_accept_many_values_4(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora extra'
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_reject_many_values_5(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora extra hola'
        message.from_user.username = "123456"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_RESPOND_TO_MATCHMAKING_HELP"
        )

    def test_respond_to_matchmaking_accept(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora'
        message.from_user.username = "aaa_jugador"
        handle_respond_to_matchmaking_accept(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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
        message = MagicMock()
        message.text = '/ver_emparejamientos oponente cancha hora'
        message.from_user.username = "zzz_jugador"
        handle_respond_to_matchmaking_reject(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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

if __name__ == '__main__':
    unittest.main()
