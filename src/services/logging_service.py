from datetime import datetime

class LoggingService:
    """Сервис для логирования событий системы"""
    
    def __init__(self):
        self.server_log = []
        self.device_log = []
        self.client_log = []
        
    def info(self, component: str, message: str):
        """Записать информационное сообщение"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {component}: {message}"
        
        # Сохраняем в соответствующий журнал
        if component == "SERVER":
            self.server_log.append(log_entry)
            print(f"🔧 {log_entry}")
        elif component == "DEVICE":
            self.device_log.append(log_entry)
            print(f"💡 {log_entry}")
        elif component == "CLIENT":
            self.client_log.append(log_entry)
            print(f"📱 {log_entry}")
        else:
            print(f"📝 {log_entry}")
    
    def get_logs(self, log_type: str, limit: int = 15):
        """Получить логи определенного типа"""
        if log_type == "SERVER":
            return self.server_log[-limit:]
        elif log_type == "DEVICE":
            return self.device_log[-limit:]
        elif log_type == "CLIENT":
            return self.client_log[-limit:]
        return []