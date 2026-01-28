from pathlib import Path

import sys

SRC_DIR = Path(__file__).resolve().parents[2] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codex_agent.core import Core


def test_core_answer_ping() -> None:
    assert Core().answer("ping") == {"reply": "pong"}


def test_core_answer_message() -> None:
    assert Core().answer("hello") == {"reply": "Processed: hello"}
