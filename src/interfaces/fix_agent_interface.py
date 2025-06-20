from abc import ABC, abstractmethod
from typing import Any, Dict

class FixAgentInterface(ABC):
    """
    Интерфейс Агента Исправлений (Fix Agent).

    Агент исправлений отвечает за анализ и устранение найденных проблем.
    """

    @abstractmethod
    def analyze_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Анализирует данные об ошибке для выявления причины.

        :param issue_data: Данные ошибки.
        :return: Результаты анализа (причина, локализация проблемы).
        """
        pass

    @abstractmethod
    def apply_fix(self, analysis_results: Dict[str, Any]) -> bool:
        """
        Применяет исправление на основе анализа.

        :param analysis_results: Результаты анализа.
        :return: Успешность выполнения исправления.
        """
        pass
