import argparse

from .core import Core


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the LAM Codex agent")
    parser.add_argument("message", nargs="*", help="Message to process")
    args = parser.parse_args()

    msg = " ".join(args.message).strip() or "Codex Agent starting"
    reply = Core().answer(msg)
    print(reply)
