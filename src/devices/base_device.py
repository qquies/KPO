from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseDevice(ABC):
    """Базовый класс для всех устройств умного дома"""
    
    def __init__(self, device_id: str, name: str, device_type: str):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.state = "off"
        self._previous_state = "off"
        
    @abstractmethod
    def turn_on(self) -> bool:
        """Включить устройство"""
        pass
    
    @abstractmethod
    def turn_off(self) -> bool:
        """Выключить устройство"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Получить статус устройства"""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "type": self.device_type,
            "state": self.state
        }
    
    def has_state_changed(self) -> bool:
        """Проверить изменилось ли состояние"""
        changed = self.state != self._previous_state
        self._previous_state = self.state
        return changed