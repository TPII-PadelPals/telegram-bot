import json
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
EXTENSION = "json"
FOLDER = "language/"
ENCODING_LENGUAJE = 'utf-8'

class LanguageManager():
    def __init__(self, language_code):
        self.dictionary = self._load_file(language_code)

    def _load_file(self, language_code):
        file_path = os.path.join(ROOT_DIR, FOLDER, f"{language_code}.{EXTENSION}")
        with open(file_path, 'r', encoding=ENCODING_LENGUAJE) as file_json:
            data = json.load(file_json)
        return data

    def get(self, key):
        if key not in self.dictionary:
            raise KeyError(f"Key '{key}' not found in language dictionary")       
        return self.dictionary[key]