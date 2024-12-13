import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXTENSION = "json"
FOLDER = "language/"
ENCODING_LENGUAJE = 'utf-8'

def get_language(name):
    file_path = os.path.join(ROOT_DIR, FOLDER, f"{name}.{EXTENSION}")
    with open(file_path, 'r', encoding=ENCODING_LENGUAJE) as file_json:
        data = json.load(file_json)
    return data