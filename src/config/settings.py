# Настройки приложения

import os
from typing import Dict, Any

class Settings:
    """Настройки системы Умный Дом"""
    
    def __init__(self):
        self.SYSTEM_NAME = "Smart Home System"
        self.VERSION = "1.0.0"
        
        # Настройки устройств
        self.DEVICE_UPDATE_INTERVAL = 2  # секунды
        self.LOG_RETENTION_DAYS = 30
        
        # Настройки по умолчанию для устройств
        self.DEFAULT_DEVICES: Dict[str, Any] = {
            "lamp_living_room": {
                "name": "Свет в гостиной",
                "type": "light", 
                "brightness": 100
            },
            "thermostat": {
                "name": "Термостат",
                "type": "climate",
                "temperature": 22
            },
            "security_camera": {
                "name": "Камера безопасности", 
                "type": "security"
            }
        }
    
    def get_device_config(self, device_id: str):
        """Получить конфигурацию устройства"""
        return self.DEFAULT_DEVICES.get(device_id, {})