import os
import unittest
from unittest.mock import patch, MagicMock
from handlers.player.configurar_disponibilidad import handle_configure_availability
from handlers.player.configurar_zona import handle_configure_zone, KM_STEERING_SEPARATOR
from handlers.player.ver_emparejamientos import handle_see_matches
from handlers.player.configurar_golpes import handle_configure_strokes


class TestTelegramBot(unittest.TestCase):

    def setUp(self):
        self.api_mock = MagicMock()
        self.api_mock.set_availability = unittest.mock.create_autospec(lambda x, y: None, return_value="")
        self.api_mock.set_available_day = unittest.mock.create_autospec(lambda x, y: None, return_value="")
        self.api_mock.set_zone = unittest.mock.create_autospec(lambda x, y, z: None, return_value="")
        self.api_mock.get_matches = unittest.mock.create_autospec(lambda x: None, return_value=[])
        self.api_mock.put_strokes = unittest.mock.create_autospec(lambda x, y: None, return_value="")
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
                          "TIME": "TIME",
                          "ALL": "ALL",
                          "STROKE_HABILITY": ["principiante", "intermedio", "avanzado"],
                          "MESSAGE_HELP_STROKE": "MESSAGE_HELP_STROKE",
                          "MESSAGE_INCORRECT_HABILITY": "MESSAGE_INCORRECT_HABILITY",
                          "MESSAGE_STROKES_UPDATED": "MESSAGE_STROKES_UPDATED",
                          "NUMBER_FOR_STROKE": {"2": "2","5": "5","1": "1","3": "3","4": "4","6": "6","7": "7","8": "8","9": "8","10": "8","11": "8","12": "8","13": "8","14": "8","15": "8","16": "8"},
                          "TIME_NAMES": {"2": "TIME_NAMES"}}
        self.bot = MagicMock()
        self.bot.reply_to = unittest.mock.create_autospec(lambda x, y: None, return_value=None)



    def test_send_disponibilidad_horaria_no_number(self):
        message = MagicMock()
        message.text = '/configurar_disponibilidad'
        handle_configure_availability(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_HELP_AVAILABILITY"],)


    def test_send_disponibilidad_horaria_no_number_border_case(self):
        message = MagicMock()
        message.text = '/configurar_disponibilidad    '
        handle_configure_availability(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_HELP_AVAILABILITY"])

    def test_send_disponibilidad_horaria_whit_number(self):
        message = MagicMock()
        message.text = '/configurar_disponibilidad 4'
        message.from_user.username = "123456"
        handle_configure_availability(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "OK")


    def test_send_disponibilidad_horaria_whit_invalid_info(self):
        message = MagicMock()
        message.text = '/configurar_disponibilidad a'
        handle_configure_availability(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_INVALID_VALUE"])


    def test_send_ubicacion_help(self):
        message = MagicMock()
        message.text = '/configurar_zona'
        handle_configure_zone(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_HELP_ZONE"])

    def test_send_ubicacion_help_border_case(self):
        message = MagicMock()
        message.text = '/configurar_zona   '
        handle_configure_zone(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            self.leng_mock["MESSAGE_HELP_ZONE"])

    def test_send_ubicacion_only_km(self):
        message = MagicMock()
        message.text = '/configurar_zona 54'
        message.from_user.username = "123456"
        handle_configure_zone(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_KM: 54.")


    def test_send_ubicacion_only_zone(self):
        message = MagicMock()
        message.text = '/configurar_zona CABA'
        message.from_user.username = "123456"
        handle_configure_zone(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_LOCATION: CABA.")


    def test_send_ubicacion_all(self):
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + '82'
        message.from_user.username = "123456"
        handle_configure_zone(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message, "MESSAGE_ZONE_UPDATED_LOCATION: CABA.\nMESSAGE_ZONE_UPDATED_KM: 82.")


    def test_send_ubicacion_error_in_km(self):
        message = MagicMock()
        message.text = '/configurar_zona CABA' + KM_STEERING_SEPARATOR + 'asd'
        handle_configure_zone(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_zone.assert_not_called()
        self.bot.reply_to.assert_called_once_with(message, self.leng_mock["MESSAGE_INVALID_VALUE"])

    def test_send_disponibilidad_diaria(self):
        message = MagicMock()
        message.text = '/configurar_disponibilidad lUnEs'
        message.from_user.username = "123456"
        handle_configure_availability(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_not_called()
        self.api_mock.set_available_day.assert_called_once()
        self.bot.reply_to.assert_called_once_with(
            message,
            "OK")

    def test_send_matches_empty(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "123456"
        handle_see_matches(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_not_called()
        self.api_mock.set_available_day.assert_not_called()
        self.bot.reply_to.assert_called_once_with(
            message,
            "MESSAGE_SEE_MATCHES_EMPTY")

    def test_send_matches_not_empty(self):
        self.api_mock.get_matches = unittest.mock.create_autospec(lambda x: None, return_value=[
            {
                "player_id_1": "test_40",
                "player_id_2": "test_48",
                "paddle_court_name": "1",
                "time_availability": "2",
                "begin_date_time": "2024-11-11T19:59:49.808321"
            }
        ])
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "test_40"
        handle_see_matches(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.set_availability.assert_not_called()
        self.api_mock.set_available_day.assert_not_called()
        # self.bot.reply_to.assert_called_once_with(
        #     message,
        #     "```\nMESSAGE_SEE_MATCHESPLAYER |COURT|TIME\ntest_48|1    |TIME_NAMES\n```")
        self.bot.reply_to.assert_called_once()

    def test_configure_strokes_help(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos'
        message.from_user.username = "123456"
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
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
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_called_once()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once()

    def test_configure_strokes_all(self):
        message = MagicMock()
        message.text = '/ver_emparejamientos all principiante'
        message.from_user.username = "123456"
        handle_configure_strokes(message, self.bot, lambda: self.api_mock, lambda: self.leng_mock)
        self.api_mock.put_strokes.assert_called_once()
        # self.bot.reply_to.assert_called_once()
        self.bot.reply_to.assert_called_once()

if __name__ == '__main__':
    unittest.main()
