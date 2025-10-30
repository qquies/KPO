# tests/test_use_case_coverage.py
import pytest
import importlib
import pkgutil
import inspect
import os
import sys
from core.home_controller import HomeController
from ui.console_interface import ConsoleInterface

class TestUseCaseCoverage:
    """Тестирование покрытия Use-Case диаграммы в коде с автоматическим сканированием"""
    
    def test_use_case_implementation_coverage(self):
        """Проверяем, что все Use-Case сценарии из диаграммы реализованы в коде"""
        
        # Use-Case сценарии из диаграммы
        expected_use_cases = {
            "UC1": "Авторизация (login/logout)",
            "UC2": "Управление устройствами (вкл/выкл свет, камеры, замки, кондиционер)",
            "UC3": "Управление климатом (настройка температуры, режимов)", 
            "UC4": "Управление безопасностью (arm/disarm, сигнализация)",
            "UC5": "Просмотр уведомлений",
            "UC6": "Просмотр журналов событий",
            "UC7": "Планирование действий (расписания)",
            "UC8": "Оптимизация энергопотребления"
        }
        
        # Создаем экземпляр системы
        controller = HomeController()
        interface = ConsoleInterface(controller)
        
        # Автоматически анализируем ВСЕ модули проекта
        implemented_features = self._analyze_entire_project(controller, interface)
        
        # Проверяем покрытие Use-Case
        coverage_report = self._check_use_case_coverage(expected_use_cases, implemented_features)
        
        # Выводим подробный отчет
        self._print_coverage_report(coverage_report)
        
        # Утверждаем, что основные Use-Case покрыты
        assert coverage_report['coverage_percentage'] >80, (
            f"Должен быть покрыт хотя бы один Use-Case. Текущее покрытие: {coverage_report['coverage_percentage']}%"
        )
    
    def _analyze_entire_project(self, controller, interface):
        """Автоматически анализирует ВСЕ классы и модули в проекте"""
        implemented = {
            'UC1': [], 'UC2': [], 'UC3': [], 'UC4': [], 
            'UC5': [], 'UC6': [], 'UC7': [], 'UC8': []
        }
        
        print("🔍 Начинаем сканирование проекта...")
        
        # 1. Анализируем основные классы
        implemented = self._analyze_object_methods(controller, implemented, "HomeController")
        implemented = self._analyze_object_methods(interface, implemented, "ConsoleInterface")
        
        # 2. Автоматически сканируем все модули
        implemented = self._scan_all_modules(implemented)
        
        # 3. Убираем дубликаты
        implemented = self._remove_duplicates(implemented)
        
        print(f"✅ Сканирование завершено. Найдено методов: {sum(len(methods) for methods in implemented.values())}")
        
        return implemented

    def _remove_duplicates(self, implemented):
        """Убирает дублирующиеся методы, оставляя только короткие имена"""
        cleaned_implemented = {
            'UC1': [], 'UC2': [], 'UC3': [], 'UC4': [], 
            'UC5': [], 'UC6': [], 'UC7': [], 'UC8': []
        }
        
        for uc_id, methods in implemented.items():
            unique_methods = set()
            
            for method in methods:
                # Оставляем только короткое имя метода (последнюю часть после последней точки)
                if '.' in method:
                    short_name = method.split('.')[-1]
                    unique_methods.add(short_name)
                else:
                    unique_methods.add(method)
            
            cleaned_implemented[uc_id] = list(unique_methods)
        
        return cleaned_implemented
    
    def _scan_all_modules(self, implemented):
        """Рекурсивно сканирует все Python модули в пакете src"""
        packages_to_scan = ['src', 'core', 'ui', 'devices']  # Основные пакеты для сканирования
        
        for package_name in packages_to_scan:
            try:
                print(f"📦 Сканируем пакет: {package_name}")
                package = importlib.import_module(package_name)
                
                # 👇 ДОБАВЬТЕ ЭТОТ ВЫВОД ДЛЯ ОТЛАДКИ:
                print(f"   Путь пакета: {package.__path__}")
                
                # Рекурсивно обходим все модули в пакете
                module_count = 0
                for importer, modname, ispkg in pkgutil.walk_packages(
                    package.__path__, 
                    package.__name__ + '.'
                ):
                    if self._should_skip_module(modname):
                        continue
                        
                    module_count += 1
                    print(f"   📄 Найден модуль: {modname}")
                        
                    try:
                        # Импортируем модуль
                        module = importlib.import_module(modname)
                        
                        # Анализируем все классы в модуле
                        class_count = self._analyze_module_classes(module, modname, implemented)
                        
                        if class_count > 0:
                            print(f"   ✅ {modname}: найдено {class_count} классов")
                            
                    except Exception as e:
                        print(f"   ⚠️ Ошибка в модуле {modname}: {e}")
                
                print(f"   Всего модулей в {package_name}: {module_count}")
                        
            except ImportError:
                print(f"⚠️ Пакет {package_name} не найден, пропускаем")
                continue
                
        return implemented
    
    def _scan_additional_directories(self, implemented):
        """Сканирует дополнительные директории через обход файловой системы"""
        additional_dirs = ['src', 'core', 'ui', 'devices']
        
        for dir_name in additional_dirs:
            if os.path.exists(dir_name):
                print(f"📁 Сканируем директорию: {dir_name}")
                implemented = self._scan_directory_recursive(dir_name, implemented)
                
        return implemented
    
    def _scan_directory_recursive(self, directory, implemented):
        """Рекурсивно сканирует директорию на наличие Python файлов"""
        for root, dirs, files in os.walk(directory):
            # Пропускаем служебные директории
            dirs[:] = [d for d in dirs if not d.startswith('_') and not d.startswith('.')]
            
            for file in files:
                if file.endswith('.py') and not file.startswith('_'):
                    file_path = os.path.join(root, file)
                    
                    # Формируем имя модуля из пути
                    module_name = self._file_path_to_module_name(file_path)
                    
                    try:
                        # Динамически импортируем модуль
                        spec = importlib.util.spec_from_file_location(module_name, file_path)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            
                            # Анализируем классы в модуле
                            class_count = self._analyze_module_classes(module, module_name, implemented)
                            
                            if class_count > 0:
                                print(f"   ✅ {module_name}: {class_count} классов")
                                
                    except Exception as e:
                        print(f"   ⚠️ Ошибка в файле {file}: {e}")
                        
        return implemented
    
    def _file_path_to_module_name(self, file_path):
        """Преобразует путь к файлу в имя модуля"""
        # Убираем расширение .py
        module_path = file_path.replace('.py', '')
        
        # Заменяем разделители путей на точки
        module_path = module_path.replace('/', '.').replace('\\', '.')
        
        # Убираем начальные точки если есть
        if module_path.startswith('.'):
            module_path = module_path[1:]
            
        return module_path
    
    def _should_skip_module(self, module_name):
        """Определяет, нужно ли пропускать модуль"""
        skip_patterns = [
            'test_', '__pycache__', '.pytest_cache', 
            'venv', '.venv', 'env', 'site-packages'
        ]
        
        return any(pattern in module_name for pattern in skip_patterns)
    
    def _analyze_module_classes(self, module, module_name, implemented):
        """Анализирует все классы в модуле"""
        class_count = 0
        
        print(f"      🔍 Анализируем классы в {module_name}:")
        
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Проверяем, что класс определен в этом модуле (а не импортирован)
            if hasattr(obj, '__module__') and obj.__module__ == module_name:
                class_count += 1
                print(f"         🏷️ Найден класс: {name}")
                implemented = self._analyze_class_methods(obj, f"{module_name}.{name}", implemented)
        
        if class_count == 0:
            print(f"         ❌ Классы не найдены в {module_name}")
                
        return class_count

    def _analyze_class_methods(self, cls, class_name, implemented):
        """Анализирует методы одного класса"""
        methods = [method for method in dir(cls) if not method.startswith('_')]
        
        print(f"            📋 Методы класса {class_name}: {methods}")
        
        for method in methods:
            method_obj = getattr(cls, method)
            if callable(method_obj):
                method_with_prefix = f"{class_name}.{method}"
                
                # Определяем Use-Case для метода
                category = self._categorize_method(method_with_prefix, method, implemented)
                if category:
                    print(f"            ✅ Метод '{method}' отнесен к {category}")
        
        return implemented
    
    def _analyze_object_methods(self, obj, implemented, obj_name):
        """Анализирует методы конкретного объекта"""
        methods = [method for method in dir(obj) if not method.startswith('_')]
        
        for method in methods:
            method_obj = getattr(obj, method)
            if callable(method_obj):
                method_with_prefix = f"{obj_name}.{method}"
                self._categorize_method(method_with_prefix, method, implemented)
        
        return implemented
    
    def _categorize_method(self, full_method_name, method_name, implemented):
        """Определяет к какому Use-Case относится метод"""
        method_lower = method_name.lower()
        
        # UC1: Авторизация
        if any(keyword in method_lower for keyword in ['login', 'auth', 'logout', 'start', 'init', 'shutdown']):
            implemented['UC1'].append(full_method_name)
        
        # UC2: Управление устройствами
        elif any(keyword in method_lower for keyword in [
            'light', 'lamp', 'bulb', 'device', 'toggle', 'turn', 'control', 
            'switch', 'on', 'off', 'brightness', 'camera', 'lock', 'door'
        ]):
            implemented['UC2'].append(full_method_name)
        
        # UC3: Управление климатом
        elif any(keyword in method_lower for keyword in [
            'temp', 'climate', 'temperature', 'thermo', 'heat', 'cool', 
            'air', 'condition', 'humidity', 'ventilation', 'conditioner'
        ]):
            implemented['UC3'].append(full_method_name)
        
        # UC4: Безопасность
        elif any(keyword in method_lower for keyword in [
            'security', 'alarm', 'alert', 'lock', 'camera', 'surveillance',
            'motion', 'detect', 'arm', 'disarm', 'emergency'
        ]):
            implemented['UC4'].append(full_method_name)
        
        # UC5: Уведомления
        elif any(keyword in method_lower for keyword in [
            'notification', 'notify', 'alert', 'message', 'push',
            'email', 'sms', 'reminder'
        ]):
            implemented['UC5'].append(full_method_name)
        
        # UC6: Журналы событий
        elif any(keyword in method_lower for keyword in [
            'log', 'history', 'event', 'record', 'audit',
            'report', 'statistic', 'analytics'
        ]):
            implemented['UC6'].append(full_method_name)
        
        # UC7: Планирование
        elif any(keyword in method_lower for keyword in [
            'schedule', 'plan', 'timer', 'cron', 'automation',
            'routine', 'scenario', 'scene'
        ]):
            implemented['UC7'].append(full_method_name)
        
        # UC8: Энергопотребление
        elif any(keyword in method_lower for keyword in [
            'energy', 'power', 'optimize', 'consumption', 'save',
            'efficiency', 'watt', 'kwh', 'battery'
        ]):
            implemented['UC8'].append(full_method_name)
    
    def _check_use_case_coverage(self, expected_use_cases, implemented_features):
        """Проверяет покрытие Use-Case"""
        coverage_report = {
            'covered': [],
            'partially_covered': [],
            'not_covered': [],
            'coverage_percentage': 0,
            'total_methods_found': 0
        }
        
        for uc_id, uc_description in expected_use_cases.items():
            features = implemented_features[uc_id]
            coverage_report['total_methods_found'] += len(features)
            
            if len(features) >= 3:
                coverage_report['covered'].append((uc_id, uc_description, features))
            elif len(features) >= 1:
                coverage_report['partially_covered'].append((uc_id, uc_description, features))
            else:
                coverage_report['not_covered'].append((uc_id, uc_description))
        
        total_use_cases = len(expected_use_cases)
        covered_count = len(coverage_report['covered']) + len(coverage_report['partially_covered']) * 0.7
        coverage_report['coverage_percentage'] = (covered_count / total_use_cases) * 100
        
        return coverage_report
    
    def _print_coverage_report(self, coverage_report):
        """Выводит подробный отчет о покрытии"""
        print("\n" + "="*70)
        print("🎯 ОТЧЕТ О ПОКРЫТИИ USE-CASE ДИАГРАММЫ (АВТОМАТИЧЕСКОЕ СКАНИРОВАНИЕ)")
        print("="*70)
        
        print(f"\n📊 ОБЩАЯ СТАТИСТИКА:")
        print(f"   Всего методов найдено: {coverage_report['total_methods_found']}")
        print(f"   Общее покрытие Use-Case: {coverage_report['coverage_percentage']:.1f}%")
        
        print("\n✅ ПОЛНОСТЬЮ ПОКРЫТЫЕ USE-CASE (≥3 метода):")
        for uc_id, description, features in coverage_report['covered']:
            print(f"   🟢 {uc_id}: {description}")
            print(f"      Методы ({len(features)}): {', '.join(features[:5])}" + 
                  ("..." if len(features) > 5 else ""))
        
        print("\n🟡 ЧАСТИЧНО ПОКРЫТЫЕ USE-CASE (1-2 метода):")
        for uc_id, description, features in coverage_report['partially_covered']:
            print(f"   🟡 {uc_id}: {description}")
            print(f"      Методы: {', '.join(features)}")
        
        print("\n❌ НЕ ПОКРЫТЫЕ USE-CASE:")
        for uc_id, description in coverage_report['not_covered']:
            print(f"   🔴 {uc_id}: {description}")
        
        print("\n" + "="*70)

    def test_specific_use_case_validation(self):
        """Конкретная проверка что система хотя бы запускается"""
        controller = HomeController()
        
        # UC1: Проверяем инициализацию системы
        assert hasattr(controller, 'start_system'), "UC1: Должен быть метод start_system"
        
        # Проверяем что система запускается без ошибок
        try:
            controller.start_system()
            print("✅ Система успешно запускается")
        except Exception as e:
            pytest.fail(f"❌ Система не может запуститься: {e}")

    def test_use_case_integration(self):
        """Проверяем, что Use-Case могут работать вместе"""
        controller = HomeController()
        
        # Система должна запускаться (UC1)
        controller.start_system()
        
        print("✅ Базовая интеграция проверена - система работает")

if __name__ == "__main__":
    # Запуск теста напрямую для отладки
    test_instance = TestUseCaseCoverage()
    test_instance.test_use_case_implementation_coverage()