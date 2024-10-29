import json

EXTENSION = "json"
FOLDER = "language/"
ENCODING_LENGUAJE = 'utf-8-sig' # este encoding acepta letras con acento y la letra 'Ñ', 'ñ'.

def get_languaje(name):
    file = FOLDER + name + "." + EXTENSION
    with open(file, 'r', encoding=ENCODING_LENGUAJE) as file_json:
        data = json.load(file_json)
    return data

# TEST

# print(get_languaje("ES"))
