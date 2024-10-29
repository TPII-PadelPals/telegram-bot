import requests


class ApiConection:
    def __init__(self, url):
        # self.url = 'http://localhost:8000'
        self.url = url

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
        try:
            response = requests.get(self.url + f'/message/availability/{time}')
            # Lanza un error si la respuesta no es 200
            response.raise_for_status()
            data = response.json()
            return data['message']
        except requests.exceptions.HTTPError as http_err:
            return f'HTTP error occurred: {http_err}'
        except Exception as err:
            return f'An error occurred: {err}'
        # return "OK"
