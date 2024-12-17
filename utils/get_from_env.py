import os

from model.api_conection import ApiConection
from utils.language import get_language


def get_from_env_lang():
    return get_language(os.getenv('TELEGRAM_BOT_LANGUAGE', 'ES'))

def get_from_env_api():
    return ApiConection(
        "http://" +
        os.getenv('GATEWAY_HOST') +
        ":" +
        os.getenv('GATEWAY_PORT'))