import os

from model.api_conection import ApiConection
from utils.language import get_language


def get_from_env_lang():
    return get_language(os.getenv('LANGUAGE', 'ES'))

def get_from_env_api():
    return ApiConection(
        "http://" +
        os.getenv('SERVICE_HOST') +
        ":" +
        os.getenv('SERVICE_PORT'))