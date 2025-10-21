from devices.base_device import BaseDevice

class Thermostat(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "climate")
        self.temperature = 22
        
    def turn_on(self):
        self.state = "on"
        return True
        
    def turn_off(self):
        self.state = "off"
        return True