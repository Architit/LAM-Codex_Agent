from __future__ import annotations

from agents.com_agent import ComAgent  # type: ignore[import]

from ..protocols.agent_protocol import AgentProtocol


class ComAgentBridge(AgentProtocol):
    """Bridge connecting CodexAgent with a ComAgent instance."""

    def __init__(self, com_agent: ComAgent) -> None:
        self.com_agent = com_agent

    def handle_inbound(self, data: dict) -> None:
        """Forward inbound data to the communication agent."""
        self.com_agent.communicate(data)

    def send_outbound(self, data: dict) -> bool:
        """Send outbound data via the communication agent."""
        try:
            self.com_agent.communicate(data)
            return True
        except Exception:
            return False
