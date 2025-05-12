from fastapi import FastAPI, WebSocket, Request
from contextlib import asynccontextmanager

from app.database.engine import init_db
from app.devices.device_routers import router as device_rt


@asynccontextmanager
async def lifespan(app1: FastAPI):
    await init_db()
    from app.events import handlers
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(device_rt)


@app.get('/')
async def welcome():
    return {'message': "Hello, world!"}


@app.middleware('http')
async def log_requests(request: Request, call_next):
    print(f"Запрос от: {request.client.host}")
    response = await call_next(request)
    print("Ответ отправлен")
    return response
