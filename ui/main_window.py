from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSlider, QSpinBox, QGroupBox
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt, QTimer
from datetime import datetime
from .circular_progress import CircularProgressBar
from core.database import DictionaryDB
from core.stats_manager import StatsManager
from core.sound_manager import SoundManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Спонтаника")
        self.setMinimumSize(800, 600)

        # Инициализация компонентов
        self.db = DictionaryDB()
        self.stats_mgr = StatsManager()
        self.sound_mgr = SoundManager()

        self.current_word = ""
        self.session_active = False
        self.session_words = []
        self.session_start_time = None

        # Создание виджетов
        self.create_widgets()
        self.create_layout()
        self.create_connections()

        # Загрузка словарей
        self.load_dictionaries()

    def create_widgets(self):
        # Прогресс-бар и слово
        self.progress_bar = CircularProgressBar()
        self.progress_bar.set_progress_color(QColor(52, 152, 219))
        self.progress_bar.font_size = 24

        self.word_label = QLabel("Нажмите Старт")
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.word_label.setStyleSheet("font-size: 48pt; font-weight: bold;")

        # Таймеры
        self.word_timer_label = QLabel("00:00")
        self.word_timer_label.setStyleSheet("font-size: 24pt;")

        self.session_timer_label = QLabel("Общее время: 00:00")
        self.session_timer_label.setStyleSheet("font-size: 14pt;")

        # Управление
        self.interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.interval_slider.setRange(30, 3600)  # 30 сек - 60 мин
        self.interval_slider.setValue(60)  # По умолчанию 1 мин
        self.interval_slider.setTickInterval(30)
        self.interval_slider.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(30, 3600)
        self.interval_spin.setValue(60)
        self.interval_spin.setSuffix(" сек")

        # Кнопки
        self.start_btn = QPushButton("Старт")
        self.pause_btn = QPushButton("Пауза")
        self.stop_btn = QPushButton("Стоп")
        self.stats_btn = QPushButton("Статистика")

        # Группа управления
        control_group = QGroupBox("Управление сессией")
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.stats_btn)
        control_group.setLayout(control_layout)

        # Группа интервала
        interval_group = QGroupBox("Интервал между словами")
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(self.interval_slider)
        interval_layout.addWidget(self.interval_spin)
        interval_group.setLayout(interval_layout)

        self.control_group = control_group
        self.interval_group = interval_group

        # Таймеры
        self.word_timer = QTimer()
        self.word_timer.setInterval(1000)  # Обновление каждую секунду

        self.session_timer = QTimer()
        self.session_timer.setInterval(1000)  # Обновление каждую секунду

    def create_layout(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Верхняя часть: таймеры
        timer_layout = QHBoxLayout()
        timer_layout.addWidget(self.word_timer_label)
        timer_layout.addStretch()
        timer_layout.addWidget(self.session_timer_label)

        # Центральная часть: прогресс и слово
        center_layout = QVBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(self.progress_bar, 0, Qt.AlignmentFlag.AlignCenter)
        center_layout.addWidget(self.word_label)
        center_layout.addStretch()

        main_layout.addLayout(timer_layout)
        main_layout.addLayout(center_layout, 1)
        main_layout.addWidget(self.interval_group)
        main_layout.addWidget(self.control_group)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_connections(self):
        self.start_btn.clicked.connect(self.start_session)
        self.pause_btn.clicked.connect(self.pause_session)
        self.stop_btn.clicked.connect(self.stop_session)
        self.stats_btn.clicked.connect(self.show_stats)

        self.interval_slider.valueChanged.connect(self.interval_spin.setValue)
        self.interval_spin.valueChanged.connect(self.interval_slider.setValue)

        self.word_timer.timeout.connect(self.update_word_timer)
        self.session_timer.timeout.connect(self.update_session_timer)

    def load_dictionaries(self):
        # Загрузка словарей из базы данных
        self.dictionaries = self.db.get_available_dictionaries()

    def start_session(self):
        if not self.session_active:
            self.sound_mgr.play("start")
            self.session_active = True
            self.session_words = []
            self.session_start_time = datetime.now()

            # Настройка таймеров
            current_interval = self.interval_spin.value()
            self.current_word_time_left = current_interval
            self.word_timer.start()
            self.session_timer.start()

            # Генерация первого слова
            self.generate_new_word()

            # Обновление интерфейса
            self.progress_bar.set_value(100)
            self.update_timers_display()

    def pause_session(self):
        if self.session_active:
            self.session_active = False
            self.word_timer.stop()
            self.sound_mgr.play("change")

    def stop_session(self):
        if self.session_active:
            self.session_active = False
            self.word_timer.stop()
            self.session_timer.stop()

            # Сохранение статистики
            if self.session_start_time:
                session_duration = (datetime.now() - self.session_start_time).total_seconds()
                self.stats_mgr.add_session(session_duration, self.session_words, ["Основной"])

            # Сброс интерфейса
            self.word_label.setText("Сессия завершена")
            self.progress_bar.set_value(0)
            self.word_timer_label.setText("00:00")
            self.session_timer_label.setText("Общее время: 00:00")

            # Воспроизведение звука в конце
            self.sound_mgr.play("finish")

    def generate_new_word(self):
        # Получаем новое слово из выбранных словарей
        self.current_word = self.db.get_random_word([1])  # ID основного словаря
        self.word_label.setText(self.current_word)
        self.session_words.append(self.current_word)
        self.sound_mgr.play("change")

        # Сброс таймера слова
        self.current_word_time_left = self.interval_spin.value()
        self.progress_bar.set_value(100)

    def update_word_timer(self):
        if self.session_active:
            self.current_word_time_left -= 1
            progress = (self.current_word_time_left / self.interval_spin.value()) * 100
            self.progress_bar.set_value(progress)

            if self.current_word_time_left <= 0:
                self.generate_new_word()

            self.update_timers_display()

    def update_session_timer(self):
        if self.session_active:
            elapsed = datetime.now() - self.session_start_time
            minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
            self.session_timer_label.setText(f"Общее время: {minutes:02d}:{seconds:02d}")

    def update_timers_display(self):
        # Отображение оставшегося времени для текущего слова
        minutes, seconds = divmod(self.current_word_time_left, 60)
        self.word_timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def show_stats(self):
        # Позже реализуем окно статистики
        print("Показ статистики")