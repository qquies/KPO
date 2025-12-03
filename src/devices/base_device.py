from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime
from typing import Any, Dict, List

class BaseDevice(ABC):
    """Базовый абстрактный класс для всех устройств умного дома."""

    def __init__(self, device_id: str, name: str, device_type: str):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        
        self.state = "off"           # Текущее состояние устройства
        self.online = True           # Устройство доступно/недоступно
        self.data: Dict[str, Any] = {}      # Текущие данные устройства
        self.error: List[str] = []           # Ошибки устройства
        self.metadata: Dict[str, Any] = {}   # Метаданные устройства
        
        # Какие команды устройство поддерживает
        self.capabilities: List[str] = ["on", "off", "toggle"]
        
        # Список слушателей событий
        self._listeners: List[Callable] = []

    # ============================================================
    #  Абстрактные методы — обязательные для всех устройств
    # ============================================================
    
    @abstractmethod
    def turn_on(self) -> bool:
        """Включить устройство"""
        pass

    @abstractmethod
    def turn_off(self) -> bool:
        """Выключить устройство"""
        pass

    @abstractmethod
    def toggle(self) -> bool:
        """Переключить состояние устройства"""
        pass

    # ============================================================
    #  Система событий
    # ============================================================

    def add_event_listener(self, callback: Callable[[Dict[str, Any]], None]):
        """Подписка на события устройства."""
        self._listeners.append(callback)

    def remove_event_listener(self, callback: Callable[[Dict[str, Any]], None]):
        """Отписка от событий."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def emit_event(self, event_type: str, payload: Dict[str, Any] = None):
        """Вызывает все подписанные обработчики событий."""
        event = {
            "device_id": self.device_id,
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "payload": payload or {}
        }

        for listener in self._listeners:
            listener(event)

    # ============================================================
    #  Проверка возможности выполнения команды
    # ============================================================
    
    def can_execute(self, command: str) -> bool:
        """
        Проверяет, можно ли выполнить команду:
        - устройство должно быть online
        - команда должна входить в capabilities
        """
        if not self.online:
            return False
        return command in self.capabilities

    # ============================================================
    #  Получение статуса
    # ============================================================

    def get_status(self) -> Dict[str, Any]:
        """Возвращает статус устройства."""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "type": self.device_type,
            "state": self.state,
            "online": self.online,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata,
            "capabilities": self.capabilities
        }