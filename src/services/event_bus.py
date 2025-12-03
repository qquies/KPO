from typing import Callable, Dict, List
import threading

class EventBus:
    """Шина событий для связи между компонентами"""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable):
        """Подписаться на события определенного типа"""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
    
    def publish(self, event_type: str, data: Dict):
        """Опубликовать событие"""
        with self._lock:
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"❌ Ошибка в обработчике {event_type}: {e}")
    
    # Стандартные события системы
    DEVICE_STATE_CHANGED = "device_state_changed"
    NOTIFICATION_CREATED = "notification_created"
    SYSTEM_ERROR = "system_error"