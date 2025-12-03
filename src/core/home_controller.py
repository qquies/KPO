import threading
from typing import Dict

from devices.device_manager import DeviceManager
from services.logging_service import LoggingService
from services.automation_service import AutomationService
from services.event_bus import EventBus
from services.notification_service import NotificationService
from config.settings import Settings

class HomeController:
    """Контроллер системы Умный дом"""
    
    def __init__(self):
        # Инициализация сервисов
        self.settings = Settings()
        self.logging_service = LoggingService()
        self.notification_service = NotificationService()
        self.event_bus = EventBus()
        self.device_manager = DeviceManager()
        self.automation_service = AutomationService(self)
        
        self.running = True
        
        # УДАЛЕНО: старый словарь devices - больше не нужен!
        
        # Настройка подписок на события
        self._setup_event_handlers()
        
        self.logging_service.info("SYSTEM", "🚀 Контроллер инициализирован")
    
    def _setup_event_handlers(self):
        """Настройка обработчиков событий"""
        self.event_bus.subscribe(
            EventBus.DEVICE_STATE_CHANGED,
            self._handle_device_state_change
        )
    
    def _handle_device_state_change(self, data: Dict):
        """Обработчик изменения состояния устройства"""
        device_id = data["device_id"]
        old_state = data["old_state"]
        new_state = data["new_state"]
        
        # Логирование
        self.logging_service.info(
            "SYSTEM", 
            f"Устройство {device_id} изменило состояние: {old_state} → {new_state}"
        )
        
        # Уведомление о важных изменениях
        if new_state == "on" and "camera" in device_id:
            self.notification_service.add_notification(
                "Камера активирована",
                f"Камера {device_id} начала запись", 
                "info"
            )
    
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
        
        return True
    
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
    
    # Методы для совместимости со старым кодом
    def get_devices(self):
        """Получить все устройства (для совместимости)"""
        return self.device_manager.devices
    
    def get_device_status(self, device_id):
        """Получить статус устройства (для совместимости)"""
        device = self.device_manager.get_device(device_id)
        return device.get_status() if device else None
    
    def send_command(self, device_id, action):
        """Отправить команду устройству (для совместимости)"""
        return self.device_manager.send_command(device_id, action)
    
    # Методы-заглушки для старого кода
    def set_temperature(self, temperature):
        """Заглушка для установки температуры"""
        return 15 <= temperature <= 30
    
    def set_brightness(self, brightness):
        """Заглушка для установки яркости"""
        return 0 <= brightness <= 100
    
    def validate_pin(self, pin_code):
        """Заглушка для проверки PIN-кода"""
        return pin_code.isdigit() and 4 <= len(pin_code) <= 6
    
    def set_energy_limit(self, energy):
        """Заглушка для установки лимита энергии"""
        return 0 <= energy <= 5000