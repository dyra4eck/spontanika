from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl, QFileInfo


class SoundManager:
    def __init__(self, config=None):
        self.config = config
        self.sounds = {}
        self.enabled = True

        # Загружаем звуки с проверкой существования
        self.load_sound("start", "sounds/start.wav")
        self.load_sound("change", "sounds/change.wav")
        self.load_sound("finish", "sounds/finish.wav")

    def load_sound(self, name, path):
        # Проверяем существует ли файл
        if QFileInfo(path).exists():
            sound = QSoundEffect()
            sound.setSource(QUrl.fromLocalFile(path))
            self.sounds[name] = sound
        else:
            print(f"Предупреждение: звуковой файл {path} не найден")
            self.sounds[name] = None

    def play(self, sound_type):
        if not self.enabled:
            return

        if self.config and not self.config.get("sounds_enabled", True):
            return

        if sound_type in self.sounds and self.sounds[sound_type]:
            self.sounds[sound_type].play()

    def set_enabled(self, enabled):
        self.enabled = enabled