import pytest
from devices.lighting.smart_light import SmartLight

# Фикстура создает экземпляр умной лампы для использования в тестах
@pytest.fixture
def light():
    return SmartLight("lamp1", "Living Room Lamp")

# Тест проверяет корректность начальной инициализации умной лампы
def test_initial_state(light):
    assert light.device_id == "lamp1"
    assert light.name == "Living Room Lamp"
    assert light.device_type == "light"
    assert light.state == "off"
    assert light.brightness == 100

# Тест проверяет базовые методы включения/выключения лампы
# Проверяет изменение состояния и сброс яркости при выключении
def test_turn_on_off(light):
    light.turn_on()
    assert light.state == "on"

    light.turn_off()
    assert light.state == "off"
    assert light.brightness == 0

# Тест проверяет взаимосвязь между яркостью и состоянием лампы
# Убеждается, что установка яркости автоматически меняет состояние (on/off)
def test_toggle_state_via_brightness(light):
    # Установим яркость > 0 → включено
    assert light.set_brightness(50) is True
    assert light.state == "on"
    assert light.brightness == 50

    # Установим яркость 0 → выключено
    assert light.set_brightness(0) is True
    assert light.state == "off"
    assert light.brightness == 0

# Тест проверяет валидацию входных значений для установки яркости
def test_set_brightness_invalid(light):
    assert light.set_brightness(-1) is False
    assert light.set_brightness(101) is False

# Тест проверяет структуру возвращаемого статуса устройства
# Убеждается, что информация о яркости включена в общий статус лампы
def test_get_status_includes_brightness(light):
    status = light.get_status()
    assert "brightness" in status
    assert status["brightness"] == light.brightness