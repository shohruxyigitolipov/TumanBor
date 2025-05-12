import asyncio
from datetime import datetime, timedelta

from app.events.emitters import event_bus
from typing import Dict
from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, device_id: str, ws: WebSocket):
        self.active[device_id] = ws
        event_bus.emit('device_connected', device_id)

    async def disconnect(self, device_id: str) -> bool:
        try:
            self.active.pop(device_id, None)
            event_bus.emit('device_disconnected', device_id)
        except:
            return False
        return True

    async def get(self, device_id) -> WebSocket | None:
        try:
            websocket = self.active[device_id]
        except:
            return None
        return websocket

    async def get_list(self) -> Dict:
        return self.active

    async def send_personal(self, device_id: str, message: str) -> bool:
        ws = self.active.get(device_id)
        if ws:
            await ws.send_text(message)
            event_bus.emit('message_to_device', device_id, message)
            return True
        else:
            return False


ws_manager = WSConnectionManager()
