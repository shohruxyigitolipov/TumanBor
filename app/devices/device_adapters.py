from abc import ABC, abstractmethod
from fastapi import WebSocket
import json
from typing import Optional


class BaseDevice(ABC):
    def __init__(self, device_id: int, device_type: str, websocket: WebSocket):
        self.device_id = device_id
        self.device_type = device_type
        self.websocket = websocket

    async def send_data_ws(self, data: dict) -> None:
        """
        Отправка данных устройству через WebSocket.
        :param data: JSON-словарь команды.
        """
        try:
            await self.websocket.send_text(data=json.dumps(data))
        except Exception as e:
            print(f'Ошибка при отправке через WebSocket: {e}')

    @abstractmethod
    async def turn_on(self) -> None:
        pass

    @abstractmethod
    async def turn_off(self) -> None:
        pass

    @abstractmethod
    async def set_state(self, state: bool) -> None:
        pass

    @abstractmethod
    async def set_timer(self, start_time: str, stop_time: str) -> None:
        pass

    @abstractmethod
    async def get_state(self) -> Optional[bool]:
        pass


class DeviceCommands(BaseDevice):
    async def turn_on(self) -> None:
        await self.send_data_ws({
            "action": "turn_on",
            "device_type": self.device_type,
            "device_id": self.device_id
        })

    async def turn_off(self) -> None:
        await self.send_data_ws({
            "action": "turn_off",
            "device_type": self.device_type,
            "device_id": self.device_id
        })

    async def set_state(self, state: bool) -> None:
        await self.send_data_ws({
            "action": "set_state",
            "state": state,
            "device_type": self.device_type,
            "device_id": self.device_id
        })

    async def set_timer(self, start_time: str, stop_time: str) -> None:
        await self.send_data_ws({
            "action": "set_timer",
            "start_time": start_time,
            "stop_time": stop_time,
            "device_type": self.device_type,
            "device_id": self.device_id
        })

    async def clear_timer(self) -> None:
        await self.send_data_ws({
            "action": "clear_timer",
            "device_type": self.device_type,
            "device_id": self.device_id
        })

    async def get_state(self) -> Optional[bool]:
        """
        Запрос состояния устройства.
        :return: Ожидаемое состояние (если сервер отвечает).
        """
        await self.send_data_ws({
            "action": "get_state",
            "device_type": self.device_type,
            "device_id": self.device_id
        })
        # ⚠ Реализация приёма ответа зависит от протокола
        # Здесь — только отправка. Ответ должен быть получен отдельно.
        return None  # или `await self.websocket.receive_json()["state"]`, если реализуешь это
