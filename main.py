import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

# Настройка для Wayland (Fedora)
os.environ["QT_QPA_PLATFORM"] = "wayland"  # или "xcb" для X11


def main():
    app = QApplication(sys.argv)

    # Проверка платформы
    print("Запуск на платформе:", app.platformName())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()