# Test Mirror Matrix — LAM-Codex_Agent (2026-02-17)

## Existing Coverage

- Core behavior tests.
- CLI integration smoke.
- Com-agent bridge queue smoke.
- Governance artifact consistency checks.

## Missing High-Value Tests

| Domain | Missing Test | Priority |
|---|---|---|
| Flash Bridge | Model fallback chain order + error fallback | P0 |
| Flash Bridge | `hibernate` auto-save file generation contract | P1 |
| Queue | Burst ordering + idempotency for com-agent bridge | P0 |
| Protocol | Envelope schema conformance across core/bridge outputs | P1 |
| Packaging | Editable-install + CLI discovery in isolated env | P2 |

## Mirror Plan

- Mirror-A: P0 queue + flash fallback tests.
- Mirror-B: P1 protocol/hibernate persistence tests.
- Mirror-C: P2 packaging/CLI environment tests.
