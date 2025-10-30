#!/usr/bin/env python3
"""
Комплексное тестирование системы Умный дом для лабораторной работы №5
"""
import sys
import os
import unittest

# Добавляем путь к src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from core.home_controller import HomeController
    from ui.console_interface import ConsoleInterface
    print("✅ Все модули загружены успешно!")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    sys.exit(1)

class TestSmartHomeSystem(unittest.TestCase):
    """Комплексное тестирование системы Умный дом"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.controller = HomeController()
        self.interface = ConsoleInterface(self.controller)
    
    def test_1_system_initialization(self):
        """Тест инициализации системы"""
        print("\n🔧 Тест 1: Инициализация системы")
        self.assertIsNotNone(self.controller)
        self.assertIsNotNone(self.interface)
        print("✅ Система инициализирована корректно")
    
    def test_2_device_management(self):
        """Тест управления устройствами"""
        print("\n💡 Тест 2: Управление устройствами")
        
        devices = self.controller.get_devices()
        self.assertIsInstance(devices, dict)
        self.assertGreater(len(devices), 0)
        print(f"✅ Найдено устройств: {len(devices)}")
        
        expected_devices = ['lamp_living_room', 'thermostat', 'security_camera']
        for device_id in expected_devices:
            self.assertIn(device_id, devices)
            print(f"✅ Устройство '{device_id}' присутствует")
    
    def test_3_command_processing(self):
        """Тест обработки команд"""
        print("\n🎮 Тест 3: Обработка команд")
        
        result = self.controller.send_command('lamp_living_room', 'on')
        self.assertTrue(result)
        print("✅ Команда 'on' выполнена успешно")
        
        device_state = self.controller.get_device_status('lamp_living_room')
        self.assertEqual(device_state['state'], 'on')
        print("✅ Состояние устройства обновлено корректно")
    
    def test_4_state_changes(self):
        """Тест изменений состояний"""
        print("\n🔄 Тест 4: Изменения состояний")
        
        initial_state = self.controller.get_device_status('lamp_living_room')['state']
        self.controller.send_command('lamp_living_room', 'toggle')
        new_state = self.controller.get_device_status('lamp_living_room')['state']
        
        self.assertNotEqual(initial_state, new_state)
        print(f"✅ Состояние изменено: {initial_state} → {new_state}")
    
    def test_5_error_handling(self):
        """Тест обработки ошибок"""
        print("\n🚨 Тест 5: Обработка ошибок")
        
        result = self.controller.send_command('unknown_device', 'on')
        self.assertFalse(result)
        print("✅ Ошибка несуществующего устройства обработана")
        
        result = self.controller.send_command('lamp_living_room', 'invalid_command')
        self.assertFalse(result)
        print("✅ Некорректная команда обработана")

def run_manual_tests():
    """Ручное тестирование для лабораторной работы"""
    print("\n" + "="*60)
    print("�� РУЧНОЕ ТЕСТИРОВАНИЕ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ")
    print("="*60)
    
    try:
        controller = HomeController()
        interface = ConsoleInterface(controller)
        controller.start_system()
        
        # Техника 1: Эквивалентное разделение
        print("\n1. 🔄 ЭКВИВАЛЕНТНОЕ РАЗДЕЛЕНИЕ")
        valid_commands = ['on', 'off', 'toggle']
        for cmd in valid_commands:
            result = controller.send_command('lamp_living_room', cmd)
            state = controller.get_device_status('lamp_living_room')['state']
            status = "✅ Успех" if result else "❌ Ошибка"
            print(f"   Команда '{cmd}': {status} → Состояние: {state}")
        
        # Техника 2: Анализ граничных значений
        print("\n2. 📊 АНАЛИЗ ГРАНИЧНЫХ ЗНАЧЕНИЙ")
        for i in range(3):
            controller.send_command('lamp_living_room', 'toggle')
            state = controller.get_device_status('lamp_living_room')['state']
            print(f"   Переключение {i+1}: {state}")
        
        print("\n🎉 РУЧНОЕ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при ручном тестировании: {e}")
        return False

if __name__ == '__main__':
    print("🚀 ЗАПУСК ТЕСТИРОВАНИЯ СИСТЕМЫ 'УМНЫЙ ДОМ'")
    
    # Запуск автоматических тестов
    print("\n🔧 АВТОМАТИЧЕСКИЕ ТЕСТЫ:")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSmartHomeSystem)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Запуск ручных тестов
    print("\n" + "="*60)
    success = run_manual_tests()
    
    if success and result.wasSuccessful():
        print("\n✅ ТЕСТИРОВАНИЕ ПРОЙДЕНО УСПЕШНО!")
    else:
        print("\n❌ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО С ОШИБКАМИ")
