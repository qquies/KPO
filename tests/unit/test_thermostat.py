import pytest
from devices.climate.thermostat import Thermostat

@pytest.fixture
def thermostat():
    return Thermostat("thermo1", "Living Room Thermostat")

# Тест проверяет корректность начальной инициализации термостата
# Убеждается, что все параметры установлены в правильные значения по умолчанию
def test_initial_state(thermostat):
    assert thermostat.device_id == "thermo1"
    assert thermostat.name == "Living Room Thermostat"
    assert thermostat.device_type == "climate"
    assert thermostat.state == "off"
    assert thermostat.temperature == 22

# Тест проверяет базовые методы включения/выключения термостата
def test_turn_on_off(thermostat):
    thermostat.turn_on()
    assert thermostat.state == "on"

    thermostat.turn_off()
    assert thermostat.state == "off"

# Тест проверяет структуру возвращаемого статуса термостата
# Убеждается, что статус содержит все необходимые поля информации
def test_get_status_contains_temperature(thermostat):
    status = thermostat.get_status()
    assert "device_id" in status
    assert "state" in status
    assert status["state"] == thermostat.state