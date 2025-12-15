from datetime import datetime
from typing import List, Dict

class NotificationService:
    def __init__(self):
        self.notifications: List[Dict] = []
        self.max_notifications = 50
    

    # Получение ВСЕХ уведомлений
    def get_all_notifications(self):
        return self.notifications


    # Удаление уведомлений
    def delete_notification(self, notification_id: int):
        self.notifications = [
            n for n in self.notifications if n["id"] != notification_id
        ]

    # Очистка уведомлений
    def clear_notifications(self):
        self.notifications.clear()

    # Количество непрочитанных
    def unread_count(self) -> int:
        return len(self.get_unread_notifications())

    def add_notification(self, title: str, message: str, level: str = "info"):
        """Добавить уведомление"""
        notification = {
            "id": len(self.notifications) + 1,
            "title": title,
            "message": message, 
            "level": level,  # info, warning, error
            "timestamp": datetime.now().isoformat(),
            "read": False
        }
        
        self.notifications.append(notification)
        
        # Ограничить количество уведомлений
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[-self.max_notifications:]
        
        print(f"🔔 {title}: {message}")
    
    def get_unread_notifications(self) -> List[Dict]:
        """Получить непрочитанные уведомления"""
        return [n for n in self.notifications if not n["read"]]
    
    def mark_as_read(self, notification_id: int):
        """Пометить уведомление как прочитанное"""
        for notification in self.notifications:
            if notification["id"] == notification_id:
                notification["read"] = True
                break