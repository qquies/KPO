# сервис хранения

import json

class StorageService:
    def save(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None