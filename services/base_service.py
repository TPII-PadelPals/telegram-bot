import requests
from model.config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self):
        """Set the base URL for the service."""
        local_server = ["localhost", "127.0.0.1"]
        host = f"{Config.SERVICE_HOST}:{Config.SERVICE_PORT}"
        self.base_url = f"http://{host}" if Config.SERVICE_HOST in local_server else f"https://{host}"
        self.x_api_key_header = {"x-api-key": ""}

    def generate_url(self, endpoint):
        """Generate a full URL from an endpoint."""
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint, params=None, headers={}):
        """Send a GET request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to {url}, params: {params}")
        headers.update(self.x_api_key_header)
        response = requests.get(url, params=params, headers=headers)
        return self._handle_response(response)

    def post(self, endpoint, data=None, json=None, headers={}):
        """Send a POST request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url}, json: {json}")
        headers.update(self.x_api_key_header)
        response = requests.post(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def put(self, endpoint, data=None, json=None, headers={}):
        """Send a PUT request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to {url}, json: {json}")
        headers.update(self.x_api_key_header)
        response = requests.put(url, data=data, json=json, headers=headers)
        return self._handle_response(response)

    def delete(self, endpoint, headers={}):
        """Send a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        headers.update(self.x_api_key_header)
        response = requests.delete(url, headers=headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Handle the response, raise an exception for bad responses."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return None
