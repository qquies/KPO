from datetime import datetime
from typing import List
import os

class LoggingService:
    """Сервис для логирования событий системы"""
    
    def __init__(self, log_to_file: bool = True):
        self.server_log: List[str] = []    # Логи сервера
        self.device_log: List[str] = []    # Логи устройств  
        self.client_log: List[str] = []    # Логи клиента
        self.system_log: List[str] = []    # Логи системы
        
        self.log_to_file = log_to_file
        self.log_file = "smart_home.log"
        
        # Создаем файл лога если нужно
        if log_to_file:
            self._setup_log_file()
    
    def _setup_log_file(self):
        """Настройка файла для логирования"""
        try:
            # Создаем папку logs если её нет
            os.makedirs("logs", exist_ok=True)
            self.log_file = "logs/smart_home.log"
            
            # Записываем заголовок
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"🚀 Сессия Умного Дома начата: {datetime.now()}\n")
                f.write(f"{'='*50}\n")
                
        except Exception as e:
            print(f"❌ Ошибка создания файла логов: {e}")
    
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
            self.system_log.append(log_entry)
            print(f"📝 {log_entry}")
        
        # Записываем в файл если включено
        if self.log_to_file:
            self._write_to_file(log_entry)
    
    def _write_to_file(self, log_entry: str):
        """Записать лог в файл"""
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"❌ Ошибка записи в файл логов: {e}")
    
    def get_logs(self, log_type: str, limit: int = 15):
        """Получить логи определенного типа"""
        if log_type == "SERVER":
            return self.server_log[-limit:]
        elif log_type == "DEVICE":
            return self.device_log[-limit:]
        elif log_type == "CLIENT":
            return self.client_log[-limit:]
        elif log_type == "SYSTEM":
            return self.system_log[-limit:]
        return []
    
    def get_all_logs(self) -> dict:
        """Получить все логи"""
        return {
            "server": self.server_log[-20:],    # Последние 20
            "device": self.device_log[-20:],
            "client": self.client_log[-20:],
            "system": self.system_log[-20:]
        }
    
    def clear_logs(self, log_type: str = "ALL"):
        """Очистить логи"""
        if log_type == "SERVER" or log_type == "ALL":
            self.server_log.clear()
        if log_type == "DEVICE" or log_type == "ALL":
            self.device_log.clear()
        if log_type == "CLIENT" or log_type == "ALL":
            self.client_log.clear()
        if log_type == "SYSTEM" or log_type == "ALL":
            self.system_log.clear()
        
        self.info("SYSTEM", f"Логи типа '{log_type}' очищены")
    
    def get_log_statistics(self) -> dict:
        """Получить статистику по логам"""
        return {
            "server_logs": len(self.server_log),
            "device_logs": len(self.device_log),
            "client_logs": len(self.client_log),
            "system_logs": len(self.system_log),
            "total_logs": len(self.server_log) + len(self.device_log) + 
                         len(self.client_log) + len(self.system_log)
        }