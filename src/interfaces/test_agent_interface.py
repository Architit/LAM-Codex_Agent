from abc import ABC, abstractmethod
from typing import Any, Dict

class TestAgentInterface(ABC):
    """
    Интерфейс для Тестового Агента (Test Agent).

    Агент тестирования отвечает за выполнение проверок и тестов,
    выявляет ошибки и формирует отчёт о состоянии системы.
    """

    @abstractmethod
    def run_tests(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Запускает процесс тестирования данных.

        :param data: Входные данные для тестирования.
        :return: Результаты тестирования в виде словаря.
        """
        pass

    @abstractmethod
    def generate_report(self, test_results: Dict[str, Any]) -> str:
        """
        Генерирует отчёт по результатам тестов.

        :param test_results: Результаты, полученные в процессе тестирования.
        :return: Отчёт в виде строки.
        """
        pass
