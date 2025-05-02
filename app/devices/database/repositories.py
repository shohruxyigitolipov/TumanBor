from sqlalchemy.ext.asyncio import AsyncSession

from app.devices.database.models import Device
from app.database.repositories import BaseRepository


class DeviceRepository(BaseRepository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)
