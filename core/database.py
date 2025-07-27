# database.py
import sqlite3
import os

class DictionaryDB:
    def __init__(self, db_path="data/word_database.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()
        
    def _create_tables(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dictionaries (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT
        )""")
        
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL,
            dict_id INTEGER NOT NULL,
            FOREIGN KEY(dict_id) REFERENCES dictionaries(id)
        )""")
    
    def add_dictionary(self, name, description, word_list):
        """Добавление нового словаря через интерфейс"""
        cur = self.conn.cursor()
        cur.execute("INSERT INTO dictionaries (name, description) VALUES (?, ?)", 
                    (name, description))
        dict_id = cur.lastrowid
        
        for word in word_list:
            cur.execute("INSERT INTO words (word, dict_id) VALUES (?, ?)", 
                        (word.strip(), dict_id))
        self.conn.commit()
    
    def get_random_word(self, dict_ids):
        """Выбор случайного слова из указанных словарей"""
        query = f"""
        SELECT word FROM words 
        WHERE dict_id IN ({','.join('?'*len(dict_ids))})
        ORDER BY RANDOM() LIMIT 1
        """
        cur = self.conn.execute(query, dict_ids)
        return cur.fetchone()[0]