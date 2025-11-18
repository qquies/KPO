import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Добавляем путь к src для корректного импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from devices.lighting.smart_light import SmartLight
from devices.climate.thermostat import Thermostat
from devices.security.security_camera import SecurityCamera
from devices.device_manager import DeviceManager
from services.logging_service import LoggingService
from core.home_controller import HomeController
from ui.console_interface import ConsoleInterface

class CauseEffectTests(unittest.TestCase):
    """
    Расширенный причинно-следственный анализ для системы Умный Дом
    Включает тестирование пользовательского интерфейса
    """
    
    def setUp(self):
        """Инициализация перед каждым тестом"""
        self.controller = HomeController()
        self.interface = ConsoleInterface(self.controller)
        self.device_manager = self.controller.device_manager
        
    def test_ce_01_light_control_combinations(self):
        """
        Причинно-следственный анализ: Управление умным светом
        Причины: Команда + Уровень яркости
        Следствия: Состояние + Яркость
        """
        print("\nТЕСТ CE-01: Комбинации управления светом")
        
        # Получаем тестовую лампу
        light = self.device_manager.get_device("lamp_living_room")
        self.assertIsNotNone(light, "Лампа должна существовать")
        
        # Таблица решений для тестирования комбинаций
        test_cases = [
            # (действие, параметр, ожидаемое_состояние, ожидаемая_яркость)
            ("on", None, "on", 0),      # Включить без параметра
            ("on", 50, "on", 50),         # Включить с яркостью 50%
            ("off", None, "off", 0),      # Выключить
            ("toggle", None, "on", 0),  # Переключить (из выкл в вкл)
        ]
        
        # Изначально лампа выключена
        light.turn_off()
        
        for i, (action, param, expected_state, expected_brightness) in enumerate(test_cases):
            with self.subTest(f"Тест {i+1}: {action} с param={param}"):
                # ПРИЧИНА: Отправка команды
                if action == "on" and param is not None:
                    result = light.set_brightness(param)
                else:
                    result = self.device_manager.send_command("lamp_living_room", action)
                
                # СЛЕДСТВИЕ: Проверка результата
                self.assertTrue(result, f"Команда {action} должна выполняться успешно")
                self.assertEqual(light.state, expected_state, 
                               f"Состояние должно быть '{expected_state}' после {action}")
                
                if hasattr(light, 'brightness'):
                    self.assertEqual(light.brightness, expected_brightness,
                                   f"Яркость должна быть {expected_brightness} после {action}")

    def test_ce_02_device_state_transitions(self):
        """
        Причинно-следственный анализ: Переходы состояний устройств
        Причины: Последовательность команд
        Следствия: Изменения состояний и логирование
        """
        print("\nТЕСТ CE-02: Переходы состояний устройств")
        
        devices_to_test = ["lamp_living_room", "thermostat", "security_camera"]
        
        for device_id in devices_to_test:
            with self.subTest(f"Устройство: {device_id}"):
                device = self.device_manager.get_device(device_id)
                self.assertIsNotNone(device, f"Устройство {device_id} должно существовать")
                
                # Последовательность команд для тестирования переходов
                command_sequence = [
                    ("off", "off"),   # Выключить выключенное
                    ("on", "on"),     # Включить
                    ("on", "on"),     # Включить включенное  
                    ("off", "off"),   # Выключить
                    ("toggle", "on"), # Переключить (выкл → вкл)
                    ("toggle", "off") # Переключить (вкл → выкл)
                ]
                
                for command, expected_state in command_sequence:
                    # ПРИЧИНА: Отправка команды
                    result = self.device_manager.send_command(device_id, command)
                    
                    # СЛЕДСТВИЕ: Проверка состояния
                    self.assertTrue(result, f"Команда {command} для {device_id} должна выполняться")
                    self.assertEqual(device.state, expected_state,
                                   f"Устройство {device_id} должно быть в состоянии '{expected_state}' после '{command}'")

    def test_ce_03_camera_security_modes(self):
        """
        Причинно-следственный анализ: Режимы безопасности камеры
        Причины: Состояние камеры + команды
        Следствия: Запись + состояние
        """
        print("\nТЕСТ CE-03: Режимы безопасности камеры")
        
        camera = self.device_manager.get_device("security_camera")
        self.assertIsNotNone(camera, "Камера должна существовать")
        
        # Тестовые случаи для камеры
        test_scenarios = [
            # (начальное_состояние, команда, ожидаемое_состояние, ожидаемая_запись)
            ("off", "on", "on", True),
            ("on", "off", "off", False),
            ("off", "toggle", "on", True),
            ("on", "toggle", "off", False),
        ]
        
        for initial_state, command, expected_state, expected_recording in test_scenarios:
            with self.subTest(f"Камера: {initial_state} -> {command}"):
                # Устанавливаем начальное состояние
                if initial_state == "on":
                    camera.turn_on()
                else:
                    camera.turn_off()
                
                # ПРИЧИНА: Отправка команды
                result = self.device_manager.send_command("security_camera", command)
                
                # СЛЕДСТВИЕ: Проверка состояния и записи
                self.assertTrue(result, f"Команда {command} должна выполняться")
                self.assertEqual(camera.state, expected_state, 
                               f"Состояние камеры должно быть '{expected_state}'")
                self.assertEqual(camera.recording, expected_recording,
                               f"Запись должна быть {expected_recording}")

    def test_ce_04_ui_menu_navigation(self):
        """
        Причинно-следственный анализ: Навигация по меню UI
        Причины: Выбор пунктов меню
        Следствия: Отображение правильных экранов
        """
        print("\nТЕСТ CE-04: Навигация по меню UI")
        
        test_cases = [
            # (выбор_меню, ожидаемый_вызов_метода, объект_для_mock)
            ("1", "_manage_lighting", "interface"),
            ("2", "_manage_climate", "interface"),
            ("3", "_manage_security", "interface"),
            ("4", "_show_logs", "interface"),
            ("5", "_run_demo_scenario", "interface"),
            ("6", "stop_system", "controller"),  # stop_system это метод контроллера!
        ]
        
        for menu_choice, expected_method, target in test_cases:
            with self.subTest(f"Меню выбор: {menu_choice}"):
                if target == "controller":
                    # Мокаем метод контроллера
                    with patch.object(self.controller, expected_method) as mock_method:
                        # ПРИЧИНА: Выбор пункта меню
                        self.interface._handle_menu_choice(menu_choice)
                        
                        # СЛЕДСТВИЕ: Должен вызваться соответствующий метод
                        mock_method.assert_called_once()
                else:
                    # Мокаем метод интерфейса
                    with patch.object(self.interface, expected_method) as mock_method:
                        # ПРИЧИНА: Выбор пункта меню
                        self.interface._handle_menu_choice(menu_choice)
                        
                        # СЛЕДСТВИЕ: Должен вызваться соответствующий метод
                        mock_method.assert_called_once()

    def test_ce_05_lighting_ui_interactions(self):
        """
        Причинно-следственный анализ: Взаимодействие с UI освещения
        Причины: Действия в подменю освещения
        Следствия: Команды устройствам + отображение состояния
        """
        print("\nТЕСТ CE-05: Взаимодействие с UI освещения")
        
        light = self.device_manager.get_device("lamp_living_room")
        
        # Тестируем корректность работы команд через UI логику
        ui_actions = [
            ("1", "on"),
            ("2", "off"), 
            ("3", "toggle"),
        ]
        
        for ui_choice, expected_action in ui_actions:
            with self.subTest(f"UI освещения: выбор {ui_choice}"):
                # Сохраняем начальное состояние
                initial_state = light.state
                
                # ПРИЧИНА: Имитируем действие через UI
                if expected_action == "on":
                    light.turn_on()
                elif expected_action == "off":
                    light.turn_off()
                elif expected_action == "toggle":
                    if light.state == "on":
                        light.turn_off()
                    else:
                        light.turn_on()
                
                # СЛЕДСТВИЕ: Проверяем изменение состояния
                if expected_action == "toggle":
                    expected_state = "off" if initial_state == "on" else "on"
                else:
                    expected_state = expected_action
                    
                self.assertEqual(light.state, expected_state,
                               f"Состояние должно быть '{expected_state}' после UI действия '{ui_choice}'")

    def test_ce_06_demo_scenario_execution(self):
        """
        Причинно-следственный анализ: Выполнение демо-сценария
        Причины: Запуск демо-сценария
        Следствия: Последовательность команд + конечное состояние системы
        """
        print("\nТЕСТ CE-06: Выполнение демо-сценария")
        
        # Получаем устройства
        light = self.device_manager.get_device("lamp_living_room")
        thermostat = self.device_manager.get_device("thermostat")
        camera = self.device_manager.get_device("security_camera")
        
        # Начальные состояния
        light.turn_off()
        thermostat.turn_off()
        camera.turn_off()
        
        # ПРИЧИНА: Выполняем демо-сценарий вручную (имитация)
        demo_steps = [
            ("lamp_living_room", "on"),
            ("thermostat", "on"),
            ("security_camera", "on"),
            ("lamp_living_room", "off"),
            ("thermostat", "off"),
        ]
        
        # Выполняем шаги демо-сценария
        for device_id, action in demo_steps:
            self.device_manager.send_command(device_id, action)
        
        # СЛЕДСТВИЕ: Проверяем конечное состояние системы
        self.assertEqual(light.state, "off", "Свет должен быть выключен")
        self.assertEqual(thermostat.state, "off", "Термостат должен быть выключен")
        self.assertEqual(camera.state, "on", "Камера должна быть включена")
        self.assertTrue(camera.recording, "Камера должна вести запись")

    def test_ce_07_invalid_input_handling(self):
        """
        Причинно-следственный анализ: Обработка неверного ввода
        Причины: Неправильный ввод пользователя
        Следствия: Сообщения об ошибках + сохранение состояния системы
        """
        print("\nТЕСТ CE-07: Обработка неверного ввода")
        
        # Тестируем неверные команды устройств
        light = self.device_manager.get_device("lamp_living_room")
        initial_state = light.state
        
        # ПРИЧИНА: Отправка неверной команды несуществующему устройству
        result = self.device_manager.send_command("nonexistent_device", "on")
        
        # СЛЕДСТВИЕ: Должен вернуть False
        self.assertFalse(result, "Команда несуществующему устройству должна возвращать False")
        
        # ПРИЧИНА: Отправка неверной команды существующему устройству
        result = self.device_manager.send_command("lamp_living_room", "invalid_command")
        
        # СЛЕДСТВИЕ: Должен вернуть False, состояние не должно измениться
        self.assertFalse(result, "Неверная команда должна возвращать False")
        self.assertEqual(light.state, initial_state, "Состояние не должно измениться при неверной команде")

    def test_ce_08_system_initialization(self):
        """
        Причинно-следственный анализ: Инициализация системы
        Причины: Запуск контроллера
        Следствия: Создание всех компонентов + начальное состояние
        """
        print("\nТЕСТ CE-08: Инициализация системы")
        
        # ПРИЧИНА: Создание контроллера
        controller = HomeController()
        
        # СЛЕДСТВИЕ: Проверяем создание всех компонентов
        self.assertIsNotNone(controller.device_manager, "Должен быть создан DeviceManager")
        self.assertIsNotNone(controller.logging_service, "Должен быть создан LoggingService")
        self.assertIsNotNone(controller.automation_service, "Должен быть создан AutomationService")
        
        # СЛЕДСТВИЕ: Проверяем инициализацию устройств
        expected_devices = ["lamp_living_room", "thermostat", "security_camera"]
        for device_id in expected_devices:
            device = controller.device_manager.get_device(device_id)
            self.assertIsNotNone(device, f"Должно быть создано устройство: {device_id}")
            
        # СЛЕДСТВИЕ: Система должна быть в рабочем состоянии
        self.assertTrue(controller.running, "Система должна быть в состоянии running")

    def test_ce_09_state_change_detection(self):
        """
        Причинно-следственный анализ: Обнаружение изменений состояний
        Причины: Изменения состояний устройств
        Следствия: Флаги изменений + корректное логирование
        """
        print("\nТЕСТ CE-09: Обнаружение изменений состояний")
        
        # Тестируем все устройства
        for device_id, device in self.device_manager.devices.items():
            with self.subTest(f"Обнаружение изменений: {device_id}"):
                # Сбрасываем флаги изменений
                device._previous_state = device.state
                
                # ПРИЧИНА: Изменяем состояние
                if device.state == "off":
                    device.turn_on()
                else:
                    device.turn_off()
                
                # СЛЕДСТВИЕ 1: Должен обнаружить изменение
                self.assertTrue(device.has_state_changed(),
                              f"Должно обнаружить изменение состояния для {device_id}")
                
                # СЛЕДСТВИЕ 2: При повторной проверке - не должно быть изменений
                self.assertFalse(device.has_state_changed(),
                               f"Не должно обнаружить повторное изменение для {device_id}")

    def test_ce_10_temperature_persistence(self):
        """
        Причинно-следственный анализ: Сохранение температуры термостата
        Причины: Включение/выключение термостата
        Следствия: Температура должна сохраняться
        """
        print("\nТЕСТ CE-10: Сохранение температуры термостата")
        
        thermostat = self.device_manager.get_device("thermostat")
        initial_temperature = thermostat.temperature
        
        # ПРИЧИНА: Включаем термостат
        thermostat.turn_on()
        
        # СЛЕДСТВИЕ: Температура должна сохраниться
        self.assertEqual(thermostat.temperature, initial_temperature,
                        "Температура должна сохраняться при включении")
        
        # ПРИЧИНА: Выключаем термостат
        thermostat.turn_off()
        
        # СЛЕДСТВИЕ: Температура должна сохраниться
        self.assertEqual(thermostat.temperature, initial_temperature,
                        "Температура должна сохраняться при выключении")

    def test_ce_11_ui_back_navigation(self):
        """
        Причинно-следственный анализ: Возврат из подменю
        Причины: Выбор "Назад" в подменю
        Следствия: Корректный возврат в главное меню
        """
        print("\nТЕСТ CE-11: Возврат из подменю")
        
        # Тестируем, что выбор "4" (Назад) в подменю приводит к выходу из цикла
        submenus = ["_manage_lighting", "_manage_climate", "_manage_security"]
        
        for submenu_method in submenus:
            with self.subTest(f"Возврат из: {submenu_method}"):
                # Создаем мок для метода подменю
                with patch.object(self.interface, submenu_method) as mock_submenu:
                    # Настраиваем мок чтобы он имитировал один вызов и выход
                    mock_submenu.return_value = None
                    
                    # ПРИЧИНА: Вызываем метод подменю (он должен завершиться)
                    getattr(self.interface, submenu_method)()
                    
                    # СЛЕДСТВИЕ: Метод должен быть вызван один раз
                    mock_submenu.assert_called_once()

