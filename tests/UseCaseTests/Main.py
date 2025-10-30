import unittest
from UseCaseDiagTests import *

def run_use_case_tests():
    print("ЗАПУСК ТЕСТИРОВАНИЯ USE-CASE ДИАГРАММЫ")
    print("=" * 50)
    
    # Создаем test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(UseCaseDiagTests)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Красивый отчет
    print("\n" + "=" * 50)
    print("ОТЧЕТ О ТЕСТИРОВАНИИ")
    print(f"Всего тестов: {result.testsRun}")
    print(f"Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалено: {len(result.failures)}")
    print(f"Ошибок: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Use-Case диаграмма корректна.")
    else:
        print("Есть проблемы, требующие исправления.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_use_case_tests()