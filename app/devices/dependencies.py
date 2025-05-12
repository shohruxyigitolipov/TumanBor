#dependencies.py

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.engine import get_db
from app.devices.device_repository import DeviceRepository
from app.devices.device_service import DeviceService


def get_device_repository(db: AsyncSession = Depends(get_db)) -> DeviceRepository:
    return DeviceRepository(db)


def get_device_service(device_repository: DeviceRepository = Depends(get_device_repository)) -> DeviceService:
    return DeviceService(device_repository)
