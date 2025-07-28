import json
from pathlib import Path


class Config:
    def __init__(self, file_path="config.json"):
        self.file_path = Path(file_path)
        self.data = {
            "interval": 60,  # По умолчанию 60 секунд
            "selected_dicts": [1],  # ID выбранных словарей
            "sounds_enabled": True,
            "theme": "light"
        }
        self.load()

    def load(self):
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r') as f:
                    self.data = json.load(f)
            except:
                # В случае ошибки используем значения по умолчанию
                self.save()

    def save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()