"""Codex-agent standalone launcher."""

from __future__ import annotations

import sys
import types
from pathlib import Path

# ── добавляем путь к Communication-agent ────────────────────────────
BASE = Path(__file__).resolve().parents[3]        # …/LAM
COMM_SRC = BASE / "LAM/default/agents/comm-agent/src"
sys.path.insert(0, str(COMM_SRC))

# ── создаём псевдонимы, чтобы импорты не падали ─────────────────────
from interfaces import com_agent_interface as _com_mod  # type: ignore

sys.modules["com_agent"] = _com_mod
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

# ── Codex agent ─────────────────────────────────────────────────────
from codex_agent.core import Core


def main() -> None:
    agent = Core()
    print(agent.answer("Codex Agent стартовал"))


if __name__ == "__main__":
    main()
