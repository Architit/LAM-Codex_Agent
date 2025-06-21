from pathlib import Path
import sys
import types

# ── добавляем пути к исходникам подмодулей ─────────────────────────────────────
BASE = Path(__file__).resolve().parents[3]             # .../LAM
COMM_SRC  = BASE / "LAM/default/agents/comm-agent/src"
CODEX_SRC = BASE / "LAM/default/agents/codex-agent/src"
sys.path.extend([str(COMM_SRC), str(CODEX_SRC)])

# ── делаем псевдоним, чтобы import "agents.com_agent" внутри Codex не падал ───
from interfaces import com_agent_interface as _com_mod  # type: ignore  # noqa: E402
sys.modules["agents"] = types.ModuleType("agents")
sys.modules["agents.com_agent"] = _com_mod

# ── основной кодекс-агент ─────────────────────────────────────────────────────
from codex_agent.core import Core  # noqa: E402


def main() -> None:
    agent = Core()
    print(agent.answer("Codex Agent стартовал"))


if __name__ == "__main__":
    main()
