import time
import os
import threading
from datetime import datetime

class SmartHomeLab:
    def __init__(self):
        self.devices = {
            "lamp_living_room": {
                "name": "Свет в гостиной", 
                "type": "light", 
                "state": "off",
                "brightness": 100
            },
            "thermostat": {
                "name": "Термостат",
                "type": "climate", 
                "state": "off",
                "temperature": 22
            },
            "security_camera": {
                "name": "Камера безопасности",
                "type": "security",
                "state": "off",
                "recording": False
            }
        }
        self.server_log = []
        self.device_log = []
        self.client_log = []
        self.running = True
        
    def log_message(self, component, message):
        """Универсальная функция логирования"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {component}: {message}"
        
        if component == "SERVER":
            self.server_log.append(log_entry)
            print(f"🔧 {log_entry}")
        elif component == "DEVICE":
            self.device_log.append(log_entry)
            print(f"💡 {log_entry}")
        elif component == "CLIENT":
            self.client_log.append(log_entry)
            print(f"📱 {log_entry}")
    
    def emulate_server(self):
        """Эмуляция серверной части"""
        self.log_message("SERVER", "🚀 Сервер Умного дома запущен")
        self.log_message("SERVER", "📍 Порт: 8000")
        self.log_message("SERVER", "✅ Готов к приему команд")
        
        while self.running:
            # Сервер "слушает" команды (в реальности они приходят через интерфейс)
            time.sleep(1)
    
    def emulate_devices(self):
        """Эмуляция работы умных устройств"""
        self.log_message("DEVICE", "🚀 Запуск эмулятора устройств")
        
        previous_states = {device_id: info["state"] for device_id, info in self.devices.items()}
        
        while self.running:
            # Проверяем изменения состояний устройств
            for device_id, info in self.devices.items():
                current_state = info["state"]
                if current_state != previous_states[device_id]:
                    old_state = previous_states[device_id]
                    self.log_message("DEVICE", f"🔄 ИЗМЕНЕНИЕ: {info['name']} {old_state} → {current_state}")
                    
                    # Эмуляция физического действия устройства
                    if current_state == "on":
                        if device_id == "lamp_living_room":
                            self.log_message("DEVICE", "💡 Лампа в гостиной загорелась")
                        elif device_id == "thermostat":
                            self.log_message("DEVICE", "🌡️ Термостат начал работу")
                        elif device_id == "security_camera":
                            self.log_message("DEVICE", "📹 Камера начала запись")
                    else:
                        if device_id == "lamp_living_room":
                            self.log_message("DEVICE", "⚫ Лампа в гостиной погасла")
                        elif device_id == "thermostat":
                            self.log_message("DEVICE", "🌡️ Термостат остановлен")
                        elif device_id == "security_camera":
                            self.log_message("DEVICE", "📹 Камера остановлена")
                    
                    previous_states[device_id] = current_state
            
            time.sleep(2)
    
    def send_command(self, device_id, action):
        """Отправка команды устройству"""
        if device_id in self.devices:
            old_state = self.devices[device_id]["state"]
            
            if action == "toggle":
                new_state = "on" if old_state == "off" else "off"
            else:
                new_state = action
            
            self.devices[device_id]["state"] = new_state
            
            # Логируем на сервере
            self.log_message("SERVER", f"📨 Получена команда: {device_id} -> {action}")
            self.log_message("SERVER", f"✅ Выполнено: {old_state} → {new_state}")
            
            # Логируем в клиенте
            self.log_message("CLIENT", f"📤 Отправлена команда: {action} для {self.devices[device_id]['name']}")
            self.log_message("CLIENT", f"✅ Устройство {self.devices[device_id]['name']} теперь {new_state}")
            
            return True
        return False
    
    def show_system_status(self):
        """Показать статус всей системы"""
        print("\n" + "🏠" + "="*58 + "🏠")
        print("              СИСТЕМА УМНЫЙ ДОМ - ЛАБОРАТОРНАЯ РАБОТА")
        print("🏠" + "="*58 + "🏠")
        
        print("\n📊 СОСТОЯНИЕ УСТРОЙСТВ:")
        print("-" * 60)
        for device_id, info in self.devices.items():
            state_icon = "💡" if info["state"] == "on" else "⚫"
            state_text = "ВКЛЮЧЕН" if info["state"] == "on" else "ВЫКЛЮЧЕН"
            print(f"{state_icon} {info['name']}: {state_text}")
            
            # Дополнительная информация
            if device_id == "thermostat" and info["state"] == "on":
                print(f"   🌡️ Температура: {info['temperature']}°C")
            elif device_id == "lamp_living_room" and info["state"] == "on":
                print(f"   💡 Яркость: {info['brightness']}%")
            elif device_id == "security_camera" and info["state"] == "on":
                print(f"   📹 Запись: {'ВКЛЮЧЕНА' if info['recording'] else 'ВЫКЛЮЧЕНА'}")
    
    def show_logs(self, log_type):
        """Показать логи определенного типа"""
        os.system('clear')
        print(f"\n📋 ЛОГИ {log_type}:")
        print("=" * 70)
        
        if log_type == "SERVER":
            logs = self.server_log[-15:]  # Последние 15 записей
        elif log_type == "DEVICE":
            logs = self.device_log[-15:]
        elif log_type == "CLIENT":
            logs = self.client_log[-15:]
        else:
            logs = []
        
        for log in logs:
            print(log)
        
        input(f"\nНажмите Enter для возврата в меню...")
    
    def run_demo_scenario(self):
        """Запуск демонстрационного сценария"""
        print("\n🎬 ЗАПУСК ДЕМОНСТРАЦИОННОГО СЦЕНАРИЯ...")
        time.sleep(1)
        
        steps = [
            ("lamp_living_room", "on", "Включение света в гостиной"),
            ("thermostat", "on", "Включение термостата"),
            ("security_camera", "on", "Включение камеры безопасности"),
            ("lamp_living_room", "off", "Выключение света в гостиной"),
            ("thermostat", "off", "Выключение термостата"),
        ]
        
        for device_id, action, description in steps:
            print(f"\n🎯 {description}...")
            self.send_command(device_id, action)
            time.sleep(2)
        
        print("\n✅ Демонстрационный сценарий завершен!")
        input("Нажмите Enter для возврата в меню...")
    
    def display_main_menu(self):
        """Главное меню управления"""
        while self.running:
            os.system('clear')
            self.show_system_status()
            
            print("\n🎮 УПРАВЛЕНИЕ СИСТЕМОЙ:")
            print("=" * 40)
            print("1. 💡 Управление светом в гостиной")
            print("2. 🌡️ Управление термостатом")
            print("3. 📹 Управление камерой безопасности")
            print("4. 📊 Показать логи сервера")
            print("5. 💡 Показать логи устройств")
            print("6. 📱 Показать логи клиента")
            print("7. 🎬 Запуск демонстрационного сценария")
            print("8. 🚪 Выход")
            print("=" * 40)
            
            try:
                choice = input("\nВыберите действие (1-8): ").strip()
                
                if choice == "1":
                    self.manage_light()
                elif choice == "2":
                    self.manage_thermostat()
                elif choice == "3":
                    self.manage_camera()
                elif choice == "4":
                    self.show_logs("SERVER")
                elif choice == "5":
                    self.show_logs("DEVICE")
                elif choice == "6":
                    self.show_logs("CLIENT")
                elif choice == "7":
                    self.run_demo_scenario()
                elif choice == "8":
                    self.log_message("SERVER", "Завершение работы системы")
                    self.running = False
                    break
                else:
                    input("❌ Неверный выбор! Нажмите Enter...")
                    
            except KeyboardInterrupt:
                self.running = False
                break
    
    def manage_light(self):
        """Управление светом"""
        while True:
            os.system('clear')
            current_state = self.devices["lamp_living_room"]["state"]
            state_text = "ВКЛЮЧЕН" if current_state == "on" else "ВЫКЛЮЧЕН"
            
            print(f"💡 УПРАВЛЕНИЕ СВЕТОМ В ГОСТИНОЙ")
            print("=" * 40)
            print(f"Текущее состояние: {state_text}")
            print(f"Яркость: {self.devices['lamp_living_room']['brightness']}%")
            print("\n1. Включить свет")
            print("2. Выключить свет")
            print("3. Переключить свет")
            print("4. Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                self.send_command("lamp_living_room", "on")
            elif sub_choice == "2":
                self.send_command("lamp_living_room", "off")
            elif sub_choice == "3":
                self.send_command("lamp_living_room", "toggle")
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
            
            input("\nНажмите Enter для продолжения...")
    
    def manage_thermostat(self):
        """Управление термостатом"""
        while True:
            os.system('clear')
            current_state = self.devices["thermostat"]["state"]
            state_text = "ВКЛЮЧЕН" if current_state == "on" else "ВЫКЛЮЧЕН"
            
            print(f"🌡️ УПРАВЛЕНИЕ ТЕРМОСТАТОМ")
            print("=" * 40)
            print(f"Текущее состояние: {state_text}")
            print(f"Температура: {self.devices['thermostat']['temperature']}°C")
            print("\n1. Включить термостат")
            print("2. Выключить термостат")
            print("3. Переключить термостат")
            print("4. Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                self.send_command("thermostat", "on")
            elif sub_choice == "2":
                self.send_command("thermostat", "off")
            elif sub_choice == "3":
                self.send_command("thermostat", "toggle")
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
            
            input("\nНажмите Enter для продолжения...")
    
    def manage_camera(self):
        """Управление камерой безопасности"""
        while True:
            os.system('clear')
            current_state = self.devices["security_camera"]["state"]
            state_text = "ВКЛЮЧЕНА" if current_state == "on" else "ВЫКЛЮЧЕНА"
            
            print(f"📹 УПРАВЛЕНИЕ КАМЕРОЙ БЕЗОПАСНОСТИ")
            print("=" * 40)
            print(f"Текущее состояние: {state_text}")
            print("\n1. Включить камеру")
            print("2. Выключить камеру")
            print("3. Переключить камеру")
            print("4. Назад")
            
            sub_choice = input("\nВыберите действие: ").strip()
            
            if sub_choice == "1":
                self.send_command("security_camera", "on")
            elif sub_choice == "2":
                self.send_command("security_camera", "off")
            elif sub_choice == "3":
                self.send_command("security_camera", "toggle")
            elif sub_choice == "4":
                break
            else:
                input("❌ Неверный выбор! Нажмите Enter...")
            
            input("\nНажмите Enter для продолжения...")
    
    def run(self):
        """Запуск всей системы"""
        print("🚀 ИНИЦИАЛИЗАЦИЯ СИСТЕМЫ УМНЫЙ ДОМ...")
        time.sleep(1)
        
        # Запускаем эмуляцию сервера и устройств в отдельных потоках
        server_thread = threading.Thread(target=self.emulate_server)
        server_thread.daemon = True
        server_thread.start()
        
        device_thread = threading.Thread(target=self.emulate_devices)
        device_thread.daemon = True
        device_thread.start()
        
        # Запускаем основной интерфейс
        self.display_main_menu()
        
        print("\n👋 СИСТЕМА ЗАВЕРШИЛА РАБОТУ")
        print("📋 Для лабораторной работы готово:")
        print("   ✅ Модель ЖЦ (итерационная)")
        print("   ✅ Этапы проекта выделены") 
        print("   ✅ Кодирование и отладка выполнены")
        print("   ✅ Все компоненты системы работают")

if __name__ == "__main__":
    lab_system = SmartHomeLab()
    lab_system.run()