from typing import Protocol


class AgentProtocol(Protocol):
    """General protocol for communication bridges."""

    def handle_inbound(self, data: dict) -> None:
        """Handle inbound data from an external agent."""
        ...

    def send_outbound(self, data: dict) -> bool:
        """Send data outbound to an external agent."""
        ...
