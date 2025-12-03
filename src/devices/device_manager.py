from devices.lighting.smart_light import SmartLight
from devices.climate.thermostat import Thermostat
from devices.security.security_camera import SecurityCamera
from services.logging_service import LoggingService
from typing import Dict
from datetime import datetime

class DeviceManager:
    """Менеджер для управления всеми устройствами"""
    
    def __init__(self):
        self.logging_service = LoggingService()
        self.devices = {}
        self.device_states = {}
        self._initialize_devices()
        
    def _initialize_devices(self):
        """Инициализация устройств по умолчанию"""
        self.add_device(SmartLight("lamp_living_room", "Свет в гостиной"))
        self.add_device(Thermostat("thermostat", "Термостат"))
        self.add_device(SecurityCamera("security_camera", "Камера безопасности"))
        
    def add_device(self, device):
        """Добавить устройство"""
        self.devices[device.device_id] = device
        self.logging_service.info("DEVICE", f"Добавлено устройство: {device.name}")
        
    def get_device(self, device_id: str):
        """Получить устройство по ID"""
        return self.devices.get(device_id)
    
    def send_command(self, device_id: str, action: str) -> bool:
        """Отправить команду устройству"""
        device = self.get_device(device_id)
        if device:
            old_state = device.state  # ← Запомнить старое состояние
            
            if action == "on":
                success = device.turn_on()
            elif action == "off":
                success = device.turn_off()
            elif action == "toggle":
                if device.state == "on":
                    success = device.turn_off()
                else:
                    success = device.turn_on()
            else:
                success = False
            
            # ЗАПИСАТЬ ИСТОРИЮ ЕСЛИ СОСТОЯНИЕ ИЗМЕНИЛОСЬ
            if success and device.state != old_state:
                self.update_device_state_history(device_id, device.state)
                self.logging_service.info("DEVICE", 
                    f"Состояние {device.name} изменено: {old_state} → {device.state}")
            
            return success
        return False
    
    def check_device_changes(self):
        """Проверить изменения состояний устройств и запустить симуляции"""
        for device_id, device in self.devices.items():
            # Проверка изменений состояний (если есть метод)
            if hasattr(device, 'has_state_changed') and device.has_state_changed():
                state_text = "включено" if device.state == "on" else "выключено"
                self.logging_service.info("DEVICE", f"{device.name} {state_text}")
                # ЗАПИСАТЬ В ИСТОРИЮ ПРИ ОБНАРУЖЕНИИ ИЗМЕНЕНИЯ
                self.update_device_state_history(device_id, device.state)
            
            # Запуск симуляций для устройств (только если устройство включено)
            if device.state == "on":
                # Симуляция температуры для термостата
                if hasattr(device, '_simulate_temperature'):
                    device._simulate_temperature()
                
                # Симуляция яркости для лампы
                if hasattr(device, '_simulate_brightness'):
                    device._simulate_brightness()
                
                # Симуляция движения для камеры
                if hasattr(device, '_simulate_motion_detection'):
                    device._simulate_motion_detection()

    def get_device_status(self, device_id: str) -> Dict:
        """Получить полный статус устройства"""
        device = self.get_device(device_id)
        if device:
            status = device.get_status()
            status["online"] = self._check_device_online(device_id)
            return status
        return {}
    
    def get_all_devices_status(self) -> Dict[str, Dict]:
        """Получить статус всех устройств"""
        return {
            device_id: self.get_device_status(device_id)
            for device_id in self.devices
        }
    
    def _check_device_online(self, device_id: str) -> bool:
        """Проверить онлайн-статус устройства (заглушка)"""
        return True  # В реальной системе здесь проверка связи
    
    def update_device_state_history(self, device_id: str, state: str):
        """Обновить историю состояний устройства"""
        if device_id not in self.device_states:
            self.device_states[device_id] = []
        
        self.device_states[device_id].append({
            "state": state,
            "timestamp": datetime.now().isoformat(),
            "online": True
        })
        
        # Ограничить историю последними 100 записями
        if len(self.device_states[device_id]) > 100:
            self.device_states[device_id] = self.device_states[device_id][-100:]