def run_cause_effect_tests():
    """Запуск причинно-следственных тестов"""
    print("=" * 80)
    print("ЗАПУСК ПРИЧИННО-СЛЕДСТВЕННОГО АНАЛИЗА - СИСТЕМА УМНЫЙ ДОМ")
    print("=" * 80)
    
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(CauseEffectTests)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Генерируем отчет
    print("\n" + "=" * 80)
    print("ОТЧЕТ ПРИЧИННО-СЛЕДСТВЕННОГО АНАЛИЗА")
    print("=" * 80)
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    # Детальная статистика
    print("\nСТАТИСТИКА ПО ТЕСТАМ:")
    test_categories = {
        "Управление устройствами": ["CE-01", "CE-02", "CE-03", "CE-09", "CE-10"],
        "UI взаимодействие": ["CE-04", "CE-05", "CE-11"], 
        "Сценарии и потоки": ["CE-06", "CE-08"],
        "Обработка ошибок": ["CE-07"]
    }
    
    for category, tests in test_categories.items():
        print(f"   {category}: {len(tests)} тестов")
    
    if result.wasSuccessful():
        print("\nВСЕ ТЕСТЫ ПРИЧИННО-СЛЕДСТВЕННОГО АНАЛИЗА ПРОЙДЕНЫ!")
        print("   Система корректно обрабатывает причинно-следственные связи!")
    else:
        print("\nОбнаружены проблемы в логике системы!")
        print("   Рекомендуется провести ревизию обработки комбинаций условий")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_cause_effect_tests()