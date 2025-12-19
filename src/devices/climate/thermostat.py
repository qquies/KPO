from devices.base_device import BaseDevice
import random

class Thermostat(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "climate")
        self.temperature = 22.0
        self.data["temperature"] = 22.0
        self.data["target_temperature"] = 22.0
        self.metadata["min_temperature"] = 15
        self.metadata["max_temperature"] = 30
        self.type = "thermostat"
        
    def turn_on(self):
        self.state = "on"
        self.emit_event("state_changed", {"state": "on"})
        return True
        
    def turn_off(self):
        self.state = "off"
        self.emit_event("state_changed", {"state": "off"})
        return True
    
    def toggle(self):
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()
    
    def set_temperature(self, temperature: float) -> bool:
        """Установить целевую температуру"""
        if not (self.metadata["min_temperature"] <= temperature <= self.metadata["max_temperature"]):
            return False
        self.data["target_temperature"] = round(temperature, 1)  # ← Округлить здесь
        self.emit_event("temperature_set", {"temperature": round(temperature, 1)})
        return True
    
    def _simulate_temperature(self):
        """Симуляция изменения температуры (вызывается периодически)"""
        if self.state == "on":
            # Плавное изменение температуры в диапазоне 18-26°C
            target = self.data.get("target_temperature", 22.0)
            
            # Температура стремится к целевой с небольшими случайными колебаниями
            diff = target - self.temperature
            change = diff * 0.1 + random.uniform(-0.3, 0.3)
            self.temperature = self.temperature + change
            # Округляем для отображения, но оставляем точную для вычислений
            display_temp = round(self.temperature, 1)
            self.data["temperature"] = display_temp
            
            # Отправляем событие при значительном изменении (>0.5°C)
            if abs(change) > 0.5:
                self.emit_event("temperature_changed", {"temperature": display_temp})
    
    def get_status(self):
        """Получить статус устройства с округленной температурой"""
        status = super().get_status()
        status["temperature"] = round(self.temperature, 1)
        status["data"]["temperature"] = round(self.data.get("temperature", 22.0), 1)
        status["data"]["target_temperature"] = round(self.data.get("target_temperature", 22.0), 1)
        return status