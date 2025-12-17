from devices.lighting.smart_light import SmartLight
from devices.climate.thermostat import Thermostat
from devices.security.security_camera import SecurityCamera
from services.logging_service import LoggingService
from devices.security.smoke_sensor import SmokeSensor
from devices.security.water_leak_sensor import WaterLeakSensor
from services.storage_service import StateStorage


from typing import Dict
from datetime import datetime

class DeviceManager:
    """Менеджер для управления всеми устройствами"""
    
    def __init__(self):
        self.logging_service = LoggingService()
        self.devices = {}
        self.device_states = {}
        self._initialize_devices()
        self.devices["smoke_sensor"] = SmokeSensor("smoke_sensor", "Датчик дыма")
        self.devices["water_leak_sensor"] = WaterLeakSensor("water_leak_sensor", "Датчик протечки")
        self.state_storage = StateStorage()
        self.restore_state()
        self.load_initial_state()
        
        
    def _initialize_devices(self):
        """Инициализация устройств по умолчанию"""
        self.add_device(SmartLight("lamp_living_room", "Свет в гостиной"))
        self.add_device(Thermostat("thermostat", "Термостат"))
        self.add_device(SecurityCamera("security_camera", "Камера безопасности"))

        # Создаем устройства
        # self.create_default_devices()
        
        # Восстанавливаем сохраненные состояния
        self.restore_state()
        
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
            old_state = device.state  # Запомнить старое состояние
            
            success = False
            
            if action == "on":
                success = device.turn_on()
            elif action == "off":
                success = device.turn_off()
            elif action == "toggle":
                if device.state == "on":
                    success = device.turn_off()
                else:
                    success = device.turn_on()
            elif ":" in action:
                # Команда с параметром (например, "set_temperature:22")
                parts = action.split(":", 1)
                command = parts[0]
                value = parts[1]
                
                if command == "set_temperature" and hasattr(device, "set_temperature"):
                    try:
                        success = device.set_temperature(float(value))
                    except ValueError:
                        success = False
                elif command == "set_brightness" and hasattr(device, "set_brightness"):
                    try:
                        success = device.set_brightness(int(value))
                    except ValueError:
                        success = False
                else:
                    success = False
            else:
                success = False
            
            # ЗАПИСАТЬ ИСТОРИЮ И СОХРАНИТЬ СОСТОЯНИЕ ЕСЛИ ИЗМЕНИЛОСЬ
            if success and device.state != old_state:
                self.update_device_state_history(device_id, device.state)
                self.logging_service.info("DEVICE", 
                    f"Состояние {device.name} изменено: {old_state} → {device.state}")
                
                # Сохраняем состояние в файл
                self.save_state()
                
                # Отправляем событие об изменении состояния
                if hasattr(self, 'event_bus'):
                    self.event_bus.publish(
                        "device_state_changed",
                        {"device_id": device_id, "old_state": old_state, "new_state": device.state}
                    )
            
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

    def save_state(self):
        state = {}

        for device_id, device in self.devices.items():
            state[device_id] = {
                "type": device.type,
                "state": getattr(device, "state", None),
                "data": getattr(device, "data", {}).copy()
            }

        self.state_storage.save(state)

    def restore_state(self):
            """Восстановить сохраненные состояния устройств"""
            if not hasattr(self, 'saved_states') or not self.saved_states:
                return
            
            restored_count = 0
            
            for device_id, saved_data in self.saved_states.items():
                device = self.get_device(device_id)
                if not device:
                    continue
                
                # Восстанавливаем состояние
                if "state" in saved_data and hasattr(device, "state"):
                    try:
                        if saved_data["state"] == "on":
                            device.turn_on()
                        elif saved_data["state"] == "off":
                            device.turn_off()
                        
                        restored_count += 1
                    except Exception as e:
                        self.logging_service.error("SYSTEM", 
                            f"Ошибка восстановления состояния {device_id}: {e}")
                
                # Восстанавливаем дополнительные данные
                if "data" in saved_data and hasattr(device, "data"):
                    for key, value in saved_data["data"].items():
                        device.data[key] = value
            
            self.logging_service.info("SYSTEM", f"Восстановлены состояния {restored_count} устройств")

    def load_initial_state(self):
        """Загрузить сохраненные состояния при запуске"""
        saved_states = self.state_storage.load()
        if saved_states:
            self.logging_service.info("SYSTEM", f"Загружено {len(saved_states)} сохраненных состояний устройств")
            # Сохраняем для последующего восстановления
            self.saved_states = saved_states
        else:
            self.saved_states = {}
            self.logging_service.info("SYSTEM", "Сохраненных состояний устройств не найдено")

    # def update_device_state_history(self, device_id: str, new_state: str):
    #     """Обновить историю состояний устройства"""
    #     if device_id not in self.device_state_history:
    #         self.device_state_history[device_id] = []
        
    #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     self.device_state_history[device_id].append({
    #         "timestamp": timestamp,
    #         "state": new_state
    #     })
    
    # Ограничиваем историю последними 100 записями
    # if len(self.device_state_history[device_id]) > 100:
    #     self.device_state_history[device_id] = self.device_state_history[device_id][-100:]

    def get_device_state_history(self, device_id: str, limit: int = 10):
        """Получить историю состояний устройства"""
        if device_id in self.device_state_history:
            return self.device_state_history[device_id][-limit:]
        return []

    def start_auto_save(self, interval_minutes: int = 5):from devices.lighting.smart_light import SmartLight
from devices.climate.thermostat import Thermostat
from devices.security.security_camera import SecurityCamera
from services.logging_service import LoggingService
from devices.security.smoke_sensor import SmokeSensor
from devices.security.water_leak_sensor import WaterLeakSensor
from services.storage_service import StateStorage
import time
from typing import Dict
from datetime import datetime

