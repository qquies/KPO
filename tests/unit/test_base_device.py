import pytest
from abc import ABC
from devices.base_device import BaseDevice

# Создаём тестовый класс-наследник для абстрактного BaseDevice
class TestDevice(BaseDevice):
    __test__ = False
    def turn_on(self):
        self.state = "on"
        return True
    
    def turn_off(self):
        self.state = "off"
        return True

@pytest.fixture
def device():
    return TestDevice("device1", "Generic Device", "generic")

# Проверка корректности начального состояния устройства
def test_initial_state(device):
    assert device.device_id == "device1"
    assert device.name == "Generic Device"
    assert device.device_type == "generic"
    assert device.state == "off"
    assert device._previous_state == "off"

# Проверка работы методов включения/выключения и отслеживания изменений состояния
def test_turn_on_off(device):
    device.turn_on()
    assert device.state == "on"
    assert device.has_state_changed() is True

    device._previous_state = device.state
    device.turn_off()
    assert device.state == "off"
    assert device.has_state_changed() is True

# Проверка логики определения изменений состояния устройства
def test_has_state_changed(device):
    device._previous_state = "off"
    device.state = "off"
    assert device.has_state_changed() is False

    device.state = "on"
    assert device.has_state_changed() is True