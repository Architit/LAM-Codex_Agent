from __future__ import annotations

from agents.com_agent import ComAgent  # type: ignore[import]

from ..protocols.agent_protocol import AgentProtocol


class ComAgentBridge(AgentProtocol):
    """Bridge CodexAgent ↔ ComAgent."""

    def __init__(self, com_agent: ComAgent) -> None:
        self.com_agent = com_agent

    def handle_inbound(self, data: dict) -> None:
        self.com_agent.communicate(data)

    def send_outbound(self, data: dict) -> bool:
        try:
            self.com_agent.communicate(data)
            return True
        except Exception:
            return False
