import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/devices/security'))

from security_camera import SecurityCamera

class TestSecurityCamera(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестового объекта перед каждым тестом"""
        self.camera = SecurityCamera("cam_001", "Front Door Camera")
    
    def test_initial_state(self):
        """Тест начального состояния камеры"""
        # Arrange & Act (объект уже создан в setUp)
        
        # Assert
        self.assertEqual(self.camera.device_id, "cam_001")
        self.assertEqual(self.camera.name, "Front Door Camera")
        self.assertEqual(self.camera.device_type, "security")
        self.assertEqual(self.camera.state, "off")
        self.assertFalse(self.camera.recording)
    
    def test_turn_on(self):
        """Тест включения камеры (должна начать запись)"""
        # Act
        result = self.camera.turn_on()
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.camera.state, "on")
        self.assertTrue(self.camera.recording)
    
    def test_turn_off(self):
        """Тест выключения камеры (должна остановить запись)"""
        # Arrange
        self.camera.turn_on()  # сначала включаем
        
        # Act
        result = self.camera.turn_off()
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.camera.state, "off")
        self.assertFalse(self.camera.recording)
    
    def test_recording_starts_when_turned_on(self):
        """Тест что запись автоматически начинается при включении"""
        # Arrange
        self.assertFalse(self.camera.recording)
        
        # Act
        self.camera.turn_on()
        
        # Assert
        self.assertTrue(self.camera.recording)
    
    def test_recording_stops_when_turned_off(self):
        """Тест что запись автоматически останавливается при выключении"""
        # Arrange
        self.camera.turn_on()
        self.assertTrue(self.camera.recording)
        
        # Act
        self.camera.turn_off()
        
        # Assert
        self.assertFalse(self.camera.recording)
    
    def test_turn_on_off_sequence(self):
        """Тест последовательности включения/выключения"""
        # Act & Assert
        self.camera.turn_on()
        self.assertEqual(self.camera.state, "on")
        self.assertTrue(self.camera.recording)
        
        self.camera.turn_off()
        self.assertEqual(self.camera.state, "off")
        self.assertFalse(self.camera.recording)
        
        self.camera.turn_on()
        self.assertEqual(self.camera.state, "on")
        self.assertTrue(self.camera.recording)
    
    def test_inheritance_from_base_device(self):
        """Тест что камера наследует от BaseDevice"""
        # Arrange & Act
        camera = SecurityCamera("test_cam", "Test Camera")
        
        # Assert
        self.assertTrue(hasattr(camera, 'device_id'))
        self.assertTrue(hasattr(camera, 'name'))
        self.assertTrue(hasattr(camera, 'device_type'))
        self.assertTrue(hasattr(camera, 'state'))
        self.assertTrue(hasattr(camera, 'recording'))
    
    def test_multiple_cameras(self):
        """Тест создания нескольких камер"""
        # Arrange & Act
        camera1 = SecurityCamera("cam_001", "Camera 1")
        camera2 = SecurityCamera("cam_002", "Camera 2")
        
        # Assert
        self.assertEqual(camera1.device_id, "cam_001")
        self.assertEqual(camera2.device_id, "cam_002")
        self.assertEqual(camera1.name, "Camera 1")
        self.assertEqual(camera2.name, "Camera 2")
        
        # Проверяем что они независимы
        camera1.turn_on()
        self.assertEqual(camera1.state, "on")
        self.assertEqual(camera2.state, "off")

if __name__ == '__main__':
    unittest.main()