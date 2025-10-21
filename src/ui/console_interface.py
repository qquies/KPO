import os
import time

class ConsoleInterface:
    def __init__(self, home_controller):
        self.controller = home_controller
        
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
        print("\n🏠 СИСТЕМА УМНЫЙ ДОМ - ПРОФЕССИОНАЛЬНАЯ ВЕРСИЯ")
        print("=" * 50)
        
        print("\n📊 СОСТОЯНИЕ УСТРОЙСТВ:")
        for device_id, device in self.controller.device_manager.devices.items():
            state_icon = "💡" if device.state == "on" else "⚫"
            state_text = "ВКЛЮЧЕН" if device.state == "on" else "ВЫКЛЮЧЕН"
            print(f"{state_icon} {device.name}: {state_text}")
    
    def _handle_menu_choice(self, choice):
        """Обработка выбора в меню"""
        if choice == "1":
            self._manage_lighting()
        elif choice == "2":
            self._manage_climate()
        elif choice == "3":
            self._manage_security()
        elif choice == "4":
            self._show_logs()
        elif choice == "5":
            self._run_demo_scenario()
        elif choice == "6":
            self.controller.stop_system()
        else:
            input("❌ Неверный выбор! Нажмите Enter...")
    
    def _manage_lighting(self):
        """Управление освещением"""
        while True:
            os.system('clear')
            device = self.controller.device_manager.get_device("lamp_living_room")
            current_state = "ВКЛЮЧЕН" if device.state == "on" else "ВЫКЛЮЧЕН"
            
            print(f"💡 УПРАВЛЕНИЕ СВЕТОМ В ГОСТИНОЙ")
            print("=" * 40)
            print(f"Текущее состояние: {current_state}")
            print("\n1. Включить свет")
            print("2. Выключить свет")
            print("3. Переключить свет")
            print("4. Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                self.controller.device_manager.send_command("lamp_living_room", "on")
                print("💡 Свет включен!")
            elif sub_choice == "2":
                self.controller.device_manager.send_command("lamp_living_room", "off")
                print("⚫ Свет выключен!")
            elif sub_choice == "3":
                self.controller.device_manager.send_command("lamp_living_room", "toggle")
                new_state = "включен" if device.state == "on" else "выключен"
                print(f"🔁 Свет переключен: {new_state}")
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
            
            time.sleep(1)
    
    def _manage_climate(self):
        """Управление климатом"""
        while True:
            os.system('clear')
            device = self.controller.device_manager.get_device("thermostat")
            current_state = "ВКЛЮЧЕН" if device.state == "on" else "ВЫКЛЮЧЕН"
            
            print(f"🌡️ УПРАВЛЕНИЕ ТЕРМОСТАТОМ")
            print("=" * 40)
            print(f"Текущее состояние: {current_state}")
            print(f"Температура: {device.temperature}°C")
            print("\n1. Включить термостат")
            print("2. Выключить термостат")
            print("3. Переключить термостат")
            print("4. Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                self.controller.device_manager.send_command("thermostat", "on")
                print("🌡️ Термостат включен!")
            elif sub_choice == "2":
                self.controller.device_manager.send_command("thermostat", "off")
                print("🌡️ Термостат выключен!")
            elif sub_choice == "3":
                self.controller.device_manager.send_command("thermostat", "toggle")
                new_state = "включен" if device.state == "on" else "выключен"
                print(f"🔁 Термостат переключен: {new_state}")
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
            
            time.sleep(1)
    
    def _manage_security(self):
        """Управление безопасностью"""
        while True:
            os.system('clear')
            device = self.controller.device_manager.get_device("security_camera")
            current_state = "ВКЛЮЧЕНА" if device.state == "on" else "ВЫКЛЮЧЕНА"
            
            print(f"📹 УПРАВЛЕНИЕ КАМЕРОЙ БЕЗОПАСНОСТИ")
            print("=" * 40)
            print(f"Текущее состояние: {current_state}")
            print("\n1. Включить камеру")
            print("2. Выключить камеру")
            print("3. Переключить камеру")
            print("4. Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                self.controller.device_manager.send_command("security_camera", "on")
                print("📹 Камера включена!")
            elif sub_choice == "2":
                self.controller.device_manager.send_command("security_camera", "off")
                print("📹 Камера выключена!")
            elif sub_choice == "3":
                self.controller.device_manager.send_command("security_camera", "toggle")
                new_state = "включена" if device.state == "on" else "выключена"
                print(f"🔁 Камера переключена: {new_state}")
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
            
            time.sleep(1)
    
    def _show_logs(self):
        """Показать логи системы"""
        print("\n📋 ЛОГИ СИСТЕМЫ:")
        print("=" * 50)
        print("Функция логирования будет реализована в следующей версии")
        input("\nНажмите Enter для возврата в меню...")
    
    def _run_demo_scenario(self):
        """Запуск демонстрационного сценария"""
        print("\n🎬 ЗАПУСК ДЕМОНСТРАЦИОННОГО СЦЕНАРИЯ...")
        
        steps = [
            ("lamp_living_room", "on", "Включение света в гостиной"),
            ("thermostat", "on", "Включение термостата"),
            ("security_camera", "on", "Включение камеры безопасности"),
            ("lamp_living_room", "off", "Выключение света в гостиной"),
            ("thermostat", "off", "Выключение термостата"),
        ]
        
        for device_id, action, description in steps:
            print(f"\n🎯 {description}...")
            self.controller.device_manager.send_command(device_id, action)
            time.sleep(2)
        
        print("\n✅ Демонстрационный сценарий завершен!")
        input("Нажмите Enter для возврата в меню...")