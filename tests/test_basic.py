#!/usr/bin/env python3
"""
Базовые тесты для системы Умный дом
"""
import sys
import os

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_system_initialization():
    """Тест инициализации системы"""
    try:
        from core.home_controller import HomeController
        from ui.console_interface import ConsoleInterface
        
        print("🧪 Тест 1: Инициализация системы...")
        controller = HomeController()
        interface = ConsoleInterface(controller)
        
        assert controller is not None, "Контроллер не создан"
        assert interface is not None, "Интерфейс не создан"
        print("✅ Система инициализирована корректно")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        return False

def test_devices_exist():
    """Тест наличия устройств"""
    try:
        from core.home_controller import HomeController
        controller = HomeController()
        
        print("🧪 Тест 2: Проверка устройств...")
        devices = controller.get_devices()
        
        assert isinstance(devices, dict), "Устройства должны быть словарем"
        assert len(devices) > 0, "Должны быть устройства"
        
        expected_devices = ['lamp_living_room', 'thermostat', 'security_camera']
        for device_id in expected_devices:
            assert device_id in devices, f"Устройство {device_id} отсутствует"
            print(f"✅ Устройство {device_id} присутствует")
        
        print("✅ Все устройства присутствуют")
        return True
    except Exception as e:
        print(f"❌ Ошибка проверки устройств: {e}")
        return False

def test_command_processing():
    """Тест обработки команд"""
    try:
        from core.home_controller import HomeController
        controller = HomeController()
        
        print("🧪 Тест 3: Обработка команд...")
        
        # Тест включения
        result = controller.send_command('lamp_living_room', 'on')
        assert result == True, "Команда включения не выполнена"
        
        # Проверка состояния
        device_state = controller.get_device_status('lamp_living_room')
        assert device_state['state'] == 'on', "Состояние не изменилось на on"
        
        print("✅ Команды обрабатываются корректно")
        return True
    except Exception as e:
        print(f"❌ Ошибка обработки команд: {e}")
        return False

if __name__ == '__main__':
    print("🚀 ЗАПУСК БАЗОВЫХ ТЕСТОВ СИСТЕМЫ УМНЫЙ ДОМ")
    print("=" * 50)
    
    tests = [
        test_system_initialization,
        test_devices_exist,
        test_command_processing
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 РЕЗУЛЬТАТ: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("❌ НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")
