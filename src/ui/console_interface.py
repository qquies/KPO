# src/ui/console_interface.py
import os

class ConsoleInterface:
    """Консольный интерфейс системы Умный дом"""
    
    def __init__(self, controller):
        self.controller = controller
    
    def display_devices(self):
        """Отобразить все устройства"""
        devices = self.controller.get_devices()
        print("\n🏠 СОСТОЯНИЕ УСТРОЙСТВ УМНОГО ДОМА:")
        print("=" * 50)
        
        for device_id, info in devices.items():
            state_icon = "💡" if info['state'] == 'on' else "⚫"
            state_text = "ВКЛЮЧЕН" if info['state'] == 'on' else "ВЫКЛЮЧЕН"
            print(f"{state_icon} {info['name']}: {state_text}")
            
            # Дополнительная информация
            if device_id == 'thermostat' and info['state'] == 'on':
                print(f"   🌡️ Температура: {info['temperature']}°C")
            elif device_id == 'lamp_living_room' and info['state'] == 'on':
                print(f"   💡 Яркость: {info['brightness']}%")
            elif device_id == 'security_camera' and info['state'] == 'on':
                recording_status = "ВКЛЮЧЕНА" if info['recording'] else "ВЫКЛЮЧЕНА"
                print(f"   📹 Запись: {recording_status}")
    
    def display_server_logs(self):
        """Отобразить логи сервера"""
        logs = self.controller.get_server_logs()
        print("\n🔧 ЛОГИ СЕРВЕРА:")
        print("=" * 50)
        if logs:
            for log in logs:
                print(log)
        else:
            print("Логи сервера пусты")
    
    def display_device_logs(self):
        """Отобразить логи устройств"""
        logs = self.controller.get_device_logs()
        print("\n💡 ЛОГИ УСТРОЙСТВ:")
        print("=" * 50)
        if logs:
            for log in logs:
                print(log)
        else:
            print("Логи устройств пусты")
    
    def process_command(self, device_id, action):
        """Обработать команду"""
        return self.controller.send_command(device_id, action)
    
    def clear_screen(self):
        """Очистить экран"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_system_status(self):
        """Показать статус системы"""
        self.display_devices()
        print("\n" + "="*50)
