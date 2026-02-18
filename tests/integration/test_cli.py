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


def test_feedback_prepare_smoke(tmp_path: Path) -> None:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SRC_DIR) + (os.pathsep + existing if existing else "")

    input_log = tmp_path / "debug.jsonl"
    input_log.write_text(
        '{"ts_utc":"2026-02-18T00:00:00Z","level":"debug","channel":"codex.bridge.external.debug","message":"bridge.send_outbound","fields":{"ok":false,"error":"enqueue_failed","external_system":"codex_openai"}}\n',
        encoding="utf-8",
    )
    out_dir = tmp_path / "pack"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "codex_agent",
            "feedback",
            "prepare",
            "--input",
            str(input_log),
            "--out-dir",
            str(out_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert (out_dir / "OPENAI_FEEDBACK_BUNDLE.json").exists()
    assert (out_dir / "SUPPORT_TICKET_DRAFT.md").exists()
