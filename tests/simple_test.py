# simple_test.py
import sys
import os

# Добавляем путь к src
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from core.home_controller import HomeController
    from ui.console_interface import ConsoleInterface
    print("Все модули загружаются!")
    
    # Тест создания системы
    controller = HomeController()
    print("Система создана!")
    
    # Тест запуска
    controller.start_system()
    print("Система запущена!")
    
    # Тест интерфейса
    interface = ConsoleInterface(controller)
    print("Интерфейс создан!")
    
    print("\nВСЁ РАБОТАЕТ! Можно запускать main.py")
    
except Exception as e:
    print(f"Ошибка: {e}")
    import traceback
    traceback.print_exc()
