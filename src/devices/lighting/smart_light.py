from devices.base_device import BaseDevice

class SmartLight(BaseDevice):
    """Умная лампа с регулировкой яркости"""
    
    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, "light")
        self.brightness = 100
        
    def turn_on(self) -> bool:
        self.state = "on"
        return True
    
    def turn_off(self) -> bool:
        self.state = "off"
        self.brightness = 0
        return True
    
    def set_brightness(self, level: int) -> bool:
        """Установить яркость (0-100)"""
        if 0 <= level <= 100:
            self.brightness = level
            self.state = "on" if level > 0 else "off"
            return True
        return False
    
    def get_status(self):
        status = super().get_status()
        status["brightness"] = self.brightness
        return status