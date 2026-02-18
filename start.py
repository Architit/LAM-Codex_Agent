from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

# Optional support for a sibling comm-agent repo if present.
COMM_SRC = PROJECT_ROOT.parent / "comm-agent" / "src"
if COMM_SRC.exists():
    sys.path.insert(0, str(COMM_SRC))

from codex_agent.core import Core  # noqa: E402


def main() -> None:
    agent = Core()
    print(agent.answer("Codex Agent starting"))


if __name__ == "__main__":
    main()
