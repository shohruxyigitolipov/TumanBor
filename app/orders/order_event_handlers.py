from app.events.emitters import event_bus
from app.devices.ws_connection import ws_manager
import datetime
from logger_module.logging_utils import get_logger_factory
from asyncio import Queue, wait_for
import uuid

get_logger = get_logger_factory(__name__)
logger = get_logger()


@event_bus.on('got_order')
async def handle_order(device_id, amount):
    pass
