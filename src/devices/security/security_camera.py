from devices.base_device import BaseDevice

class SecurityCamera(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "security")
        self.recording = False
        
    def turn_on(self):
        self.state = "on"
        self.recording = True
        return True
        
    def turn_off(self):
        self.state = "off" 
        self.recording = False
        return True