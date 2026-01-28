#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMM_SRC="/mnt/c/Users/lkise/OneDrive/Documenten/GitHub/LAM/LAM/default/agents/comm-agent/src"
CODEX_SRC="$ROOT/src"

PYTHONPATH="$COMM_SRC:$CODEX_SRC" pytest -q -p no:cacheprovider "$@"
