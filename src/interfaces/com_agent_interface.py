from abc import ABC, abstractmethod
from typing import Any

# Forward import of actual ComAgent class for convenience
from agents.com_agent import ComAgent

class ComAgentInterface(ABC):
    """
    Интерфейс Агента Связи (Communication Agent).

    Агент связи отвечает за коммуникацию между агентами и ядром системы.
    """

    @abstractmethod
    def establish_connection(self, endpoint: str) -> bool:
        """
        Устанавливает соединение с указанной конечной точкой.

        :param endpoint: Адрес конечной точки.
        :return: Статус успешности соединения.
        """
        pass

    @abstractmethod
    def send_data(self, data: Any) -> bool:
        """
        Отправляет данные на конечную точку.

        :param data: Данные для отправки.
        :return: Статус успешности отправки.
        """
        pass

    @abstractmethod
    def receive_data(self) -> Any:
        """
        Получает данные от конечной точки.

        :return: Полученные данные.
        """
        pass
