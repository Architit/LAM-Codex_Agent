from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from codex_agent.feedback import prepare_support_pack, verify_support_receipt


def test_prepare_support_pack_writes_required_files(tmp_path: Path) -> None:
    log = tmp_path / "debug.jsonl"
    event = {
        "ts_utc": "2026-02-18T00:00:00Z",
        "level": "debug",
        "channel": "codex.bridge.external.debug",
        "message": "bridge.send_outbound",
        "fields": {
            "ok": False,
            "error": "enqueue_failed",
            "external_system": "codex_openai",
            "api_key": "sk-secret",
        },
    }
    log.write_text(json.dumps(event) + "\n", encoding="utf-8")

    out = prepare_support_pack(log, tmp_path / "artifacts")
    assert out["bundle_json"].exists()
    assert out["bundle_md"].exists()
    assert out["ticket_draft"].exists()
    assert out["receipt_template"].exists()

    bundle = json.loads(out["bundle_json"].read_text(encoding="utf-8"))
    assert bundle["summary"]["critical_incidents"] == 1
    sample_fields = bundle["incidents"][0]["sample"]["fields"]
    assert sample_fields["api_key"] == "<redacted>"


def test_verify_support_receipt_happy_path(tmp_path: Path) -> None:
    submitted = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
    receipt = {
        "schema_version": "1.0",
        "status": "MANUAL_SUBMISSION_CONFIRMED",
        "evidence": {
            "platform": "help.openai.com",
            "case_id": "ABC-123",
            "submitted_by": "user@example.com",
            "submitted_at_utc": submitted,
            "attachments_included": ["OPENAI_FEEDBACK_BUNDLE.json"],
        },
        "operator_signoff": {"acknowledged": True, "notes": "ok"},
    }
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    assert verify_support_receipt(path, max_age_hours=100000) == []


def test_verify_support_receipt_fails_without_case_id(tmp_path: Path) -> None:
    submitted = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
    receipt = {
        "schema_version": "1.0",
        "status": "MANUAL_SUBMISSION_CONFIRMED",
        "evidence": {
            "platform": "help.openai.com",
            "case_id": "",
            "submitted_by": "user@example.com",
            "submitted_at_utc": submitted,
            "attachments_included": ["OPENAI_FEEDBACK_BUNDLE.json"],
        },
        "operator_signoff": {"acknowledged": True, "notes": "ok"},
    }
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    errors = verify_support_receipt(path, max_age_hours=100000)
    assert any("case_id" in e for e in errors)
