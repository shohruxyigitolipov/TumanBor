import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories import BaseRepository
from .models import Device


class DeviceRepository(BaseRepository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)

    async def get_by_registration_code(self, code: str) -> Device | None:
        result = await self.session.execute(
            select(Device).where(Device.registration_code == code)
        )
        return result.scalar_one_or_none()

    async def mark_as_registered(self, device: Device):
        device.is_registered = True
        device.registered_at = datetime.datetime.now()
        await self.session.commit()

    async def create(self, name: str) -> Device:
        device = Device(name=name)
        self.session.add(device)
        await self.session.commit()
        await self.session.refresh(device)
        return device

    async def get_by_auth_token(self, auth_token: str) -> Device:
        stmt = select(Device).where(Device.auth_token == auth_token)
        result = await self.session.execute(stmt)
        device = result.scalar_one_or_none()
        return device
