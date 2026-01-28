def test_bridge_send_outbound_queue_api():
    from interfaces.com_agent_interface import ComAgent
    from codex_agent.integrations.com_agent_bridge import ComAgentBridge

    ca = ComAgent()
    ca.register_agent("codex", object())

    bridge = ComAgentBridge(ca)
    assert bridge.send_outbound({"recipient": "codex", "ping": "pong"}) is True

    sender, msg = ca.receive_data()
    assert sender == "codex"
    assert msg["ping"] == "pong"
