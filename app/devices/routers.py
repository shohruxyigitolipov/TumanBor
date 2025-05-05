import asyncio

from fastapi import APIRouter, HTTPException, Depends, WebSocket, status, WebSocketDisconnect

from app.devices.database.service import DeviceService
from .dependencies import get_device_service
from .schemas import *
from .ws_connection import ws_manager

router = APIRouter(prefix='/devices')

devices = {
    1: Device(id=1, name='raspberrypi', status=True),
    2: Device(id=2, name='esp8266', status=False),
    3: Device(id=3, name='esp32s3')
}


@router.post('/register', response_model=DeviceRegisterResponse, tags=['Регистрация устройства'])
async def register_device(data: DeviceRegisterRequest, service: DeviceService = Depends(get_device_service)):
    try:
        device = await service.register_device_by_code(data.registration_code)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return DeviceRegisterResponse(id=device.id, auth_token=device.auth_token)


@router.websocket('/ws/{device_id}/connect')
async def websocket_connection(websocket: WebSocket, device_id: int,
                               service: DeviceService = Depends(get_device_service)):
    await websocket.accept()
    try:
        data = await asyncio.wait_for(websocket.receive_json(), timeout=15)
    except asyncio.TimeoutError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    token = data.get('auth_token') if isinstance(data, dict) else None
    verified = await service.verify_auth_token(device_id=device_id, auth_token=token)
    if not verified:
        print('Неверный auth_token!')
        await websocket.send_json({'error': 'Неверный auth_token'})
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await ws_manager.connect(device_id=device_id, ws=websocket)
    print('Успешно подключено!')
    try:
        while True:
            msg = await websocket.receive_text()
            await websocket.send_text(f'Вы сказали: {msg}')
    except WebSocketDisconnect:
        print(f"Device: {device_id} отключился")


@router.post('/{device_id}/cmd', tags=['Сообщение устройству, команды'])
async def control_device(device_id: int, request: DeviceControlAPIRequest,
                         service: DeviceService = Depends(get_device_service)):
    cmd = request.cmd
    sent = await ws_manager.send_personal(device_id, message=cmd)
    if not sent:
        raise HTTPException(status_code=404, detail='Устройство не подключено!')
    return {'action': 'cmd', 'status': 'done'}


@router.get('/', response_model=DeviceIDListResponse, tags=['Получить список ID, устройств'])
async def list_device_ids(service: DeviceService = Depends(get_device_service)):
    try:
        devices_id_list = await service.get(only_id=True)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'device_ids': devices_id_list}


@router.get('/{device_id}', response_model=Device, tags=['Получить устройство'])
async def get_device(device_id: int, service: DeviceService = Depends(get_device_service)):
    try:
        device = await service.get(device_id=device_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return device


@router.get('/{device_id}/status', response_model=DeviceStatusResponse, tags=['Получить статус устройства'])
async def get_device_status_r(device_id: int, service: DeviceService = Depends(get_device_service)):
    try:
        device = service.get(device_id=device_id)
    except ValueError:
        raise HTTPException(status_code=404, detail='Device not found')
    device_status = 0
    return {'device_id': device_id, 'status': device_status}


@router.post('/{device_id}/control', response_model=DeviceControlResponse,
             tags=['Контролировать устройство', 'отправлять команды'])
async def control_device_r(device_id: int, request: DeviceControlAPIRequest):
    device = devices.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail='Device not found')

    print(f'Received command: {request.cmd} for device: {device.name}')
    return {'device_id': device.id, 'command_executed': request.cmd}
