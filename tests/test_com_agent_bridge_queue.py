from __future__ import annotations

from typing import Any

import pytest

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


def test_bridge_emits_external_debug_log(monkeypatch: pytest.MonkeyPatch) -> None:
    from codex_agent.integrations import com_agent_bridge as bridge_module
    from codex_agent.integrations.com_agent_bridge import ComAgentBridge

    captured: list[tuple[str, str, str, dict[str, Any]]] = []

    def fake_log(level: str, channel: str, message: str, **fields: Any) -> None:
        captured.append((level, channel, message, fields))

    monkeypatch.setattr(bridge_module, "_lam_log", fake_log)

    ca: ComAgent = StubComAgent()
    ca.register_agent("codex", object())
    bridge = ComAgentBridge(ca)

    assert (
        bridge.send_outbound(
            {
                "recipient": "codex",
                "intent": "code_fix",
                "provider": "codex_openai",
                "context": {"trace_id": "trace-123", "task_id": "T-1"},
            }
        )
        is True
    )

    assert captured, "expected debug log event from bridge"
    level, channel, _, fields = captured[-1]
    assert level == "debug"
    assert channel == "codex.bridge.external.debug"
    assert fields["external_system"] == "codex_openai"
    assert fields["trace_id"] == "trace-123"
