from __future__ import annotations

from typing import Any

from interfaces.com_agent_interface import ComAgent


class StubComAgent:
    def __init__(self) -> None:
        self._agents: dict[str, Any] = {}
        self._queue: list[tuple[str, dict]] = []

    def register_agent(self, name: str, agent: Any) -> None:
        self._agents[name] = agent

    def send_data(self, recipient: str, data: Any) -> bool:
        self._queue.append((recipient, dict(data)))
        return True

    def receive_data(self) -> tuple[str, Any]:
        return self._queue.pop(0)


def test_bridge_send_outbound_queue_api():
    from codex_agent.integrations.com_agent_bridge import ComAgentBridge

    ca: ComAgent = StubComAgent()
    ca.register_agent("codex", object())

    bridge = ComAgentBridge(ca)
    assert bridge.send_outbound({"recipient": "codex", "ping": "pong"}) is True

    sender, msg = ca.receive_data()
    assert sender == "codex"
    assert msg["ping"] == "pong"
