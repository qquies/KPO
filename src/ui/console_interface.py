import os
import time
from datetime import datetime

class ConsoleInterface:
    def __init__(self, home_controller):
        self.controller = home_controller
        
    def display_main_menu(self):
        """Главное меню управления"""
        while self.controller.running:
            os.system('clear')
            self._show_enhanced_system_status()
            
            print("\n🎮 УПРАВЛЕНИЕ СИСТЕМОЙ:")
            print("=" * 50)
            print("1. 💡 Управление освещением")
            print("2. 🌡️ Управление климатом") 
            print("3. 📹 Управление безопасностью")
            print("4. 📊 Расширенная информация")
            print("5. 🔔 Уведомления")
            print("6. 🎬 Демонстрационные сценарии")
            print("7. ⚙️ Настройки системы")
            print("8. 🚪 Выход")
            print("=" * 50)
            
            choice = input("\nВыберите действие (1-8): ").strip()
            self._handle_menu_choice(choice)
    
    def _show_enhanced_system_status(self):
        """Показать расширенный статус системы"""
        print(f"\n🏠 {self.controller.settings.SYSTEM_NAME} v{self.controller.settings.VERSION}")
        print("=" * 60)
        
        # ИСПРАВЛЕНИЕ: используем device_manager вместо devices
        devices_status = self.controller.device_manager.get_all_devices_status()
        online_count = sum(1 for status in devices_status.values() if status.get("online"))
        on_count = sum(1 for status in devices_status.values() if status.get("state") == "on")
        
        print(f"📊 СТАТИСТИКА: {on_count}/{len(devices_status)} устройств активно | "
              f"{online_count}/{len(devices_status)} онлайн")
        
        # Уведомления (проверяем что сервис существует)
        if hasattr(self.controller, 'notification_service'):
            unread_notifications = len(self.controller.notification_service.get_unread_notifications())
            if unread_notifications > 0:
                print(f"🔔 УВЕДОМЛЕНИЯ: {unread_notifications} непрочитанных")
        
        print("\n📋 СОСТОЯНИЕ УСТРОЙСТВ:")
        print("-" * 60)
        
        # ИСПРАВЛЕНИЕ: используем device_manager
        for device_id, status in devices_status.items():
            device = self.controller.device_manager.get_device(device_id)
            
            # Иконки состояний
            state_icon = "💡" if status["state"] == "on" else "⚫"
            online_icon = "🟢" if status.get("online", True) else "🔴"
            
            # Дополнительная информация
            extra_info = ""
            if device_id == "thermostat" and status["state"] == "on":
                extra_info = f" | 🌡️ {getattr(device, 'temperature', 'N/A')}°C"
            elif device_id == "lamp_living_room" and status["state"] == "on":
                extra_info = f" | 💡 {getattr(device, 'brightness', 'N/A')}%"
            elif device_id == "security_camera" and status["state"] == "on":
                recording_status = "🔴 Запись" if getattr(device, 'recording', False) else "⏸️ Пауза"
                extra_info = f" | {recording_status}"
            
            state_text = "ВКЛ" if status["state"] == "on" else "ВЫКЛ"
            print(f"{online_icon} {state_icon} {device.name}: {state_text}{extra_info}")
    
    def _handle_menu_choice(self, choice):
        """Обработка выбора в меню"""
        menu_actions = {
            "1": self._manage_lighting,
            "2": self._manage_climate,
            "3": self._manage_security,
            "4": self._show_advanced_info,
            "5": self._show_notifications,
            "6": self._run_demo_scenario,
            "7": self._show_system_settings,
            "8": self.controller.stop_system,
        }
        
        action = menu_actions.get(choice)
        if action:
            action()
        else:
            input("❌ Неверный выбор! Нажмите Enter...")
    
    def _manage_lighting(self):
        """Управление освещением"""
        device = self.controller.device_manager.get_device("lamp_living_room")
        if not device:
            print("❌ Устройство не найдено!")
            return
            
        while True:
            os.system('clear')
            status = self.controller.device_manager.get_device_status("lamp_living_room")
            
            print(f"💡 УПРАВЛЕНИЕ ОСВЕЩЕНИЕМ")
            print("=" * 50)
            print(f"Устройство: {device.name}")
            print(f"Состояние: {'🟢 ВКЛЮЧЕН' if status['state'] == 'on' else '⚫ ВЫКЛЮЧЕН'}")
            print(f"Яркость: {getattr(device, 'brightness', 'N/A')}%")
            print(f"Онлайн: {'🟢 Да' if status['online'] else '🔴 Нет'}")
            
            print("\n1. 🔄 Переключить свет")
            print("2. 💡 Включить свет")
            print("3. ⚫ Выключить свет")
            print("4. ↩️ Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                success = self.controller.device_manager.send_command("lamp_living_room", "toggle")
                action = "переключен"
            elif sub_choice == "2":
                success = self.controller.device_manager.send_command("lamp_living_room", "on")
                action = "включен"
            elif sub_choice == "3":
                success = self.controller.device_manager.send_command("lamp_living_room", "off")
                action = "выключен"
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
                continue
            
            if success:
                print(f"✅ Свет {action}!")
            else:
                print("❌ Ошибка выполнения команды!")
            
            time.sleep(1)
    
    def _manage_climate(self):
        """Управление климатом"""
        device = self.controller.device_manager.get_device("thermostat")
        if not device:
            print("❌ Устройство не найдено!")
            return
            
        while True:
            os.system('clear')
            status = self.controller.device_manager.get_device_status("thermostat")
            
            print(f"🌡️ УПРАВЛЕНИЕ КЛИМАТОМ")
            print("=" * 50)
            print(f"Устройство: {device.name}")
            print(f"Состояние: {'🟢 ВКЛЮЧЕН' if status['state'] == 'on' else '⚫ ВЫКЛЮЧЕН'}")
            print(f"Текущая температура: {getattr(device, 'temperature', 'N/A')}°C")
            print(f"Онлайн: {'🟢 Да' if status['online'] else '🔴 Нет'}")
            
            print("\n1. 🔄 Переключить термостат")
            print("2. 🌡️ Включить обогрев")
            print("3. ❄️ Выключить обогрев")
            print("4. ↩️ Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                success = self.controller.device_manager.send_command("thermostat", "toggle")
                action = "переключен"
            elif sub_choice == "2":
                success = self.controller.device_manager.send_command("thermostat", "on")
                action = "включен"
            elif sub_choice == "3":
                success = self.controller.device_manager.send_command("thermostat", "off")
                action = "выключен"
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
                continue
            
            if success:
                print(f"✅ Термостат {action}!")
            else:
                print("❌ Ошибка выполнения команды!")
            
            time.sleep(1)
    
    def _manage_security(self):
        """Управление безопасностью"""
        device = self.controller.device_manager.get_device("security_camera")
        if not device:
            print("❌ Устройство не найдено!")
            return
            
        while True:
            os.system('clear')
            status = self.controller.device_manager.get_device_status("security_camera")
            
            print(f"📹 УПРАВЛЕНИЕ БЕЗОПАСНОСТЬЮ")
            print("=" * 50)
            print(f"Устройство: {device.name}")
            print(f"Состояние: {'🟢 ВКЛЮЧЕНА' if status['state'] == 'on' else '⚫ ВЫКЛЮЧЕНА'}")
            print(f"Запись: {'🔴 ВКЛЮЧЕНА' if getattr(device, 'recording', False) else '⏸️ ВЫКЛЮЧЕНА'}")
            print(f"Онлайн: {'🟢 Да' if status['online'] else '🔴 Нет'}")
            
            print("\n1. 🔄 Переключить камеру")
            print("2. 📹 Включить наблюдение")
            print("3. ⏸️ Выключить наблюдение")
            print("4. ↩️ Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                success = self.controller.device_manager.send_command("security_camera", "toggle")
                action = "переключена"
            elif sub_choice == "2":
                success = self.controller.device_manager.send_command("security_camera", "on")
                action = "включена"
            elif sub_choice == "3":
                success = self.controller.device_manager.send_command("security_camera", "off")
                action = "выключена"
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
                continue
            
            if success:
                print(f"✅ Камера {action}!")
            else:
                print("❌ Ошибка выполнения команды!")
            
            time.sleep(1)
    
    def _show_advanced_info(self):
        """Показать расширенную информацию о системе"""
        os.system('clear')
        
        print("📊 РАСШИРЕННАЯ ИНФОРМАЦИЯ О СИСТЕМЕ")
        print("=" * 60)
        
        # Статистика системы
        devices_status = self.controller.device_manager.get_all_devices_status()
        total_devices = len(devices_status)
        online_devices = sum(1 for status in devices_status.values() if status.get("online"))
        active_devices = sum(1 for status in devices_status.values() if status.get("state") == "on")
        
        print(f"\n📈 СТАТИСТИКА СИСТЕМЫ:")
        print(f"   Всего устройств: {total_devices}")
        print(f"   Онлайн устройств: {online_devices}")
        print(f"   Активных устройств: {active_devices}")
        if total_devices > 0:
            print(f"   Процент активности: {(active_devices/total_devices)*100:.1f}%")
        
        # Уведомления
        if hasattr(self.controller, 'notification_service'):
            notifications = self.controller.notification_service.notifications
            unread_count = len([n for n in notifications if not n['read']])
            print(f"\n🔔 УВЕДОМЛЕНИЯ: {unread_count} непрочитанных из {len(notifications)}")
        
        input("\nНажмите Enter для возврата в меню...")
    
    def _show_notifications(self):
        """Показать уведомления"""
        if not hasattr(self.controller, 'notification_service'):
            print("❌ Сервис уведомлений не доступен")
            input("Нажмите Enter для возврата...")
            return
            
        os.system('clear')
        
        notifications = self.controller.notification_service.notifications
        unread_notifications = self.controller.notification_service.get_unread_notifications()
        
        print("🔔 УВЕДОМЛЕНИЯ СИСТЕМЫ")
        print("=" * 60)
        print(f"Всего: {len(notifications)} | Непрочитанных: {len(unread_notifications)}")
        print("-" * 60)
        
        if not notifications:
            print("📭 Уведомлений нет")
        else:
            # Показать последние 10 уведомлений
            for notification in notifications[-10:]:
                level_icon = {
                    "info": "ℹ️",
                    "warning": "⚠️", 
                    "error": "❌"
                }.get(notification['level'], "📝")
                
                read_icon = "📪" if notification['read'] else "📬"
                time_str = notification['timestamp'][11:16]
                
                print(f"{read_icon} {level_icon} [{time_str}] {notification['title']}")
                print(f"      {notification['message']}")
                print()
        
        print("\n1. 📪 Пометить все как прочитанные")
        print("2. 🗑️ Очистить все уведомления") 
        print("3. ↩️ Назад")
        
        choice = input("\nВыберите действие: ").strip()
        
        if choice == "1":
            for notification in unread_notifications:
                self.controller.notification_service.mark_as_read(notification['id'])
            print("✅ Все уведомления помечены как прочитанные")
            time.sleep(1)
        
        elif choice == "2":
            self.controller.notification_service.notifications = []
            print("✅ Все уведомления очищены")
            time.sleep(1)
    
    def _show_system_settings(self):
        """Показать настройки системы"""
        os.system('clear')
        
        print("⚙️ НАСТРОЙКИ СИСТЕМЫ")
        print("=" * 50)
        print(f"Версия системы: {self.controller.settings.VERSION}")
        print(f"Интервал обновления: {self.controller.settings.DEVICE_UPDATE_INTERVAL} сек")
        print(f"Хранение логов: {self.controller.settings.LOG_RETENTION_DAYS} дней")
        
        print("\n1. ↩️ Назад")
        
        input("\nНажмите Enter для возврата...")
    
    def _run_demo_scenario(self):
        """Запуск демонстрационного сценария"""
        print("\n🎬 ЗАПУСК ДЕМОНСТРАЦИОННОГО СЦЕНАРИЯ...")
        time.sleep(1)
        
        steps = [
            ("lamp_living_room", "on", "💡 Включение света в гостиной"),
            ("thermostat", "on", "🌡️ Включение термостата"),
            ("security_camera", "on", "📹 Включение камеры безопасности"),
            ("lamp_living_room", "off", "⚫ Выключение света в гостиной"), 
            ("thermostat", "off", "❄️ Выключение термостата"),
            ("security_camera", "off", "⏸️ Выключение камеры безопасности"),
        ]
        
        for device_id, action, description in steps:
            print(f"\n🎯 {description}...")
            success = self.controller.device_manager.send_command(device_id, action)
            if success:
                print("   ✅ Успешно!")
            else:
                print("   ❌ Ошибка!")
            time.sleep(2)
        
        print("\n✅ Демонстрационный сценарий завершен!")
        input("Нажмите Enter для возврата в меню...")