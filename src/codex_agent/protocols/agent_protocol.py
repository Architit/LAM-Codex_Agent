# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
from typing import Protocol


class AgentProtocol(Protocol):
    def handle_inbound(self, data: dict) -> None: ...
    def send_outbound(self, data: dict) -> bool: ...
