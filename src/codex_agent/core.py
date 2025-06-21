"""
codex_agent/core.py
Минимальная рабочая логика Codex-агента
Ping → Pong, иначе эхо-ответ.
"""

from __future__ import annotations

from typing import Any, Dict


class Core:
    """
    Очень простой Codex-агент:
    – хранит имя (по умолчанию «codex»)
    – умеет отвечать на сообщения через метод ``answer``.
    """

    def __init__(self, name: str = "codex") -> None:
        self.name = name

    # ────────────────────────────────────────────────────────────────
    def answer(self, data: str | Dict[str, Any]) -> Dict[str, str]:
        """
        Возвращает ответ в формате ``{"reply": <…>}``.

        • если пришёл ping (в любом регистре) → ``{"reply": "pong"}``;
        • иначе → ``{"reply": "Processed: <исходный текст>"}``.

        ``data`` может быть строкой или словарём вида ``{"msg": "<текст>"}``.
        """
        # поддерживаем оба формата входа
        if isinstance(data, dict) and "msg" in data:
            msg = str(data["msg"])
        else:
            msg = str(data)

        if msg.strip().lower() == "ping":
            return {"reply": "pong"}

        return {"reply": f"Processed: {msg}"}

    # ────────────────────────────────────────────────────────────────
    def __repr__(self) -> str:  # для удобного вывода
        return f"<Core agent '{self.name}'>"


# локальный запуск: python core.py
if __name__ == "__main__":
    agent = Core()
    print(agent.answer("ping"))        # → {'reply': 'pong'}
    print(agent.answer({"msg": "hi"})) # → {'reply': 'Processed: hi'}
