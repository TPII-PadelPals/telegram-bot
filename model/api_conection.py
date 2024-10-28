import requests


class ApiConection:
    def __init__(self):
        # TODO: encapsular en una variable de entorno la dirección y el puerto
        self.url = 'http://localhost:8000'

    def get_hi_name(self, name):
        try:
            response = requests.get(self.url + f'/message/{name}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            return data['message']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'

    def set_availability(self, time: int):
        # todo finalizar
        return "OK"
