from pathlib import Path
import sys
import types

# ─── путь к src комм-агента (если скрипт запускают отдельно) ──────────────────
AGENTS_DIR = Path(__file__).resolve().parents[2]            # …/default/agents
COMM_SRC = AGENTS_DIR / "comm-agent" / "src"
sys.path.append(str(COMM_SRC))

# ─── псевдоним для внутреннего import'а codex-агента ──────────────────────────
from interfaces import com_agent_interface as _com_mod  # noqa: E402
sys.modules.setdefault("agents", types.ModuleType("agents"))
sys.modules["agents.com_agent"] = _com_mod

from codex_agent.core import Core  # noqa: E402


def main() -> None:
    agent = Core()
    print(agent.answer("Codex Agent стартовал"))


if __name__ == "__main__":
    main()
