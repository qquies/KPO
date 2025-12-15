import time
from datetime import datetime

class ScheduleService:
    def __init__(self, controller):
        self.controller = controller
        self.schedule = {}   # "HH:MM" -> [(device_id, action)]

    def add_task(self, time_str: str, device_id: str, action: str) -> bool:
        """Добавить задачу в расписание"""
        if not self._validate_time(time_str):
            return False

        self.schedule.setdefault(time_str, []).append((device_id, action))
        return True

    def remove_tasks(self, time_str: str):
        """Удалить задачи на указанное время"""
        self.schedule.pop(time_str, None)

    def run(self):
        """Фоновая проверка расписания"""
        while self.controller.running:
            current_time = datetime.now().strftime("%H:%M")

            if current_time in self.schedule:
                for device_id, action in self.schedule[current_time]:
                    self.controller.send_command(device_id, action)

            time.sleep(60)

    def _validate_time(self, time_str: str) -> bool:
        try:
            h, m = map(int, time_str.split(":"))
            return 0 <= h <= 23 and 0 <= m <= 59
        except:
            return False