from codex_agent.core import Core


def main() -> None:
    agent = Core()
    reply = agent.answer("Codex Agent стартовал")
    print(reply)
