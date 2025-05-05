
from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, device_id: str, ws: WebSocket):
        if device_id in self.active:
            await self.active[device_id].close(code=4000, reason="Signed in elsewhere")
        self.active[device_id] = ws

    async def disconnect(self, device_id: str):
        try:
            self.active.pop(device_id, None)
        except:
            return False
        return True

    async def send_personal(self, device_id: str, message: str):
        ws = self.active.get(device_id)
        if ws:
            await ws.send_text(message)
            return True
        else:
            return False


ws_manager = WSConnectionManager()
