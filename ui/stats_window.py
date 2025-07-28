import json
import os
from datetime import datetime


class StatsManager:
    def __init__(self):
        self.stats_file = "core/stats.json"
        self.data = self.load_or_init_stats()

    def load_or_init_stats(self):
        try:
            # Проверка существования файла
            if not os.path.exists(self.stats_file):
                return self.init_stats_file()

            # Проверка пустого файла
            if os.path.getsize(self.stats_file) == 0:
                return self.init_stats_file()

            # Загрузка данных
            with open(self.stats_file, 'r') as f:
                return json.load(f)

        except (json.JSONDecodeError, FileNotFoundError):
            return self.init_stats_file()

    def init_stats_file(self):
        """Создает новый файл статистики с базовой структурой"""
        initial_data = {
            "sessions": [],
            "dictionaries": {},
            "total_time": 0,
            "words_count": 0
        }
        with open(self.stats_file, 'w') as f:
            json.dump(initial_data, f, indent=4)
        return initial_data

    def add_session(self, duration, words):
        session_data = {
            "date": datetime.now().isoformat(),
            "duration": duration,
            "words": words,
            "word_count": len(words)
        }
        self.data["sessions"].append(session_data)
        self.data["total_time"] += duration
        self.data["words_count"] += len(words)
        self.save_data()

    def save_data(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.data, f, indent=4)