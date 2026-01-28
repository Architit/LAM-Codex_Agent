from codex_agent.core import Core


def main() -> None:
    agent = Core()
    reply = agent.answer("Codex Agent starting")
    print(reply)


if __name__ == "__main__":
    main()
