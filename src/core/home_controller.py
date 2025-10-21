import threading
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
        
    def start_system(self):
        """Запуск всей системы"""
        self.logging_service.info("SYSTEM", "🚀 Запуск системы Умный Дом")
        
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
        self.logging_service.info("SYSTEM", "🛑 Система остановлена")