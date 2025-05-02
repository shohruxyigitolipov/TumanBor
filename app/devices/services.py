from app.devices.database.models import Device
from app.devices.database.repositories import DeviceRepository
from app.services import BaseService

class DeviceService(BaseService[DeviceRepository]):
    def __init__(self, order_repository: DeviceRepository):
        super().__init__(order_repository)
        self.order_repository = order_repository
