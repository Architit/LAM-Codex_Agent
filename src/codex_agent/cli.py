from __future__ import annotations

import sys

from .core import Core
from .feedback import main_feedback


def main() -> None:
    # Backward-compatible behavior:
    # `lam-codex-agent ping` still works as before.
    argv = sys.argv[1:]
    if not argv:
        print(Core().answer("Codex Agent starting"))
        return

    if argv[0] == "feedback":
        raise SystemExit(main_feedback(argv[1:]))

    msg = " ".join(argv).strip() or "Codex Agent starting"
    print(Core().answer(msg))
