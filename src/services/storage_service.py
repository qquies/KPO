import json
import os


class StateStorage:
    def __init__(self, filename="/Users/evgenii/Documents/Лабы/Лабы Проектирование ПО/KPO/src/data/device_state.json"):
        self.filename = filename
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def save(self, data: dict):
        temp_file = self.filename + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, self.filename)

    def load(self) -> dict:
        if not os.path.exists(self.filename):
            return {}

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, OSError):
            # если файл битый или пустой — начинаем с чистого состояния
            return {}