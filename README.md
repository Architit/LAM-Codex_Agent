# LAM-Codex_Agent

Small local scaffold for a Codex-style agent in the LAM ecosystem. Provides a
minimal Core with a simple answer method and optional bridge stubs.

## Structure

- `src/codex_agent/`: Core, protocols, integrations, CLI
- `src/agents/`: stub agents
- `src/core/`: memory core
- `start.py`: local launcher (adds `src` to `PYTHONPATH`)
- `reqs/requirements.txt`: dev tools
- `tests/`: placeholders

## Quick start (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python start.py
```

## Install as a package (editable)

```powershell
pip install -e .
lam-codex-agent ping
python -m codex_agent ping
```

## Notes

- `start.py` will also add a sibling `../comm-agent/src` to `PYTHONPATH` if it
  exists, so integration stubs can be resolved locally.
- `Core.answer("ping")` returns `{"reply": "pong"}`; other messages return
  `{"reply": "Processed: <message>"}`.

## Dev tools

```powershell
ruff src/
mypy src/
pytest tests/
```
