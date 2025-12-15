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


class SmartHomeGUI:
    """Графический интерфейс системы Умный Дом"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏠 Умный Дом - Система управления")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2c3e50')
        
        # Инициализация контроллера
        self.controller = HomeController()
        self.controller.start_system()
        
        # Переменные для обновления интерфейса
        self.update_interval = 2000  # 2 секунды
        
        # Стили
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Запуск обновления интерфейса
        self.update_ui()
        
        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        style.theme_use('clam')
        
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
        """Создание всех виджетов интерфейса"""
        # Главный контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель - Управление устройствами
        left_frame = ttk.LabelFrame(main_frame, text="📱 Управление устройствами", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Правая панель - Информация и логи
        right_frame = ttk.LabelFrame(main_frame, text="📊 Информация системы", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Левая панель: Устройства
        self.create_device_controls(left_frame)
        
        # Правая панель: Информация
        self.create_info_panels(right_frame)
        
        # Нижняя панель - Быстрые действия
        self.create_bottom_panel(main_frame)
    
    def create_device_controls(self, parent):
        """Создание панели управления устройствами"""
        # Контейнер для устройств с прокруткой
        devices_container = ttk.Frame(parent)
        devices_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas для прокрутки
        canvas = tk.Canvas(devices_container, bg=self.colors['bg_light'])
        scrollbar = ttk.Scrollbar(devices_container, orient="vertical", command=canvas.yview)
        self.devices_scroll_frame = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.devices_scroll_frame, anchor="nw")
        
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
        
        # Вкладка 4: Демо сценарии
        demo_tab = ttk.Frame(notebook)
        notebook.add(demo_tab, text="🎬 Демо")
        self.create_demo_tab(demo_tab)
    
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
        """Создание нижней панели с быстрыми действиями"""
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        # Кнопки быстрых действий
        actions = [
            ("🔄 Все обновить", self.refresh_all),
            ("🚪 Выйти", self.on_closing),
            ("⚙️ Настройки", self.show_settings),
            ("❓ Помощь", self.show_help)
        ]
        
        for text, command in actions:
            ttk.Button(bottom_frame, text=text, command=command).pack(side=tk.LEFT, padx=5)
    
    def create_device_card(self, device_id, device_info):
        """Создание карточки устройства"""
        card_frame = ttk.LabelFrame(self.devices_scroll_frame, text=f"📱 {device_info['name']}", padding=10)
        card_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Статус устройства
        status_frame = ttk.Frame(card_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        # Иконка состояния
        state_icon = "🟢" if device_info['state'] == 'on' else "⚫"
        state_text = "ВКЛ" if device_info['state'] == 'on' else "ВЫКЛ"
        state_color = 'green' if device_info['state'] == 'on' else 'gray'
        
        ttk.Label(status_frame, text=state_icon, font=('Arial', 14)).pack(side=tk.LEFT)
        ttk.Label(status_frame, text=state_text, font=('Arial', 10, 'bold'), 
                 foreground=state_color).pack(side=tk.LEFT, padx=5)
        
        # Дополнительная информация
        if device_id == "thermostat":
            temp = device_info.get('data', {}).get('temperature', 'N/A')
            ttk.Label(status_frame, text=f"🌡️ {round(temp,2)}°C", font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        elif device_id == "lamp_living_room":
            brightness = device_info.get('data', {}).get('brightness', 'N/A')
            ttk.Label(status_frame, text=f"💡 {brightness}%", font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        elif device_id == "security_camera":
            motion = device_info.get('data', {}).get('motion_detected', False)
            motion_text = "🔴 Движение" if motion else "✅ Нет движения"
            ttk.Label(status_frame, text=motion_text, font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # Кнопки управления
        btn_frame = ttk.Frame(card_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Текущее состояние определяет, какие кнопки показывать
        if device_info['state'] == 'on':
            ttk.Button(btn_frame, text="⚫ Выключить", 
                      command=lambda d=device_id: self.toggle_device(d, 'off')).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="🔄 Переключить", 
                      command=lambda d=device_id: self.toggle_device(d, 'toggle')).pack(side=tk.LEFT, padx=2)
        else:
            ttk.Button(btn_frame, text="🟢 Включить", 
                      command=lambda d=device_id: self.toggle_device(d, 'on')).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="🔄 Переключить", 
                      command=lambda d=device_id: self.toggle_device(d, 'toggle')).pack(side=tk.LEFT, padx=2)
        
        # Специальные кнопки для разных устройств
        if device_id == "thermostat" and device_info['state'] == 'on':
            ttk.Button(btn_frame, text="🌡️ Установить температуру", 
                      command=self.set_temperature_dialog).pack(side=tk.LEFT, padx=2)
        elif device_id == "lamp_living_room" and device_info['state'] == 'on':
            ttk.Button(btn_frame, text="💡 Установить яркость", 
                      command=self.set_brightness_dialog).pack(side=tk.LEFT, padx=2)
        
        return card_frame
    
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
        # Очищаем старые карточки
        for widget in self.devices_scroll_frame.winfo_children():
            widget.destroy()
        
        # Получаем статус всех устройств
        devices_status = self.controller.device_manager.get_all_devices_status()
        
        # Создаем новые карточки
        for device_id, device_info in devices_status.items():
            self.create_device_card(device_id, device_info)
    
    def refresh_logs(self):
        """Обновление отображения логов"""
        log_type = self.log_type_var.get()
        logs = self.controller.logging_service.get_logs(log_type, limit=50)
        
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
            self.controller.stop_system()
            self.root.destroy()


def main():
    """Главная функция запуска GUI"""
    root = tk.Tk()
    app = SmartHomeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()