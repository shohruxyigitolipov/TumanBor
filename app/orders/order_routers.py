from fastapi import APIRouter
from pydantic import BaseModel

from app.devices.device_service import DeviceService
from app.devices.ws_connection import ws_manager
from app.orders.parsers import PaymentInfoParser
from app.events.emitters import event_bus
from logger_module.logging_utils import get_logger_factory
import uuid

get_logger = get_logger_factory(__name__)
logger = get_logger()

router = APIRouter(prefix='/orders')


class OrderText(BaseModel):
    text: str


class ReportData(BaseModel):
    data: str


class ParsedData(BaseModel):
    device_id: int
    payment_name: str
    amount: float
    datetime: str
    status: bool
    transaction_id: int


@router.post('/new')
async def get_order(request: OrderText):
    parsed_dict = PaymentInfoParser(text=request.text).parse()
    data = ParsedData(**parsed_dict)
    if not data.device_id and data.status:
        print('...')
        return data
    request_id = str(uuid.uuid4())
    message = {"cmd": f"PAYMENT_OK:{1}",
               f"request_id": f"{request_id}"}
    response = await ws_manager.send_personal(data.device_id, message=message, request_id=request_id, timeout=30)
    logger.info(f'Получил ответ на запрос({message}: [{response}]')
    return response


@router.post('/report')
async def report_order(request: ReportData):
    pass
