from devices.base_device import BaseDevice
import random
from datetime import datetime
import threading
import time


class SmartLight(BaseDevice):
    """Умная лампа с яркостью и цветом."""

    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, "light")

        self.type = "lamp"

        # данные устройства
        self.data["brightness"] = 0
        self.data["color_temp"] = 4000
        self.data["color"] = "#FFFFFF"
        self.data["temperature"] = 22.0  # Добавляем температуру

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
            "max_color_temp": 6500,
            "min_temperature": 18.0,
            "max_temperature": 26.0
        })

        # Для фоновой симуляции
        self._simulation_thread = None
        self._stop_simulation = threading.Event()

    # ============================================================
    #  Основные методы управления
    # ============================================================

    def turn_on(self) -> bool:
        self.state = "on"
        # Если яркость была 0, устанавливаем разумное значение
        if self.data["brightness"] == 0:
            self.data["brightness"] = 80
        self.emit_event("state_changed", {"state": "on"})
        # Запускаем симуляцию температуры при включении
        self._start_temperature_simulation()
        return True

    def turn_off(self) -> bool:
        self.state = "off"
        self.data["brightness"] = 0
        self.emit_event("state_changed", {"state": "off"})
        # Останавливаем симуляцию температуры при выключении
        self._stop_temperature_simulation()
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
            self._start_temperature_simulation()

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

    # ============================================================
    #  Симуляция температуры
    # ============================================================

    def _simulate_temperature(self):
        """Медленно изменяет температуру в диапазоне 18-26°C когда устройство включено"""
        if self.state == "on":
            current_temp = self.data.get("temperature", 22.0)
            min_temp = self.metadata.get("min_temperature", 18.0)
            max_temp = self.metadata.get("max_temperature", 26.0)
            
            # Целевая температура - плавно меняется в пределах диапазона
            # Можно добавить зависимость от времени суток или случайные колебания
            hour = datetime.now().hour
            
            # Днем температура выше, ночью ниже
            if 10 <= hour <= 18:
                # Днем: 23-26°C
                target_temp = random.uniform(23.0, 26.0)
            elif 19 <= hour <= 22:
                # Вечером: 21-24°C
                target_temp = random.uniform(21.0, 24.0)
            else:
                # Ночью/утром: 18-22°C
                target_temp = random.uniform(18.0, 22.0)
            
            # Ограничиваем целевую температуру диапазоном
            target_temp = max(min_temp, min(max_temp, target_temp))
            
            # Плавное изменение температуры (коэффициент 0.1 для медленного изменения)
            diff = target_temp - current_temp
            change = diff * 0.1 + random.uniform(-0.1, 0.1)  # Добавляем небольшие случайные колебания
            
            # Ограничиваем максимальное изменение за один вызов
            change = max(-0.3, min(0.3, change))
            
            new_temp = current_temp + change
            
            # Ограничиваем в диапазоне
            new_temp = max(min_temp, min(max_temp, new_temp))
            
            if abs(new_temp - current_temp) > 0.05:  # Изменяем только если разница заметна
                self.data["temperature"] = round(new_temp, 1)
                self.emit_event("temperature_changed", {"temperature": round(new_temp, 1)})

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

    def _temperature_simulation_loop(self):
        """Фоновый поток для симуляции температуры"""
        while not self._stop_simulation.wait(5):  # Проверка каждые 5 секунд
            if self.state == "on":
                self._simulate_temperature()
                self._simulate_brightness()  # Также обновляем яркость

    def _start_temperature_simulation(self):
        """Запуск фоновой симуляции температуры"""
        if self._simulation_thread is None or not self._simulation_thread.is_alive():
            self._stop_simulation.clear()
            self._simulation_thread = threading.Thread(
                target=self._temperature_simulation_loop,
                daemon=True
            )
            self._simulation_thread.start()

    def _stop_temperature_simulation(self):
        """Остановка фоновой симуляции температуры"""
        if self._simulation_thread and self._simulation_thread.is_alive():
            self._stop_simulation.set()
            self._simulation_thread.join(timeout=2)

    def check_device_changes(self):
        """Проверка изменений устройства (вызывается периодически)"""
        # Симуляция температуры и яркости теперь в фоновом потоке
        # Но можно оставить здесь для обратной совместимости
        if self.state == "on":
            self._simulate_temperature()
            self._simulate_brightness()
        return super().check_device_changes()

    # ============================================================
    #  Статус
    # ============================================================

    def get_status(self):
        status = super().get_status()
        # Добавляем температуру в статус
        status["temperature"] = self.data.get("temperature", 22.0)
        return status

    def cleanup(self):
        """Очистка ресурсов при удалении устройства"""
        self._stop_temperature_simulation()
        super().cleanup()
