from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
from typing import List




class DeviceCreate(BaseModel):
    name: str


class DeviceDataInfo(BaseModel):
    registration_code: str
    auth_token: str

    class Config:
        from_attributes = True


class DeviceInfo(BaseModel):
    id: int
    name: str
    last_seen: str | None = None
    data: DeviceDataInfo

    class Config:
        from_attributes = True


class DeviceControl_response(BaseModel):
    action: str
    state: bool | int
    device_id: int


class DeviceStatus_response(BaseModel):
    device_id: int
    state: bool


class Device(BaseModel):
    device_id: int


class CommandResponse(Device):
    success: bool
    command: str


class ErrorResponse(BaseModel):
    error: str


class ActiveDevicesResponse(BaseModel):
    active_devices: list[int]

    class Config:
        arbitrary_types_allowed = True


class Command(str, Enum):
    PAYMENT_OK = 'payment_ok'
    turn_on = 'turn_on'
    turn_off = 'turn_off'
    reboot = 'reboot'


class DeviceControlAPIRequest(BaseModel):
    cmd: Command


class DeviceIDListResponse(BaseModel):
    device_ids: List[int]


class DeviceStatusResponse(BaseModel):
    device_id: int
    status: int | bool = False


class DeviceControlResponse(BaseModel):
    device_id: int
    command_executed: Command
