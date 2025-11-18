# tests/test_boundary_value_analysis.py
import pytest
from core.home_controller import HomeController


class TestBoundaryValueAnalysis:
    """Тесты анализа граничных значений для ключевых функций системы."""

    def setup_method(self):
        self.controller = HomeController()

    # Температура: границы 15–30 (включительно)
    @pytest.mark.parametrize(
        "input_c, expected, note",
        [
            (14, False, "ниже минимума"),
            (15, True, "нижняя граница"),
            (30, True, "верхняя граница"),
            (31, False, "выше максимума"),
        ],
    )
    def test_temperature_boundaries(self, input_c, expected, note):
        result = self.controller.set_temperature(input_c)
        assert result == expected, f"Температура {input_c}°C ({note})"

    # Яркость: границы 0–100 (включительно)
    @pytest.mark.parametrize(
        "brightness, expected, note",
        [
            (-1, False, "ниже минимума"),
            (0, True, "нижняя граница"),
            (100, True, "верхняя граница"),
            (101, False, "выше максимума"),
        ],
    )
    def test_brightness_boundaries(self, brightness, expected, note):
        result = self.controller.set_brightness(brightness)
        assert result == expected, f"Яркость {brightness}% ({note})"

    # PIN: длина 4–6 (включительно)
    @pytest.mark.parametrize(
        "pin, expected, note",
        [
            ("123", False, "короче минимума"),
            ("1234", True, "нижняя граница"),
            ("123456", True, "верхняя граница"),
            ("1234567", False, "длиннее максимума"),
        ],
    )
    def test_pin_boundaries(self, pin, expected, note):
        result = self.controller.validate_pin(pin)
        assert result == expected, f"PIN '{pin}' ({note})"

    # Время: формат HH:MM и диапазоны 00:00–23:59
    @pytest.mark.parametrize(
        "time_str, expected, note",
        [
            ("00:00", True, "нижняя граница"),
            ("23:59", True, "верхняя граница"),
            ("24:00", False, "час=24 недопустим"),
            ("-1:00", False, "отрицательный час"),
            ("12:60", False, "минуты=60 недопустимо"),
            ("12:59", True, "валидное время"),
            ("1:30", False, "нет ведущего нуля (формат)")
        ],
    )
    def test_time_boundaries(self, time_str, expected, note):
        result = self.controller.set_schedule_time(time_str)
        assert result == expected, f"Время '{time_str}' ({note})"

    # Энергия: границы 0–5000 (включительно)
    @pytest.mark.parametrize(
        "energy, expected, note",
        [
            (-1, False, "ниже минимума"),
            (0, True, "нижняя граница"),
            (5000, True, "верхняя граница"),
            (5001, False, "выше максимума"),
        ],
    )
    def test_energy_boundaries(self, energy, expected, note):
        result = self.controller.set_energy_limit(energy)
        assert result == expected, f"Энергия {energy}Вт ({note})"