class DeviceManager:
    """Менеджер для управления всеми устройствами"""
    
    def __init__(self, event_bus=None):
        self.logging_service = LoggingService()
        self.event_bus = event_bus
        self.devices = {}
        self.device_states = {}
        self.state_storage = StateStorage()
        self._initialize_devices()
        
    def _initialize_devices(self):
        """Инициализация устройств по умолчанию"""
        # Создаем все устройства
        self.add_device(SmartLight("lamp_living_room", "Свет в гостиной"))
        self.add_device(Thermostat("thermostat", "Термостат"))
        self.add_device(SecurityCamera("security_camera", "Камера безопасности"))
        self.add_device(SmokeSensor("smoke_sensor", "Датчик дыма"))
        self.add_device(WaterLeakSensor("water_leak_sensor", "Датчик протечки"))
        
        # Восстанавливаем сохраненные состояния
        self.restore_state()
        
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
            old_state = device.state  # Запомнить старое состояние
            
            success = False
            
            if action == "on":
                success = device.turn_on()
            elif action == "off":
                success = device.turn_off()
            elif action == "toggle":
                if device.state == "on":
                    success = device.turn_off()
                else:
                    success = device.turn_on()
            elif ":" in action:
                # Команда с параметром (например, "set_temperature:22")
                parts = action.split(":", 1)
                command = parts[0]
                value = parts[1]
                
                if command == "set_temperature" and hasattr(device, "set_temperature"):
                    try:
                        success = device.set_temperature(float(value))
                    except ValueError:
                        success = False
                elif command == "set_brightness" and hasattr(device, "set_brightness"):
                    try:
                        success = device.set_brightness(int(value))
                    except ValueError:
                        success = False
                elif command == "on_and_set_temperature" and hasattr(device, "set_temperature"):
                    try:
                        # Включаем устройство
                        device.turn_on()
                        # Устанавливаем температуру
                        success = device.set_temperature(float(value))
                    except ValueError:
                        success = False
                elif command == "on_and_set_brightness" and hasattr(device, "set_brightness"):
                    try:
                        # Включаем устройство
                        device.turn_on()
                        # Устанавливаем яркость
                        success = device.set_brightness(int(value))
                    except ValueError:
                        success = False
                else:
                    success = False
            else:
                success = False
            
            # ЗАПИСАТЬ ИСТОРИЮ И СОХРАНИТЬ СОСТОЯНИЕ ЕСЛИ ИЗМЕНИЛОСЬ
            if success and device.state != old_state:
                self.update_device_state_history(device_id, device.state)
                self.logging_service.info("DEVICE", 
                    f"Состояние {device.name} изменено: {old_state} → {device.state}")
                
                # Сохраняем состояние в файл
                self.save_state()
                
                # Отправляем событие об изменении состояния
                if self.event_bus:
                    self.event_bus.publish(
                        "device_state_changed",
                        {"device_id": device_id, "old_state": old_state, "new_state": device.state}
                    )
            
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

    def save_state(self):
        """Сохранить текущие состояния всех устройств"""
        state = {}

        for device_id, device in self.devices.items():
            # Определяем тип устройства
            if hasattr(device, 'type'):
                device_type = device.type
            elif hasattr(device, '__class__'):
                device_type = device.__class__.__name__
            else:
                device_type = "unknown"
            
            state[device_id] = {
                "type": device_type,
                "state": getattr(device, "state", None),
                "data": getattr(device, "data", {}).copy()
            }

        success = self.state_storage.save(state)
        if success:
            self.logging_service.info("SYSTEM", f"Сохранены состояния {len(state)} устройств")
        return success

    def restore_state(self):
        """Восстановить сохраненные состояния устройств"""
        saved_states = self.state_storage.load()
        
        if not saved_states:
            self.logging_service.info("SYSTEM", "Сохраненных состояний не найдено")
            return
        
        restored_count = 0
        
        for device_id, saved_data in saved_states.items():
            device = self.get_device(device_id)
            if not device:
                continue
            
            # Восстанавливаем состояние
            if "state" in saved_data and hasattr(device, "state"):
                try:
                    if saved_data["state"] == "on":
                        device.turn_on()
                    elif saved_data["state"] == "off":
                        device.turn_off()
                    
                    restored_count += 1
                except Exception as e:
                    self.logging_service.error("SYSTEM", 
                        f"Ошибка восстановления состояния {device_id}: {e}")
            
            # Восстанавливаем дополнительные данные
            if "data" in saved_data and hasattr(device, "data"):
                for key, value in saved_data["data"].items():
                    device.data[key] = value
        
        if restored_count > 0:
            self.logging_service.info("SYSTEM", f"Восстановлены состояния {restored_count} устройств")

    def get_device_state_history(self, device_id: str, limit: int = 10):
        """Получить историю состояний устройства"""
        if device_id in self.device_states:
            return self.device_states[device_id][-limit:]
        return []

    def start_auto_save(self, interval_minutes: int = 5):
        """Запустить автоматическое сохранение состояний по расписанию"""
        def save_periodically():
            while True:
                time.sleep(interval_minutes * 60)
                self.save_state()
        
        import threading
        save_thread = threading.Thread(target=save_periodically, daemon=True)
        save_thread.start()
        self.logging_service.info("SYSTEM", f"Автосохранение запущено (каждые {interval_minutes} минут)")
        """Запустить автоматическое сохранение состояний по расписанию"""
        def save_periodically():
            while True:
                time.sleep(interval_minutes * 60)
                self.save_state()
        
        import threading
        save_thread = threading.Thread(target=save_periodically, daemon=True)
        save_thread.start()
        self.logging_service.info("SYSTEM", f"Автосохранение запущено (каждые {interval_minutes} минут)")