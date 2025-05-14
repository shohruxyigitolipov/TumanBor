# device_repository
from app.database.repositories import BaseRepository
from app.devices.device_models import Device, DeviceDatas
from app.orders.models import OrderInfo
from app.obj_types import SchemaType
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import desc, asc
import datetime
from typing import List, Sequence


class DeviceRepository(BaseRepository[Device]):
    def __init__(self, session: AsyncSession):
        super().__init__(Device, session)

    async def create(self, schema: SchemaType) -> Device:
        device = Device(**schema.model_dump())
        device.data = DeviceDatas()
        self.session.add(device)
        await self.session.commit()
        stmt = (
            select(Device).options(selectinload(Device.data))
            .where(Device.id == device.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def mark_as_registered(self, device: Device):
        device.registered_at = datetime.datetime.now()
        await self.session.commit()

    async def get_by_auth_token(self, auth_token: str) -> Device:
        stmt = select(Device).join(Device.data).options(selectinload(Device.data)).where(
            DeviceDatas.auth_token == auth_token)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_devices(self) -> Sequence[Device]:
        stmt = select(Device).options(
            selectinload(Device.data))
        result = await self.session.execute(stmt)
        devices = result.scalars().all()
        return devices

    async def get_filtered_sorted(self, name: str = None, sort: str = None) -> Sequence[Device]:
        stmt = select(Device).options(
            selectinload(Device.data))
        if name:
            stmt = stmt.where(Device.name.ilike(f'%{name}%'))
        if sort:
            if sort.startswith('-'):
                column = sort[1:]
                order = desc
            else:
                column = sort
                order = asc
            if hasattr(Device, column):
                stmt = stmt.order_by(order(getattr(Device, column)))
        result = await self.session.execute(stmt)
        return result.scalars().all()


