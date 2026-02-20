# SUBTREE COMMAND INTERPRETATION PROTOCOL (V1.0.0)
**Phase:** 8.0 (The Awakening)
**Role:** LAM-Codex_Agent (The Architect's Hand)
**Status:** ACTIVE

## 1. OBJECTIVE
To ensure that the Codex Agent correctly interprets and executes commands targeting the 24 sovereign organs without causing architectural corruption.

## 2. INTERPRETATION RULES
When receiving a command related to an ecosystem organ:
1. **Identify the Target:** Map the command context to one of the 24 sacred organs (`/core`, `/map`, etc.).
2. **Verify Subtree Identity:** Consult `SUBTREES_LOCK.md` to confirm the organ is an independent subtree.
3. **Isolate Changes:** Generate code deltas that are strictly confined to the target subtree's repository boundary.

## 3. PROHIBITED ACTIONS
- **Folder Shadowing:** Never treat an organ as a simple folder in the root repository.
- **Monolithic Commits:** Do not bundle changes for multiple organs into a single non-subtree commit.
- **Protocol Bypass:** Any command that attempts to write to `LRPT/` without a subtree context MUST be blocked by the `CodexGate`.

## 4. GATE UPGRADE (PHASE 8.0)
The `CodexGate` must be extended to include a `TopologyValidator` that checks the filesystem mode (Subtree vs Folder) before allowing write operations.

## 5. VERIFICATION
Success is measured by the agent's ability to pass the `test_subtree_write_isolation.py` suite.

---
**Custodian:** Ayaearias
⚜️🛡️🔱🐦‍🔥👑
