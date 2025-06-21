"""
LAM Codex-agent standalone launcher.

Запускает Codex-агент из подмодуля и делает shim,
чтобы его импорт «agents.com_agent» не падал.
"""

from pathlib import Path
import importlib
import sys
import types

# ───────────────────────────────────────────────────────────────────────────────
# Пути к src-папкам обоих агентов
# <repo>/LAM
ROOT = Path(__file__).resolve().parents[2]           # ← корень репозитория

COMM_SRC = ROOT / "LAM" / "default" / "agents" / "comm-agent" / "src"
CODEX_SRC = ROOT / "LAM" / "default" / "agents" / "codex-agent" / "src"
sys.path.insert(0, str(COMM_SRC))  # comm-agent первым
sys.path.insert(0, str(CODEX_SRC))  # codex-agent вторым

# ───────────────────────────────────────────────────────────────────────────────
# Шим: agents.com_agent → настоящий ComAgent
from interfaces import com_agent_interface as _com_mod  # type: ignore  # noqa: E402

sys.modules["com_agent"] = _com_mod
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

# ───────────────────────────────────────────────────────────────────────────────
# Codex-agent
from codex_agent.core import Core  # noqa: E402


def main() -> None:
    agent = Core()
    print(agent.answer("Codex Agent стартовал"))


if __name__ == "__main__":
    main()
