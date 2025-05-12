from fastapi import APIRouter, HTTPException, Depends, WebSocket, Query

from app.devices.device_service import DeviceService
from .dependencies import get_device_service
from .schemas import *
from .ws_connection import ws_manager
from .ws_handlers import websocket_handler

router = APIRouter(prefix='/devices')


@router.post('/{device_id}/cmd', tags=['Сообщение устройству, команды'])
async def control_device(device_id: int, request: DeviceControlAPIRequest):
    cmd = request.cmd
    sent = await ws_manager.send_personal(device_id, message=cmd)
    if not sent:
        raise HTTPException(status_code=404, detail='Устройство не подключено!')
    return {'action': 'cmd', 'status': 'done'}


@router.websocket('/ws/{device_id}/connect')
async def websocket_connection(websocket: WebSocket, device_id: int,
                               service: DeviceService = Depends(get_device_service)):
    await websocket.accept()
    print('⏳Установлена временная связь.\n'
          ' Ожидание дополнительных данных...')
    await websocket_handler.handle_connection(websocket=websocket, device_id=device_id, service=service)
    # {"auth_token": "abc123"}


@router.get('/{device_id}/status', response_model=DeviceStatus_response)
async def get_device_status_r(device_id: int,
                              device_type: str = Query(..., description='Получение статуса устройства'),
                              service: DeviceService = Depends(get_device_service)):
    state = await service.get_device_status(device_id=device_id, device_type=device_type)
    return DeviceStatus_response(
        device_id=device_id,
        state=state
    )


@router.get('/active', response_model=ActiveDevicesResponse, summary='Список активных устройств')
async def active_devices(service: DeviceService = Depends(get_device_service)):
    device_ids = await service.get_active_devices()
    print(device_ids)
    return ActiveDevicesResponse(active_devices=device_ids)


@router.get('/all', response_model=List[DeviceInfo])
async def get_all_devices_in_short(service: DeviceService = Depends(get_device_service),
                                   name: str = Query(None), sort: str = Query(None)):
    devices = await service.list_filtered_sorted(name=name, sort=sort)
    return devices


@router.post('/create', response_model=DeviceInfo, response_model_exclude_none=True)
async def create_device(data: DeviceCreate, service: DeviceService = Depends(get_device_service)):
    device = await service.create(data)

    return device
