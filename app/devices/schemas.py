from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from enum import Enum
from typing import List

class DeviceCreate(BaseModel):
    name: str = Field(..., example='raspberrypi4')


class DeviceRegisterRequest(BaseModel):
    registration_code: str = Field(..., example='abc')


class DeviceRegisterResponse(BaseModel):
    id: int
    auth_token: str


class DeviceInfo(BaseModel):
    id: int
    name: str
    registration_code: str
    auth_token: str
    is_registered: bool
    created_at: datetime
    registered_at: datetime | None = None
    last_seen: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class DeviceShort(BaseModel):
    id: int
    name: str
    is_registered: bool
    model_config = ConfigDict(from_attributes=True)


class Device(BaseModel):
    id: int
    name: str | None = None
    status: int | bool = False


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
