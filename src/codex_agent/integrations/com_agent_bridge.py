from __future__ import annotations

from interfaces.com_agent_interface import ComAgent  # comm-agent queue API

from ..protocols.agent_protocol import AgentProtocol

try:
    from lam_logging import log as _lam_log
except Exception:  # pragma: no cover - bridge logging is optional in standalone mode
    _lam_log = None


class ComAgentBridge(AgentProtocol):
    """Bridge CodexAgent ↔ ComAgent (queue-based)."""

    def __init__(self, com_agent: ComAgent) -> None:
        self.com_agent = com_agent

    @staticmethod
    def _recipient(data: dict) -> str:
        r = data.get("recipient") or data.get("to") or data.get("target")
        if not r:
            raise ValueError("Missing recipient in data['recipient'|'to'|'target']")
        return str(r)

    @staticmethod
    def _context(data: dict) -> dict:
        ctx = data.get("context")
        if isinstance(ctx, dict):
            return ctx
        return {}

    @classmethod
    def _should_debug_external(cls, data: dict) -> bool:
        intent = str(data.get("intent", "")).lower()
        action = str(data.get("action", "")).lower()
        operation = str(data.get("operation", "")).lower()
        external_system = str(data.get("external_system") or data.get("provider") or "").lower()
        if external_system in {"codex_openai", "openai_codex", "openai"}:
            return True
        if "code_fix" in {intent, action, operation}:
            return True
        debug = data.get("debug")
        return bool(isinstance(debug, dict) and debug.get("force_external_debug"))

    @classmethod
    def _debug_log(cls, event: str, recipient: str, data: dict, *, ok: bool, error: str | None = None) -> None:
        if _lam_log is None or not cls._should_debug_external(data):
            return
        ctx = cls._context(data)
        _lam_log(
            "debug",
            "codex.bridge.external.debug",
            event,
            debug_protocol="codex_code_fix_debug_v1",
            external_system=str(data.get("external_system") or data.get("provider") or "codex_openai"),
            recipient=recipient,
            intent=data.get("intent"),
            action=data.get("action"),
            operation=data.get("operation"),
            request_id=data.get("request_id") or ctx.get("request_id"),
            trace_id=ctx.get("trace_id"),
            task_id=ctx.get("task_id"),
            ok=ok,
            error=error,
        )

    def handle_inbound(self, data: dict) -> None:
        # inbound → кладём в очередь адресату
        recipient = self._recipient(data)
        ok = self.com_agent.send_data(recipient, data)
        self._debug_log("bridge.handle_inbound", recipient, data, ok=ok, error=None if ok else "enqueue_failed")

    def send_outbound(self, data: dict) -> bool:
        # outbound → кладём в очередь адресату
        recipient = "unknown"
        try:
            recipient = self._recipient(data)
            ok = self.com_agent.send_data(recipient, data)
            self._debug_log("bridge.send_outbound", recipient, data, ok=ok, error=None if ok else "enqueue_failed")
            return ok
        except Exception as exc:
            self._debug_log("bridge.send_outbound", recipient, data, ok=False, error=type(exc).__name__)
            return False
