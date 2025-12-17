# services/schedule_service.py
import time
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import threading
import json
import os


class ScheduleService:
    def __init__(self, controller):
        self.controller = controller
        self.schedule = {}  # "HH:MM" -> [{"device_id": str, "action": str, "enabled": bool, "days": List[int]}]
        self.running = True
        self.schedule_file = "schedule.json"
        
        # Загружаем сохраненные задачи
        self.load_schedule()
        
        # Запускаем проверку расписания в отдельном потоке
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
    
    def add_task(self, time_str: str, device_id: str, action: str, 
                 days: List[int] = None, enabled: bool = True) -> bool:
        """Добавить задачу в расписание"""
        if not self._validate_time(time_str):
            return False
        
        if days is None:
            days = [0, 1, 2, 3, 4, 5, 6]  # Все дни недели
        
        task = {
            "device_id": device_id,
            "action": action,
            "enabled": enabled,
            "days": days,
            "added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if time_str not in self.schedule:
            self.schedule[time_str] = []
        
        self.schedule[time_str].append(task)
        self.save_schedule()
        return True
    
    def remove_task(self, time_str: str, task_index: int = None):
        """Удалить задачу или все задачи на указанное время"""
        if task_index is not None and time_str in self.schedule:
            if 0 <= task_index < len(self.schedule[time_str]):
                del self.schedule[time_str][task_index]
                if not self.schedule[time_str]:  # Если список пуст
                    del self.schedule[time_str]
        elif time_str in self.schedule:
            del self.schedule[time_str]
        
        self.save_schedule()
    
    def toggle_task(self, time_str: str, task_index: int, enabled: bool):
        """Включить/выключить задачу"""
        if time_str in self.schedule and 0 <= task_index < len(self.schedule[time_str]):
            self.schedule[time_str][task_index]["enabled"] = enabled
            self.save_schedule()
    
    def get_all_tasks(self) -> List[Dict]:
        """Получить все задачи в удобном формате для отображения"""
        tasks = []
        for time_str, task_list in self.schedule.items():
            for i, task in enumerate(task_list):
                tasks.append({
                    "time": time_str,
                    "index": i,
                    "device_id": task["device_id"],
                    "action": task["action"],
                    "enabled": task["enabled"],
                    "days": task["days"],
                    "added": task.get("added", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                })
        
        # Сортируем по времени
        tasks.sort(key=lambda x: x["time"])
        return tasks
    
    def get_device_names(self) -> Dict[str, str]:
        """Получить имена устройств"""
        devices = self.controller.device_manager.get_all_devices_status()
        device_names = {}
        for device_id, info in devices.items():
            device_names[device_id] = info.get("name", device_id)
        return device_names
    
    def run(self):
        """Фоновая проверка расписания"""
        last_checked_minute = -1
        
        while self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.weekday()  # 0 = Monday, 6 = Sunday
            
            # Проверяем только если минута изменилась
            if now.minute != last_checked_minute and current_time in self.schedule:
                for task in self.schedule[current_time]:
                    if task["enabled"] and current_day in task["days"]:
                        # Выполняем задачу
                        self.controller.device_manager.send_command(
                            task["device_id"], 
                            task["action"]
                        )
                
                last_checked_minute = now.minute
            
            time.sleep(5)  # Проверяем каждые 5 секунд
    
    def save_schedule(self):
        """Сохранить расписание в файл"""
        try:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(self.schedule, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения расписания: {e}")
    
    def load_schedule(self):
        """Загрузить расписание из файла"""
        try:
            if os.path.exists(self.schedule_file):
                with open(self.schedule_file, 'r', encoding='utf-8') as f:
                    self.schedule = json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки расписания: {e}")
            self.schedule = {}
    
    def _validate_time(self, time_str: str) -> bool:
        """Проверить формат времени"""
        try:
            h, m = map(int, time_str.split(":"))
            return 0 <= h <= 23 and 0 <= m <= 59
        except:
            return False
    
    def get_day_names(self, day_numbers: List[int]) -> str:
        """Получить названия дней недели"""
        day_names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        if len(day_numbers) == 7:
            return "Ежедневно"
        elif day_numbers == [0, 1, 2, 3, 4]:
            return "Будни"
        elif day_numbers == [5, 6]:
            return "Выходные"
        else:
            return ", ".join([day_names[d] for d in sorted(day_numbers)])

    def update_task(self, old_time: str, task_index: int, new_time: str = None, 
                new_device_id: str = None, new_action: str = None, 
                new_days: List[int] = None, new_enabled: bool = None) -> bool:
        """Обновить существующую задачу"""
        if old_time not in self.schedule or task_index >= len(self.schedule[old_time]):
            return False
        
        # Получаем старую задачу
        old_task = self.schedule[old_time][task_index]
        
        # Определяем новые значения (используем старые, если новые не указаны)
        device_id = new_device_id if new_device_id is not None else old_task["device_id"]
        action = new_action if new_action is not None else old_task["action"]
        enabled = new_enabled if new_enabled is not None else old_task["enabled"]
        days = new_days if new_days is not None else old_task["days"]
        
        # Проверяем новое время
        time_str = new_time if new_time is not None else old_time
        if new_time and not self._validate_time(time_str):
            return False
        
        # Создаем обновленную задачу
        updated_task = {
            "device_id": device_id,
            "action": action,
            "enabled": enabled,
            "days": days,
            "added": old_task["added"]  # Сохраняем оригинальное время добавления
        }
        
        # Если время изменилось, нужно удалить из старого времени и добавить в новое
        if new_time and new_time != old_time:
            # Удаляем из старого времени
            del self.schedule[old_time][task_index]
            if not self.schedule[old_time]:  # Если список пуст
                del self.schedule[old_time]
            
            # Добавляем в новое время
            if time_str not in self.schedule:
                self.schedule[time_str] = []
            self.schedule[time_str].append(updated_task)
        else:
            # Обновляем на том же месте
            self.schedule[old_time][task_index] = updated_task
        
        self.save_schedule()
        return True

    def run(self):
        """Фоновая проверка расписания"""
        last_checked_minute = -1
        
        while self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.weekday()  # 0 = Monday, 6 = Sunday
            
            # Проверяем только если минута изменилась
            if now.minute != last_checked_minute and current_time in self.schedule:
                for task in self.schedule[current_time]:
                    if task["enabled"] and current_day in task["days"]:
                        # Выполняем задачу
                        action = task["action"]
                        
                        # Проверяем сложные команды
                        if ":" in action:
                            # Команда с параметром
                            parts = action.split(":", 1)
                            command = parts[0]
                            value = parts[1]
                            
                            if command == "set_temperature":
                                # Установка температуры (термостат должен быть включен)
                                device = self.controller.device_manager.get_device(task["device_id"])
                                if device and hasattr(device, "set_temperature"):
                                    device.set_temperature(float(value))
                            elif command == "on_and_set_temperature":
                                # Включить и установить температуру
                                self.controller.device_manager.send_command(task["device_id"], "on")
                                device = self.controller.device_manager.get_device(task["device_id"])
                                if device and hasattr(device, "set_temperature"):
                                    device.set_temperature(float(value))
                            elif command == "set_brightness":
                                # Установка яркости (лампа должна быть включена)
                                device = self.controller.device_manager.get_device(task["device_id"])
                                if device and hasattr(device, "set_brightness"):
                                    device.set_brightness(int(value))
                            elif command == "on_and_set_brightness":
                                # Включить и установить яркость
                                self.controller.device_manager.send_command(task["device_id"], "on")
                                device = self.controller.device_manager.get_device(task["device_id"])
                                if device and hasattr(device, "set_brightness"):
                                    device.set_brightness(int(value))
                        else:
                            # Простая команда
                            self.controller.device_manager.send_command(task["device_id"], action)
                
                last_checked_minute = now.minute
            
            time.sleep(5)  # Проверяем каждые 5 секунд
    
    def stop(self):
        """Остановить сервис расписания"""
        self.running = False
        self.save_schedule()