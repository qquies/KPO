import unittest
from CreateUseCaseDiag import *

class UseCaseDiagTests(unittest.TestCase):
    def setUp(self):
        """Создаем диаграмму с правильными связями"""
        self.diagram, self.elements = create_smart_home_diagram()
        self.diagram = setup_correct_connections(self.diagram, self.elements)
        
        # Распаковываем элементы для удобства
        (self.user, self.uc1, self.uc2, self.uc3, self.uc4, 
         self.uc5, self.uc6, self.uc7, self.uc8, 
         self.notification_db, self.log_db) = self.elements
    
    def test_UC_01_user_actor_exists(self):
        """Проверка наличия актера 'Пользователь'"""
        user = self.diagram.get_element("Пользователь")
        self.assertIsNotNone(user, "Актер 'Пользователь' должен существовать")
        self.assertEqual(user.type, "actor", "Пользователь должен быть актером")
        print("UC-01: Актер 'Пользователь' присутствует")
    
    def test_UC_02_user_connections_count(self):
        """Проверка количества связей пользователя с use-case"""
        user = self.diagram.get_element("Пользователь")
        usecase_connections = [conn for conn in user.connections 
                             if conn['target'].type == 'usecase']
        
        self.assertEqual(len(usecase_connections), 8, 
                        "Пользователь должен быть связан с 8 use-case")
        print("UC-02: Пользователь связан с 8 use-case")
    
    def test_UC_03_meaningful_usecase_names(self):
        """Проверка осмысленности названий use-case"""
        meaningful_keywords = ['управление', 'авторизация', 'просмотр', 
                              'планирование', 'оптимизация']
        
        usecases = self.diagram.get_elements_by_type('usecase')
        for uc in usecases:
            name_lower = uc.name.lower()
            has_meaning = any(keyword in name_lower for keyword in meaningful_keywords)
            self.assertTrue(has_meaning, 
                          f"Use-case '{uc.name}' должен иметь осмысленное название")
        print("UC-03: Все use-case имеют осмысленные названия")
    
    def test_UC_04_database_connections(self):
        """Проверка связей использования с БД"""
        # Проверяем, что UC5 использует БД уведомлений через include
        uc5_includes = self.uc5.include_connections
        self.assertEqual(len(uc5_includes), 1, 
                        "UC5 должен иметь одну include связь")
        
        uc5_db_connection = uc5_includes[0]
        self.assertEqual(uc5_db_connection['target'].name, "БД уведомлений")
        self.assertEqual(uc5_db_connection['relationship'], 'include')
        print("UC-04: UC5 использует БД уведомлений через <<include>>")
        
        # Проверяем, что UC6 использует БД логов через include
        uc6_includes = self.uc6.include_connections
        self.assertEqual(len(uc6_includes), 1, 
                        "UC6 должен иметь одну include связь")
        
        uc6_db_connection = uc6_includes[0]
        self.assertEqual(uc6_db_connection['target'].name, "БД логов")
        self.assertEqual(uc6_db_connection['relationship'], 'include')
        print("UC-04: UC6 использует БД логов через <<include>>")

        """Проверка, что БД не являются актерами"""
        databases = self.diagram.get_elements_by_type('database')
        self.assertEqual(len(databases), 2, "Должны быть 2 БД")
        
        actors = self.diagram.get_elements_by_type('actor')
        actor_names = [actor.name for actor in actors]
        
        # Проверяем, что БД не в списке актеров
        self.assertNotIn("БД уведомлений", actor_names)
        self.assertNotIn("БД логов", actor_names)
        print("UC-04: БД правильно определены как database")

        """Проверка отсутствия прямых связей актеров с БД"""
        user_connections = self.user.get_all_connections()
        
        # Пользователь не должен быть напрямую связан с БД
        db_connections = [
            conn for conn in user_connections 
            if conn['target'].type == 'database'
        ]
        self.assertEqual(len(db_connections), 0,
                        "Пользователь не должен напрямую обращаться к БД")
        print("UC-04: Нет прямых связей актеров с БД")
    
    def test_UC_05_system_boundary_elements(self):
        """Проверка элементов внутри границ системы"""
        usecases = self.diagram.get_elements_by_type('usecase')
        self.assertGreater(len(usecases), 0, "В системе должны быть use-case")
        
        # Проверяем, что use-case логически сгруппированы
        smart_home_keywords = ['безопасность', 'климат', 'устройства', 'оптимизация']
        smart_home_usecases = [
            uc for uc in usecases 
            if any(keyword in uc.name.lower() for keyword in smart_home_keywords)
        ]
        self.assertGreaterEqual(len(smart_home_usecases), 4, 
                               "Должны быть use-case для основных функций умного дома")
        print("UC-05: Система имеет логическую группировку use-case")
    
    def test_UC_06_basic_functionality_coverage(self):
        """Проверка покрытия базовой функциональности"""
        required_functions = [
            'авторизация', 'управление устройствами', 'управление климатом', 'управление безопасностью',
            'просмотр уведомлений', 'просмотр журналов событий', 'планирование действий', 'оптимизация энергопотребления'
        ]
        
        usecase_names = [uc.name.lower() for uc in self.diagram.get_elements_by_type('usecase')]
        
        missing_functions = []
        for func in required_functions:
            if not any(func in name for name in usecase_names):
                missing_functions.append(func)
        
        self.assertEqual(len(missing_functions), 0,
                        f"Отсутствуют функции: {missing_functions}")
        print("UC-06: Базовая функциональность покрыта")
    
    def test_UC_07_diagram_readability(self):
        """Проверка читаемости диаграммы"""
        elements = self.diagram.elements
        
        # Проверяем, что нет элементов с одинаковыми именами
        names = [elem.name for elem in elements.values()]
        unique_names = set(names)
        self.assertEqual(len(names), len(unique_names), 
                        "Все имена элементов должны быть уникальными")
        
        # Проверяем, что use-case имеют разумную длину названий
        usecases = self.diagram.get_elements_by_type('usecase')
        for uc in usecases:
            self.assertLessEqual(len(uc.name), 100, 
                               f"Название use-case '{uc.name}' слишком длинное")
        print("UC-07: Диаграмма читаема и организована")
    
    def test_UC_08_no_duplicate_functionality(self):
        """Проверка отсутствия дублирующей функциональности"""
        usecases = self.diagram.get_elements_by_type('usecase')
        functionality_keywords = []
        
        for uc in usecases:
            # Извлекаем ключевые слова из названий
            keywords = [word for word in uc.name.lower().split() 
                       if word not in ['и', 'в', 'на', 'с', 'управление']]
            functionality_keywords.extend(keywords)
        
        # Проверяем на дубликаты ключевых слов
        from collections import Counter
        keyword_counts = Counter(functionality_keywords)
        duplicates = {k: v for k, v in keyword_counts.items() if v > 2}
        
        self.assertEqual(len(duplicates), 0,
                        f"Возможные дубликаты функциональности: {duplicates}")
        print("UC-08: Дублирующей функциональности не обнаружено")
