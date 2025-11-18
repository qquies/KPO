import pytest
from unittest.mock import MagicMock, patch

from core.home_controller import HomeController

@pytest.fixture
def controller():
    """Создает контроллер с замоканными сервисами, чтобы не запускались потоки"""
    with patch("core.home_controller.DeviceManager") as dm_mock:
        with patch("core.home_controller.LoggingService") as log_mock:
            with patch("core.home_controller.DeviceManager") as auto_mock:
                dm_mock.return_value = MagicMock()
                log_mock.return_value = MagicMock()
                auto_mock.return_value = MagicMock()

                ctrl = HomeController()
                return ctrl


# ---------------------------
#   ТЕСТЫ НА СТАТУС УСТРОЙСТВ
# ---------------------------

def test_get_devices(controller):
    devices = controller.get_devices()
    assert "lamp_living_room" in devices    # Проверяет существование устройства
    assert "thermostat" in devices
    assert isinstance(devices, dict)        # Проверяет тип возвращаемых данных


def test_get_device_status_valid(controller):
    status = controller.get_device_status("lamp_living_room")
    assert status["type"] == "light"        # Проверка типа устройства
    assert status["state"] in ["on", "off"] # Проверка допустимых состояний


def test_get_device_status_invalid(controller):
    assert controller.get_device_status("unknown_device") is None


# ---------------------------
#      ТЕСТЫ НА КОМАНДЫ
# ---------------------------

def test_send_command_on(controller):
    result = controller.send_command("lamp_living_room", "on")
    assert result is True                                               # Проверяет успешность команды
    assert controller.devices["lamp_living_room"]["state"] == "on"      # Проверяет изменение состояния


def test_send_command_off(controller):
    controller.devices["lamp_living_room"]["state"] = "on"              # Включаем лампу
    result = controller.send_command("lamp_living_room", "off")         # Выключаем
    assert result is True
    assert controller.devices["lamp_living_room"]["state"] == "off"     # Проверка: состояние изменилось


def test_send_command_toggle(controller):
    controller.devices["lamp_living_room"]["state"] = "off"
    controller.send_command("lamp_living_room", "toggle")
    assert controller.devices["lamp_living_room"]["state"] == "on"


def test_send_command_invalid_device(controller):
    result = controller.send_command("xxx", "on")                       # Несуществующее устройство
    assert result is False                                              # Должен вернуть false при ошибке


def test_send_command_invalid_action(controller):
    result = controller.send_command("lamp_living_room", "bad_command") # Неверная команда
    assert result is False                                              # Должен вернуть false при неизвестной команде


# ---------------------------
#         ЛОГИ
# ---------------------------

def test_server_logs(controller):
    controller.log_message("SERVER", "Test server log")             # Записываем серверный лог
    logs = controller.get_server_logs()                             # Получаем серверные логи
    assert any("Test server log" in log for log in logs)            # Проверяем наличие лога


def test_device_logs(controller):
    controller.log_message("DEVICE", "Test device log")             # Записываем лог устройства
    logs = controller.get_device_logs()                             # Получаем логи устройств
    assert any("Test device log" in log for log in logs)            # Проверяем наличие лога


def test_get_all_logs(controller):
    controller.log_message("SERVER", "S")                           # Записываем серверный лог
    controller.log_message("DEVICE", "D")                           # Записываем лог устройства

    logs = controller.get_all_logs()                                # Получаем ВСЕ логи
    assert "server" in logs                                         # Проверяем структуру ответа
    assert "devices" in logs                                        # Должны быть обе категории
    assert len(logs["server"]) > 0                                  # Серверные логи не пустые
    assert len(logs["devices"]) > 0                                 # Логи устройств не пустые


# ---------------------------
#       ЗАГЛУШКИ (VALIDATION)
# ---------------------------

def test_set_temperature_valid(controller):
    assert controller.set_temperature(20) is True


def test_set_temperature_invalid(controller):
    assert controller.set_temperature(5 - 1) is False
    assert controller.set_temperature(31) is False


def test_set_brightness_valid(controller):
    assert controller.set_brightness(50) is True


def test_set_brightness_invalid(controller):
    assert controller.set_brightness(-1) is False
    assert controller.set_brightness(101) is False


def test_validate_pin_valid(controller):
    assert controller.validate_pin("1234") is True
    assert controller.validate_pin("123456") is True


def test_validate_pin_invalid(controller):
    assert controller.validate_pin("12") is False
    assert controller.validate_pin("abcdef") is False


def test_set_schedule_time_valid(controller):
    assert controller.set_schedule_time("12:30") is True


def test_set_schedule_time_invalid(controller):
    assert controller.set_schedule_time("99:99") is False
    assert controller.set_schedule_time("ab:cd") is False


def test_set_energy_limit_valid(controller):
    assert controller.set_energy_limit(3000) is True


def test_set_energy_limit_invalid(controller):
    assert controller.set_energy_limit(-1) is False
    assert controller.set_energy_limit(5001) is False


# ---------------------------
#   ЗАПУСК/ОСТАНОВКА СИСТЕМЫ
# ---------------------------

def test_stop_system(controller):
    controller.running = True
    controller.stop_system()
    assert controller.running is False
    controller.logging_service.info.assert_called()