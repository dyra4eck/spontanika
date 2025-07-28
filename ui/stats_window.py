# stats_window.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg


class StatsWindow(QWidget):
    def __init__(self, stats_manager):
        super().__init__()
        self.stats_mgr = stats_manager
        self.setWindowTitle("Статистика тренировок")
        self.setGeometry(300, 300, 800, 600)

        layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.setLayout(layout)

        self.update_plot()

    def update_plot(self):
        daily_data = self.stats_mgr.get_daily_stats()
        dates = sorted(daily_data.keys())
        minutes = [daily_data[date]["total_time"] / 60 for date in dates]

        self.plot_widget.clear()
        bar = pg.BarGraphItem(
            x=range(len(dates)),
            height=minutes,
            width=0.6
        )
        self.plot_widget.addItem(bar)

        self.plot_widget.setLabel('left', "Минут")
        self.plot_widget.setLabel('bottom', "Даты")
        self.plot_widget.getAxis('bottom').setTicks([[(i, date) for i, date in enumerate(dates)]])