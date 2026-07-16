from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QFileDialog,
)

from typing import Dict, List

from pairwise_engine import generate_pairwise, parse_parameters
from export import export_to_csv, format_as_tsv


class MainWindow(QMainWindow):
    """Главное окно приложения Pairwise Test Case Generator."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pairwise Test Case Generator")
        self.resize(900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # --- Таблица параметров ---
        self.param_table = QTableWidget(0, 2)
        self.param_table.setHorizontalHeaderLabels(["Параметр", "Значения (через запятую)"])
        self.param_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.param_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.param_table.setAlternatingRowColors(True)
        self.param_table.itemChanged.connect(self._update_buttons_state)
        layout.addWidget(self.param_table)

        # --- Кнопки управления параметрами ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.add_btn = QPushButton("Добавить параметр")
        self.add_btn.clicked.connect(self.add_parameter)
        btn_layout.addWidget(self.add_btn)

        self.remove_btn = QPushButton("Удалить выбранный")
        self.remove_btn.clicked.connect(self.remove_parameter)
        btn_layout.addWidget(self.remove_btn)

        btn_layout.addStretch()

        self.generate_btn = QPushButton("Сгенерировать")
        self.generate_btn.clicked.connect(self.generate)
        self.generate_btn.setEnabled(False)
        btn_layout.addWidget(self.generate_btn)

        layout.addLayout(btn_layout)

        # --- Таблица результатов ---
        self.result_table = QTableWidget(0, 0)
        self.result_table.setHorizontalHeaderLabels(["Результат"])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.result_table.setAlternatingRowColors(True)
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.result_table)

        # --- Кнопки экспорта ---
        export_layout = QHBoxLayout()
        export_layout.setSpacing(8)

        self.export_csv_btn = QPushButton("Экспорт в CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.export_csv_btn.setEnabled(False)
        export_layout.addWidget(self.export_csv_btn)

        self.copy_btn = QPushButton("Копировать в буфер обмена")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setEnabled(False)
        export_layout.addWidget(self.copy_btn)

        export_layout.addStretch()
        layout.addLayout(export_layout)

        # Хранилище последнего сгенерированного результата
        self._last_result: List[Dict[str, str]] = []

    def _update_buttons_state(self):
        """Обновляет состояние кнопок в зависимости от наличия данных."""
        has_rows = self.param_table.rowCount() > 0
        self.generate_btn.setEnabled(has_rows)

    def add_parameter(self):
        """Добавляет новую строку в таблицу параметров."""
        self.param_table.blockSignals(True)
        row = self.param_table.rowCount()
        self.param_table.insertRow(row)
        self.param_table.setItem(row, 0, QTableWidgetItem(""))
        self.param_table.setItem(row, 1, QTableWidgetItem(""))
        self.param_table.blockSignals(False)
        self._update_buttons_state()

    def remove_parameter(self):
        """Удаляет выбранную строку из таблицы параметров."""
        current_row = self.param_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Удаление", "Выберите строку для удаления.")
            return
        self.param_table.removeRow(current_row)
        self._update_buttons_state()

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
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка ввода", str(error))
            return

        # Генерируем pairwise-комбинации
        result = generate_pairwise(parameters)

        if not result:
            QMessageBox.information(
                self, "Результат", "Не удалось сгенерировать комбинации.\n"
                "Проверьте корректность введённых данных."
            )
            return

        # Сохраняем результат для экспорта/копирования
        self._last_result = result

        # Заполняем таблицу результатов
        param_names = list(parameters.keys())
        self.result_table.setColumnCount(len(param_names))
        self.result_table.setHorizontalHeaderLabels(param_names)
        self.result_table.setRowCount(len(result))

        for row_idx, combo in enumerate(result):
            for col_idx, name in enumerate(param_names):
                self.result_table.setItem(
                    row_idx, col_idx, QTableWidgetItem(combo[name])
                )

        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.export_csv_btn.setEnabled(True)
        self.copy_btn.setEnabled(True)

    def export_csv(self):
        """Экспортирует результат в CSV-файл."""
        if not self._last_result:
            QMessageBox.warning(self, "Экспорт", "Сначала сгенерируйте комбинации.")
            return

        filepath, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как CSV", "", "CSV файлы (*.csv)"
        )
        if not filepath:
            return

        export_to_csv(self._last_result, filepath)
        QMessageBox.information(self, "Экспорт", f"Данные сохранены в:\n{filepath}")

    def copy_to_clipboard(self):
        """Копирует результат в буфер обмена в формате TSV для Excel / Google Sheets."""
        if not self._last_result:
            QMessageBox.warning(self, "Копирование", "Сначала сгенерируйте комбинации.")
            return

        tsv_text = format_as_tsv(self._last_result)
        clipboard = QApplication.clipboard()
        clipboard.setText(tsv_text)
        QMessageBox.information(
            self,
            "Копирование",
            "Данные скопированы в буфер обмена.\n"
            "Вставьте в Excel или Google Sheets (Ctrl+V / Cmd+V).",
        )
