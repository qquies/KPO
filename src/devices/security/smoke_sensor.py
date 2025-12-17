from devices.base_device import BaseDevice

class SmokeSensor(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "smoke")
        self.state = "off"
        self.data["enabled"] = False
        self.data["triggered"] = False
        self.type = "smoke"

    def turn_on(self):
        self.state = "on"
        self.data["enabled"] = True
        self.emit_event("state_changed", {"device_id": self.device_id, "state": "on"})
        return True

    def turn_off(self):
        self.state = "off"
        self.data["enabled"] = False
        self.data["triggered"] = False
        self.emit_event("state_changed", {"device_id": self.device_id, "state": "off"})
        return True

    def toggle(self):
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()

    def trigger_alarm(self):
        """Эмулирует срабатывание датчика"""
        if self.state == "on" and not self.data["triggered"]:
            self.data["triggered"] = True
            # Отправляем событие
            self.emit_event("state_changed", {"device_id": self.device_id, "state": "alarm"})
            # Добавляем уведомление через EventBus/HomeController
            if hasattr(self, "event_bus"):
                self.event_bus.publish("device_alarm", {
                    "device_id": self.device_id,
                    "type": "fire",
                    "message": f"⚠️ Датчик {self.name} обнаружил пожар!"
                })
            return True
        return False