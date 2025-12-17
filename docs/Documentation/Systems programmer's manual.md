# Руководство системного программиста
# Система "Умный Дом"

## Содержание
1. [Обзор системы](#обзор-системы)
2. [Архитектура системы](#архитектура-системы)
3. [Модули системы](#модули-системы)
4. [Запуск и настройка](#запуск-и-настройка)
5. [Работа с устройством](#работа-с-устройствами)
6. [API и интерфейсы](#api-и-интерфейсы)
7. [Мониторинг и логирование](#мониторинг-и-логирование)
8. [Расписание и автоматизация](#расписание-и-автоматизация)
9. [Уведомления и оповещения](#уведомления-и-оповещения)
10. [Отладка и устранение неисправностей](#отладка-и-устранение-неисправностей)

---

## 1. Обзор системы <a name="обзор-системы"></a>

### 1.1 Назначение системы
Система "Умный Дом" предназначена для управления умными устройствами в доме через централизованный контроллер. Система поддерживает:
- Управление освещением
- Контроль климата
- Безопасность (камеры, датчики)
- Автоматизацию по расписанию
- Уведомления о событиях

### 1.2 Основные характеристики
- **Версия**: 1.0.0
- **Язык программирования**: Python 3.8+
- **Архитектура**: Многопоточная, событийно-ориентированная
- **Поддерживаемые ОС**: Windows, Linux, macOS

### 1.3 Технические требования
- Python 3.8 или выше
- 2 ГБ оперативной памяти (минимум)
- 100 МБ свободного места на диске
- Доступ к интернету (для отправки email-уведомлений)

---

## 2. Архитектура системы <a name="архитектура-системы"></a>

### 2.1 Компоненты системы

```
Умный Дом (архитектура)
├── Core Layer (Ядро)
│   ├── HomeController (Главный контроллер)
│   ├── Settings (Настройки)
│   └── ConsoleInterface (Консольный интерфейс)
│
├── Device Layer (Устройства)
│   ├── BaseDevice (Базовый класс устройства)
│   ├── SmartLight (Умная лампа)
│   ├── Thermostat (Термостат)
│   ├── SecurityCamera (Камера безопасности)
│   ├── SmokeSensor (Датчик дыма)
│   └── WaterLeakSensor (Датчик протечки)
│
├── Service Layer (Сервисы)
│   ├── DeviceManager (Менеджер устройств)
│   ├── EventBus (Шина событий)
│   ├── LoggingService (Сервис логирования)
│   ├── NotificationService (Сервис уведомлений)
│   ├── ScheduleService (Сервис расписания)
│   ├── AutomationService (Сервис автоматизации)
│   ├── EmailService (Сервис email)
│   └── StateStorage (Хранилище состояний)
│
└── UI Layer (Интерфейс)
    ├── SmartHomeGUI (Графический интерфейс)
    └── ConsoleInterface (Консольный интерфейс)
```

### 2.2 Потоки выполнения
Система использует многопоточность для параллельного выполнения задач:

1. **Основной поток** - графический интерфейс
2. **Поток мониторинга устройств** - проверка состояния устройств
3. **Поток сервера** - обработка запросов
4. **Поток расписания** - выполнение задач по расписанию
5. **Потоки симуляции** - для каждого устройства (температура, движение)

### 2.3 Поток данных
```
Устройство → DeviceManager → EventBus → HomeController
                                     ↓
                Сервисы (логирование, уведомления, email)
                                     ↓
                               Пользовательский интерфейс
```

---

## 3. Модули системы <a name="модули-системы"></a>

### 3.1 Core Layer (Ядро)

#### 3.1.1 HomeController (`core/home_controller.py`)
**Назначение**: Главный координатор системы

**Основные функции**:
- Инициализация всех сервисов
- Запуск/остановка системы
- Обработка событий от устройств
- Координация работы всех компонентов

**Ключевые методы**:
```python
start_system()      # Запуск системы
stop_system()       # Остановка системы
setup_event_handlers() # Настройка обработчиков событий
```

#### 3.1.2 Settings (`config/settings.py`)
**Назначение**: Хранение конфигурации системы

**Конфигурационные параметры**:
- `SYSTEM_NAME`: Название системы
- `VERSION`: Версия системы
- `DEVICE_UPDATE_INTERVAL`: Интервал обновления устройств (сек)
- `LOG_RETENTION_DAYS`: Время хранения логов (дней)
- `DEFAULT_DEVICES`: Конфигурация устройств по умолчанию

### 3.2 Device Layer (Устройства)

#### 3.2.1 BaseDevice (`devices/base_device.py`)
**Назначение**: Абстрактный базовый класс для всех устройств

**Абстрактные методы**:
```python
turn_on()    # Включить устройство
turn_off()   # Выключить устройство
toggle()     # Переключить состояние
```

**Общие атрибуты**:
- `device_id`: Уникальный идентификатор устройства
- `name`: Имя устройства
- `state`: Текущее состояние ("on"/"off")
- `data`: Дополнительные данные устройства
- `capabilities`: Список поддерживаемых команд

#### 3.2.2 Типы устройств

**SmartLight** (`devices/lighting/smart_light.py`):
- Управление яркостью (0-100%)
- Управление цветовой температурой (2700K-6500K)
- Управление цветом (HEX)
- Симуляция температуры

**Thermostat** (`devices/climate/thermostat.py`):
- Установка температуры (15-30°C)
- Плавная симуляция изменения температуры
- Поддержка целевой температуры

**SecurityCamera** (`devices/security/security_camera.py`):
- Обнаружение движения (симуляция)
- Запись видео
- Распознавание по времени суток
- Фоновый поток симуляции движения

**SmokeSensor** (`devices/security/smoke_sensor.py`):
- Обнаружение задымления
- Тревожная сигнализация
- Email-уведомления

**WaterLeakSensor** (`devices/security/water_leak_sensor.py`):
- Обнаружение протечек
- Тревожная сигнализация
- Email-уведомления

### 3.3 Service Layer (Сервисы)

#### 3.3.1 DeviceManager (`devices/device_manager.py`)
**Назначение**: Централизованное управление всеми устройствами

**Основные функции**:
- Регистрация и удаление устройств
- Отправка команд устройствам
- Сохранение и восстановление состояний
- Мониторинг изменений состояний

**Ключевые методы**:
```python
add_device(device)            # Добавить устройство
get_device(device_id)         # Получить устройство
send_command(device_id, action) # Отправить команду
save_state()                  # Сохранить состояния
restore_state()               # Восстановить состояния
```

#### 3.3.2 EventBus (`services/event_bus.py`)
**Назначение**: Шина событий для связи между компонентами

**Принцип работы**: Паттерн "Издатель-Подписчик"

**Стандартные события**:
- `DEVICE_STATE_CHANGED`: Изменение состояния устройства
- `NOTIFICATION_CREATED`: Создание уведомления
- `SYSTEM_ERROR`: Ошибка системы

**Методы**:
```python
subscribe(event_type, callback) # Подписаться на событие
publish(event_type, data)       # Опубликовать событие
```

#### 3.3.3 LoggingService (`services/logging_service.py`)
**Назначение**: Централизованное логирование

**Типы логов**:
- `SYSTEM`: Системные события
- `DEVICE`: События устройств
- `SERVER`: События сервера
- `CLIENT`: События клиента

**Функции**:
- Запись логов в файл (`logs/smart_home.log`)
- Автоматическая ротация логов (7 дней)
- Получение логов по типу
- Статистика логов

#### 3.3.4 ScheduleService (`services/schedule_service.py`)
**Назначение**: Выполнение задач по расписанию

**Формат задач**:
```json
{
  "08:00": [
    {
      "device_id": "lamp_living_room",
      "action": "on",
      "enabled": true,
      "days": [0, 1, 2, 3, 4]
    }
  ]
}
```

**Поддерживаемые команды**:
- Простые: `on`, `off`, `toggle`
- С параметрами: `set_temperature:22`, `set_brightness:80`
- Комбинированные: `on_and_set_temperature:22`

#### 3.3.5 EmailService (`services/email_service.py`)
**Назначение**: Отправка email-уведомлений

**Конфигурация**:
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "ваш_email@gmail.com"
SENDER_PASSWORD = "ваш_пароль"
```

**Использование**:
```python
email_service.send_alert("Заголовок", "Сообщение")
```

### 3.4 UI Layer (Интерфейс)

#### 3.4.1 SmartHomeGUI (`ui/smart_home_gui.py`)
**Технология**: Tkinter

**Основные компоненты**:
1. **Панель устройств**: Карточки устройств с управлением
2. **Вкладки информации**:
   - Статус системы
   - Логи
   - Уведомления
   - Расписание
   - Демо-сценарии
3. **Быстрые действия**: Панель быстрого доступа

#### 3.4.2 ConsoleInterface (`ui/console_interface.py`)
**Назначение**: Консольный интерфейс для отладки и администрирования

**Режимы работы**:
- Интерактивное меню
- Просмотр статуса
- Ручное управление устройствами
- Демонстрационные сценарии

---

## 4. Запуск и настройка <a name="запуск-и-настройка"></a>

### 4.1 Первоначальная настройка

#### 4.1.1 Установка зависимостей
```bash
# Клонирование репозитория
git clone <repository-url>
cd smart-home-system

# Установка Python зависимостей
pip install -r requirements.txt
```

#### 4.1.2 Настройка конфигурации

1. **Настройки системы** (`config/settings.py`):
```python
class Settings:
    def __init__(self):
        self.SYSTEM_NAME = "Smart Home System"
        self.VERSION = "1.0.0"
        self.DEVICE_UPDATE_INTERVAL = 2  # секунды
        self.LOG_RETENTION_DAYS = 30
```

2. **Настройка email** (`services/email_service.py`):
```python
class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "ваш_email@gmail.com"
        self.sender_password = "ваш_пароль_приложения"
        self.receiver_email = "получатель@gmail.com"
```

**Важно**: Для Gmail необходимо использовать пароль приложения, а не обычный пароль.

### 4.2 Запуск системы

#### 4.2.1 Графический интерфейс
```bash
# Основной запуск
python main.py

# Альтернативный запуск
python ui/smart_home_gui.py
```

#### 4.2.2 Консольный интерфейс
```bash
python -c "from ui.console_interface import ConsoleInterface; \
           from core.home_controller import HomeController; \
           controller = HomeController(); \
           controller.start_system(); \
           console = ConsoleInterface(controller); \
           console.display_main_menu()"
```

#### 4.2.3 Запуск как службы (Linux)
```bash
# Создание systemd службы
sudo nano /etc/systemd/system/smart-home.service

# Содержимое файла:
[Unit]
Description=Smart Home System
After=network.target

[Service]
Type=simple
User=ваш_пользователь
WorkingDirectory=/путь/к/проекту
ExecStart=/usr/bin/python3 /путь/к/проекту/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Активация службы
sudo systemctl enable smart-home.service
sudo systemctl start smart-home.service
```

### 4.3 Конфигурационные файлы

#### 4.3.1 `device_state.json`
**Назначение**: Хранение состояний устройств между запусками

**Расположение**: `/data/device_state.json`

**Формат**:
```json
{
  "lamp_living_room": {
    "type": "lamp",
    "state": "on",
    "data": {
      "brightness": 80,
      "color_temp": 4000
    }
  }
}
```

#### 4.3.2 `schedule.json`
**Назначение**: Хранение задач расписания

**Расположение**: Корневая директория проекта

**Формат**: См. раздел 3.3.4

#### 4.3.3 `smart_home.log`
**Назначение**: Логи системы

**Расположение**: `logs/smart_home.log`

**Формат логов**:
```
[2024-01-15 14:30:45] SYSTEM: 🚀 Контроллер инициализирован
[2024-01-15 14:30:46] DEVICE: Добавлено устройство: Свет в гостиной
```

---

## 5. Работа с устройствами <a name="работа-с-устройствами"></a>

### 5.1 Добавление нового устройства

#### 5.1.1 Создание класса устройства

```python
from devices.base_device import BaseDevice

class NewDevice(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "new_type")
        
        # Настройка данных устройства
        self.data["custom_field"] = "значение"
        
        # Добавление возможностей
        self.capabilities.extend(["custom_command"])
        
        # Добавление метаданных
        self.metadata.update({
            "min_value": 0,
            "max_value": 100
        })
    
    def turn_on(self):
        self.state = "on"
        self.emit_event("state_changed", {"state": "on"})
        return True
    
    def turn_off(self):
        self.state = "off"
        self.emit_event("state_changed", {"state": "off"})
        return True
    
    def toggle(self):
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()
    
    def custom_command(self, value):
        """Пользовательская команда"""
        if self.min_value <= value <= self.max_value:
            self.data["custom_field"] = value
            self.emit_event("custom_changed", {"value": value})
            return True
        return False
```

#### 5.1.2 Регистрация устройства в системе

```python
# В DeviceManager._initialize_devices()
def _initialize_devices(self):
    # Существующие устройства
    self.add_device(SmartLight("lamp_living_room", "Свет в гостиной"))
    self.add_device(Thermostat("thermostat", "Термостат"))
    
    # Новое устройство
    self.add_device(NewDevice("new_device", "Новое устройство"))
```

### 5.2 Команды устройств

#### 5.2.1 Базовые команды
```python
# Включение
device_manager.send_command("device_id", "on")

# Выключение
device_manager.send_command("device_id", "off")

# Переключение
device_manager.send_command("device_id", "toggle")
```

#### 5.2.2 Команды с параметрами
```python
# Установка температуры
device_manager.send_command("thermostat", "set_temperature:22")

# Установка яркости
device_manager.send_command("lamp_living_room", "set_brightness:80")

# Включение и установка параметра
device_manager.send_command("thermostat", "on_and_set_temperature:22")
```

#### 5.2.3 Проверка возможности выполнения
```python
device = device_manager.get_device("device_id")
if device and device.can_execute("command"):
    # Команда может быть выполнена
    success = device_manager.send_command("device_id", "command")
```

### 5.3 Симуляция устройств

#### 5.3.1 Принцип симуляции
Каждое устройство может иметь фоновые потоки симуляции:
- **Температура**: Плавное изменение по времени суток
- **Движение**: Случайное обнаружение с разной вероятностью
- **Яркость**: Автоматическая регулировка

#### 5.3.2 Настройка симуляции
```python
class SmartDevice(BaseDevice):
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "smart")
        
        # Фоновый поток симуляции
        self._simulation_thread = None
        self._stop_simulation = threading.Event()
    
    def turn_on(self):
        self.state = "on"
        self._start_simulation()  # Запуск симуляции
        return True
    
    def turn_off(self):
        self.state = "off"
        self._stop_simulation()   # Остановка симуляции
        return True
    
    def _simulation_loop(self):
        while not self._stop_simulation.wait(5):
            if self.state == "on":
                self._simulate_behavior()
    
    def _start_simulation(self):
        if not self._simulation_thread or not self._simulation_thread.is_alive():
            self._stop_simulation.clear()
            self._simulation_thread = threading.Thread(
                target=self._simulation_loop,
                daemon=True
            )
            self._simulation_thread.start()
    
    def _stop_simulation(self):
        if self._simulation_thread and self._simulation_thread.is_alive():
            self._stop_simulation.set()
            self._simulation_thread.join(timeout=2)
```

---

## 6. API и интерфейсы <a name="api-и-интерфейсы"></a>

### 6.1 Программный интерфейс

#### 6.1.1 HomeController API

**Получение контроллера**:
```python
from core.home_controller import HomeController

controller = HomeController()
controller.start_system()
```

**Основные методы**:
```python
# Управление системой
controller.start_system()
controller.stop_system()

# Управление устройствами
devices = controller.get_devices()
status = controller.get_device_status("device_id")
success = controller.send_command("device_id", "action")

# Валидация
is_valid_temp = controller.set_temperature(22)
is_valid_brightness = controller.set_brightness(80)
is_valid_pin = controller.validate_pin("1234")
is_valid_energy = controller.set_energy_limit(1000)
```

#### 6.1.2 DeviceManager API

**Получение менеджера**:
```python
device_manager = controller.device_manager
```

**Основные методы**:
```python
# Управление устройствами
device_manager.add_device(device)
device = device_manager.get_device("device_id")
all_devices = device_manager.get_all_devices_status()

# Команды
success = device_manager.send_command("device_id", "action")

# Состояния
device_manager.save_state()
device_manager.restore_state()
device_manager.start_auto_save(interval_minutes=5)
```

#### 6.1.3 EventBus API

**Подписка на события**:
```python
def event_handler(data):
    print(f"Событие: {data}")

event_bus = controller.event_bus
event_bus.subscribe(EventBus.DEVICE_STATE_CHANGED, event_handler)
```

**Публикация событий**:
```python
event_bus.publish("custom_event", {"key": "value"})
```

### 6.2 Файловые интерфейсы

#### 6.2.1 Состояния устройств
**Чтение**:
```python
from services.storage_service import StateStorage

storage = StateStorage()
states = storage.load()
```

**Запись**:
```python
states = {
    "device_id": {
        "type": "device_type",
        "state": "on",
        "data": {"field": "value"}
    }
}
storage.save(states)
```

#### 6.2.2 Расписание
**Чтение**:
```python
import json

with open("schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)
```

**Запись**:
```python
with open("schedule.json", "w", encoding="utf-8") as f:
    json.dump(schedule, f, ensure_ascii=False, indent=2)
```

### 6.3 Сетевые интерфейсы

#### 6.3.1 Email интерфейс
```python
from services.email_service import EmailService

email_service = EmailService()
success = email_service.send_alert("Заголовок", "Сообщение")
```

#### 6.3.2 Локальный сервер (заглушка)
Система включает эмуляцию серверной части в отдельном потоке:
```python
def _run_server(self):
    while self.running:
        threading.Event().wait(1)  # Эмуляция работы
```

---

## 7. Мониторинг и логирование <a name="мониторинг-и-логирование"></a>

### 7.1 Система логирования

#### 7.1.1 Уровни логирования
```python
# Информационные сообщения
logging_service.info("COMPONENT", "Сообщение")

# Примеры:
logging_service.info("SYSTEM", "🚀 Контроллер инициализирован")
logging_service.info("DEVICE", f"Устройство {name} изменено состояние")
logging_service.info("CLIENT", "Подключен новый клиент")
```

#### 7.1.2 Получение логов
```python
# По типу компонента
system_logs = logging_service.get_logs("SYSTEM", limit=50)
device_logs = logging_service.get_logs("DEVICE", limit=50)

# Все логи
all_logs = logging_service.get_all_logs()

# Статистика
stats = logging_service.get_log_statistics()
print(f"Всего логов: {stats['total_logs']}")
```

#### 7.1.3 Логи из файла
```python
# Чтение из файла (до 200 последних записей)
file_logs = logging_service.read_logs_from_file(limit=200)
```

### 7.2 Мониторинг состояния

#### 7.2.1 Статус системы
```python
devices_status = device_manager.get_all_devices_status()

# Подсчет статистики
total = len(devices_status)
online = sum(1 for s in devices_status.values() if s.get("online"))
active = sum(1 for s in devices_status.values() if s.get("state") == "on")
```

#### 7.2.2 История состояний
```python
# Получение истории для устройства
history = device_manager.get_device_state_history("device_id", limit=10)

for entry in history:
    print(f"{entry['timestamp']}: {entry['state']}")
```

#### 7.2.3 Уведомления
```python
# Получение уведомлений
notifications = notification_service.notifications
unread = notification_service.get_unread_notifications()

# Управление уведомлениями
notification_service.mark_as_read(notification_id)
notification_service.delete_notification(notification_id)
notification_service.clear_notifications()
```

### 7.3 Производительность

#### 7.3.1 Мониторинг потоков
```python
import threading

# Получение информации о потоках
threads = threading.enumerate()
print(f"Активных потоков: {len(threads)}")

for thread in threads:
    print(f"  {thread.name}: {thread.is_alive()}")
```

#### 7.3.2 Использование памяти
```python
import psutil
import os

process = psutil.Process(os.getpid())
memory_usage = process.memory_info().rss / 1024 / 1024  # МБ
print(f"Использование памяти: {memory_usage:.2f} МБ")
```

---

## 8. Расписание и автоматизация <a name="расписание-и-автоматизация"></a>

### 8.1 Создание задач расписания

#### 8.1.1 Через графический интерфейс
1. Перейдите на вкладку "📅 Расписание"
2. Нажмите "➕ Добавить задачу"
3. Заполните параметры:
   - Время выполнения
   - Устройство
   - Действие
   - Дни недели
   - Статус (включено/выключено)

#### 8.1.2 Программно
```python
from services.schedule_service import ScheduleService

schedule_service = controller.schedule_service

# Добавление задачи
success = schedule_service.add_task(
    time_str="08:00",                    # Время
    device_id="lamp_living_room",        # Устройство
    action="on",                         # Действие
    days=[0, 1, 2, 3, 4],               # Пн-Пт
    enabled=True                         # Активна
)

# Специальные действия
schedule_service.add_task(
    time_str="22:00",
    device_id="thermostat",
    action="on_and_set_temperature:18",  # Включить и установить температуру
    days=[0, 1, 2, 3, 4, 5, 6],         # Все дни
    enabled=True
)
```

### 8.2 Управление задачами

#### 8.2.1 Просмотр задач
```python
# Получение всех задач
tasks = schedule_service.get_all_tasks()

for task in tasks:
    print(f"{task['time']}: {task['device_id']} -> {task['action']}")
```

#### 8.2.2 Редактирование задач
```python
# Включение/выключение задачи
schedule_service.toggle_task("08:00", task_index=0, enabled=False)

# Обновление задачи
schedule_service.update_task(
    old_time="08:00",
    task_index=0,
    new_time="08:30",
    new_device_id="thermostat",
    new_action="on",
    new_days=[0, 1, 2, 3, 4],
    new_enabled=True
)
```

#### 8.2.3 Удаление задач
```python
# Удаление конкретной задачи
schedule_service.remove_task("08:00", task_index=0)

# Удаление всех задач на определенное время
schedule_service.remove_task("08:00")
```

### 8.3 Демонстрационные сценарии

#### 8.3.1 Встроенные сценарии
```python
# Вечерний режим
automation_service.run_evening_scenario()

# Утренний режим
automation_service.run_morning_scenario()

# Режим отсутствия
automation_service.run_away_scenario()

# Полная демонстрация
automation_service.run_full_demo()
```

#### 8.3.2 Создание пользовательских сценариев
```python
class CustomAutomation:
    def __init__(self, controller):
        self.controller = controller
    
    def custom_scenario(self):
        """Пользовательский сценарий"""
        steps = [
            ("lamp_living_room", "on", "Включение света"),
            ("thermostat", "on", "Включение отопления"),
            ("security_camera", "on", "Включение камеры"),
        ]
        
        for device_id, action, description in steps:
            print(f"Выполнение: {description}")
            self.controller.device_manager.send_command(device_id, action)
            time.sleep(1)
        
        print("Сценарий выполнен!")
```

---

## 9. Уведомления и оповещения <a name="уведомления-и-оповещения"></a>

### 9.1 Система уведомлений

#### 9.1.1 Создание уведомлений
```python
# Программно
notification_service.add_notification(
    title="Заголовок",
    message="Текст сообщения",
    level="info"  # info, warning, error
)

# Автоматически при событиях
# - Изменение состояния устройства
# - Срабатывание датчиков
# - Ошибки системы
```

#### 9.1.2 Уровни уведомлений
- **info**: Информационные сообщения
- **warning**: Предупреждения
- **error**: Критические ошибки

### 9.2 Email-оповещения

#### 9.2.1 Настройка SMTP
1. Для Gmail:
   - Включите двухфакторную аутентификацию
   - Создайте пароль приложения
   - Используйте его в настройках

2. Для других провайдеров:
   - Укажите соответствующий SMTP сервер и порт
   - Используйте правильные учетные данные

#### 9.2.2 Отправка оповещений
```python
# При срабатывании датчика
if device_type in ["smoke", "water"]:
    email_service.send_alert(
        f"🚨 Тревога: {device.name}",
        f"Датчик '{device.name}' сработал.\nТип: {device_type}\nВремя: {datetime.now()}"
    )
```

#### 9.2.3 Кастомизация email
```python
def send_custom_email(subject, body, receiver=None):
    """Отправка кастомного email"""
    if receiver is None:
        receiver = email_service.receiver_email
    
    msg = MIMEMultipart()
    msg["From"] = email_service.sender_email
    msg["To"] = receiver
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "plain", "utf-8"))
    
    # Отправка через SMTP
    # ...
```

### 9.3 Интеграция с внешними системами

#### 9.3.1 Webhook-уведомления
```python
import requests

def send_webhook(url, data):
    """Отправка уведомления через webhook"""
    try:
        response = requests.post(url, json=data, timeout=5)
        return response.status_code == 200
    except Exception as e:
        logging_service.error("SYSTEM", f"Webhook error: {e}")
        return False

# Использование
webhook_data = {
    "device_id": device_id,
    "event": event_type,
    "timestamp": datetime.now().isoformat(),
    "data": event_data
}
send_webhook("https://api.example.com/webhook", webhook_data)
```

#### 9.3.2 Telegram-бот
```python
import telebot

class TelegramNotifier:
    def __init__(self, token, chat_id):
        self.bot = telebot.TeleBot(token)
        self.chat_id = chat_id
    
    def send_notification(self, message):
        try:
            self.bot.send_message(self.chat_id, message)
            return True
        except Exception as e:
            print(f"Telegram error: {e}")
            return False

# Использование
telegram = TelegramNotifier("YOUR_BOT_TOKEN", "YOUR_CHAT_ID")
telegram.send_notification(f"🚨 Сработал датчик: {device_name}")
```

---

## 10. Отладка и устранение неисправностей <a name="отладка-и-устранение-неисправностей"></a>

### 10.1 Распространенные проблемы

#### 10.1.1 Система не запускается
**Проверьте**:
1. Установлен ли Python 3.8+
2. Установлены ли зависимости (`pip install -r requirements.txt`)
3. Достаточно ли прав для записи в директорию проекта
4. Не заняты ли необходимые порты

**Логи**: Проверьте `logs/smart_home.log` на наличие ошибок

#### 10.1.2 Устройства не отвечают
**Проверьте**:
1. Корректность инициализации устройств в `DeviceManager`
2. Наличие методов `turn_on()`, `turn_off()`, `toggle()` в классе устройства
3. Корректность `device_id` при отправке команд

**Отладка**:
```python
# Проверка существования устройства
device = device_manager.get_device("device_id")
if device:
    print(f"Устройство найдено: {device.name}")
    print(f"Состояние: {device.state}")
    print(f"Возможности: {device.capabilities}")
else:
    print("Устройство не найдено!")
```

#### 10.1.3 Email не отправляются
**Проверьте**:
1. Корректность SMTP настроек
2. Пароль приложения для Gmail
3. Доступность SMTP сервера
4. Настройки брандмауэра

**Тест отправки**:
```python
# Тестовая отправка
success = email_service.send_alert("Тест", "Тестовое сообщение")
print(f"Отправка {'успешна' if success else 'не удалась'}")
```

### 10.2 Инструменты отладки

#### 10.2.1 Логирование отладки
```python
# Включение подробного логирования
import logging
logging.basicConfig(level=logging.DEBUG)

# Логирование конкретных модулей
device_logger = logging.getLogger("devices")
device_logger.setLevel(logging.DEBUG)
```

#### 10.2.2 Мониторинг событий
```python
# Подписка на все события для отладки
def debug_event_handler(data):
    print(f"[DEBUG] Событие: {data}")

event_bus.subscribe(EventBus.DEVICE_STATE_CHANGED, debug_event_handler)
event_bus.subscribe(EventBus.NOTIFICATION_CREATED, debug_event_handler)
event_bus.subscribe(EventBus.SYSTEM_ERROR, debug_event_handler)
```

#### 10.2.3 Проверка потоков
```python
import threading
import time

def thread_monitor():
    """Мониторинг состояния потоков"""
    while True:
        print("\n" + "="*50)
        print(f"Время: {time.strftime('%H:%M:%S')}")
        print(f"Активных потоков: {threading.active_count()}")
        
        for thread in threading.enumerate():
            print(f"  {thread.name}: {'Активен' if thread.is_alive() else 'Не активен'}")
        
        time.sleep(10)

# Запуск монитора в отдельном потоке
monitor_thread = threading.Thread(target=thread_monitor, daemon=True)
monitor_thread.start()
```

### 10.3 Восстановление после сбоев

#### 10.3.1 Восстановление состояний
```python
# Принудительное восстановление
device_manager.restore_state()

# Проверка восстановленных состояний
states = device_manager.state_storage.load()
print(f"Восстановлено состояний: {len(states)}")
```

#### 10.3.2 Очистка кэша
```python
import os
import shutil

def clear_cache():
    """Очистка кэш-файлов системы"""
    cache_files = [
        "device_state.json",
        "schedule.json",
        "logs/smart_home.log"
    ]
    
    for file in cache_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"Удален: {file}")
            except Exception as e:
                print(f"Ошибка удаления {file}: {e}")
    
    print("Кэш очищен!")
```

#### 10.3.3 Сброс к заводским настройкам
```python
def factory_reset():
    """Полный сброс системы"""
    import json
    
    # Сброс состояний устройств
    with open("data/device_state.json", "w") as f:
        json.dump({}, f)
    
    # Сброс расписания
    with open("schedule.json", "w") as f:
        json.dump({}, f)
    
    # Очистка логов
    open("logs/smart_home.log", "w").close()
    
    print("Заводские настройки восстановлены!")
```

### 10.4 Профилирование производительности

#### 10.4.1 Измерение времени выполнения
```python
import time
import cProfile
import pstats

def profile_function(func, *args, **kwargs):
    """Профилирование функции"""
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    profiler.disable()
    
    print(f"Время выполнения: {end_time - start_time:.4f} сек")
    
    # Вывод статистики
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)
    
    return result

# Пример использования
profile_function(device_manager.send_command, "lamp_living_room", "on")
```

#### 10.4.2 Мониторинг памяти
```python
import tracemalloc

def monitor_memory():
    """Мониторинг использования памяти"""
    tracemalloc.start()
    
    # Ваш код здесь
    
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    
    print("[ Топ 10 по использованию памяти ]")
    for stat in top_stats[:10]:
        print(stat)
    
    tracemalloc.stop()
```

---

## Приложение A: Шпаргалка команд

### A.1 Запуск и управление
```bash
# Запуск GUI
python main.py

# Запуск консольного интерфейса
python -m ui.console_interface

# Запуск с отладкой
python -m pdb main.py
```

### A.2 Полезные команды Python
```python
# Проверка состояния системы
controller.running  # True если система работает

# Получение всех устройств
devices = controller.device_manager.devices

# Принудительное сохранение
controller.device_manager.save_state()

# Просмотр логов
logs = controller.logging_service.get_all_logs()
```

### A.3 Быстрые тесты
```python
# Тест отправки команды
success = controller.send_command("lamp_living_room", "toggle")
print(f"Команда {'успешна' if success else 'не удалась'}")

# Тест email
success = controller.email_service.send_alert("Тест", "Тестовое сообщение")

# Проверка расписания
tasks = controller.schedule_service.get_all_tasks()
```

---

## Приложение B: Структура файлов проекта

```
smart-home-system/
├── core/                    # Ядро системы
│   ├── __init__.py
│   └── home_controller.py   # Главный контроллер
│
├── config/                  # Конфигурация
│   ├── __init__.py
│   └── settings.py         # Настройки системы
│
├── devices/                 # Устройства
│   ├── __init__.py
│   ├── base_device.py      # Базовый класс устройства
│   ├── lighting/           # Устройства освещения
│   │   └── smart_light.py
│   ├── climate/            # Климатические устройства
│   │   └── thermostat.py
│   └── security/           # Устройства безопасности
│       ├── security_camera.py
│       ├── smoke_sensor.py
│       └── water_leak_sensor.py
│
├── services/               # Сервисы
│   ├── __init__.py
│   ├── device_manager.py   # Менеджер устройств
│   ├── event_bus.py        # Шина событий
│   ├── logging_service.py  # Сервис логирования
│   ├── notification_service.py # Уведомления
│   ├── schedule_service.py # Расписание
│   ├── automation_service.py # Автоматизация
│   ├── email_service.py    # Email уведомления
│   └── storage_service.py  # Хранилище состояний
│
├── ui/                     # Пользовательский интерфейс
│   ├── __init__.py
│   ├── smart_home_gui.py   # Графический интерфейс
│   └── console_interface.py # Консольный интерфейс
│
├── data/                   # Данные
│   └── device_state.json   # Состояния устройств
│
├── logs/                   # Логи
│   └── smart_home.log
│
├── tests/                  # Тесты
│   └── test_devices.py
│
├── main.py                 # Точка входа
├── schedule.json           # Расписание задач
├── requirements.txt        # Зависимости
└── README.md              # Документация
```

---

## Приложение C: Примеры использования

### C.1 Создание кастомного устройства
```python
from devices.base_device import BaseDevice
import random

class SmartBlinds(BaseDevice):
    """Умные жалюзи"""
    
    def __init__(self, device_id, name):
        super().__init__(device_id, name, "blinds")
        
        self.data["position"] = 0  # 0-100%
        self.data["tilt"] = 0      # -45 to 45 градусов
        
        self.capabilities.extend(["set_position", "set_tilt"])
        
        self.metadata.update({
            "min_position": 0,
            "max_position": 100,
            "min_tilt": -45,
            "max_tilt": 45
        })
    
    def turn_on(self):
        self.state = "on"
        self.emit_event("state_changed", {"state": "on"})
        return True
    
    def turn_off(self):
        self.state = "off"
        self.emit_event("state_changed", {"state": "off"})
        return True
    
    def toggle(self):
        if self.state == "on":
            return self.turn_off()
        else:
            return self.turn_on()
    
    def set_position(self, position):
        if self.metadata["min_position"] <= position <= self.metadata["max_position"]:
            self.data["position"] = position
            self.emit_event("position_changed", {"position": position})
            return True
        return False
    
    def set_tilt(self, tilt):
        if self.metadata["min_tilt"] <= tilt <= self.metadata["max_tilt"]:
            self.data["tilt"] = tilt
            self.emit_event("tilt_changed", {"tilt": tilt})
            return True
        return False
    
    def _simulate_sunlight(self):
        """Симуляция изменения положения по времени суток"""
        if self.state == "on":
            hour = datetime.now().hour
            
            if 6 <= hour <= 18:  # День
                target_position = random.randint(30, 70)
                target_tilt = random.randint(-30, 30)
            else:  # Ночь
                target_position = random.randint(0, 30)
                target_tilt = 0
            
            # Плавное изменение
            current_pos = self.data["position"]
            diff = target_position - current_pos
            change = diff * 0.1
            new_pos = max(0, min(100, current_pos + change))
            
            if abs(change) > 1:
                self.set_position(int(new_pos))
                self.set_tilt(target_tilt)
```

### C.2 Интеграция с внешним API
```python
import requests
from threading import Thread

class WeatherIntegration:
    """Интеграция с погодным API"""
    
    def __init__(self, api_key, controller):
        self.api_key = api_key
        self.controller = controller
        self.weather_data = {}
        self.update_interval = 1800  # 30 минут
    
    def start_monitoring(self):
        """Запуск мониторинга погоды"""
        def update_weather():
            while True:
                self.fetch_weather()
                time.sleep(self.update_interval)
        
        thread = Thread(target=update_weather, daemon=True)
        thread.start()
    
    def fetch_weather(self):
        """Получение данных о погоде"""
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": "Moscow",
                    "appid": self.api_key,
                    "units": "metric"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.weather_data = {
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "conditions": data["weather"][0]["main"]
                }
                
                # Адаптация устройств под погоду
                self.adapt_to_weather()
                
                return True
        except Exception as e:
            print(f"Ошибка получения погоды: {e}")
        
        return False
    
    def adapt_to_weather(self):
        """Адаптация устройств под погодные условия"""
        temp = self.weather_data.get("temperature")
        
        if temp is not None:
            if temp < 18:  # Холодно
                self.controller.send_command("thermostat", "on_and_set_temperature:22")
            elif temp > 25:  # Жарко
                self.controller.send_command("thermostat", "off")
```

---

## Заключение

Данное руководство системного программиста предоставляет полную информацию о проекте "Умный Дом". Система разработана с использованием современных принципов программирования и может быть легко расширена новыми устройствами и функциональностью.

Для получения дополнительной помощи или сообщения об ошибках, пожалуйста, обратитесь к разработчикам системы.

**Версия документации**: 1.0.5
**Последнее обновление**: Декабрь 2025  
**Автор**: Система "Умный Дом"
