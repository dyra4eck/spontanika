# sound_manager.py
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl


class SoundManager:
    def __init__(self):
        self.sounds = {
            "start": self._load_sound("sounds/start.wav"),
            "change": self._load_sound("sounds/change.wav"),
            "finish": self._load_sound("sounds/finish.wav")
        }

    def _load_sound(self, path):
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(path))
        return sound

    def play(self, sound_type):
        if sound_type in self.sounds:
            self.sounds[sound_type].play()