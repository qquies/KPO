# tests/test_exhaustive_testing.py
import pytest
from core.home_controller import HomeController


class TestExhaustiveTesting:
    """Исчерпывающее тестирование для небольших конечных доменов."""

    def setup_method(self):
        self.controller = HomeController()

    def test_exhaustive_temperature(self):
        """Полный перебор температур в разумном окне и проверка истинного диапазона 15..30."""
        passed = 0
        total = 0
        for t in range(-10, 46):  # покрываем за пределами диапазона
            total += 1
            expected = 15 <= t <= 30
            result = self.controller.set_temperature(t)
            assert result == expected, f"Температура {t}°C: ожидалось {expected}, получили {result}"
            passed += 1
        assert passed == total

    def test_exhaustive_brightness(self):
        """Полный перебор яркости в окне -10..110 и проверка истинного диапазона 0..100."""
        passed = 0
        total = 0
        for b in range(-10, 111):
            total += 1
            expected = 0 <= b <= 100
            result = self.controller.set_brightness(b)
            assert result == expected, f"Яркость {b}%: ожидалось {expected}, получили {result}"
            passed += 1
        assert passed == total

    def test_exhaustive_time_all_minutes(self):
        """Полный перебор всех валидных минут суток и точечные невалидные примеры."""
        # Все валидные HH:MM от 00:00 до 23:59 должны быть True
        for h in range(0, 24):
            for m in range(0, 60):
                time_str = f"{h:02d}:{m:02d}"
                assert self.controller.set_schedule_time(time_str), f"Ожидалось True для {time_str}"

        # Невалидные точки
        invalid = [
            "24:00",  # час вне диапазона
            "-1:00",  # отрицательный час
            "12:60",  # минуты вне диапазона
            "1:30",   # нестрогий формат
            "12:0",   # нестрогий формат
            "1200",   # нет двоеточия
            "ab:cd",  # буквы
        ]
        for s in invalid:
            assert not self.controller.set_schedule_time(s), f"Ожидалось False для '{s}'"

    def test_exhaustive_energy(self):
        """Полный перебор энергии в диапазоне 0..5000 и точечные невалидные значения."""
        # Валидные 0..5000 включительно
        for e in range(0, 5001):
            assert self.controller.set_energy_limit(e), f"Ожидалось True для энергии {e}Вт"

        # Невалидные точки
        for e in [-10, -1, 5001, 10000]:
            assert not self.controller.set_energy_limit(e), f"Ожидалось False для энергии {e}Вт"


