from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REDACT_KEYS = {
    "authorization",
    "token",
    "api_key",
    "apikey",
    "secret",
    "password",
    "bearer",
    "openai_api_key",
}


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not path.exists():
        return out
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except Exception:
            continue
        if isinstance(item, dict):
            out.append(item)
    return out


def _lower(value: Any) -> str:
    return str(value or "").lower()


def _is_external_debug_event(event: dict[str, Any]) -> bool:
    channel = _lower(event.get("channel"))
    if channel.startswith("comm.external.") or channel.startswith("codex.bridge.external."):
        return True
    fields = event.get("fields")
    if not isinstance(fields, dict):
        return False
    return _lower(fields.get("external_system")) in {"codex_openai", "openai_codex", "openai"}


def _sanitize(value: Any, key_hint: str = "") -> Any:
    if any(k in _lower(key_hint) for k in REDACT_KEYS):
        return "<redacted>"
    if isinstance(value, dict):
        return {str(k): _sanitize(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize(v, key_hint) for v in value]
    if isinstance(value, str):
        if "bearer " in value.lower():
            return "<redacted>"
        return value if len(value) <= 1200 else value[:1200] + "...<truncated>"
    return value


def _severity(event: dict[str, Any]) -> str:
    level = _lower(event.get("level"))
    fields = event.get("fields")
    if not isinstance(fields, dict):
        fields = {}
    if level in {"critical", "fatal", "error"}:
        return "critical"
    if fields.get("ok") is False:
        return "critical"
    if _lower(fields.get("error")):
        return "critical"
    if level in {"warn", "warning"}:
        return "high"
    return "info"


def _fingerprint(event: dict[str, Any]) -> str:
    fields = event.get("fields")
    if not isinstance(fields, dict):
        fields = {}
    signature = {
        "channel": event.get("channel"),
        "message": event.get("message"),
        "external_system": fields.get("external_system"),
        "intent": fields.get("intent"),
        "action": fields.get("action"),
        "operation": fields.get("operation"),
        "error": fields.get("error"),
    }
    blob = json.dumps(signature, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def build_feedback_bundle(debug_log: Path, max_incidents: int = 200) -> dict[str, Any]:
    events = _read_jsonl(debug_log)
    external = [x for x in events if _is_external_debug_event(x)]
    grouped: dict[str, dict[str, Any]] = {}

    for ev in external:
        fp = _fingerprint(ev)
        sev = _severity(ev)
        ts = str(ev.get("ts_utc") or "")
        fields = ev.get("fields")
        if not isinstance(fields, dict):
            fields = {}

        row = grouped.get(fp)
        if row is None:
            row = {
                "incident_id": fp[:16],
                "fingerprint": fp,
                "count": 0,
                "severity": sev,
                "first_seen_utc": ts,
                "last_seen_utc": ts,
                "channel": ev.get("channel"),
                "message": ev.get("message"),
                "external_system": fields.get("external_system"),
                "error": fields.get("error"),
                "intent": fields.get("intent"),
                "action": fields.get("action"),
                "operation": fields.get("operation"),
                "sample": _sanitize(ev),
            }
            grouped[fp] = row

        row["count"] += 1
        if ts and (not row["first_seen_utc"] or ts < row["first_seen_utc"]):
            row["first_seen_utc"] = ts
        if ts and (not row["last_seen_utc"] or ts > row["last_seen_utc"]):
            row["last_seen_utc"] = ts
        if row["severity"] != "critical" and sev == "critical":
            row["severity"] = "critical"

    incidents = sorted(grouped.values(), key=lambda x: (-int(x["count"]), str(x["severity"])))
    incidents = incidents[: max(1, max_incidents)]

    critical = sum(1 for x in incidents if x.get("severity") == "critical")
    high = sum(1 for x in incidents if x.get("severity") == "high")

    return {
        "generated_at_utc": _now_utc(),
        "source_file": str(debug_log),
        "total_events": len(events),
        "external_events": len(external),
        "summary": {
            "incidents": len(incidents),
            "critical_incidents": critical,
            "high_incidents": high,
        },
        "incidents": incidents,
    }


def render_bundle_md(bundle: dict[str, Any]) -> str:
    summary = bundle.get("summary") if isinstance(bundle, dict) else {}
    if not isinstance(summary, dict):
        summary = {}
    lines = [
        "# OPENAI_FEEDBACK_BUNDLE",
        "",
        f"- generated_at_utc: {bundle.get('generated_at_utc')}",
        f"- source_file: {bundle.get('source_file')}",
        f"- total_events: {bundle.get('total_events')}",
        f"- external_events: {bundle.get('external_events')}",
        f"- incidents: {summary.get('incidents', 0)}",
        f"- critical_incidents: {summary.get('critical_incidents', 0)}",
        "",
        "## Top Incidents",
        "",
        "| severity | count | channel | error | external_system | incident_id |",
        "|---|---:|---|---|---|---|",
    ]
    incidents = bundle.get("incidents")
    if isinstance(incidents, list):
        for it in incidents[:50]:
            if not isinstance(it, dict):
                continue
            lines.append(
                f"| {it.get('severity','')} | {it.get('count',0)} | {it.get('channel','')} | {it.get('error','')} | {it.get('external_system','')} | {it.get('incident_id','')} |"
            )
    lines.append("")
    return "\n".join(lines)


def _draft_md(bundle: dict[str, Any]) -> str:
    incidents = bundle.get("incidents")
    top: dict[str, Any] = {}
    if isinstance(incidents, list) and incidents and isinstance(incidents[0], dict):
        top = incidents[0]
    return "\n".join(
        [
            "# OpenAI Support Ticket Request",
            "",
            "**Subject:** Critical API Incident Report (Automated Bundle)",
            "",
            "**Description:**",
            "We detected critical failures in our integration.",
            "- Environment: PROD/TEST",
            f"- Timestamp (UTC): {bundle.get('generated_at_utc')}",
            f"- Error Code/Type: {top.get('error', '{{ERROR_TYPE_FROM_LOG}}')}",
            "",
            "**Steps to Reproduce:**",
            "1. See attached `OPENAI_FEEDBACK_BUNDLE.md` for full execution trace.",
            f"2. Request ID: `{top.get('incident_id', '{{REQUEST_ID}}')}`",
            "",
            "**Attachments:**",
            "1. `OPENAI_FEEDBACK_BUNDLE.json` (Technical logs)",
            "2. `OPENAI_FEEDBACK_BUNDLE.md` (Human readable summary)",
            "",
        ]
    )


def _receipt_template() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": "MANUAL_SUBMISSION_CONFIRMED",
        "evidence": {
            "platform": "help.openai.com",
            "case_id": "YOUR_TICKET_ID_HERE",
            "submitted_by": "user@email.com",
            "submitted_at_utc": "2026-02-18T10:00:00Z",
            "attachments_included": [
                "OPENAI_FEEDBACK_BUNDLE.json",
                "OPENAI_FEEDBACK_BUNDLE.md",
            ],
        },
        "operator_signoff": {
            "acknowledged": True,
            "notes": "Ticket created, waiting for response.",
        },
    }


def prepare_support_pack(
    input_log: Path,
    out_dir: Path,
    max_incidents: int = 200,
    allow_empty_input: bool = False,
) -> dict[str, Path]:
    if not input_log.exists() and not allow_empty_input:
        raise FileNotFoundError(f"debug input log not found: {input_log}")

    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = build_feedback_bundle(input_log, max_incidents=max_incidents)

    bundle_json = out_dir / "OPENAI_FEEDBACK_BUNDLE.json"
    bundle_md = out_dir / "OPENAI_FEEDBACK_BUNDLE.md"
    draft_md = out_dir / "SUPPORT_TICKET_DRAFT.md"
    receipt_tpl = out_dir / "SUPPORT_RECEIPT_TEMPLATE.json"

    bundle_json.write_text(json.dumps(bundle, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    bundle_md.write_text(render_bundle_md(bundle), encoding="utf-8")
    draft_md.write_text(_draft_md(bundle), encoding="utf-8")
    receipt_tpl.write_text(json.dumps(_receipt_template(), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return {
        "bundle_json": bundle_json,
        "bundle_md": bundle_md,
        "ticket_draft": draft_md,
        "receipt_template": receipt_tpl,
    }


def _parse_utc(raw: str) -> datetime | None:
    text = str(raw or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except Exception:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def verify_support_receipt(path: Path, max_age_hours: int = 168) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"missing receipt: {path}"]
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"invalid json: {exc}"]
    if not isinstance(doc, dict):
        return ["receipt must be a JSON object"]

    evidence = doc.get("evidence")
    signoff = doc.get("operator_signoff")

    if str(doc.get("schema_version", "")) != "1.0":
        errors.append("schema_version must be 1.0")
    if str(doc.get("status", "")).strip() != "MANUAL_SUBMISSION_CONFIRMED":
        errors.append("status must equal MANUAL_SUBMISSION_CONFIRMED")
    if not isinstance(evidence, dict):
        errors.append("evidence must be object")
        evidence = {}
    if not isinstance(signoff, dict):
        errors.append("operator_signoff must be object")
        signoff = {}

    case_id = str(evidence.get("case_id", "")).strip()
    if not case_id or case_id == "YOUR_TICKET_ID_HERE":
        errors.append("evidence.case_id must be a real non-empty ticket id")

    attachments = evidence.get("attachments_included")
    if not isinstance(attachments, list):
        errors.append("evidence.attachments_included must be list")
        attachments = []
    required = {"OPENAI_FEEDBACK_BUNDLE.json", "OPENAI_FEEDBACK_BUNDLE.md"}
    missing_required = sorted(required.difference({str(x) for x in attachments}))
    if missing_required:
        errors.append(f"evidence.attachments_included missing required: {', '.join(missing_required)}")

    if signoff.get("acknowledged") is not True:
        errors.append("operator_signoff.acknowledged must be true")

    submitted = _parse_utc(str(evidence.get("submitted_at_utc", "")).strip())
    if submitted is None:
        errors.append("evidence.submitted_at_utc must be valid ISO timestamp")
    else:
        age_h = (datetime.now(timezone.utc) - submitted).total_seconds() / 3600.0
        if age_h < 0:
            errors.append("evidence.submitted_at_utc must not be in the future")
        if age_h > max_age_hours:
            errors.append(f"evidence.submitted_at_utc is stale (>{max_age_hours}h)")

    return errors


def main_feedback(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="OpenAI feedback workflow (B1 manual mode).")
    sub = parser.add_subparsers(dest="feedback_cmd", required=True)

    p_prepare = sub.add_parser("prepare", help="Build support pack from debug log.")
    p_prepare.add_argument("--input", default=".gateway/external_debug/codex_openai_codefix_debug.jsonl")
    p_prepare.add_argument("--out-dir", default="artifacts/openai_support_pack")
    p_prepare.add_argument("--max-incidents", type=int, default=200)
    p_prepare.add_argument("--allow-empty-input", action="store_true")

    p_verify = sub.add_parser("verify", help="Verify manually filled support receipt.")
    p_verify.add_argument("--receipt", required=True)
    p_verify.add_argument("--max-age-hours", type=int, default=168)

    args = parser.parse_args(argv)

    if args.feedback_cmd == "prepare":
        try:
            paths = prepare_support_pack(
                input_log=Path(args.input).resolve(),
                out_dir=Path(args.out_dir).resolve(),
                max_incidents=max(1, int(args.max_incidents)),
                allow_empty_input=bool(args.allow_empty_input),
            )
        except FileNotFoundError as exc:
            print(f"FEEDBACK_PREPARE_FAIL {exc}")
            return 1
        print("FEEDBACK_PREPARE_OK")
        print(f"bundle_json={paths['bundle_json']}")
        print(f"bundle_md={paths['bundle_md']}")
        print(f"ticket_draft={paths['ticket_draft']}")
        print(f"receipt_template={paths['receipt_template']}")
        return 0

    errors = verify_support_receipt(Path(args.receipt).resolve(), max_age_hours=max(1, int(args.max_age_hours)))
    if errors:
        print("FEEDBACK_VERIFY_FAIL")
        for err in errors:
            print(f"- {err}")
        return 1
    print("FEEDBACK_VERIFY_OK")
    return 0
