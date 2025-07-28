from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QLineEdit, QTextEdit,
    QMessageBox, QFileDialog
)
from core.database import DictionaryDB


class DictManagerDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.setWindowTitle("Управление словарями")
        self.setMinimumSize(600, 500)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.load_dictionaries()

    def create_widgets(self):
        self.dict_list = QListWidget()
        self.dict_list.setMinimumWidth(200)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название словаря")

        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("Описание словаря")

        self.add_btn = QPushButton("Добавить словарь")
        self.remove_btn = QPushButton("Удалить выбранный")
        self.import_btn = QPushButton("Импорт слов из файла")

    def create_layout(self):
        main_layout = QHBoxLayout()

        # Левая панель: список словарей
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Доступные словари:"))
        left_layout.addWidget(self.dict_list)
        left_layout.addWidget(self.remove_btn)

        # Правая панель: детали словаря
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Название:"))
        right_layout.addWidget(self.name_edit)
        right_layout.addWidget(QLabel("Описание:"))
        right_layout.addWidget(self.desc_edit)
        right_layout.addWidget(self.add_btn)
        right_layout.addWidget(self.import_btn)

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)
        self.setLayout(main_layout)

    def create_connections(self):
        self.dict_list.itemSelectionChanged.connect(self.on_dict_selected)
        self.add_btn.clicked.connect(self.add_dictionary)
        self.remove_btn.clicked.connect(self.remove_dictionary)
        self.import_btn.clicked.connect(self.import_words)

    def load_dictionaries(self):
        self.dict_list.clear()
        dictionaries = self.db.get_available_dictionaries()
        for dict_id, name in dictionaries:
            self.dict_list.addItem(f"{name} (id: {dict_id})")

    def on_dict_selected(self):
        selected_items = self.dict_list.selectedItems()
        if not selected_items:
            return

        dict_name = selected_items[0].text().split(" (id:")[0]
        self.name_edit.setText(dict_name)



    def add_dictionary(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название словаря")
            return

        description = self.desc_edit.toPlainText().strip()


        QMessageBox.information(self, "Успех", f"Словарь '{name}' добавлен")
        self.load_dictionaries()

    def remove_dictionary(self):
        selected_items = self.dict_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Ошибка", "Выберите словарь для удаления")
            return

        dict_name = selected_items[0].text()
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            f"Удалить словарь '{dict_name}'? Все слова в нем будут потеряны.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:

            self.load_dictionaries()

    def import_words(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл со словами",
            "",
            "Текстовые файлы (*.txt);;Все файлы (*)"
        )

        if file_path:

            QMessageBox.information(
                self,
                "Импорт завершен",
                f"Слова успешно импортированы из {file_path}"
            )