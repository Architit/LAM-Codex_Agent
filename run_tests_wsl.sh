#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_ROOT="${ECO_WORK_ROOT:-$(cd "$ROOT/../../../../.." && pwd)}"
COMM_SRC="${COMM_SRC:-$WORK_ROOT/LAM/LAM/default/agents/comm-agent/src}"
CODEX_SRC="$ROOT/src"

PYTHONPATH="$COMM_SRC:$CODEX_SRC" pytest -q -p no:cacheprovider "$@"
