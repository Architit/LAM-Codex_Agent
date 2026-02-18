#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Resolve workspace root robustly across standalone and nested-monorepo layouts.
if [[ -n "${ECO_WORK_ROOT:-}" ]]; then
  WORK_ROOT="$ECO_WORK_ROOT"
elif [[ -d "$ROOT/../LAM/LAM/default/agents/comm-agent/src" ]]; then
  WORK_ROOT="$(cd "$ROOT/.." && pwd)"
else
  WORK_ROOT="$(cd "$ROOT/../../../../.." && pwd)"
fi

COMM_SRC="${COMM_SRC:-$WORK_ROOT/LAM/LAM/default/agents/comm-agent/src}"
CODEX_SRC="$ROOT/src"

PYTHONPATH="$COMM_SRC:$CODEX_SRC" pytest -q -p no:cacheprovider "$@"
