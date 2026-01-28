from __future__ import annotations

from interfaces.com_agent_interface import ComAgent  # comm-agent queue API

from ..protocols.agent_protocol import AgentProtocol


class ComAgentBridge(AgentProtocol):
    """Bridge CodexAgent ↔ ComAgent (queue-based)."""

    def __init__(self, com_agent: ComAgent) -> None:
        self.com_agent = com_agent

    @staticmethod
    def _recipient(data: dict) -> str:
        r = data.get("recipient") or data.get("to") or data.get("target")
        if not r:
            raise ValueError("Missing recipient in data['recipient'|'to'|'target']")
        return str(r)

    def handle_inbound(self, data: dict) -> None:
        # inbound → кладём в очередь адресату
        self.com_agent.send_data(self._recipient(data), data)

    def send_outbound(self, data: dict) -> bool:
        # outbound → кладём в очередь адресату
        try:
            return self.com_agent.send_data(self._recipient(data), data)
        except Exception:
            return False
