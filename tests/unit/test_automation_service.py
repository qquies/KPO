import pytest
from unittest.mock import MagicMock, patch
from services.automation_service import AutomationService

@pytest.fixture
def mock_controller():
    controller = MagicMock()
    controller.device_manager.send_command.return_value = True
    return controller

# Тест проверяет выполнение демо-сценария автоматизации
# Убеждается, что все команды отправляются правильным устройствам в правильной последовательности
def test_run_demo_scenario(mock_controller):
    automation = AutomationService(mock_controller)
    
    # Патчим time.sleep, чтобы тест шел быстро
    with patch("time.sleep", return_value=None):
        automation.run_demo_scenario()
    
    # Проверяем, что send_command вызывался для каждого устройства
    expected_calls = [
        ("lamp_living_room", "on"),
        ("thermostat", "on"),
        ("security_camera", "on"),
        ("lamp_living_room", "off"),
        ("thermostat", "off")
    ]
    
    for device_id, action in expected_calls:
        mock_controller.device_manager.send_command.assert_any_call(device_id, action)