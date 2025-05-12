from fastapi import WebSocket, status
from starlette.websockets import WebSocketDisconnect
import asyncio

from app.devices.device_service import DeviceService
from app.devices.ws_connection import ws_manager
from app.events.emitters import event_bus


class WebSocketHandler:
    @staticmethod
    async def handle_connection(websocket: WebSocket, device_id: int, service: DeviceService):
        try:
            data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
        except asyncio.TimeoutError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        token = data.get("auth_token") if isinstance(data, dict) else None
        verified = await service.verify_auth_token(device_id=device_id, auth_token=token)

        if not verified:
            event_bus.emit('device_wrong_auth_token', device_id)
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        await ws_manager.connect(device_id=device_id, ws=websocket)

        try:
            while True:
                msg = await websocket.receive_text()
                event_bus.emit('message_from_device', device_id, msg)

        except WebSocketDisconnect:
            event_bus.emit('device_disconnected', device_id)


websocket_handler = WebSocketHandler
