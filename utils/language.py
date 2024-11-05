import json

EXTENSION = "json"
FOLDER = "language/"
# este encoding acepta letras con acento y la letra 'Ñ', 'ñ'. si no
# funciona agregar -sig
ENCODING_LENGUAJE = 'utf-8'


def get_language(name):
    file = FOLDER + name + "." + EXTENSION
    with open(file, 'r', encoding=ENCODING_LENGUAJE) as file_json:
        data = json.load(file_json)
    return data
