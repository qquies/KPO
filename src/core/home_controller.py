# src/core/home_controller.py
import logging
from datetime import datetime
import threading
import re
from devices.device_manager import DeviceManager
from services.logging_service import LoggingService
from services.automation_service import AutomationService

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

        self.device_manager = DeviceManager()
        self.logging_service = LoggingService()
        self.automation_service = AutomationService(self)
        self.running = True

    # 👇 МЕТОДЫ-ЗАГЛУШКИ
    def set_temperature(self, temperature):
        """Заглушка для установки температуры"""
        # Допустимый диапазон: 15-30°C
        return 15 <= temperature <= 30
    
    def set_brightness(self, brightness):
        """Заглушка для установки яркости"""
        # Допустимый диапазон: 0-100%
        return 0 <= brightness <= 100
    
    def validate_pin(self, pin_code):
        """Заглушка для проверки PIN-кода"""
        # Допустимый PIN: 4-6 цифр
        return pin_code.isdigit() and 4 <= len(pin_code) <= 6
    
    def set_schedule_time(self, time_str):
        if not re.fullmatch(r"\d{2}:\d{2}", time_str):
            return False
        hours, minutes = time_str.split(':')
        return 0 <= int(hours) <= 23 and 0 <= int(minutes) <= 59
    
    def set_energy_limit(self, energy):
        """Заглушка для установки лимита энергии"""
        # Допустимый диапазон: 0-5000 Вт
        return 0 <= energy <= 5000
        
    def start_system(self):
        """Запуск всей системы"""
        self.logging_service.info("SYSTEM", "Запуск системы Умный Дом")
        
        # Запускаем сервисы в отдельных потоках
        server_thread = threading.Thread(target=self._run_server)
        server_thread.daemon = True
        server_thread.start()
        
        device_thread = threading.Thread(target=self._run_device_monitor)
        device_thread.daemon = True
        device_thread.start()
        
    def _run_server(self):
        """Запуск серверной части"""
        while self.running:
            # Эмуляция работы сервера
            threading.Event().wait(1)
            
    def _run_device_monitor(self):
        """Мониторинг устройств"""
        while self.running:
            self.device_manager.check_device_changes()
            threading.Event().wait(2)
            
    def stop_system(self):
        """Остановка системы"""
        self.running = False
        self.logging_service.info("SYSTEM", "Система остановлена")
