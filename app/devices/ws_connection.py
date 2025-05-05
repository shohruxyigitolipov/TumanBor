
from fastapi import WebSocket
from starlette.websockets import WebSocketState


class WSConnectionManager:
    def __init__(self):
        self.active: dict[str, WebSocket] = {}

    async def connect(self, device_id: str, ws: WebSocket):
        old_ws = self.active.get(device_id)

        if old_ws and old_ws.application_state != WebSocketState.DISCONNECTED:
            try:
                await old_ws.close(code=4000, reason="Signed in elsewhere")
            except Exception as e:
                # логируем, но не прерываем
                print(f"[WS] Error while closing old connection: {e}")

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
