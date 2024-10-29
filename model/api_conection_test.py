import unittest
from unittest.mock import patch, Mock
from api_conection import ApiConection  # Cambia `my_module` al nombre real del archivo donde está la clase


class TestApiConection(unittest.TestCase):

    def setUp(self):
        self.api = ApiConection("https://api.example.com")

    @patch('requests.get')
    def test_get_hi_name_success(self, mock_get):
        # Simulamos una respuesta exitosa
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Hola, Carlos!'}
        mock_get.return_value = mock_response

        result = self.api.get_hi_name("Carlos")
        self.assertEqual(result, 'Hola, Carlos!')

    @patch('requests.get')
    def test_get_hi_name_other_error(self, mock_get):
        mock_get.side_effect = Exception("Connection timeout")

        result = self.api.get_hi_name("Carlos")
        self.assertIn('An error occurred', result)

    @patch('requests.post')
    def test_set_availability_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'OK!'}
        mock_post.return_value = mock_response

        result = self.api.set_availability(10)
        self.assertEqual(result, 'OK!')

    @patch('requests.post')
    def test_set_zone_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Zona seteada'}
        mock_post.return_value = mock_response

        result = self.api.set_zone("CABA", 15)
        self.assertEqual(result, 'Zona seteada')

    @patch('requests.post')
    def test_set_zone_only_zone_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Zona seteada'}
        mock_post.return_value = mock_response

        result = self.api.set_zone("CABA", None)
        self.assertEqual(result, 'Zona seteada')

    @patch('requests.post')
    def test_set_zone_only_km_success(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'message': 'Zona seteada'}
        mock_post.return_value = mock_response

        result = self.api.set_zone(None, 15)
        self.assertEqual(result, 'Zona seteada')

    # @patch('requests.post')
    # def test_set_zone_no_values_error(self):
    #     # Prueba para el caso donde no se proporciona `zone` ni `km`
    #     try:
    #         ApiConection("https://api.example.com").set_zone(zone=None, km=None)
    #         print("NO lanza excepcion")
    #         assert False
    #     except ValueError:
    #         print("OK")
    #         assert True
    #     except:
    #         print("lanza otra excepcion")
    #         assert False



if __name__ == "__main__":
    unittest.main()
