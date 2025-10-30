# src/core/home_controller.py
import logging
from datetime import datetime

class HomeController:
    """Контроллер системы Умный дом"""
    
    def __init__(self):
        self.devices = {
            'lamp_living_room': {
                'name': 'Свет в гостиной', 
                'state': 'off', 
                'type': 'light',
                'brightness': 100
            },
            'thermostat': {
                'name': 'Термостат', 
                'state': 'off', 
                'type': 'climate', 
                'temperature': 22
            },
            'security_camera': {
                'name': 'Камера безопасности', 
                'state': 'off', 
                'type': 'security',
                'recording': False
            }
        }
        self.server_log = []
        self.device_log = []
        
        # Настройка логирования
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('SmartHome')
        
        # Логируем создание устройств
        for device_id, info in self.devices.items():
            self.log_message("DEVICE", f"➕ Добавлено устройство: {info['name']}")
    
    def log_message(self, component, message):
        """Универсальная функция логирования"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {component}: {message}"
        
        if component == "SERVER":
            self.server_log.append(log_entry)
        elif component == "DEVICE":
            self.device_log.append(log_entry)
        elif component == "SYSTEM":
            self.server_log.append(log_entry)
        
        print(log_entry)
        return log_entry
    
    def get_devices(self):
        """Получить все устройства"""
        return self.devices
    
    def get_device_status(self, device_id):
        """Получить статус устройства"""
        if device_id in self.devices:
            return self.devices[device_id]
        return None
    
    def send_command(self, device_id, action):
        """Отправить команду устройству"""
        if device_id not in self.devices:
            self.log_message("SERVER", f"❌ Ошибка: Устройство {device_id} не найдено")
            return False
        
        device = self.devices[device_id]
        old_state = device['state']
        
        # Обработка команд
        if action == 'on':
            device['state'] = 'on'
            self.log_message("SERVER", f"✅ Команда: {device_id} -> {action}")
            self.log_message("DEVICE", f"🔄 {device['name']}: {old_state} → on")
            
        elif action == 'off':
            device['state'] = 'off'
            self.log_message("SERVER", f"✅ Команда: {device_id} -> {action}")
            self.log_message("DEVICE", f"🔄 {device['name']}: {old_state} → off")
            
        elif action == 'toggle':
            new_state = 'on' if old_state == 'off' else 'off'
            device['state'] = new_state
            self.log_message("SERVER", f"✅ Команда: {device_id} -> {action}")
            self.log_message("DEVICE", f"🔄 {device['name']}: {old_state} → {new_state}")
            
        else:
            self.log_message("SERVER", f"❌ Ошибка: Некорректная команда '{action}' для {device_id}")
            return False
        
        return True
    
    def start_system(self):
        """Запуск системы"""
        self.log_message("SYSTEM", "🚀 Запуск системы Умный Дом")
        self.log_message("SERVER", "📍 Готов к приему команд")
        return True
    
    def get_server_logs(self):
        """Получить логи сервера"""
        return self.server_log[-10:]  # Последние 10 записей
    
    def get_device_logs(self):
        """Получить логи устройств"""
        return self.device_log[-10:]  # Последние 10 записей
    
    def get_all_logs(self):
        """Получить все логи"""
        return {
            'server': self.server_log,
            'devices': self.device_log
        }
