from devices.base_device import BaseDevice
import random
import time
import threading
from datetime import datetime


class SecurityCamera(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "security")
        self.recording = False
        self.data["recording"] = False
        self.data["motion_detected"] = False
        self.data["last_motion_time"] = None
        self.metadata["motion_detection_enabled"] = True
        
        # Для фоновой симуляции движения
        self._motion_simulation_thread = None
        self._stop_motion_simulation_flag = threading.Event()  # ИЗМЕНЕНО: переименовано
        self._motion_check_interval = random.uniform(30, 60)  # 30-60 секунд
        self._last_motion_check = time.time()
        
        # Время суток влияет на вероятность движения
        self._daytime_probability = {
            "night_low": 0.1,    # 00:00-05:59 - низкая вероятность
            "morning_medium": 0.3,  # 06:00-08:59 - средняя
            "day_high": 0.5,     # 09:00-17:59 - высокая
            "evening_high": 0.4, # 18:00-21:59 - высокая
            "night_medium": 0.2  # 22:00-23:59 - средняя
        }

    def turn_on(self):
        self.state = "on"
        self.recording = True
        self.data["recording"] = True
        self.emit_event("state_changed", {"state": "on", "recording": True})
        # Запускаем симуляцию движения при включении
        self._start_motion_simulation()
        return True
        
    def turn_off(self):
        self.state = "off" 
        self.recording = False
        self.data["recording"] = False
        self.data["motion_detected"] = False
        # Останавливаем симуляцию движения при выключении
        self._stop_motion_simulation()  # Вызываем метод, а не Event
        self.emit_event("state_changed", {"state": "off", "recording": False})
        return True
    
    def toggle(self):
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()
    
    def _simulate_motion_detection(self):
        """Периодически (раз в 30-60 секунд) 'обнаруживать движение'"""
        if self.state == "on" and self.metadata.get("motion_detection_enabled", True):
            current_time = time.time()
            
            # Проверяем, прошло ли достаточно времени с последней проверки
            if current_time - self._last_motion_check >= self._motion_check_interval:
                # Обновляем время последней проверки
                self._last_motion_check = current_time
                
                # Генерируем новый случайный интервал для следующей проверки
                self._motion_check_interval = random.uniform(30, 60)
                
                # Определяем вероятность обнаружения в зависимости от времени суток
                probability = self._get_current_motion_probability()
                
                # Случайно определяем, было ли обнаружено движение
                if random.random() < probability:
                    # "Обнаруживаем" движение
                    self.data["motion_detected"] = True
                    self.data["last_motion_time"] = current_time
                    
                    # Дополнительные случайные данные для реалистичности
                    motion_data = {
                        "device_id": self.device_id,
                        "timestamp": current_time,
                        "motion_intensity": random.uniform(0.3, 1.0),
                        "motion_duration": random.uniform(1, 5),  # секунды
                        "motion_location": random.choice([
                            "front_door", "back_yard", "living_room", 
                            "kitchen", "garage", "driveway"
                        ]),
                        "confidence": random.uniform(0.7, 0.95)  # уверенность системы
                    }
                    
                    # Отправляем событие через EventBus
                    self.emit_event("motion_detected", motion_data)
                    
                    # Логирование для отладки
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Камера '{self.name}' "
                          f"обнаружила движение в зоне: {motion_data['motion_location']}")
                    
                    # Автоматически сбрасываем обнаружение через случайное время
                    reset_time = random.uniform(8, 15)  # 8-15 секунд
                    threading.Timer(reset_time, self._reset_motion_detection).start()
                    
                else:
                    # Если движение уже было обнаружено, проверяем не пора ли его сбросить
                    if self.data.get("motion_detected", False):
                        last_motion = self.data.get("last_motion_time")
                        if last_motion and (current_time - last_motion > 10):  # Сброс через 10 секунд
                            self._reset_motion_detection()

    def _get_current_motion_probability(self):
        """Возвращает вероятность обнаружения движения в зависимости от времени суток"""
        hour = datetime.now().hour
        
        if 0 <= hour < 6:    # Ночь (00:00-05:59)
            return self._daytime_probability["night_low"]
        elif 6 <= hour < 9:  # Утро (06:00-08:59)
            return self._daytime_probability["morning_medium"]
        elif 9 <= hour < 18: # День (09:00-17:59)
            return self._daytime_probability["day_high"]
        elif 18 <= hour < 22: # Вечер (18:00-21:59)
            return self._daytime_probability["evening_high"]
        else:                # Поздний вечер/ночь (22:00-23:59)
            return self._daytime_probability["night_medium"]

    def _reset_motion_detection(self):
        """Сбрасывает обнаружение движения"""
        if self.data.get("motion_detected", False):
            self.data["motion_detected"] = False
            self.emit_event("motion_cleared", {
                "device_id": self.device_id,
                "timestamp": time.time()
            })
            
    def _motion_simulation_loop(self):
        """Фоновый поток для симуляции обнаружения движения"""
        # ИЗМЕНЕНО: используем переименованный флаг
        while not self._stop_motion_simulation_flag.wait(5):  # Проверка каждые 5 секунд
            if self.state == "on":
                self._simulate_motion_detection()

    def _start_motion_simulation(self):
        """Запуск фоновой симуляции движения"""
        if self._motion_simulation_thread is None or not self._motion_simulation_thread.is_alive():
            # ИЗМЕНЕНО: используем переименованный флаг
            self._stop_motion_simulation_flag.clear()
            self._motion_simulation_thread = threading.Thread(
                target=self._motion_simulation_loop,
                daemon=True,
                name=f"MotionSim-{self.device_id}"
            )
            self._motion_simulation_thread.start()

    def _stop_motion_simulation(self):
        """Остановка фоновой симуляции движения"""
        # ИЗМЕНЕНО: устанавливаем флаг остановки
        self._stop_motion_simulation_flag.set()
        
        # Ждем завершения потока
        if self._motion_simulation_thread and self._motion_simulation_thread.is_alive():
            self._motion_simulation_thread.join(timeout=2)
            
            # Проверяем, завершился ли поток
            if self._motion_simulation_thread.is_alive():
                print(f"Предупреждение: Поток симуляции движения для камеры {self.device_id} не завершился вовремя")
            else:
                # Очищаем ссылку на поток
                self._motion_simulation_thread = None

    def enable_motion_detection(self):
        """Включить обнаружение движения"""
        self.metadata["motion_detection_enabled"] = True
        self.emit_event("motion_detection_enabled", {
            "device_id": self.device_id,
            "enabled": True
        })
        return True

    def disable_motion_detection(self):
        """Выключить обнаружение движения"""
        self.metadata["motion_detection_enabled"] = False
        self.data["motion_detected"] = False
        self.emit_event("motion_detection_disabled", {
            "device_id": self.device_id,
            "enabled": False
        })
        return True

    def check_device_changes(self):
        """Проверка изменений устройства (вызывается периодически)"""
        if self.state == "on":
            self._simulate_motion_detection()
        return super().check_device_changes()

    def get_status(self):
        """Получить статус камеры"""
        status = super().get_status()
        status.update({
            "motion_detected": self.data.get("motion_detected", False),
            "motion_detection_enabled": self.metadata.get("motion_detection_enabled", True),
            "last_motion_time": self.data.get("last_motion_time"),
            "recording": self.data.get("recording", False)
        })
        return status

    def cleanup(self):
        """Очистка ресурсов при удалении устройства"""
        self._stop_motion_simulation()
        super().cleanup()
