from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ComAgent(Protocol):
    """
    Contract for comm-agent queue API.

    NOTE: Do NOT import comm-agent implementation here.
    This is a structural contract used across agent repos.
    """

    def register_agent(self, name: str, agent: Any) -> None: ...
    def send_data(self, recipient: str, data: Any) -> bool: ...
    def receive_data(self) -> tuple[str, Any]: ...


class ComAgentInterface(ABC):
    """
    Интерфейс Агента Связи (Communication Agent).
    """

    @abstractmethod
    def establish_connection(self, endpoint: str) -> bool:
        pass

    @abstractmethod
    def send_data(self, data: Any) -> bool:
        pass

    @abstractmethod
    def receive_data(self) -> Any:
        pass
