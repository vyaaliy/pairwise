"""
Модуль для экспорта сгенерированных тестовых данных.
"""

import csv
import io
from typing import Dict, List


def export_to_csv(data: List[Dict[str, str]], filepath: str) -> None:
    """
    Экспортирует тестовые данные в CSV-файл.

    Args:
        data: Список словарей с тестовыми комбинациями.
        filepath: Путь к файлу для сохранения.
    """
    if not data:
        return

    fieldnames = list(data[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def format_as_tsv(data: List[Dict[str, str]]) -> str:
    """
    Форматирует тестовые данные как TSV (tab-separated) для вставки в Excel / Google Sheets.

    Args:
        data: Список словарей с тестовыми комбинациями.

    Returns:
        Строка в формате TSV.
    """
    if not data:
        return ""

    fieldnames = list(data[0].keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()
