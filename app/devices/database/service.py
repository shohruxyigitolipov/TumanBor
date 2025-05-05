from collections.abc import Sequence

from app.devices.schemas import Device, DeviceCreate
from app.services import BaseService
from app.devices.database.repositories import DeviceRepository
from typing import List, Union


class DeviceService(BaseService[DeviceRepository]):
    def __init__(self, repo: DeviceRepository):
        super().__init__(repo)
        self.repo = repo

    async def register_device_by_code(self, code: str) -> Device:
        device = await self.repo.get_by_registration_code(code=code)

        if not device:
            raise ValueError("Invalid registration code")
        if device.is_registered:
            raise ValueError("Device already registered")

        await self.repo.mark_as_registered(device)
        return device

    async def create_device(self, data: DeviceCreate) -> Device:
        return await self.repo.create(name=data.name)

    async def get(self, device_id: int = None, only_id: bool = False) -> Device | Sequence[Device] | List:
        if device_id:
            device = await self.repo.get_by_id(id=device_id)
            return device

        devices = await self.repo.list_all()
        id_list = []
        if only_id:
            for device in devices:
                id_list.append(device.id)
            return id_list
        return devices

    async def verify_auth_token(self, device_id: int, auth_token: str):
        device = await self.repo.get_by_auth_token(auth_token=auth_token)
        if device and device.id == device_id:
            return True
        return False
