# stats_manager.py
import json
from datetime import datetime
from pathlib import Path

class StatsManager:
    def __init__(self, file_path="data/user_stats.json"):
        self.file = Path(file_path)
        self.file.parent.mkdir(exist_ok=True)
        
        if not self.file.exists():
            self.data = {"sessions": [], "daily": {}}
            self._save()
        else:
            with open(self.file, 'r') as f:
                self.data = json.load(f)
    
    def add_session(self, duration, words_used, dicts_used):
        """Добавление данных сессии"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "duration_sec": duration,
            "words_count": len(words_used),
            "dicts": dicts_used,
            "words": words_used
        }
        self.data["sessions"].append(session)
        
        # Обновление ежедневной статистики
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data["daily"]:
            self.data["daily"][today] = {"sessions": 0, "total_time": 0}
            
        self.data["daily"][today]["sessions"] += 1
        self.data["daily"][today]["total_time"] += duration
        
        self._save()
    
    def get_daily_stats(self):
        """Получение данных для графика активности"""
        return self.data["daily"]
    
    def _save(self):
        with open(self.file, 'w') as f:
            json.dump(self.data, f, indent=2)