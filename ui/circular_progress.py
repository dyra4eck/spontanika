from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from PyQt6.QtCore import Qt, QRectF, QSize  # Добавлен импорт QSize


class CircularProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.max_value = 100
        self.width = 200
        self.height = 200
        self.progress_width = 10
        self.progress_color = QColor(41, 128, 185)
        self.text_color = QColor(50, 50, 50)
        self.font_size = 16
        self.setFixedSize(self.width, self.height)  # Установка фиксированного размера

    def set_value(self, value):
        self.value = min(max(0, value), self.max_value)
        self.update()

    def set_progress_color(self, color):
        self.progress_color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Фон
        painter.fillRect(self.rect(), self.palette().window())

        # Размеры для рисования
        side = min(self.width, self.height)
        rect = QRectF(0, 0, side, side)
        rect.adjust(self.progress_width, self.progress_width,
                    -self.progress_width, -self.progress_width)

        # Рисуем базовую окружность
        pen = QPen()
        pen.setColor(QColor(200, 200, 200))
        pen.setWidth(self.progress_width)
        painter.setPen(pen)
        painter.drawEllipse(rect)

        # Рисуем прогресс
        if self.value > 0:
            pen.setColor(self.progress_color)
            painter.setPen(pen)
            span = int(360 * 16 * (self.value / self.max_value))
            painter.drawArc(rect, 90 * 16, -span)

        # Рисуем текст
        painter.setPen(QPen(self.text_color))
        painter.setFont(QFont("Arial", self.font_size))
        text = f"{int(self.value)}%"
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(self.width, self.height)  # Возвращаем QSize вместо кортежа