#!/usr/bin/env python3
"""
Умный Дом - Графический интерфейс управления (Tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
import sys
import os

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.home_controller import HomeController
from services.logging_service import LoggingService
from services.event_bus import EventBus


class SmartHomeGUI:
    """Графический интерфейс системы Умный Дом"""
    
    def __init__(self, root, controller):
        self.root = root
        self.root.title("🏠 Умный Дом - Система управления")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')

        self.root = root
        self.controller = controller
        
        # Инициализация контроллера
        self.controller = HomeController()
        self.controller.start_system()
        
        # Переменные для обновления интерфейса
        self.update_interval = 3000  # 5 секунды
        
        # Стили
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Запуск обновления интерфейса
        self.update_ui()
        
        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.controller.event_bus.subscribe(
            EventBus.DEVICE_STATE_CHANGED,
            self.on_device_state_changed
        )

        self.test_schedule_service()
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')

        self.bg_beige = style.lookup("TFrame", "background")
        
        # Цветовая схема
        self.colors = {
            'bg_dark': '#2c3e50',
            'bg_medium': '#34495e',
            'bg_light': '#ecf0f1',
            'text_light': '#ecf0f1',
            'text_dark': '#2c3e50',
            'primary': '#3498db',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#1abc9c'
        }
    
    def create_widgets(self):
        """Создание всех виджетов интерфейса (GRID layout)"""

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # GRID-конфигурация
        main_frame.columnconfigure(0, weight=0)  # быстрые действия
        main_frame.columnconfigure(1, weight=2)  # устройства (центр)
        main_frame.columnconfigure(2, weight=2)  # информация
        main_frame.rowconfigure(0, weight=1)

        # ========= ЛЕВАЯ КОЛОНКА — БЫСТРЫЕ ДЕЙСТВИЯ =========
        quick_frame = ttk.LabelFrame(main_frame, text="⚡ Быстрые действия", padding=10)
        quick_frame.grid(row=0, column=0, sticky="ns", padx=(0, 8))

        self.create_bottom_panel(quick_frame)

        # ========= ЦЕНТР — УПРАВЛЕНИЕ УСТРОЙСТВАМИ =========
        devices_frame = ttk.LabelFrame(main_frame, text="📱 Управление устройствами", padding=10)
        devices_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 8))

        self.create_device_controls(devices_frame)

        # ========= ПРАВО — ИНФОРМАЦИЯ =========
        info_frame = ttk.LabelFrame(main_frame, text="📊 Информация системы", padding=10)
        info_frame.grid(row=0, column=2, sticky="nsew")

        self.create_info_panels(info_frame)

    def on_device_state_changed(self, data):
        """Метод для обработки одного изменения"""
        device_id = data['device_id']
        device_info = self.controller.device_manager.get_device_status(device_id)
        
        if device_id in self.device_frames:
            self.device_frames[device_id].update_state(device_info)
    
    def create_device_controls(self, parent):
        """Создание панели управления устройствами"""
        # Контейнер для устройств с прокруткой
        devices_container = ttk.Frame(parent)
        devices_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas для прокрутки
        canvas = tk.Canvas(
            devices_container,
            highlightthickness=0,
            bg=self.bg_beige,
            bd=0
            #background=self.root.cget("bg")
        )
        scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
        self.devices_scroll_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.devices_scroll_frame, anchor="nw")

        window_id = canvas.create_window(
            (0, 0),
            window=self.devices_scroll_frame,
            anchor="nw"
        )

        def resize_scroll_frame(event):
            canvas.itemconfig(window_id, width=event.width)

        canvas.bind("<Configure>", resize_scroll_frame)
        
        # Список устройств будет заполняться динамически
        self.device_frames = {}
        
        # Обновление размера scrollarea
        self.devices_scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Кнопка обновления
        ttk.Button(parent, text="🔄 Обновить статус", command=self.refresh_devices).pack(pady=5)
    
    def create_info_panels(self, parent):
        """Создание информационных панелей"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка 1: Статус системы
        status_tab = ttk.Frame(notebook)
        notebook.add(status_tab, text="📈 Статус")
        self.create_status_tab(status_tab)
        
        # Вкладка 2: Логи
        logs_tab = ttk.Frame(notebook)
        notebook.add(logs_tab, text="📝 Логи")
        self.create_logs_tab(logs_tab)
        
        # Вкладка 3: Уведомления
        notifications_tab = ttk.Frame(notebook)
        notebook.add(notifications_tab, text="🔔 Уведомления")
        self.create_notifications_tab(notifications_tab)
        
        # Вкладка 4: Расписание
        schedule_tab = ttk.Frame(notebook)
        notebook.add(schedule_tab, text="📅 Расписание")
        self.create_schedule_tab(schedule_tab)
        
        # Вкладка 5: Демо сценарии
        demo_tab = ttk.Frame(notebook)
        notebook.add(demo_tab, text="🎬 Сценарии")
        self.create_demo_tab(demo_tab)

    def create_schedule_tab(self, parent):
        """Создание вкладки с расписанием"""
        # Панель управления
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Кнопка добавления задачи была здесь, но давайте проверим что она создается
        ttk.Button(control_frame, text="➕ Добавить задачу", 
                command=self.add_schedule_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Обновить", 
                command=self.refresh_schedule).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="✏️ Редактировать", 
                command=self.edit_selected_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Удалить", 
                command=self.remove_selected_task).pack(side=tk.LEFT, padx=5)
        
        # Таблица с задачами
        schedule_frame = ttk.Frame(parent)
        schedule_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview для отображения задач
        columns = ("time", "device", "action", "days", "status", "added", "index")
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=columns, 
                                        show="headings", height=15)
        
        # Настройка колонок
        column_config = [
            ("time", "Время", 80),
            ("device", "Устройство", 150),
            ("action", "Действие", 100),
            ("days", "Дни", 100),
            ("status", "Статус", 80),
            ("added", "Добавлено", 120)
        ]
        
        for col_id, heading, width in column_config:
            self.schedule_tree.heading(col_id, text=heading)
            self.schedule_tree.column(col_id, width=width)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(schedule_frame, orient="vertical", 
                                command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        self.schedule_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Привязка двойного клика для редактирования
        self.schedule_tree.bind("<Double-1>", self.edit_schedule_task)
        
        # Обновляем список задач
        self.refresh_schedule()

    def edit_selected_task(self):
        """Редактировать выбранную задачу"""
        selection = self.schedule_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите задачу для редактирования!")
            return
        
        # Получаем данные выбранной задачи
        item = self.schedule_tree.item(selection[0])
        item_values = item['values']
        
        # Получаем индекс задачи из скрытой колонки
        if len(item_values) >= 7:  # Проверяем наличие индекса
            task_index = item_values[6]  # Индекс в скрытой колонке
            
            # Получаем все задачи
            if hasattr(self.controller, 'schedule_service'):
                tasks = self.controller.schedule_service.get_all_tasks()
                
                # Находим задачу по индексу
                task_to_edit = None
                for task in tasks:
                    if task.get("index") == task_index:
                        task_to_edit = task
                        break
                
                if task_to_edit:
                    # Открываем диалог редактирования
                    self.open_edit_task_dialog(task_to_edit)
                else:
                    messagebox.showerror("Ошибка", "Не удалось найти задачу для редактирования")
        else:
            messagebox.showerror("Ошибка", "Не удалось получить информацию о задаче")

    def open_edit_task_dialog(self, task):
        """Открыть диалог редактирования задачи"""
        # Создаем диалог
        dialog = tk.Toplevel(self.root)
        dialog.title("✏️ Редактировать задачу")
        dialog.geometry("400x500")
        dialog.resizable(False, False)
        
        # Основной фрейм
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="✏️ Редактирование задачи", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Отображаем информацию о задаче
        info_frame = ttk.LabelFrame(main_frame, text="Текущие параметры", padding=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = f"Время: {task['time']}\n"
        info_text += f"Устройство: {task['device_id']}\n"
        info_text += f"Действие: {task['action']}\n"
        
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)
        
        # Поле для нового времени
        time_frame = ttk.Frame(main_frame)
        time_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(time_frame, text="Новое время (ЧЧ:ММ):").pack(side=tk.LEFT)
        time_var = tk.StringVar(value=task['time'])
        time_entry = ttk.Entry(time_frame, textvariable=time_var, width=10)
        time_entry.pack(side=tk.LEFT, padx=10)
        
        # Чекбокс для активации/деактивации
        enabled_var = tk.BooleanVar(value=task['enabled'])
        ttk.Checkbutton(main_frame, text="Задача активна", 
                        variable=enabled_var).pack(anchor=tk.W, pady=10)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        def save_changes():
            """Сохранить изменения"""
            new_time = time_var.get()
            
            # Проверяем формат времени
            try:
                hours, minutes = map(int, new_time.split(':'))
                if not (0 <= hours <= 23 and 0 <= minutes <= 59):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", 
                                "Неверный формат времени! Используйте ЧЧ:ММ (например, 08:30)")
                return
            
            try:
                # Обновляем задачу
                success = self.controller.schedule_service.update_task(
                    task_index=task["index"],
                    new_time=new_time,
                    enabled=enabled_var.get()
                )
                
                if success:
                    messagebox.showinfo("Успех", "Задача успешно обновлена!")
                    self.refresh_schedule()
                    dialog.destroy()
                else:
                    messagebox.showerror("Ошибка", "Не удалось обновить задачу!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при обновлении задачи: {str(e)}")
        
        ttk.Button(button_frame, text="💾 Сохранить", 
                command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="❌ Отмена", 
                command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def add_schedule_task(self):
        """Диалог добавления новой задачи в расписание"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Добавить задачу в расписание")
        dialog.geometry("500x650")  # Увеличим высоту окна
        dialog.resizable(False, False)
        
        # Создаем основной фрейм с прокруткой
        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем Canvas для прокрутки
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Фрейм для ввода времени
        time_frame = ttk.LabelFrame(scrollable_frame, text="⏰ Время выполнения", padding=10)
        time_frame.pack(fill=tk.X, pady=5)
        
        time_inner_frame = ttk.Frame(time_frame)
        time_inner_frame.pack()
        
        ttk.Label(time_inner_frame, text="Час (0-23):").grid(row=0, column=0, padx=5, pady=5)
        hour_var = tk.StringVar(value="08")
        hour_spin = ttk.Spinbox(time_inner_frame, from_=0, to=23, textvariable=hour_var, 
                            width=5, wrap=True)
        hour_spin.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(time_inner_frame, text="Минута (0-59):").grid(row=0, column=2, padx=5, pady=5)
        minute_var = tk.StringVar(value="00")
        minute_spin = ttk.Spinbox(time_inner_frame, from_=0, to=59, textvariable=minute_var, 
                                width=5, wrap=True)
        minute_spin.grid(row=0, column=3, padx=5, pady=5)
        
        # Фрейм для выбора устройства
        device_frame = ttk.LabelFrame(scrollable_frame, text="📱 Устройство", padding=10)
        device_frame.pack(fill=tk.X, pady=5)
        
        # Получаем список устройств
        devices = self.controller.device_manager.get_all_devices_status()
        device_list = [(device_id, info.get("name", device_id), info.get("type", "unknown")) 
                    for device_id, info in devices.items()]
        
        # Создаем список для отображения
        device_names = []
        device_ids = []
        device_types = {}
        
        # Добавляем устройства с указанием типа
        for device_id, name, dtype in device_list:
            display_name = f"{name} ({dtype})"
            device_names.append(display_name)
            device_ids.append(device_id)
            device_types[device_id] = dtype
        
        ttk.Label(device_frame, text="Выберите устройство:").pack(anchor=tk.W, pady=2)
        device_var = tk.StringVar(value=device_names[0] if device_names else "")
        device_combo = ttk.Combobox(device_frame, textvariable=device_var, 
                                values=device_names, state="readonly", height=10)
        device_combo.pack(fill=tk.X, pady=5)
        
        # Фрейм для выбора действия
        action_frame = ttk.LabelFrame(scrollable_frame, text="⚡ Действие", padding=10)
        action_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(action_frame, text="Выберите действие:").pack(anchor=tk.W, pady=2)
        action_var = tk.StringVar(value="on")
        action_combo = ttk.Combobox(action_frame, textvariable=action_var, 
                                values=["on", "off", "toggle"], state="readonly")
        action_combo.pack(fill=tk.X, pady=5)
        
        # Фрейм для параметров (будет скрыт/показан динамически)
        param_frame = ttk.LabelFrame(scrollable_frame, text="🔧 Параметры", padding=10)
        
        # Для термостата - выбор температуры
        temp_frame = ttk.Frame(param_frame)
        ttk.Label(temp_frame, text="Температура (°C):").pack(side=tk.LEFT, padx=5)
        temp_var = tk.StringVar(value="22")
        temp_spin = ttk.Spinbox(temp_frame, from_=15, to=30, textvariable=temp_var, 
                            width=5, wrap=True)
        temp_spin.pack(side=tk.LEFT, padx=5)
        
        # Для лампы - выбор яркости
        brightness_frame = ttk.Frame(param_frame)
        ttk.Label(brightness_frame, text="Яркость (%):").pack(side=tk.LEFT, padx=5)
        brightness_var = tk.StringVar(value="80")
        brightness_spin = ttk.Spinbox(brightness_frame, from_=0, to=100, textvariable=brightness_var, 
                                    width=5, wrap=True)
        brightness_spin.pack(side=tk.LEFT, padx=5)
        
        # Функция для обновления доступных действий в зависимости от устройства
        def update_actions(*args):
            selected_name = device_var.get()
            if selected_name and selected_name in device_names:
                index = device_names.index(selected_name)
                device_id = device_ids[index]
                device_type = device_types.get(device_id, "unknown")
                
                # Скрываем параметры
                param_frame.pack_forget()
                
                # Обновляем доступные действия
                if device_type == "thermostat":
                    action_combo['values'] = ["on", "off", "toggle", "set_temperature", "set_temperature_and_on"]
                    action_var.set("set_temperature_and_on")
                elif device_type == "lamp":
                    action_combo['values'] = ["on", "off", "toggle", "set_brightness", "set_brightness_and_on"]
                    action_var.set("set_brightness_and_on")
                else:
                    action_combo['values'] = ["on", "off", "toggle"]
                    action_var.set("on")
        
        # Функция для отображения параметров в зависимости от действия
        def update_params(*args):
            action = action_var.get()
            selected_name = device_var.get()
            
            if selected_name and selected_name in device_names:
                index = device_names.index(selected_name)
                device_id = device_ids[index]
                device_type = device_types.get(device_id, "unknown")
                
                # Показываем/скрываем параметры
                if "temperature" in action and device_type == "thermostat":
                    param_frame.pack(fill=tk.X, pady=5)
                    temp_frame.pack(pady=5)
                    brightness_frame.pack_forget()
                elif "brightness" in action and device_type == "lamp":
                    param_frame.pack(fill=tk.X, pady=5)
                    brightness_frame.pack(pady=5)
                    temp_frame.pack_forget()
                else:
                    param_frame.pack_forget()
        
        # Связываем события (универсальный способ)
        def setup_trace():
            try:
                # Для Python 3.14+
                if hasattr(device_var, 'trace_add'):
                    device_var.trace_add("write", lambda *args: update_actions())
                    action_var.trace_add("write", lambda *args: update_params())
                else:
                    # Для Python < 3.14
                    device_var.trace("w", lambda *args: update_actions())
                    action_var.trace("w", lambda *args: update_params())
            except:
                # Альтернатива: привязка к событиям Combobox
                device_combo.bind('<<ComboboxSelected>>', lambda e: update_actions())
                action_combo.bind('<<ComboboxSelected>>', lambda e: update_params())
        
        setup_trace()
        
        # Фрейм для выбора дней недели
        days_frame = ttk.LabelFrame(scrollable_frame, text="📅 Дни недели", padding=10)
        days_frame.pack(fill=tk.X, pady=5)
        
        day_names = ["Понедельник", "Вторник", "Среда", "Четверг", 
                    "Пятница", "Суббота", "Воскресенье"]
        day_vars = []
        
        for i, day_name in enumerate(day_names):
            var = tk.BooleanVar(value=(i < 5))  # По умолчанию будни
            day_vars.append(var)
            cb = ttk.Checkbutton(days_frame, text=day_name, variable=var)
            cb.pack(anchor=tk.W, pady=2)
        
        # Быстрые выборы дней
        quick_days_frame = ttk.Frame(days_frame)
        quick_days_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(quick_days_frame, text="Все дни", 
                command=lambda: [v.set(True) for v in day_vars]).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_days_frame, text="Только будни", 
                command=lambda: [v.set(i < 5) for i, v in enumerate(day_vars)]).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_days_frame, text="Только выходные", 
                command=lambda: [v.set(i >= 5) for i, v in enumerate(day_vars)]).pack(side=tk.LEFT, padx=2)
        
        # Фрейм для статуса
        status_frame = ttk.LabelFrame(scrollable_frame, text="✅ Статус", padding=10)
        status_frame.pack(fill=tk.X, pady=5)
        
        enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(status_frame, text="Включить задачу", 
                    variable=enabled_var).pack(anchor=tk.W, pady=2)
        
        # Фрейм для кнопок (должен быть ВНУТРИ scrollable_frame)
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        def save_task():
            """Сохранение задачи"""
            # Формируем время
            try:
                hour = int(hour_var.get())
                minute = int(minute_var.get())
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "Неверное время!")
                return
            
            time_str = f"{hour:02d}:{minute:02d}"
            
            # Получаем ID устройства
            selected_name = device_var.get()
            if selected_name not in device_names:
                messagebox.showerror("Ошибка", "Выберите устройство!")
                return
            
            index = device_names.index(selected_name)
            device_id = device_ids[index]
            device_type = device_types.get(device_id, "unknown")
            
            # Получаем действие
            action = action_var.get()
            
            # Обрабатываем специальные действия с параметрами
            if action == "set_temperature":
                try:
                    temperature = float(temp_var.get())
                    if not (15 <= temperature <= 30):
                        raise ValueError
                    # Преобразуем в команду для контроллера
                    action_cmd = f"set_temperature:{temperature}"
                except ValueError:
                    messagebox.showerror("Ошибка", "Температура должна быть от 15 до 30°C!")
                    return
            elif action == "set_temperature_and_on":
                try:
                    temperature = float(temp_var.get())
                    if not (15 <= temperature <= 30):
                        raise ValueError
                    # Двойное действие: включить и установить температуру
                    action_cmd = f"on_and_set_temperature:{temperature}"
                except ValueError:
                    messagebox.showerror("Ошибка", "Температура должна быть от 15 до 30°C!")
                    return
            elif action == "set_brightness":
                try:
                    brightness = int(brightness_var.get())
                    if not (0 <= brightness <= 100):
                        raise ValueError
                    action_cmd = f"set_brightness:{brightness}"
                except ValueError:
                    messagebox.showerror("Ошибка", "Яркость должна быть от 0 до 100%!")
                    return
            elif action == "set_brightness_and_on":
                try:
                    brightness = int(brightness_var.get())
                    if not (0 <= brightness <= 100):
                        raise ValueError
                    action_cmd = f"on_and_set_brightness:{brightness}"
                except ValueError:
                    messagebox.showerror("Ошибка", "Яркость должна быть от 0 до 100%!")
                    return
            else:
                action_cmd = action
            
            # Получаем выбранные дни
            selected_days = [i for i, var in enumerate(day_vars) if var.get()]
            if not selected_days:
                messagebox.showerror("Ошибка", "Выберите хотя бы один день!")
                return
            
            # Получаем статус
            enabled = enabled_var.get()
            
            # Проверяем, существует ли schedule_service
            if not hasattr(self.controller, 'schedule_service'):
                messagebox.showerror("Ошибка", "Сервис расписания не доступен!")
                return
            
            # Добавляем задачу
            try:
                success = self.controller.schedule_service.add_task(
                    time_str, device_id, action_cmd, selected_days, enabled
                )
                
                if success:
                    messagebox.showinfo("Успех", "Задача добавлена в расписание!")
                    self.refresh_schedule()
                    dialog.destroy()
                else:
                    messagebox.showerror("Ошибка", "Не удалось добавить задачу!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при добавлении задачи: {str(e)}")
        
        # Создаем кнопки (теперь они внутри scrollable_frame)
        ttk.Button(button_frame, text="✅ Сохранить", 
                command=save_task).pack(side=tk.LEFT, padx=5, pady=10)
        ttk.Button(button_frame, text="❌ Отмена", 
                command=dialog.destroy).pack(side=tk.LEFT, padx=5, pady=10)
        
        # Инициализация при открытии
        update_actions()
        update_params()
        
        # Прокручиваем в начало
        canvas.yview_moveto(0)
        
        # Центрируем диалог
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_set()
        dialog.wait_window()

    def test_schedule_service(self):
        """Тестовый метод для проверки работы schedule_service"""
        if hasattr(self.controller, 'schedule_service'):
            print(f"Schedule service доступен")
            print(f"Количество задач: {len(self.controller.schedule_service.schedule)}")
            return True
        else:
            print("Schedule service НЕ доступен")
            return False

    def refresh_schedule(self):
        """Обновить отображение расписания"""
        # Очищаем текущий список
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        # Получаем все задачи
        if hasattr(self.controller, 'schedule_service'):
            tasks = self.controller.schedule_service.get_all_tasks()
            device_names = self.controller.schedule_service.get_device_names()
            
            for task in tasks:
                time_str = task["time"]
                device_name = device_names.get(task["device_id"], task["device_id"])
                action = task["action"]
                days = self.controller.schedule_service.get_day_names(task["days"])
                status = "✅ Вкл" if task["enabled"] else "❌ Выкл"
                added = task["added"][:16]  # Обрезаем секунды
                
                # Определяем иконку и текст действия
                action_text = action
                if ":" in action:
                    parts = action.split(":", 1)
                    command = parts[0]
                    value = parts[1]
                    
                    if command == "set_temperature":
                        action_text = f"🌡️ {value}°C"
                    elif command == "on_and_set_temperature":
                        action_text = f"🟢 + 🌡️ {value}°C"
                    elif command == "set_brightness":
                        action_text = f"💡 {value}%"
                    elif command == "on_and_set_brightness":
                        action_text = f"🟢 + 💡 {value}%"
                    else:
                        action_icon = {
                            "on": "🟢",
                            "off": "⚫",
                            "toggle": "🔄"
                        }.get(command, "⚡")
                        action_text = f"{action_icon} {command}"
                else:
                    action_icon = {
                        "on": "🟢",
                        "off": "⚫",
                        "toggle": "🔄"
                    }.get(action, "⚡")
                    action_text = f"{action_icon} {action}"
                
                # Вставляем в таблицу
                self.schedule_tree.insert("", tk.END, values=(
                    time_str,
                    f"{device_name}",
                    action_text,
                    days,
                    status,
                    added,
                    task.get("index") 
                ))

    def remove_selected_task(self):
        """Удалить выбранную задачу"""
        selection = self.schedule_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления!")
            return
        
        if not messagebox.askyesno("Подтверждение", 
                                "Удалить выбранную задачу?"):
            return
        
        # Получаем данные выбранной задачи
        item = self.schedule_tree.item(selection[0])
        time_str = item['values'][0]
        
        # Находим индекс задачи
        tasks = self.controller.schedule_service.get_all_tasks()
        task_to_delete = None
        
        for task in tasks:
            if task["time"] == time_str:
                # Сравниваем другие поля для точного определения
                device_names = self.controller.schedule_service.get_device_names()
                device_name = device_names.get(task["device_id"], task["device_id"])
                
                if device_name in item['values'][1]:
                    task_to_delete = task
                    break
        
        if task_to_delete:
            self.controller.schedule_service.remove_task(
                task_to_delete["time"], 
                task_to_delete["index"]
            )
            messagebox.showinfo("Успех", "Задача удалена!")
            self.refresh_schedule()
        else:
            messagebox.showerror("Ошибка", "Не удалось найти задачу для удаления")

    def edit_schedule_task(self, event=None):
        """Редактировать выбранную задачу (двойной клик)"""
        selection = self.schedule_tree.selection()
        if not selection:
            return
        
        # Получаем данные выбранной задачи
        item = self.schedule_tree.item(selection[0])
        time_str = item['values'][0]
        
        # Находим задачу
        tasks = self.controller.schedule_service.get_all_tasks()
        task_to_edit = None
        
        for task in tasks:
            if task["time"] == time_str:
                device_names = self.controller.schedule_service.get_device_names()
                device_name = device_names.get(task["device_id"], task["device_id"])
                
                if device_name in item['values'][1]:
                    task_to_edit = task
                    break
        
        if task_to_edit:
            # Создаем диалог редактирования
            dialog = tk.Toplevel(self.root)
            dialog.title("✏️ Редактировать задачу")
            dialog.geometry("300x200")
            
            ttk.Label(dialog, text=f"Задача: {time_str} - {device_name}", 
                    font=('Arial', 10, 'bold')).pack(pady=10)
            
            # Переключение статуса
            status_frame = ttk.Frame(dialog)
            status_frame.pack(pady=10)
            
            status_var = tk.BooleanVar(value=task_to_edit["enabled"])
            
            def toggle_status():
                self.controller.schedule_service.toggle_task(
                    task_to_edit["time"], 
                    task_to_edit["index"], 
                    status_var.get()
                )
                messagebox.showinfo("Успех", "Статус изменен!")
                self.refresh_schedule()
                dialog.destroy()
            
            ttk.Checkbutton(status_frame, text="Задача активна", 
                        variable=status_var).pack()
            
            ttk.Button(status_frame, text="💾 Сохранить", 
                    command=toggle_status).pack(pady=10)
            
            # Кнопка удаления
            def delete_task():
                if messagebox.askyesno("Подтверждение", "Удалить эту задачу?"):
                    self.controller.schedule_service.remove_task(
                        task_to_edit["time"], 
                        task_to_edit["index"]
                    )
                    messagebox.showinfo("Успех", "Задача удалена!")
                    self.refresh_schedule()
                    dialog.destroy()
            
            ttk.Button(dialog, text="🗑️ Удалить задачу", 
                    command=delete_task).pack(pady=5)
            
            ttk.Button(dialog, text="❌ Закрыть", 
                    command=dialog.destroy).pack(pady=5)
        else:
            messagebox.showerror("Ошибка", "Не удалось найти задачу для редактирования")
    
    def create_status_tab(self, parent):
        """Создание вкладки со статусом"""
        # Статистика системы
        stats_frame = ttk.LabelFrame(parent, text="📊 Статистика системы", padding=10)
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.stats_labels = {}
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack()
        
        stats = [
            ("Всего устройств:", "total_devices"),
            ("Онлайн:", "online_devices"),
            ("Активно:", "active_devices"),
            ("Процент активности:", "activity_percent")
        ]
        
        for i, (text, key) in enumerate(stats):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(stats_grid, text=text, font=('Arial', 10)).grid(row=row, column=col, sticky=tk.W, padx=5, pady=5)
            self.stats_labels[key] = ttk.Label(stats_grid, text="0", font=('Arial', 10, 'bold'))
            self.stats_labels[key].grid(row=row, column=col+1, sticky=tk.W, padx=5, pady=5)
        
        # График активности (упрощенный)
        activity_frame = ttk.LabelFrame(parent, text="📈 Активность", padding=10)
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.activity_text = scrolledtext.ScrolledText(activity_frame, height=10, width=50)
        self.activity_text.pack(fill=tk.BOTH, expand=True)
        self.activity_text.config(state=tk.DISABLED)
    
    def create_logs_tab(self, parent):
        """Создание вкладки с логами"""
        # Панель фильтрации
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Тип логов:").pack(side=tk.LEFT, padx=5)
        
        self.log_type_var = tk.StringVar(value="SYSTEM")
        log_types = ["SYSTEM", "DEVICE", "SERVER", "CLIENT"]
        self.log_type_combo = ttk.Combobox(filter_frame, textvariable=self.log_type_var, 
                                          values=log_types, state="readonly", width=15)
        self.log_type_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Показать", command=self.refresh_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Очистить", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        
        # Отображение логов
        logs_frame = ttk.Frame(parent)
        logs_frame.pack(fill=tk.BOTH, expand=True)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=20, width=70)
        self.logs_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.logs_text.config(state=tk.DISABLED)
    
    def create_notifications_tab(self, parent):
        """Создание вкладки с уведомлениями"""
        # Панель управления уведомлениями
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="📪 Все прочитано", command=self.mark_all_read).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🗑️ Очистить все", command=self.clear_notifications).pack(side=tk.LEFT, padx=5)
        
        # Список уведомлений
        notifications_frame = ttk.Frame(parent)
        notifications_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview для уведомлений
        columns = ("id", "time", "title", "status", "level")
        self.notifications_tree = ttk.Treeview(notifications_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.notifications_tree.heading("id", text="ID")
        self.notifications_tree.heading("time", text="Время")
        self.notifications_tree.heading("title", text="Заголовок")
        self.notifications_tree.heading("status", text="Статус")
        self.notifications_tree.heading("level", text="Уровень")
        
        self.notifications_tree.column("id", width=50)
        self.notifications_tree.column("time", width=80)
        self.notifications_tree.column("title", width=200)
        self.notifications_tree.column("status", width=80)
        self.notifications_tree.column("level", width=80)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(notifications_frame, orient="vertical", command=self.notifications_tree.yview)
        self.notifications_tree.configure(yscrollcommand=scrollbar.set)
        
        self.notifications_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Информация о выбранном уведомлении
        details_frame = ttk.LabelFrame(parent, text="Детали уведомления", padding=10)
        details_frame.pack(fill=tk.X, pady=5)
        
        self.notification_details = tk.Text(details_frame, height=4, width=70)
        self.notification_details.pack(fill=tk.X)
        self.notification_details.config(state=tk.DISABLED)
        
        # Привязка события выбора
        self.notifications_tree.bind("<<TreeviewSelect>>", self.on_notification_select)
    
    def create_demo_tab(self, parent):
        """Создание вкладки с демо сценариями"""
        demo_frame = ttk.Frame(parent)
        demo_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(demo_frame, text="🎬 Демонстрационные сценарии", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(demo_frame, text="Выберите сценарий для запуска:", 
                 font=('Arial', 10)).pack(pady=5)
        
        # Кнопки сценариев
        scenarios = [
            ("🏠 Вечерний режим", self.run_evening_scenario, "Включение вечернего освещения"),
            ("🌅 Утренний режим", self.run_morning_scenario, "Плавное пробуждение"),
            ("🚪 Режим отсутствия", self.run_away_scenario, "Имитация присутствия"),
            ("🎯 Полная демонстрация", self.run_full_demo, "Все устройства")
        ]
        
        for name, command, description in scenarios:
            btn = ttk.Button(demo_frame, text=name, command=command)
            btn.pack(fill=tk.X, pady=5)
            
            ttk.Label(demo_frame, text=description, 
                     font=('Arial', 8), foreground='gray').pack(pady=(0, 10))
    
    def create_bottom_panel(self, parent):
        """Создание нижней панели с быстрыми действиями в столбик слева"""
        # Создаем основной фрейм для всей нижней панели
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill=tk.X, pady=10, padx=10, anchor='w')  # anchor='w' прижимает к левому краю
        
        # Заголовок для панели быстрых действий
        ttk.Label(bottom_frame, text="⚡ Быстрые действия", 
                font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Создаем фрейм для кнопок и выравниваем по левому краю
        buttons_frame = ttk.Frame(bottom_frame)
        buttons_frame.pack(anchor='w')  # Прижимаем контейнер с кнопками к левому краю
        
        # Кнопки быстрых действий В СТОЛБИК
        actions = [
            ("🔄 Все обновить", self.refresh_all),
            ("📅 Добавить задачу", self.add_schedule_task),
            ("⚙️ Настройки", self.show_settings),
            ("❓ Помощь", self.show_help),
            ("🚪 Выйти", self.on_closing)
        ]
        
        # Создаем кнопки и упаковываем их сверху вниз, выровненные по левому краю
        for text, command in actions:
            btn = ttk.Button(buttons_frame, text=text, command=command)
            # Используем anchor='w' и fill=tk.X чтобы кнопки растягивались по ширине и были слева
            btn.pack(fill=tk.X, pady=3, anchor='w')
        
        # Добавляем разделитель сверху, также слева
        ttk.Separator(parent, orient='horizontal').pack(fill=tk.X, pady=10, before=bottom_frame, anchor='w')
        
    def create_device_card(self, device_id, device_info):
        """Создание карточки устройства с правильным управлением состоянием"""

        card_frame = ttk.LabelFrame(
            self.devices_scroll_frame,
            text=f"📱 {device_info['name']}",
            padding=10
        )
        card_frame.pack(fill=tk.X, expand=True, pady=5, padx=5)

        # ========================================================
        # 0. ОСНОВНОЙ ФРЕЙМ СОСТОЯНИЯ (❗ ОБЯЗАТЕЛЕН)
        # ========================================================
        state_frame = ttk.Frame(card_frame)
        state_frame.pack(fill=tk.X, pady=5)
        
        # ========================================================
        # 1. МЕТКИ СОСТОЯНИЯ (будут обновляться)
        # ========================================================
        
        # Левый блок: иконка и основное состояние
        left_state_frame = ttk.Frame(state_frame)
        left_state_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Метка для иконки состояния
        card_frame._state_icon_label = ttk.Label(left_state_frame, font=('Arial', 14))
        card_frame._state_icon_label.pack(side=tk.LEFT, padx=2)
        
        # Метка для текста состояния (ВКЛ/ВЫКЛ/Тревога)
        card_frame._state_text_label = ttk.Label(left_state_frame, font=('Arial', 10, 'bold'))
        card_frame._state_text_label.pack(side=tk.LEFT, padx=2)
        
        # Правый блок: дополнительные данные
        right_data_frame = ttk.Frame(state_frame)
        right_data_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Метка для дополнительных данных (температура, яркость и т.д.)
        card_frame._data_label = ttk.Label(right_data_frame, font=('Arial', 10))
        card_frame._data_label.pack(side=tk.LEFT, padx=10)
        
        # ========================================================
        # 2. ФРЕЙМ ДЛЯ КНОПОК УПРАВЛЕНИЯ
        # ========================================================
        
        btn_frame = ttk.Frame(card_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Сохраняем ID устройства для кнопок
        card_frame.device_id = device_id
        card_frame.device_type = device_info['type']
        
        # ========================================================
        # 3. ФУНКЦИЯ ОБНОВЛЕНИЯ СОСТОЯНИЯ
        # ========================================================
        
        def update_state(new_info):
            """Обновить все элементы состояния устройства"""
            # Определяем текущее состояние
            if new_info['type'] in ['smoke', 'water']:
                is_active = new_info['data'].get('enabled', False)
                triggered = new_info['data'].get('triggered', False)
            else:
                is_active = new_info['state'] == 'on'
                triggered = False
            
            # Обновляем иконку и текст состояния
            if triggered:
                # Режим тревоги
                card_frame._state_icon_label.config(text="🔥")
                card_frame._state_text_label.config(text="Тревога", foreground='red')
                card_frame._state_text_label.config(font=('Arial', 10, 'bold'))
            else:
                # Нормальный режим
                if is_active:
                    card_frame._state_icon_label.config(text="🟢")
                    card_frame._state_text_label.config(text="ВКЛ", foreground='green')
                else:
                    card_frame._state_icon_label.config(text="⚫")
                    card_frame._state_text_label.config(text="ВЫКЛ", foreground='gray')
                card_frame._state_text_label.config(font=('Arial', 10, 'bold'))
            
            # Обновляем дополнительные данные
            if device_id == "thermostat":
                temp = new_info.get('data', {}).get('temperature', 'N/A')
                card_frame._data_label.config(text=f"🌡️ {temp}°C")
            elif device_id == "lamp_living_room":
                brightness = new_info.get('data', {}).get('brightness', 'N/A')
                card_frame._data_label.config(text=f"💡 {brightness}%")
            elif device_id == "security_camera":
                motion = new_info.get('data', {}).get('motion_detected', False)
                motion_text = "🔴 Движение" if motion else "✅ Нет движения"
                card_frame._data_label.config(text=motion_text)
            else:
                card_frame._data_label.config(text="")
        
        # ========================================================
        # 4. СОЗДАНИЕ КНОПОК УПРАВЛЕНИЯ
        # ========================================================
        
        # Кнопки включения/выключения
        if device_info['type'] in ['smoke', 'water']:
            # Для датчиков - включаем/выключаем мониторинг
            is_active = device_info['data'].get('enabled', False)
            
            if is_active:
                ttk.Button(btn_frame, text="⚫ Выключить", 
                        command=lambda d=device_id: self.toggle_device(d, 'off')).pack(side=tk.LEFT, padx=2)
            else:
                ttk.Button(btn_frame, text="🟢 Включить", 
                        command=lambda d=device_id: self.toggle_device(d, 'on')).pack(side=tk.LEFT, padx=2)
            
            # Кнопка "Переключить"
            ttk.Button(btn_frame, text="🔄 Переключить", 
                    command=lambda d=device_id: self.toggle_device(d, 'toggle')).pack(side=tk.LEFT, padx=2)
            
            # Кнопка для эмуляции срабатывания
            if device_info['type'] == "smoke":
                ttk.Button(btn_frame, text="🔥 Сработать", 
                        command=lambda d=device_id: self.trigger_device_alarm(d)).pack(side=tk.LEFT, padx=2)
            elif device_info['type'] == "water":
                ttk.Button(btn_frame, text="💧 Сработать", 
                        command=lambda d=device_id: self.trigger_device_alarm(d)).pack(side=tk.LEFT, padx=2)
        else:
            # Для обычных устройств
            is_active = device_info['state'] == 'on'
            
            if is_active:
                ttk.Button(btn_frame, text="⚫ Выключить", 
                        command=lambda d=device_id: self.toggle_device(d, 'off')).pack(side=tk.LEFT, padx=2)
            else:
                ttk.Button(btn_frame, text="🟢 Включить", 
                        command=lambda d=device_id: self.toggle_device(d, 'on')).pack(side=tk.LEFT, padx=2)
            
            ttk.Button(btn_frame, text="🔄 Переключить", 
                    command=lambda d=device_id: self.toggle_device(d, 'toggle')).pack(side=tk.LEFT, padx=2)
            
            # Специальные кнопки для разных устройств
            if device_id == "thermostat" and is_active:
                ttk.Button(btn_frame, text="🌡️ Установить температуру", 
                        command=self.set_temperature_dialog).pack(side=tk.LEFT, padx=2)
            elif device_id == "lamp_living_room" and is_active:
                ttk.Button(btn_frame, text="💡 Установить яркость", 
                        command=self.set_brightness_dialog).pack(side=tk.LEFT, padx=2)
        
        # ========================================================
        # 5. ИНИЦИАЛИЗАЦИЯ И ВОЗВРАТ
        # ========================================================
        
        # Инициализируем состояние
        update_state(device_info)
        
        # Сохраняем функцию обновления
        card_frame.update_state = update_state
        
        return card_frame

    def trigger_device_alarm(self, device_id):
        """Эмуляция срабатывания датчика + email"""
        device = self.controller.device_manager.get_device(device_id)

        if not device or not hasattr(device, "trigger_alarm"):
            return

        success = device.trigger_alarm()

        if not success:
            messagebox.showinfo(
                "Информация",
                f"{device.name} уже сработал или выключен"
            )
            return

        # 1. GUI уведомление
        messagebox.showwarning(
            "⚠️ ТРЕВОГА",
            f"{device.name} обнаружил опасность!"
        )

        # 2. Лог
        self.controller.logging_service.info(
            "SYSTEM",
            f"Сработал датчик: {device.name}"
        )

        # 3. Уведомление в системе
        if hasattr(self.controller, "notification_service"):
            self.controller.notification_service.add_notification(
                title=f"Тревога: {device.name}",
                message=f"Обнаружена проблема: {device.name}",
                level="error"
            )

        self.refresh_notifications()

        # 4. 📧 ОТПРАВКА EMAIL
        if hasattr(self.controller, "email_service"):
            subject = f"🚨 Тревога в умном доме: {device.name}"

            text = (
                f"Датчик '{device.name}' сработал.\n\n"
                f"Тип датчика: {device_id}\n"
                f"Проверьте ситуацию немедленно!"
            )

            self.controller.email_service.send_alert(
                subject,
                text
            )
    
    def toggle_device(self, device_id, action):
        """Переключение состояния устройства"""
        success = self.controller.device_manager.send_command(device_id, action)
        if success:
            messagebox.showinfo("Успех", f"Устройство {device_id} успешно {'включено' if action == 'on' else 'выключено'}")
            self.refresh_devices()
        else:
            messagebox.showerror("Ошибка", f"Не удалось выполнить команду для {device_id}")
    
    def set_temperature_dialog(self):
        """Диалог установки температуры"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Установка температуры")
        dialog.geometry("300x150")
        
        ttk.Label(dialog, text="Установите температуру (15-30°C):", 
                 font=('Arial', 10)).pack(pady=10)
        
        temp_var = tk.StringVar(value="22")
        temp_spin = ttk.Spinbox(dialog, from_=15, to=30, textvariable=temp_var, width=10)
        temp_spin.pack(pady=10)
        
        def apply_temp():
            try:
                temp = float(temp_var.get())
                device = self.controller.device_manager.get_device("thermostat")
                if device and hasattr(device, 'set_temperature'):
                    success = device.set_temperature(temp)
                    if success:
                        messagebox.showinfo("Успех", f"Температура установлена на {temp}°C")
                        dialog.destroy()
                        self.refresh_devices()
                    else:
                        messagebox.showerror("Ошибка", "Недопустимое значение температуры")
                else:
                    messagebox.showerror("Ошибка", "Устройство не найдено")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное число")
        
        ttk.Button(dialog, text="Установить", command=apply_temp).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack(pady=5)
    
    def set_brightness_dialog(self):
        """Диалог установки яркости"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Установка яркости")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Установите яркость (0-100%):", 
                 font=('Arial', 10)).pack(pady=10)
        
        brightness_var = tk.IntVar(value=80)
        
        scale = ttk.Scale(dialog, from_=0, to=100, variable=brightness_var, 
                         orient=tk.HORIZONTAL, length=200)
        scale.pack(pady=10)
        
        value_label = ttk.Label(dialog, text=f"{brightness_var.get()}%")
        value_label.pack()
        
        def update_label(val):
            value_label.config(text=f"{int(float(val))}%")
        
        scale.configure(command=update_label)
        
        def apply_brightness():
            brightness = brightness_var.get()
            device = self.controller.device_manager.get_device("lamp_living_room")
            if device and hasattr(device, 'set_brightness'):
                success = device.set_brightness(brightness)
                if success:
                    messagebox.showinfo("Успех", f"Яркость установлена на {brightness}%")
                    dialog.destroy()
                    self.refresh_devices()
                else:
                    messagebox.showerror("Ошибка", "Недопустимое значение яркости")
            else:
                messagebox.showerror("Ошибка", "Устройство не найдено")
        
        ttk.Button(dialog, text="Установить", command=apply_brightness).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack(pady=5)

    def refresh_devices(self):
        """Обновление отображения устройств"""
        devices_status = self.controller.device_manager.get_all_devices_status()

        for device_id, device_info in devices_status.items():
            if device_id in self.device_frames:
                # обновляем состояние существующей карточки
                self.device_frames[device_id].update_state(device_info)
            else:
                # создаем новую карточку
                frame = self.create_device_card(device_id, device_info)
                self.device_frames[device_id] = frame
    
    def refresh_logs(self):
        """Обновление отображения логов"""
        log_type = self.log_type_var.get()

        all_logs = self.controller.logging_service.read_logs_from_file(limit=300)

        log_type = self.log_type_var.get()
        if log_type:
            logs = [l for l in all_logs if f"{log_type}:" in l]
        else:
            logs = all_logs
        
        self.logs_text.config(state=tk.NORMAL)
        self.logs_text.delete(1.0, tk.END)
        
        for log in logs:
            self.logs_text.insert(tk.END, log + "\n")
        
        self.logs_text.config(state=tk.DISABLED)
        self.logs_text.see(tk.END)
    
    def refresh_notifications(self):
        """Обновление списка уведомлений"""
        # Очищаем текущий список
        for item in self.notifications_tree.get_children():
            self.notifications_tree.delete(item)
        
        # Получаем уведомления
        if hasattr(self.controller, 'notification_service'):
            notifications = self.controller.notification_service.notifications
            
            for notification in notifications[-50:]:  # Последние 50
                level_icon = {
                    "info": "ℹ️",
                    "warning": "⚠️",
                    "error": "❌"
                }.get(notification['level'], "📝")
                
                read_icon = "📪" if notification['read'] else "📬"
                time_str = notification['timestamp'][11:16] if len(notification['timestamp']) > 11 else notification['timestamp']
                
                self.notifications_tree.insert("", tk.END, values=(
                    notification['id'],
                    time_str,
                    notification['title'][:30],
                    read_icon,
                    level_icon
                ))
    
    def refresh_status(self):
        """Обновление статуса системы"""
        devices_status = self.controller.device_manager.get_all_devices_status()
        total_devices = len(devices_status)
        online_devices = sum(1 for status in devices_status.values() if status.get("online", True))
        active_devices = sum(1 for status in devices_status.values() if status.get("state") == "on")
        
        # Обновляем статистику
        self.stats_labels['total_devices'].config(text=str(total_devices))
        self.stats_labels['online_devices'].config(text=str(online_devices))
        self.stats_labels['active_devices'].config(text=str(active_devices))
        
        if total_devices > 0:
            percent = (active_devices / total_devices) * 100
            self.stats_labels['activity_percent'].config(text=f"{percent:.1f}%")
        
        # Обновляем историю активности
        self.activity_text.config(state=tk.NORMAL)
        
        # Добавляем текущую запись
        timestamp = datetime.now().strftime("%H:%M:%S")
        active_text = f"{active_devices}/{total_devices}"
        new_entry = f"[{timestamp}] Активных устройств: {active_text}\n"
        
        # Получаем текущий текст и добавляем новую запись
        current_text = self.activity_text.get(1.0, tk.END)
        lines = current_text.split('\n')
        
        # Ограничиваем количество строк
        if len(lines) > 20:
            lines = lines[-20:]
        
        lines.insert(0, new_entry.strip())
        self.activity_text.delete(1.0, tk.END)
        self.activity_text.insert(1.0, '\n'.join(lines))
        
        self.activity_text.config(state=tk.DISABLED)
        self.activity_text.see(tk.END)
    
    def mark_all_read(self):
        """Пометить все уведомления как прочитанные"""
        if hasattr(self.controller, 'notification_service'):
            unread = self.controller.notification_service.get_unread_notifications()
            for notification in unread:
                self.controller.notification_service.mark_as_read(notification['id'])
            messagebox.showinfo("Успех", "Все уведомления помечены как прочитанные")
            self.refresh_notifications()
    
    def clear_notifications(self):
        """Очистить все уведомления"""
        if hasattr(self.controller, 'notification_service'):
            self.controller.notification_service.clear_notifications()
            messagebox.showinfo("Успех", "Все уведомления очищены")
            self.refresh_notifications()
    
    def clear_logs(self):
        """Очистить логи"""
        log_type = self.log_type_var.get()
        self.controller.logging_service.clear_logs(log_type)
        messagebox.showinfo("Успех", f"Логи типа '{log_type}' очищены")
        self.refresh_logs()
    
    def on_notification_select(self, event):
        """Обработка выбора уведомления"""
        selection = self.notifications_tree.selection()
        if selection:
            item = self.notifications_tree.item(selection[0])
            notification_id = item['values'][0]
            
            # Находим полное уведомление
            if hasattr(self.controller, 'notification_service'):
                notifications = self.controller.notification_service.notifications
                for notification in notifications:
                    if notification['id'] == notification_id:
                        # Показываем детали
                        self.notification_details.config(state=tk.NORMAL)
                        self.notification_details.delete(1.0, tk.END)
                        
                        details = f"Заголовок: {notification['title']}\n"
                        details += f"Сообщение: {notification['message']}\n"
                        details += f"Время: {notification['timestamp']}\n"
                        details += f"Уровень: {notification['level']}\n"
                        details += f"Статус: {'Прочитано' if notification['read'] else 'Новое'}"
                        
                        self.notification_details.insert(1.0, details)
                        self.notification_details.config(state=tk.DISABLED)
                        
                        # Помечаем как прочитанное
                        if not notification['read']:
                            self.controller.notification_service.mark_as_read(notification_id)
                            self.refresh_notifications()
                        break
    
    def run_evening_scenario(self):
        """Запуск вечернего сценария"""
        def scenario():
            steps = [
                ("lamp_living_room", "on", "Включение света"),
                (None, None, "Установка яркости 70%"),
                (None, None, "Включение камеры"),
                ("thermostat", "on", "Включение термостата на 23°C")
            ]
            
            for device_id, action, description in steps:
                if device_id and action:
                    self.controller.device_manager.send_command(device_id, action)
                    time.sleep(1)
            
            messagebox.showinfo("Сценарий", "Вечерний режим активирован!")
        
        threading.Thread(target=scenario, daemon=True).start()
    
    def run_morning_scenario(self):
        """Запуск утреннего сценария"""
        def scenario():
            # Плавное включение света
            device = self.controller.device_manager.get_device("lamp_living_room")
            if device and hasattr(device, 'set_brightness'):
                for brightness in range(0, 81, 20):
                    device.set_brightness(brightness)
                    time.sleep(0.5)
            
            # Выключение камеры
            self.controller.device_manager.send_command("security_camera", "off")
            
            messagebox.showinfo("Сценарий", "Утренний режим активирован!")
        
        threading.Thread(target=scenario, daemon=True).start()
    
    def run_away_scenario(self):
        """Запуск сценария отсутствия"""
        def scenario():
            # Включение камеры
            self.controller.device_manager.send_command("security_camera", "on")
            
            # Выключение света
            self.controller.device_manager.send_command("lamp_living_room", "off")
            
            # Установка температуры на экономный режим
            device = self.controller.device_manager.get_device("thermostat")
            if device and hasattr(device, 'set_temperature'):
                device.set_temperature(18)
            
            messagebox.showinfo("Сценарий", "Режим отсутствия активирован!")
        
        threading.Thread(target=scenario, daemon=True).start()
    
    def run_full_demo(self):
        """Запуск полной демонстрации"""
        def scenario():
            steps = [
                ("lamp_living_room", "on", "Включение света в гостиной"),
                ("thermostat", "on", "Включение термостата"),
                ("security_camera", "on", "Включение камеры безопасности"),
                ("lamp_living_room", "off", "Выключение света в гостиной"),
                ("thermostat", "off", "Выключение термостата"),
                ("security_camera", "off", "Выключение камеры безопасности"),
            ]
            
            for device_id, action, description in steps:
                self.controller.device_manager.send_command(device_id, action)
                time.sleep(2)
            
            messagebox.showinfo("Демо", "Демонстрационный сценарий завершен!")
        
        threading.Thread(target=scenario, daemon=True).start()
    
    def refresh_all(self):
        """Обновить все данные"""
        self.refresh_devices()
        self.refresh_logs()
        self.refresh_notifications()
        self.refresh_status()
        self.refresh_schedule()  # Добавляем обновление расписания
        messagebox.showinfo("Обновление", "Все данные обновлены!")
    
    def show_settings(self):
        """Показать настройки"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Настройки системы")
        dialog.geometry("400x300")
        
        ttk.Label(dialog, text="⚙️ Настройки системы", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        settings_frame = ttk.Frame(dialog)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Интервал обновления
        ttk.Label(settings_frame, text="Интервал обновления (мс):").grid(row=0, column=0, sticky=tk.W, pady=5)
        interval_var = tk.StringVar(value=str(self.update_interval))
        interval_entry = ttk.Entry(settings_frame, textvariable=interval_var, width=10)
        interval_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        def save_settings():
            try:
                new_interval = int(interval_var.get())
                if 500 <= new_interval <= 10000:
                    self.update_interval = new_interval
                    messagebox.showinfo("Успех", "Настройки сохранены!")
                    dialog.destroy()
                else:
                    messagebox.showerror("Ошибка", "Интервал должен быть от 500 до 10000 мс")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректное число")
        
        ttk.Button(dialog, text="Сохранить", command=save_settings).pack(pady=10)
        ttk.Button(dialog, text="Отмена", command=dialog.destroy).pack(pady=5)
    
    def show_help(self):
        """Показать справку"""
        help_text = """
        🏠 Система Умный Дом - Руководство пользователя
        
        Основные функции:
        1. Управление устройствами:
           - Включение/выключение устройств
           - Установка температуры для термостата
           - Установка яркости для лампы
        
        2. Мониторинг:
           - Просмотр статуса всех устройств
           - Просмотр логов системы
           - Уведомления о событиях
        
        3. Сценарии:
           - Автоматические сценарии для разных ситуаций
           - Демонстрационные режимы
        
        4. Настройки:
           - Настройка интервала обновления
        
        Для получения дополнительной помощи обратитесь к документации.
        """
        
        messagebox.showinfo("Помощь", help_text)
    
    def update_ui(self):
        """Периодическое обновление интерфейса"""
        try:
            self.refresh_devices()
            self.refresh_status()
            self.refresh_notifications()
        except Exception as e:
            print(f"Ошибка обновления UI: {e}")
        
        # Планируем следующее обновление
        self.root.after(self.update_interval, self.update_ui)
    
    def on_closing(self):
        """Обработка закрытия приложения"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            # Сохраняем расписание перед выходом
            if hasattr(self.controller, 'schedule_service'):
                self.controller.schedule_service.stop()
            
            self.controller.stop_system()
            self.root.destroy()


def main():
    """Главная функция запуска GUI"""
    root = tk.Tk()
    app = SmartHomeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()