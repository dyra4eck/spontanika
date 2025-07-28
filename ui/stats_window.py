from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QTabWidget
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import pyqtgraph as pg
from datetime import datetime


class StatsWindow(QWidget):
    def __init__(self, stats_manager):
        super().__init__()
        self.stats_mgr = stats_manager
        self.setWindowTitle("Статистика тренировок")
        self.setGeometry(300, 300, 800, 600)

        self.create_widgets()
        self.create_layout()
        self.update_data()

    def create_widgets(self):
        # Вкладки
        self.tabs = QTabWidget()

        # График активности
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setTitle("Активность по дням", color='k', size='12pt')
        self.plot_widget.setLabel('left', "Минут")
        self.plot_widget.setLabel('bottom', "Даты")
        self.plot_widget.showGrid(x=True, y=True)

        # Таблица сессий
        self.sessions_table = QTableWidget()
        self.sessions_table.setColumnCount(5)
        self.sessions_table.setHorizontalHeaderLabels([
            "Дата", "Длительность", "Слов", "Словари", "Слова"
        ])
        self.sessions_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.sessions_table.verticalHeader().setVisible(False)

        # Кнопки
        self.close_btn = QPushButton("Закрыть")
        self.export_btn = QPushButton("Экспорт в CSV")

    def create_layout(self):
        main_layout = QVBoxLayout()

        # Добавляем вкладки
        self.tabs.addTab(self.plot_widget, "График активности")
        self.tabs.addTab(self.sessions_table, "История сессий")
        main_layout.addWidget(self.tabs)

        # Кнопки внизу
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.close_btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # Подключение сигналов
        self.close_btn.clicked.connect(self.close)
        self.export_btn.clicked.connect(self.export_to_csv)

    def update_data(self):
        # Обновляем график
        daily_data = self.stats_mgr.get_daily_stats()
        dates = sorted(daily_data.keys())
        minutes = [daily_data[date]["total_time"] / 60 for date in dates]

        self.plot_widget.clear()
        bar = pg.BarGraphItem(
            x=range(len(dates)),
            height=minutes,
            width=0.6,
            brush=(52, 152, 219)
        )
        self.plot_widget.addItem(bar)
        self.plot_widget.getAxis('bottom').setTicks([[(i, date) for i, date in enumerate(dates)]])

        # Обновляем таблицу сессий
        sessions = self.stats_mgr.data.get("sessions", [])
        self.sessions_table.setRowCount(len(sessions))

        for i, session in enumerate(sessions):
            # Форматирование времени
            total_seconds = session["duration_sec"]
            minutes, seconds = divmod(total_seconds, 60)
            duration_str = f"{int(minutes):02d}:{int(seconds):02d}"

            # Форматирование даты
            dt = datetime.fromisoformat(session["timestamp"])
            date_str = dt.strftime("%d.%m.%Y %H:%M")

            # Заполнение строки
            self.sessions_table.setItem(i, 0, QTableWidgetItem(date_str))
            self.sessions_table.setItem(i, 1, QTableWidgetItem(duration_str))
            self.sessions_table.setItem(i, 2, QTableWidgetItem(str(session["words_count"])))
            self.sessions_table.setItem(i, 3, QTableWidgetItem(", ".join(session.get("dicts", []))))
            self.sessions_table.setItem(i, 4, QTableWidgetItem(", ".join(session["words"])))

    def export_to_csv(self):
        # Реализуем позже
        print("Экспорт в CSV")