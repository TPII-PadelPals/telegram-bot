import os

from model.api_conection import ApiConection
from utils.language import get_language
from core.config import settings

def get_from_env_lang():
    return get_language(settings.TELEGRAM_BOT_LANGUAGE)

def get_from_env_api():
    return ApiConection(
        "http://" +
        settings.GATEWAY_HOST +
        ":" +
        settings.GATEWAY_PORT)