import pytest
from services.logging_service import LoggingService

@pytest.fixture
def logger():
    return LoggingService()

# Тест проверяет запись информационных логов для серверных событий
# Убеждается, что сообщения категории "SERVER" корректно сохраняются и извлекаются
def test_info_server_log(logger):
    logger.info("SERVER", "Server started")
    logs = logger.get_logs("SERVER")
    assert any("Server started" in log for log in logs)

# Тест проверяет запись информационных логов для событий устройств
# Убеждается, что сообщения категории "DEVICE" корректно сохраняются и извлекаются
def test_info_device_log(logger):
    logger.info("DEVICE", "Device updated")
    logs = logger.get_logs("DEVICE")
    assert any("Device updated" in log for log in logs)

# Тест проверяет запись информационных логов для клиентских событий
# Убеждается, что сообщения категории "CLIENT" корректно сохраняются и извлекаются
def test_info_client_log(logger):
    logger.info("CLIENT", "Client message")
    logs = logger.get_logs("CLIENT")
    assert any("Client message" in log for log in logs)

# Тест проверяет обработку сообщений от неизвестных компонентов системы
# Убеждается, что логи неизвестных категорий не попадают в серверные логи
def test_info_unknown_component(logger):
    logger.info("UNKNOWN", "Test unknown")
    logs = logger.get_logs("SERVER")
    assert "Test unknown" not in logs

# Тест проверяет работу ограничения количества возвращаемых логов (пагинацию)
# Убеждается, что параметр limit корректно ограничивает количество возвращаемых записей
def test_get_logs_limit(logger):
    for i in range(20):
        logger.info("SERVER", f"Message {i}")
    logs = logger.get_logs("SERVER", limit=10)
    assert len(logs) == 10
    assert logs[0].endswith("Message 10")
    assert logs[-1].endswith("Message 19")