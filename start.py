# LAM/default/agents/codex-agent/start.py
from pathlib import Path
import sys

# ➜  добавляем .../codex-agent/src в PYTHONPATH
SRC_DIR = Path(__file__).resolve().parent / "src"
sys.path.append(str(SRC_DIR))

from codex_agent.core import Core


def main() -> None:
    agent = Core()
    reply = agent.answer("Codex Agent стартовал")
    print(reply)


if __name__ == "__main__":
    main()
