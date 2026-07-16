from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)
from PySide6.QtCore import Qt

from pairwise_engine import generate_pairwise, parse_parameters


class MainWindow(QMainWindow):
    """Главное окно приложения Pairwise Test Case Generator."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pairwise Test Case Generator")
        self.resize(900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # --- Таблица параметров ---
        self.param_table = QTableWidget(0, 2)
        self.param_table.setHorizontalHeaderLabels(["Параметр", "Значения (через запятую)"])
        self.param_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.param_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.param_table)

        # --- Кнопки управления параметрами ---
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton("Добавить параметр")
        self.add_btn.clicked.connect(self.add_parameter)
        btn_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Удалить выбранный параметр")
        self.remove_btn.clicked.connect(self.remove_parameter)
        btn_layout.addWidget(self.remove_btn)

        self.generate_btn = QPushButton("Сгенерировать")
        self.generate_btn.clicked.connect(self.generate)
        btn_layout.addWidget(self.generate_btn)

        layout.addLayout(btn_layout)

        # --- Таблица результатов ---
        self.result_table = QTableWidget(0, 0)
        self.result_table.setHorizontalHeaderLabels(["Результат"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.result_table)

    def add_parameter(self):
        """Добавляет новую строку в таблицу параметров."""
        row = self.param_table.rowCount()
        self.param_table.insertRow(row)
        self.param_table.setItem(row, 0, QTableWidgetItem(""))
        self.param_table.setItem(row, 1, QTableWidgetItem(""))

    def remove_parameter(self):
        """Удаляет выбранную строку из таблицы параметров."""
        current_row = self.param_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите параметр для удаления.")
            return
        self.param_table.removeRow(current_row)

    def generate(self):
        """Считывает параметры, генерирует pairwise-комбинации и выводит результат."""
        # Собираем данные из таблицы параметров
        raw_params = []
        for row in range(self.param_table.rowCount()):
            name_item = self.param_table.item(row, 0)
            values_item = self.param_table.item(row, 1)
            name = name_item.text() if name_item else ""
            values = values_item.text() if values_item else ""
            raw_params.append((name, values))

        # Парсим и валидируем
        try:
            parameters = parse_parameters(raw_params)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка ввода", str(e))
            return

        if not parameters:
            QMessageBox.warning(self, "Ошибка", "Нет параметров для генерации.")
            return

        # Генерируем pairwise-комбинации
        result = generate_pairwise(parameters)

        if not result:
            QMessageBox.information(self, "Результат", "Не удалось сгенерировать комбинации.")
            return

        # Заполняем таблицу результатов
        param_names = list(parameters.keys())
        self.result_table.setColumnCount(len(param_names))
        self.result_table.setHorizontalHeaderLabels(param_names)
        self.result_table.setRowCount(len(result))

        for row_idx, combo in enumerate(result):
            for col_idx, name in enumerate(param_names):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(combo[name]))

        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
