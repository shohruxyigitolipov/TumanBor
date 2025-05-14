from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from app.database.engine import init_db
from app.devices.device_routers import router as device_rt
from app.orders.order_routers import router as order_rt
from config import LoggingSettings
from logger_module.logging_config import LoggingConfig
import logging

settings = LoggingSettings()  # прочитает .env автоматически
LoggingConfig(settings).setup()


def get_logger(name: str = __name__) -> logging.Logger:
    return logging.getLogger(name)


@asynccontextmanager
async def lifespan(app1: FastAPI):
    await init_db()
    from app.events import handlers
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(device_rt)
app.include_router(order_rt)


@app.get('/')
async def welcome():
    return {'message': "Hello, world!"}


@app.middleware('http')
async def log_requests(request: Request, call_next):
    print(f"Запрос от: {request.client.host}")
    response = await call_next(request)
    print("Ответ отправлен")
    return response
