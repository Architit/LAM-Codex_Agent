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
pytest tests/  # expects `lam-codex-agent` on PATH (pip install -e .)
```

## Gemini Flash Bridge (`flash_brain.py`)

Fast CLI for low-friction prompts and async note offloading.

Setup:

```powershell
pip install -q -U google-genai
$env:GEMINI_API_KEY="YOUR_KEY"
```

Quick use:

```powershell
python flash_brain.py ask "сделай скелет модуля памяти для LAM"
python flash_brain.py ask --prompt-file .\notes\idea.txt --save .\drafts\idea.flash.md
python flash_brain.py offload --input-dir .\notes\inbox --output-dir .\notes\outbox
```

Notes:
- Default model fallback chain: `gemini-3-flash,gemini-2.5-flash`
- Override with `--models` or env `GEMINI_FLASH_MODELS`
