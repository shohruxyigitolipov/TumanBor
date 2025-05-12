from app.devices.ws_connection import ws_manager
from app.events.emitters import event_bus
import datetime


@event_bus.on("device_connected")
async def handle_connect(device_id):
    print(f"✅ Устройство {device_id} подключено.")
    await ws_manager.send_personal(device_id, 'Вы подключились')


@event_bus.on("device_disconnected")
async def handle_disconnect(device_id):
    print(f"[{device_id}] Сессия завершена и удалена.❌")
    await ws_manager.disconnect(device_id)

@event_bus.on('websocket_disconnected')
async def handle_ws_disconnect(device_id):
    print(f'[{device_id}] Websocket соединение потеряно.⛓️‍💥')

@event_bus.on("message_from_device")
async def handle_message(device_id, message):
    print(f"📨 {device_id} прислал: {message}")
    await ws_manager.send_personal(device_id, f"Вы сказали: {message}")

@event_bus.on('message_to_device')
async def handle_message_to_device(device_id, message):
    print(f'{device_id} Отправлено сообщение: {message}')

@event_bus.on('device_timeout')
async def handle_timeout(device_id, last_pong_time):
    print(f'Текущее время: {datetime.datetime.now()}\n'
          f'Время последнего pong\'а: {last_pong_time}'
          f"[{device_id}] Таймаут heartbeat")


@event_bus.on('device_send_error')
async def handle_send_error(device_id, error):
    print(f'[{device_id}], Ошибка отправки команды: {error}')


@event_bus.on('device_error')
async def handle_error(device_id, error):
    print(f"[{device_id}] Ошибка в работе устройства: {error}")


@event_bus.on('device_session_end')
async def handle_session_end(device_id):
    print(f'[{device_id}], Сессия завершена')

@event_bus.on('websocket_wrong_auth_token')
async def handle_auth_token_wrong(device_id):
    print("Неверный auth_token!")
    await ws_manager.send_personal(device_id, message='Неверный auth_token')

    # await websocket.send_json({"error": "Неверный auth_token"})
