class Conditioner:
    def conditioner(self):
        self.device_id = device_id
        self.name = name
        self.state = "off"
        self.temperature = 22

    def set_temperature(self, temp):
        """Установка температуры - попадет в UC3"""
        self.temperature = temp
        return True
    def __init__(self, device_id, name):
        self.device_id = device_id
        self.name = name
        self.state = "off"
        self.temperature = 22
        
    def turn_on(self):
        self.state = "on"
        return True
        
    def turn_off(self):
        self.state = "off"
        return True