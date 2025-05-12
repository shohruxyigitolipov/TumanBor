from app.devices.device_adapters import DeviceCommands
from fastapi import WebSocket, HTTPException, status

from app.devices.device_repository import DeviceRepository
from app.devices.ws_connection import ws_manager
from app.services import BaseService


class DeviceService(BaseService[DeviceRepository]):
    def __init__(self, repo: DeviceRepository):
        """
        Сервис для работы с устройствами, содержащий как методы, связанные с базой данных,
        так и управляющие действия через WebSocket.

        :param repo: Репозиторий для работы с таблицей устройств.
        """
        super().__init__(repo)

    async def list_all(self):
        """
        Получить все устройства из базы данных.

        :return: Список всех устройств.
        """
        return await self.repo.get_all_devices()

    async def list_filtered_sorted(self, name: str = None, sort: str = None):
        """
        Получить устройства с фильтрацией по имени и сортировкой.

        :param name: Фильтр по имени устройства.
        :param sort: Поле сортировки.
        :return: Список отфильтрованных и отсортированных устройств.
        """
        return await self.repo.get_filtered_sorted(name=name, sort=sort)

    @staticmethod
    async def get_websocket_or_404(device_id: int) -> WebSocket:
        """
        Получить активное WebSocket-соединение устройства, или вернуть 404, если соединение отсутствует.

        :param device_id: Идентификатор устройства.
        :return: WebSocket-объект.
        :raises HTTPException: Если соединение отсутствует.
        """
        session = await ws_manager.get(device_id)
        websocket = session.websocket
        if not websocket:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Устройство {device_id} не подключено.'
            )
        return websocket

    @staticmethod
    async def control_device(device_id: int, device_type: str, state: bool = None,
                             start_time: str = None, stop_time: str = None):
        """
        Управлять устройством через WebSocket.

        Поддерживает:
        - установку таймера (start_time и stop_time)
        - включение/выключение устройства (state)
        - очистку таймера

        :param device_id: ID устройства.
        :param device_type: Тип устройства.
        :param state: Целевое состояние (вкл/выкл).
        :param start_time: Время включения.
        :param stop_time: Время выключения.
        :return: Результат действия и текущее состояние.
        """
        try:
            websocket = await DeviceService.get_websocket_or_404(device_id)
        except Exception as e:
            print(f'Ошибка Websocket, {e}')
            return 'Не удалось найти соединений', state

        device = DeviceCommands(device_type=device_type, device_id=device_id, websocket=websocket)

        if start_time and stop_time:
            await device.set_timer(start_time=start_time, stop_time=stop_time)
            return 'Set timer', state
        elif state is not None:
            await device.set_state(state=state)
            return 'Set state', state
        else:
            await device.clear_timer()
            return 'Clear timer', 0

    @staticmethod
    async def get_device_status(device_id: int, device_type: str) -> bool:
        """
        Получить текущее состояние устройства через WebSocket.

        :param device_id: Идентификатор устройства.
        :param device_type: Тип устройства.
        :return: True — включено, False — выключено.
        """
        websocket = await DeviceService.get_websocket_or_404(device_id)
        device = DeviceCommands(device_type=device_type, device_id=device_id, websocket=websocket)
        return await device.get_state()

    @staticmethod
    async def get_active_devices() -> list[int]:
        """
        Получить список ID всех устройств, у которых есть активное WebSocket-соединение.

        :return: Список ID активных устройств.
        """
        return await ws_manager.get_list()

    async def verify_auth_token(self, device_id: int, auth_token: str):
        device = await self.repo.get_by_auth_token(auth_token=auth_token)
        if device and device.id == device_id:
            return True
        return False
