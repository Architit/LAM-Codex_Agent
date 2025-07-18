from typing import Protocol


class CodexProtocol(Protocol):
    def answer(self, prompt: str) -> str: ...
    def load_context(self, ctx: dict) -> None: ...
