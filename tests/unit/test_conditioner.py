import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src/devices/climate'))

from conditioner import Conditioner

class TestConditioner(unittest.TestCase):
    
    def setUp(self):
        """Подготовка тестового объекта перед каждым тестом"""
        self.conditioner = Conditioner("ac_001", "Living Room AC")
    
    def test_initial_state(self):
        """Тест начального состояния кондиционера"""
        # Arrange & Act (объект уже создан в setUp)
        
        # Assert
        self.assertEqual(self.conditioner.device_id, "ac_001")
        self.assertEqual(self.conditioner.name, "Living Room AC")
        self.assertEqual(self.conditioner.state, "off")
        self.assertEqual(self.conditioner.temperature, 22)
    
    def test_turn_on(self):
        """Тест включения кондиционера"""
        # Act
        result = self.conditioner.turn_on()
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.conditioner.state, "on")
    
    def test_turn_off(self):
        """Тест выключения кондиционера"""
        # Arrange
        self.conditioner.turn_on()  # сначала включаем
        
        # Act
        result = self.conditioner.turn_off()
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.conditioner.state, "off")
    
    def test_set_temperature(self):
        """Тест установки температуры"""
        # Arrange
        new_temp = 24
        
        # Act
        result = self.conditioner.set_temperature(new_temp)
        
        # Assert
        self.assertTrue(result)
        self.assertEqual(self.conditioner.temperature, 24)
    
    def test_set_temperature_multiple_times(self):
        """Тест многократного изменения температуры"""
        # Act & Assert
        self.conditioner.set_temperature(18)
        self.assertEqual(self.conditioner.temperature, 18)
        
        self.conditioner.set_temperature(26)
        self.assertEqual(self.conditioner.temperature, 26)
        
        self.conditioner.set_temperature(22)
        self.assertEqual(self.conditioner.temperature, 22)
    
    def test_turn_on_off_sequence(self):
        """Тест последовательности включения/выключения"""
        # Act & Assert
        self.conditioner.turn_on()
        self.assertEqual(self.conditioner.state, "on")
        
        self.conditioner.turn_off()
        self.assertEqual(self.conditioner.state, "off")
        
        self.conditioner.turn_on()
        self.assertEqual(self.conditioner.state, "on")

if __name__ == '__main__':
    unittest.main()