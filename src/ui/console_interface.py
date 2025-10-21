import os
from services.logging_service import LoggingService

class ConsoleInterface:
    """Консольный интерфейс для управления системой"""
    
    def __init__(self, home_controller):
        self.controller = home_controller
        self.logging_service = LoggingService()
        
    def display_main_menu(self):
        """Главное меню управления"""
        while self.controller.running:
            os.system('clear')
            self._show_system_status()
            
            print("\n🎮 УПРАВЛЕНИЕ СИСТЕМОЙ:")
            print("=" * 40)
            print("1. 💡 Управление освещением")
            print("2. 🌡️ Управление климатом")
            print("3. 📹 Управление безопасностью")
            print("4. 📊 Показать логи системы")
            print("5. 🎬 Демонстрационные сценарии")
            print("6. 🚪 Выход")
            print("=" * 40)
            
            choice = input("\nВыберите действие (1-6): ").strip()
            self._handle_menu_choice(choice)
    
    def _show_system_status(self):
        """Показать статус системы"""
        print("\n" + "🏠" + "="*58 + "🏠")
        print("              СИСТЕМА УМНЫЙ ДОМ - ПРОФЕССИОНАЛЬНАЯ ВЕРСИЯ")
        print("🏠" + "="*58 + "🏠")
        
        print("\n📊 СОСТОЯНИЕ УСТРОЙСТВ:")
        print("-" * 60)
        for device_id, device in self.controller.device_manager.devices.items():
            state_icon = "💡" if device.state == "on" else "⚫"
            state_text = "ВКЛЮЧЕН" if device.state == "on" else "ВЫКЛЮЧЕН"
            print(f"{state_icon} {device.name}: {state_text}")
    
    def _handle_menu_choice(self, choice):
        """Обработка выбора в меню"""
        menu_actions = {
            "1": self._manage_lighting,
            "2": self._manage_climate,
            "3": self._manage_security,
            "4": self._show_logs,
            "5": self._run_demo_scenario,
            "6": self._exit_system
        }
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            input("❌ Неверный выбор! Нажмите Enter...")
    
    def _exit_system(self):
        """Выход из системы"""
        self.controller.stop_system()