import os
import unittest
from unittest.mock import patch, MagicMock
from handlers.player.configurar_disponibilidad import handle_configure_availability
from handlers.player.configurar_zona import handle_configure_zone, KM_STEERING_SEPARATOR


class TestTelegramBot(unittest.TestCase):

    def setUp(self):
        self.api_mock = MagicMock()
        self.api_mock.set_availability = unittest.mock.create_autospec(lambda x, y: None, return_value="")
        self.api_mock.set_zone = unittest.mock.create_autospec(lambda x, y, z: None, return_value="")
        self.leng_mock = {"MESSAGE_HELP_AVAILABILITY": "MESSAGE_HELP_AVAILABILITY",
                          "MESSAGE_HELP_ZONE": "MESSAGE_HELP_ZONE",
                          "MESSAGE_ZONE_UPDATED_LOCATION": "MESSAGE_ZONE_UPDATED_LOCATION",
                          "MESSAGE_ZONE_UPDATED_KM": "MESSAGE_ZONE_UPDATED_KM",
                          "MESSAGE_INVALID_VALUE": "MESSAGE_INVALID_VALUE"}
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


if __name__ == '__main__':
    unittest.main()
