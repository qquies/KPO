from Functions import *

def create_smart_home_diagram():
    """Создает полную диаграмму умного дома с правильными связями"""
    diagram = UseCaseDiagram("Умный дом")
    
    # Создаем актеров
    user = UseCaseElement("Пользователь", "actor")
    
    # Создаем Use Cases
    uc1 = UseCaseElement("Авторизация (login/logout)", "usecase")
    uc2 = UseCaseElement("Управление устройствами (вкл/выкл свет, камеры, замки, кондиционер)", "usecase")
    uc3 = UseCaseElement("Управление климатом (настройка температуры, режимов)", "usecase")
    uc4 = UseCaseElement("Управление безопасностью (arm/disarm, сигнализация)", "usecase")
    uc5 = UseCaseElement("Просмотр уведомлений", "usecase")
    uc6 = UseCaseElement("Просмотр журналов событий", "usecase")
    uc7 = UseCaseElement("Планирование действий (расписания)", "usecase")
    uc8 = UseCaseElement("Оптимизация энергопотребления", "usecase")
    
    # Создаем БД как внутренние компоненты (не актеры!)
    notification_db = UseCaseElement("БД уведомлений", "database")
    log_db = UseCaseElement("БД логов", "database")
    
    # Добавляем все элементы в диаграмму
    elements = [user, uc1, uc2, uc3, uc4, uc5, uc6, uc7, uc8, notification_db, log_db]
    for element in elements:
        diagram.add_element(element)
    
    return diagram, elements

def setup_correct_connections(diagram, elements):
    """Настраивает правильные связи между элементами"""
    user, uc1, uc2, uc3, uc4, uc5, uc6, uc7, uc8, notification_db, log_db = elements
    
    # Пользователь связан со всеми основными use-case (ассоциации)
    user_use_cases = [uc1, uc2, uc3, uc4, uc5, uc6, uc7, uc8]
    for use_case in user_use_cases:
        user.add_connection(use_case, "association")
    
    # Use-case используют БД через связи <<include>>
    uc5.add_include_connection(notification_db)  # Просмотр уведомлений использует БД уведомлений
    uc6.add_include_connection(log_db)           # Просмотр журналов использует БД логов
    
    return diagram