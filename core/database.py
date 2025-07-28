import sqlite3
import os
from pathlib import Path


class DictionaryDB:
    def __init__(self, db_path="data/word_database.db"):
        self.db_path = db_path
        Path(os.path.dirname(db_path)).mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        self._load_default_dicts()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dictionaries (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            dict_id INTEGER NOT NULL,
            FOREIGN KEY(dict_id) REFERENCES dictionaries(id)
        )""")
        self.conn.commit()

    def _load_default_dicts(self):
        # Проверяем, есть ли уже словари
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dictionaries")
        count = cursor.fetchone()[0]

        if count == 0:
            # Добавляем основной словарь
            cursor.execute(
                "INSERT INTO dictionaries (name, description) VALUES (?, ?)",
                ("Основной словарь", "Стандартный набор слов для импровизации")
            )
            dict_id = cursor.lastrowid

            # Добавляем слова
            words = ["дом", "лес", "река", "солнце", "книга", "город", "дорога",
                     "окно", "стол", "ветер", "дождь", "огонь", "земля", "небо"]
            for word in words:
                cursor.execute(
                    "INSERT INTO words (word, dict_id) VALUES (?, ?)",
                    (word, dict_id)
                )

            self.conn.commit()

    def get_random_word(self, dict_ids):
        cursor = self.conn.cursor()
        query = f"""
        SELECT word FROM words 
        WHERE dict_id IN ({','.join(['?'] * len(dict_ids))})
        ORDER BY RANDOM() LIMIT 1
        """
        cursor.execute(query, dict_ids)
        result = cursor.fetchone()
        return result[0] if result else "слово"

    def get_available_dictionaries(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM dictionaries")
        return cursor.fetchall()