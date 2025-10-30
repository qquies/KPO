import threading
import re
from devices.device_manager import DeviceManager
from services.logging_service import LoggingService
from services.automation_service import AutomationService

class HomeController:
    """Главный контроллер системы умного дома"""
    
    def __init__(self):
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
