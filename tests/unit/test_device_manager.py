import unittest
import sys
import os
from unittest.mock import Mock, patch

# Добавляем пути к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/devices'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/devices/lighting'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/devices/climate'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/devices/security'))

class TestDeviceManager(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестового объекта перед каждым тестом"""
        self.mock_logging_service = Mock()
    
    def _create_device_manager(self):
        """Создает DeviceManager с мокнутым logging_service"""
        with patch('device_manager.LoggingService') as mock_logging_class:
            mock_logging_class.return_value = self.mock_logging_service
            from device_manager import DeviceManager
            manager = DeviceManager()
            # Очищаем устройства для чистых тестов и сбрасываем счетчик вызовов
            manager.devices = {}
            self.mock_logging_service.reset_mock()  # Сбрасываем счетчик вызовов
            return manager
    
    def test_initialization(self):
        """Тест инициализации DeviceManager"""
        # Arrange & Act
        with patch('device_manager.LoggingService') as mock_logging_class:
            mock_logging_class.return_value = self.mock_logging_service
            from device_manager import DeviceManager
            manager = DeviceManager()
            
        # Assert
        self.assertIsNotNone(manager.devices)
        self.assertIsNotNone(manager.logging_service)
        # Проверяем что было добавлено 3 устройства по умолчанию
        self.assertEqual(len(manager.devices), 3)
        # Проверяем что было 3 вызова логирования для начальных устройств
        self.assertEqual(self.mock_logging_service.info.call_count, 3)
        
    def test_add_device(self):
        """Тест добавления устройства"""
        # Arrange
        manager = self._create_device_manager()
        test_device = Mock()
        test_device.device_id = "test_light"
        test_device.name = "Test Light"
        
        # Act
        manager.add_device(test_device)
        
        # Assert
        self.assertIn("test_light", manager.devices)
        self.assertEqual(manager.devices["test_light"], test_device)
        manager.logging_service.info.assert_called_once_with(
            "DEVICE", "Добавлено устройство: Test Light"
        )
    
    def test_get_device_existing(self):
        """Тест получения существующего устройства"""
        # Arrange
        manager = self._create_device_manager()
        test_device = Mock()
        test_device.device_id = "test_light"
        manager.devices["test_light"] = test_device
        
        # Act
        result = manager.get_device("test_light")
        
        # Assert
        self.assertEqual(result, test_device)
    
    def test_get_device_nonexistent(self):
        """Тест получения несуществующего устройства"""
        # Arrange
        manager = self._create_device_manager()
        
        # Act
        result = manager.get_device("nonexistent")
        
        # Assert
        self.assertIsNone(result)
    
    def test_send_command_turn_on(self):
        """Тест отправки команды включения"""
        # Arrange
        manager = self._create_device_manager()
        mock_device = Mock()
        mock_device.turn_on.return_value = True
        manager.devices["test_device"] = mock_device
        
        # Act
        result = manager.send_command("test_device", "on")
        
        # Assert
        self.assertTrue(result)
        mock_device.turn_on.assert_called_once()
    
    def test_send_command_turn_off(self):
        """Тест отправки команды выключения"""
        # Arrange
        manager = self._create_device_manager()
        mock_device = Mock()
        mock_device.turn_off.return_value = True
        manager.devices["test_device"] = mock_device
        
        # Act
        result = manager.send_command("test_device", "off")
        
        # Assert
        self.assertTrue(result)
        mock_device.turn_off.assert_called_once()
    
    def test_send_command_toggle_from_off_to_on(self):
        """Тест команды toggle с выключенного состояния"""
        # Arrange
        manager = self._create_device_manager()
        mock_device = Mock()
        mock_device.state = "off"
        mock_device.turn_on.return_value = True
        manager.devices["test_device"] = mock_device
        
        # Act
        result = manager.send_command("test_device", "toggle")
        
        # Assert
        self.assertTrue(result)
        mock_device.turn_on.assert_called_once()
        mock_device.turn_off.assert_not_called()
    
    def test_send_command_toggle_from_on_to_off(self):
        """Тест команды toggle с включенного состояния"""
        # Arrange
        manager = self._create_device_manager()
        mock_device = Mock()
        mock_device.state = "on"
        mock_device.turn_off.return_value = True
        manager.devices["test_device"] = mock_device
        
        # Act
        result = manager.send_command("test_device", "toggle")
        
        # Assert
        self.assertTrue(result)
        mock_device.turn_off.assert_called_once()
        mock_device.turn_on.assert_not_called()
    
    def test_send_command_nonexistent_device(self):
        """Тест отправки команды несуществующему устройству"""
        # Arrange
        manager = self._create_device_manager()
        
        # Act
        result = manager.send_command("nonexistent", "on")
        
        # Assert
        self.assertFalse(result)
    
    def test_send_command_invalid_action(self):
        """Тест отправки невалидной команды"""
        # Arrange
        manager = self._create_device_manager()
        mock_device = Mock()
        manager.devices["test_device"] = mock_device
        
        # Act
        result = manager.send_command("test_device", "invalid_action")
        
        # Assert
        self.assertFalse(result)
        mock_device.turn_on.assert_not_called()
        mock_device.turn_off.assert_not_called()
    
    def test_check_device_changes(self):
        """Тест проверки изменений состояний устройств"""
        # Arrange
        manager = self._create_device_manager()
        
        # Создаем моки устройств с разными состояниями
        mock_device1 = Mock()
        mock_device1.name = "Device 1"
        mock_device1.state = "on"
        mock_device1.has_state_changed.return_value = True
        
        mock_device2 = Mock()
        mock_device2.name = "Device 2" 
        mock_device2.state = "off"
        mock_device2.has_state_changed.return_value = False
        
        manager.devices = {
            "device1": mock_device1,
            "device2": mock_device2
        }
        
        # Act
        manager.check_device_changes()
        
        # Assert
        # Должен быть записан только лог для device1 (у которого было изменение)
        manager.logging_service.info.assert_called_once_with(
            "DEVICE", "Device 1 включено"
        )
    
    def test_multiple_devices_management(self):
        """Тест управления несколькими устройствами"""
        # Arrange
        manager = self._create_device_manager()
        
        # Создаем моки устройств
        light = Mock()
        light.device_id = "light1"
        light.name = "Light 1"
        
        thermostat = Mock()
        thermostat.device_id = "thermo1" 
        thermostat.name = "Thermostat 1"
        
        camera = Mock()
        camera.device_id = "camera1"
        camera.name = "Camera 1"
        
        # Act
        manager.add_device(light)
        manager.add_device(thermostat)
        manager.add_device(camera)
        
        # Assert
        self.assertEqual(len(manager.devices), 3)
        self.assertIn("light1", manager.devices)
        self.assertIn("thermo1", manager.devices)
        self.assertIn("camera1", manager.devices)
        
        # Проверяем что все устройства доступны по ID
        self.assertEqual(manager.get_device("light1"), light)
        self.assertEqual(manager.get_device("thermo1"), thermostat)
        self.assertEqual(manager.get_device("camera1"), camera)
        
        # Проверяем что было 3 вызова логирования для добавленных устройств
        self.assertEqual(manager.logging_service.info.call_count, 3)

if __name__ == '__main__':
    unittest.main()