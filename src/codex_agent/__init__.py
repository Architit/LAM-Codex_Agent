from .core import Core  # noqa: F401

try:
    from .integrations.com_agent_bridge import ComAgentBridge  # noqa: F401
except Exception:  # Optional dependency on agents package
    ComAgentBridge = None  # type: ignore[assignment]

__all__ = ["Core", "ComAgentBridge"]
