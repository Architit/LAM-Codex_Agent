from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[2] / "src"


def test_cli_smoke() -> None:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SRC_DIR) + (os.pathsep + existing if existing else "")

    result = subprocess.run(
        [sys.executable, "-m", "codex_agent", "ping"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert "pong" in result.stdout


def test_entrypoint_smoke() -> None:
    exe = "lam-codex-agent"
    if not shutil.which(exe):
        pytest.skip(f"{exe} not found on PATH; install editable package first")

    result = subprocess.run(
        [exe, "ping"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "pong" in result.stdout
