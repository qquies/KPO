#!/usr/bin/env python3
"""
Умный Дом - Профессиональная система управления
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Добавляем путь к src в систему

from core.home_controller import HomeController
from ui.console_interface import ConsoleInterface

def main():
    """Главная функция запуска системы"""
    print("=" * 60)
    print("        🏠 СИСТЕМА УМНЫЙ ДОМ - ПРОФЕССИОНАЛЬНАЯ ВЕРСИЯ")
    print("=" * 60)
    
    try:
        # Создаем и запускаем систему
        controller = HomeController()
        controller.start_system()
        
        # Запускаем интерфейс
        interface = ConsoleInterface(controller)
        interface.display_main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Программа завершена пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка системы: {e}")

if __name__ == "__main__":
    main()