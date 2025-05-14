from fastapi import APIRouter
from pydantic import BaseModel

from app.devices.device_service import DeviceService
from app.devices.ws_connection import ws_manager
from app.orders.parsers import PaymentInfoParser
from app.events.emitters import event_bus
from logger_module.logging_utils import get_logger_factory

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/orders')


class OrderText(BaseModel):
    text: str


class ParsedData(BaseModel):
    device_id: int
    payment_name: str
    amount: float
    datetime: str
    status: bool
    transaction_id: int


async def do_order(data):
    if not data.device_id and data.status:
        return
    event_bus.emit('got_order', data.device_id, data.amount)


@event_bus.on('got_order')
async def handle_order(device_id, amount):
    message = f"PAYMENT_OK:{amount}"
    await ws_manager.send_personal(device_id, message=message)


@router.post('/new', response_model=ParsedData)
async def get_order(request: OrderText):
    parsed_dict = PaymentInfoParser(text=request.text).parse()
    data = ParsedData(**parsed_dict)
    await do_order(data)
    return data
