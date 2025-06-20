from __future__ import annotations

from typing import Optional

from .protocols.codex_protocol import CodexProtocol
from .integrations.com_agent_bridge import ComAgentBridge


class Core(CodexProtocol):
    """Main Codex agent implementation."""

    def __init__(self) -> None:
        self.context: dict = {}
        self.bridge: Optional[ComAgentBridge] = None

    def load_context(self, ctx: dict) -> None:
        self.context.update(ctx)

    def answer(self, prompt: str) -> str:
        return f"Processed: {prompt}"

    def register_bridge(self, bridge: ComAgentBridge) -> None:
        self.bridge = bridge
