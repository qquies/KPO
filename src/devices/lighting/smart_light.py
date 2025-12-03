from devices.base_device import BaseDevice
import random
from datetime import datetime


class SmartLight(BaseDevice):
    """Умная лампа с яркостью и цветом."""

    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, "light")

        # данные устройства
        self.data["brightness"] = 0
        self.data["color_temp"] = 4000
        self.data["color"] = "#FFFFFF"

        # возможности
        self.capabilities.extend([
            "set_brightness",
            "set_color",
            "set_color_temp"
        ])

        # метаданные
        self.metadata.update({
            "max_brightness": 100,
            "min_color_temp": 2700,
            "max_color_temp": 6500
        })

    # ============================================================
    #  Основные методы управления
    # ============================================================

    def turn_on(self) -> bool:
        self.state = "on"
        # Если яркость была 0, устанавливаем разумное значение
        if self.data["brightness"] == 0:
            self.data["brightness"] = 80
        self.emit_event("state_changed", {"state": "on"})
        return True

    def turn_off(self) -> bool:
        self.state = "off"
        self.data["brightness"] = 0
        self.emit_event("state_changed", {"state": "off"})
        return True

    def toggle(self) -> bool:
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()

    # ============================================================
    #  Дополнительные методы устройства
    # ============================================================

    def set_brightness(self, level: int) -> bool:
        if not 0 <= level <= 100:
            return False

        self.data["brightness"] = level

        if level > 0:
            self.state = "on"

        self.emit_event("brightness_changed", {"brightness": level})
        return True

    def set_color_temp(self, kelvin: int) -> bool:
        if not (self.metadata["min_color_temp"] <= kelvin <= self.metadata["max_color_temp"]):
            return False

        self.data["color_temp"] = kelvin
        self.emit_event("color_temp_changed", {"color_temp": kelvin})
        return True

    def set_color(self, hex_color: str) -> bool:
        self.data["color"] = hex_color
        self.emit_event("color_changed", {"color": hex_color})
        return True

    def _simulate_brightness(self):
        """Симуляция изменения яркости (вызывается периодически)"""
        if self.state == "on":
            current_brightness = self.data.get("brightness", 80)
            
            # Имитация изменения яркости по времени суток или случайно
            hour = datetime.now().hour
            
            # Утром (6-9) и вечером (18-22) - выше яркость
            # Днем (10-17) - средняя яркость
            # Ночью (23-5) - низкая яркость
            
            if 6 <= hour <= 9 or 18 <= hour <= 22:
                target_brightness = random.uniform(70, 100)
            elif 10 <= hour <= 17:
                target_brightness = random.uniform(50, 80)
            else:  # ночь
                target_brightness = random.uniform(20, 40)
            
            # Плавное изменение яркости
            diff = target_brightness - current_brightness
            change = diff * 0.1 + random.uniform(-2, 2)
            new_brightness = max(20, min(100, current_brightness + change))
            
            if abs(new_brightness - current_brightness) > 1:
                self.data["brightness"] = int(new_brightness)
                self.emit_event("brightness_changed", {"brightness": int(new_brightness)})

    # ============================================================
    #  Статус
    # ============================================================

    def get_status(self):
        status = super().get_status()
        return status