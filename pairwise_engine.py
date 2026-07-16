"""
Модуль для генерации pairwise-набора тестовых данных.
"""

from typing import Dict, List, Tuple

from allpairspy import AllPairs


def generate_pairwise(parameters: Dict[str, List[str]]) -> List[Dict[str, str]]:
    """
    Генерирует pairwise-набор тестовых данных на основе переданных параметров.

    Args:
        parameters: Словарь вида {название_параметра: [список_значений]}

    Returns:
        Список словарей с тестовыми комбинациями.
    """
    if not parameters:
        return []

    param_names = list(parameters.keys())
    param_values = list(parameters.values())

    result: List[Dict[str, str]] = []

    for combo in AllPairs(param_values):
        row = dict(zip(param_names, combo))
        result.append(row)

    return result


def parse_parameters(
    raw_params: List[Tuple[str, str]],
) -> Dict[str, List[str]]:
    """
    Преобразует сырые данные из таблицы в словарь параметров.
    Каждая строка — (название_параметра, строка_значений_через_запятую).

    Returns:
        Словарь вида {название_параметра: [значение1, значение2, ...]}.

    Raises:
        ValueError: Если параметр пустой или не содержит значений.
    """
    parameters: Dict[str, List[str]] = {}

    for param_name, values_str in raw_params:
        name = param_name.strip()
        if not name:
            raise ValueError("Название параметра не может быть пустым.")

        values = [v.strip() for v in values_str.split(",") if v.strip()]
        if not values:
            raise ValueError(f"Параметр '{name}' не содержит значений.")

        parameters[name] = values

    return parameters
