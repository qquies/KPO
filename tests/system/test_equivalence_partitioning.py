# tests/test_equivalence_partitioning.py
import pytest
from core.home_controller import HomeController

class TestEquivalencePartitioning:
    """Тестирование методом эквивалентного разделения"""
    
    def setup_method(self):
        """Подготовка перед каждым тестом"""
        self.controller = HomeController()
    
    def test_temperature_equivalence_partitioning(self):
        """Эквивалентное разделение для управления температурой"""
        
        # Классы эквивалентности для температуры
        test_cases = [
            # (температура, ожидаемый_результат, описание_класса)
            
            # ДОПУСТИМЫЙ КЛАСС: 15-30°C
            (15, True, "Нижняя граница допустимого диапазона"),
            (22, True, "Середина допустимого диапазона"), 
            (30, True, "Верхняя граница допустимого диапазона"),
            (25, True, "Нормальное значение в диапазоне"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: <15°C
            (14, False, "Чуть ниже минимальной температуры"),
            (0, False, "Нулевая температура"),
            (-10, False, "Отрицательная температура"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: >30°C  
            (31, False, "Чуть выше максимальной температуры"),
            (40, False, "Высокая температура"),
            (100, False, "Очень высокая температура"),
        ]
        
        print("ТЕСТИРОВАНИЕ ТЕМПЕРАТУРЫ - ЭКВИВАЛЕНТНОЕ РАЗДЕЛЕНИЕ")
        print("=" * 60)
        
        passed = 0
        total = 0
        
        for temperature, expected_result, description in test_cases:
            total += 1
            try:
                # Вызываем метод установки температуры
                result = self.controller.set_temperature(temperature)
                
                # Проверяем результат
                if result == expected_result:
                    passed += 1
                    status = "ПРОЙДЕН"
                else:
                    status = "НЕ ПРОЙДЕН"
                
                print(f"  {status} | {temperature:3}°C | {description}")
                    
            except Exception as e:
                # Если метод не реализован, пропускаем с предупреждением
                print(f"  ПРОПУЩЕНО | {temperature:3}°C | {description} (ошибка: {e})")
        
        print(f"  ИТОГ: {passed}/{total} тестов пройдено")
        # Жёсткая проверка: если какой-либо кейс не прошёл — падаем
        assert passed == total, f"Температура: пройдено {passed} из {total}"
    
    def test_light_brightness_equivalence_partitioning(self):
        """Эквивалентное разделение для яркости света"""
        
        # Классы эквивалентности для яркости (0-100%)
        test_cases = [
            # (яркость, ожидаемый_результат, описание_класса)
            
            # ДОПУСТИМЫЙ КЛАСС: 0-100%
            (0, True, "Минимальная яркость (выключено)"),
            (50, True, "Средняя яркость"),
            (100, True, "Максимальная яркость"),
            (75, True, "Высокая яркость"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: <0%
            (-1, False, "Отрицательная яркость"),
            (-50, False, "Сильно отрицательная яркость"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: >100%
            (101, False, "Свыше 100% яркости"),
            (150, False, "Яркость 150%"),
        ]
        
        print("\nТЕСТИРОВАНИЕ ЯРКОСТИ СВЕТА - ЭКВИВАЛЕНТНОЕ РАЗДЕЛЕНИЕ")
        print("=" * 60)
        
        passed = 0
        total = 0
        
        for brightness, expected_result, description in test_cases:
            total += 1
            try:
                # Пробуем разные возможные названия методов
                if hasattr(self.controller, 'set_brightness'):
                    result = self.controller.set_brightness(brightness)
                elif hasattr(self.controller, 'set_light_brightness'):
                    result = self.controller.set_light_brightness(brightness)
                elif hasattr(self.controller, 'adjust_brightness'):
                    result = self.controller.adjust_brightness(brightness)
                else:
                    print(f"  ПРОПУЩЕНО | {brightness:3}% | {description} (методы не реализованы)")
                    continue
                
                # Проверяем результат
                if result == expected_result:
                    passed += 1
                    status = "ПРОЙДЕН"
                else:
                    status = "НЕ ПРОЙДЕН"
                
                print(f"  {status} | {brightness:3}% | {description}")
                    
            except Exception as e:
                print(f"  ПРОПУЩЕНО | {brightness:3}% | {description} (ошибка: {e})")
        
        print(f"  ИТОГ: {passed}/{total} тестов пройдено")
        # Жёсткая проверка
        assert passed == total, f"Яркость: пройдено {passed} из {total}"
    
    def test_security_pin_equivalence_partitioning(self):
        """Эквивалентное разделение для PIN-кода безопасности"""
        
        # Классы эквивалентности для PIN-кода (4-6 цифр)
        test_cases = [
            # (pin_код, ожидаемый_результат, описание_класса)
            
            # ДОПУСТИМЫЙ КЛАСС: 4-6 цифр
            ("1234", True, "Корректный PIN из 4 цифр"),
            ("12345", True, "Корректный PIN из 5 цифр"), 
            ("123456", True, "Корректный PIN из 6 цифр"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: <4 цифр
            ("123", False, "Слишком короткий PIN"),
            ("12", False, "Очень короткий PIN"),
            ("", False, "Пустой PIN"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: >6 цифр
            ("1234567", False, "Слишком длинный PIN"),
            ("12345678", False, "Очень длинный PIN"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: не цифры
            ("abcd", False, "PIN с буквами"),
            ("12a4", False, "PIN с буквой в середине"),
            ("!@#$", False, "PIN со спецсимволами"),
            ("12 34", False, "PIN с пробелом"),
        ]
        
        print("\nТЕСТИРОВАНИЕ PIN-КОДА - ЭКВИВАЛЕНТНОЕ РАЗДЕЛЕНИЕ")
        print("=" * 60)
        
        passed = 0
        total = 0
        
        for pin_code, expected_result, description in test_cases:
            total += 1
            try:
                # Пробуем методы безопасности
                if hasattr(self.controller, 'set_security_pin'):
                    result = self.controller.set_security_pin(pin_code)
                elif hasattr(self.controller, 'validate_pin'):
                    result = self.controller.validate_pin(pin_code)
                elif hasattr(self.controller, 'arm_security'):
                    result = self.controller.arm_security(pin_code)
                else:
                    print(f"  ПРОПУЩЕНО | '{pin_code:6}' | {description} (методы не реализованы)")
                    continue
                
                # Проверяем результат
                if result == expected_result:
                    passed += 1
                    status = "ПРОЙДЕН"
                else:
                    status = "НЕ ПРОЙДЕН"
                
                print(f"  {status} | '{pin_code:6}' | {description}")
                    
            except Exception as e:
                print(f"  ПРОПУЩЕНО | '{pin_code:6}' | {description} (ошибка: {e})")
        
        print(f"  ИТОГ: {passed}/{total} тестов пройдено")
        # Жёсткая проверка
        assert passed == total, f"PIN: пройдено {passed} из {total}"
    
    def test_schedule_time_equivalence_partitioning(self):
        """Эквивалентное разделение для времени расписания"""
        
        # Классы эквивалентности для времени (00:00 - 23:59)
        test_cases = [
            # (время, ожидаемый_результат, описание_класса)
            
            # ДОПУСТИМЫЙ КЛАСС: корректное время
            ("00:00", True, "Полночь"),
            ("12:00", True, "Полдень"),
            ("23:59", True, "Почти полночь"),
            ("09:30", True, "Утреннее время"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: неверный формат
            ("24:00", False, "Время после полуночи"),
            ("25:00", False, "Несуществующий час"),
            ("12:60", False, "Несуществующие минуты"),
            ("12:99", False, "Слишком большие минуты"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: неправильный формат
            ("1200", False, "Отсутствуют двоеточия"),
            ("12:0", False, "Одна цифра в минутах"),
            ("1:30", False, "Одна цифра в часах"),
            ("abc:de", False, "Буквы вместо цифр"),
        ]
        
        print("\nТЕСТИРОВАНИЕ ВРЕМЕНИ РАСПИСАНИЯ - ЭКВИВАЛЕНТНОЕ РАЗДЕЛЕНИЕ")
        print("=" * 60)
        
        passed = 0
        total = 0
        
        for time_str, expected_result, description in test_cases:
            total += 1
            try:
                # Пробуем методы расписания
                if hasattr(self.controller, 'set_schedule_time'):
                    result = self.controller.set_schedule_time(time_str)
                elif hasattr(self.controller, 'add_schedule'):
                    result = self.controller.add_schedule("test", time_str)
                else:
                    print(f"  ПРОПУЩЕНО | '{time_str:5}' | {description} (методы не реализованы)")
                    continue
                
                # Проверяем результат
                if result == expected_result:
                    passed += 1
                    status = "ПРОЙДЕН"
                else:
                    status = "НЕ ПРОЙДЕН"
                
                print(f"  {status} | '{time_str:5}' | {description}")
                    
            except Exception as e:
                print(f"  ПРОПУЩЕНО | '{time_str:5}' | {description} (ошибка: {e})")
        
        print(f"  ИТОГ: {passed}/{total} тестов пройдено")
        # Жёсткая проверка
        assert passed == total, f"Время расписания: пройдено {passed} из {total}"
    
    def test_energy_consumption_equivalence_partitioning(self):
        """Эквивалентное разделение для потребления энергии"""
        
        # Классы эквивалентности для энергии (0-5000 Вт)
        test_cases = [
            # (энергия, ожидаемый_результат, описание_класса)
            
            # ДОПУСТИМЫЙ КЛАСС: 0-5000 Вт
            (0, True, "Нулевое потребление"),
            (1000, True, "Низкое потребление"),
            (2500, True, "Среднее потребление"),
            (5000, True, "Максимальное потребление"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: <0 Вт
            (-1, False, "Отрицательное потребление"),
            (-100, False, "Сильно отрицательное потребление"),
            
            # НЕДОПУСТИМЫЙ КЛАСС: >5000 Вт
            (5001, False, "Свыше лимита"),
            (10000, False, "Очень высокое потребление"),
        ]
        
        print("\nТЕСТИРОВАНИЕ ПОТРЕБЛЕНИЯ ЭНЕРГИИ - ЭКВИВАЛЕНТНОЕ РАЗДЕЛЕНИЕ")
        print("=" * 60)
        
        passed = 0
        total = 0
        
        for energy, expected_result, description in test_cases:
            total += 1
            try:
                # Пробуем методы энергопотребления
                if hasattr(self.controller, 'set_energy_limit'):
                    result = self.controller.set_energy_limit(energy)
                elif hasattr(self.controller, 'check_energy_consumption'):
                    result = self.controller.check_energy_consumption(energy)
                else:
                    print(f"  ПРОПУЩЕНО | {energy:4} Вт | {description} (методы не реализованы)")
                    continue
                
                # Проверяем результат
                if result == expected_result:
                    passed += 1
                    status = "ПРОЙДЕН"
                else:
                    status = "НЕ ПРОЙДЕН"
                
                print(f"  {status} | {energy:4} Вт | {description}")
                    
            except Exception as e:
                print(f"  ПРОПУЩЕНО | {energy:4} Вт | {description} (ошибка: {e})")
        
        print(f"  ИТОГ: {passed}/{total} тестов пройдено")
        # Жёсткая проверка
        assert passed == total, f"Энергия: пройдено {passed} из {total}"

if __name__ == "__main__":
    # Запуск теста напрямую для отладки
    test_instance = TestEquivalencePartitioning()
    test_instance.setup_method()
    
    print("ЗАПУСК ТЕСТОВ ЭКВИВАЛЕНТНОГО РАЗДЕЛЕНИЯ")
    print("=" * 70)
    
    # Запускаем все тесты
    test_instance.test_temperature_equivalence_partitioning()
    test_instance.test_light_brightness_equivalence_partitioning() 
    test_instance.test_security_pin_equivalence_partitioning()
    test_instance.test_schedule_time_equivalence_partitioning()
    test_instance.test_energy_consumption_equivalence_partitioning()
    
    print("\n" + "=" * 70)
    print("ВСЕ ТЕСТЫ ЭКВИВАЛЕНТНОГО РАЗДЕЛЕНИЯ ЗАВЕРШЕНЫ")
