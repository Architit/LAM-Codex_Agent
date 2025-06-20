from typing import Protocol


class CodexProtocol(Protocol):
    """Protocol for Codex agents."""

    def answer(self, prompt: str) -> str:
        """Return answer for given prompt."""
        ...

    def load_context(self, ctx: dict) -> None:
        """Load persistent context for agent."""
        ...
