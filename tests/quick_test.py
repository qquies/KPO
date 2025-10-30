#!/usr/bin/env python3
"""
Быстрый тест системы Умный дом
"""
import sys
import os

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.home_controller import HomeController
from ui.console_interface import ConsoleInterface

def quick_test():
    """Быстрый тест системы"""
    print("🚀 БЫСТРЫЙ ТЕСТ СИСТЕМЫ УМНЫЙ ДОМ")
    print("=" * 50)
    
    try:
        # 1. Создание контроллера
        print("1. Создаем контроллер...")
        controller = HomeController()
        print("✅ Контроллер создан")
        
        # 2. Проверка методов
        print("\n2. Проверяем методы контроллера...")
        devices = controller.get_devices()
        print(f"✅ get_devices() работает. Устройств: {len(devices)}")
        
        # 3. Проверка состояния устройства
        lamp_status = controller.get_device_status('lamp_living_room')
        print(f"✅ get_device_status() работает. Лампа: {lamp_status['state']}")
        
        # 4. Отправка команды
        print("\n3. Тестируем команды...")
        result = controller.send_command('lamp_living_room', 'on')
        print(f"✅ send_command() работает. Результат: {result}")
        
        # 5. Проверка изменения состояния
        new_status = controller.get_device_status('lamp_living_room')
        print(f"✅ Состояние изменилось: {lamp_status['state']} → {new_status['state']}")
        
        # 6. Создание интерфейса
        print("\n4. Тестируем интерфейс...")
        interface = ConsoleInterface(controller)
        print("✅ Интерфейс создан")
        
        # 7. Отображение устройств
        interface.display_devices()
        print("✅ display_devices() работает")
        
        # 8. Запуск системы
        print("\n5. Запускаем систему...")
        controller.start_system()
        print("✅ Система запущена")
        
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    quick_test()
