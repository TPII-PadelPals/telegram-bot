import unittest
from unittest.mock import patch, MagicMock
from padelpals_bot import send_welcome, send_double, set_availability


class TestTelegramBot(unittest.TestCase):

    @patch('telebot.TeleBot.reply_to')
    def test_start_command(self, mock_reply_to):
        # Crea un mensaje de prueba simulando el mensaje del comando /start
        message = MagicMock()
        message.text = '/start'

        # Llama a la función del manejador de /start
        send_welcome(message)

        # Verifica si se llamó a reply_to con los argumentos correctos
        mock_reply_to.assert_called_once_with(message, "Bienvenido a PadelPals")

    @patch('telebot.TeleBot.reply_to')
    def test_send_double(self, mock_reply_to):
        message = MagicMock()
        message.text = '/duplicar J2'

        send_double(message)

        mock_reply_to.assert_called_once_with(message, "J2J2")

    @patch('telebot.TeleBot.reply_to')
    def test_send_disponibilidad_horaria_no_number(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_disponibilidad'
        set_availability(message)
        mock_reply_to.assert_called_once_with(message, 'Indicanos los horarios que suelas tener disponibles:\n- Mañana de 8hs hasta 12hs.\n- Tarde de 12hs hasta 18hs.\n- Noche de 18hs hasta 00hs.\n1: Mañana\n2: Tarde\n3: Noche\n4: Mañana y tarde\n5: Mañana y noche\n6: Tarde y noche\n7: Todos\nAsignación: /configurar_disponibilidad <Numero>')

    @patch('telebot.TeleBot.reply_to')
    def test_send_disponibilidad_horaria_whit_number(self, mock_reply_to):
        message = MagicMock()
        message.text = '/configurar_disponibilidad 4'
        set_availability(message)
        mock_reply_to.assert_called_once_with(message, 'OK')


if __name__ == '__main__':
    unittest.main()
