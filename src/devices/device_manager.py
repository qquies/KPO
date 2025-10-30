from devices.lighting.smart_light import SmartLight
from devices.climate.thermostat import Thermostat
from devices.security.security_camera import SecurityCamera
from services.logging_service import LoggingService

class DeviceManager:
    """Менеджер для управления всеми устройствами"""
    
    def __init__(self):
        self.logging_service = LoggingService()
        self.devices = {}
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
            if action == "on":
                return device.turn_on()
            elif action == "off":
                return device.turn_off()
            elif action == "toggle":
                if device.state == "on":
                    return device.turn_off()
                else:
                    return device.turn_on()
        return False
    
    def check_device_changes(self):
        """Проверить изменения состояний устройств"""
        for device_id, device in self.devices.items():
            if device.has_state_changed():
                state_text = "включено" if device.state == "on" else "выключено"
                self.logging_service.info("DEVICE", 
                    f"{device.name} {state_text}")
