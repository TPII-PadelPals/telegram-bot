import unittest
from unittest.mock import patch, MagicMock
from padelpals_bot import send_welcome, send_double


class TestTelegramBot(unittest.TestCase):

    @patch('telebot.TeleBot.reply_to')
    def test_start_command(self, mock_reply_to):
        # Crea un mensaje de prueba simulando el mensaje del comando /start
        message = MagicMock()
        message.text = '/start'

        # Llama a la función del manejador de /start
        send_welcome(message)

        # Verifica si se llamó a reply_to con los argumentos correctos
        mock_reply_to.assert_called_once_with(message, "Hola! Soy un bot creado con Telebot")

    @patch('telebot.TeleBot.reply_to')
    def test_send_double(self, mock_reply_to):
        message = MagicMock()
        message.text = '/duplicar J2'

        send_double(message)

        mock_reply_to.assert_called_once_with(message, "J2J2")


if __name__ == '__main__':
    unittest.main()
