class AutomationService:
    def __init__(self, home_controller):
        self.controller = home_controller
        
    def run_demo_scenario(self):
        """Запуск демонстрационного сценария"""
        steps = [
            ("lamp_living_room", "on", "Включение света в гостиной"),
            ("thermostat", "on", "Включение термостата"),
            ("security_camera", "on", "Включение камеры безопасности"),
        ]
        
        for device_id, action, description in steps:
            print(f"🎯 {description}...")
            self.controller.device_manager.send_command(device_id, action)