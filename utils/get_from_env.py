from model.api_conection import ApiConection
from core.config import settings

def get_from_env_api():
    return ApiConection(f"http://{settings.GATEWAY_HOST}:{settings.GATEWAY_PORT}")