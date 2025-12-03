from devices.base_device import BaseDevice
import random
import time

class SecurityCamera(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "security")
        self.recording = False
        self.data["recording"] = False
        self.data["motion_detected"] = False
        self.data["last_motion_time"] = None
        self.metadata["motion_detection_enabled"] = True
        self.metadata["last_simulation_time"] = time.time()
        
    def turn_on(self):
        self.state = "on"
        self.recording = True
        self.data["recording"] = True
        self.emit_event("state_changed", {"state": "on", "recording": True})
        return True
        
    def turn_off(self):
        self.state = "off" 
        self.recording = False
        self.data["recording"] = False
        self.data["motion_detected"] = False
        self.emit_event("state_changed", {"state": "off", "recording": False})
        return True
    
    def toggle(self):
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()
    
    def _simulate_motion_detection(self):
        """Симуляция обнаружения движения (вызывается периодически)"""
        if self.state == "on" and self.metadata.get("motion_detection_enabled", True):
            current_time = time.time()
            last_sim_time = self.metadata.get("last_simulation_time", current_time)
            last_motion_time = self.data.get("last_motion_time")
            
            # Проверяем каждые 30-90 секунд (случайный интервал)
            time_since_last = current_time - last_sim_time
            
            # Если движение уже обнаружено, проверяем нужно ли его сбросить
            if self.data.get("motion_detected", False) and last_motion_time:
                # Сбрасываем через 5-10 секунд после обнаружения
                if current_time - last_motion_time > random.uniform(5, 10):
                    self.data["motion_detected"] = False
                    self.emit_event("motion_cleared", {
                        "device_id": self.device_id,
                        "timestamp": current_time
                    })
            # Вероятность обнаружения движения увеличивается со временем
            elif time_since_last > 30:
                # Случайно обнаруживаем движение (вероятность ~20% каждые 10 секунд после 30)
                if random.random() < 0.2 or time_since_last > 90:
                    self.data["motion_detected"] = True
                    self.data["last_motion_time"] = current_time
                    self.metadata["last_simulation_time"] = current_time
                    
                    # Отправляем событие через EventBus
                    self.emit_event("motion_detected", {
                        "device_id": self.device_id,
                        "timestamp": current_time
                    })