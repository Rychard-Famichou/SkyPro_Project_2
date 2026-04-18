import pytest

from aeroplane.aeroplane import Aeroplane


# --- ТЕСТЫ ВАЛИДАЦИИ СТРОК ---
@pytest.mark.parametrize(
    "input_val, expected",
    [
        ("AFL123", "AFL123"),  # Обычная строка
        (123, "123"),  # Число вместо строки
        (None, "Unknown"),  # None -> Unknown
        ("", ""),  # Пустая строка
    ],
)
def test_validate_str(input_val, expected):
    # Тестируем через инициализацию атрибута callsign или country
    plane = Aeroplane(input_val, "Russia", 0, 0, 0, 0)
    assert plane.callsign == expected


# --- ТЕСТЫ ВАЛИДАЦИИ ЧИСЕЛ ---
@pytest.mark.parametrize(
    "input_val, expected",
    [
        (10000, 10000.0),  # Int -> Float
        ("5000", 5000.0),  # Строка-число -> Float
        (None, 0.0),  # None -> 0.0
        ("abc", 0.0),  # Невалидная строка -> 0.0
        (12.5, 12.5),  # Число с плавающей точкой
    ],
)
def test_validate_num(input_val, expected):
    # Тестируем через baro_altitude или любой другой числовой атрибут
    plane = Aeroplane("AF1", "France", 0, 0, input_val, 0)
    assert plane.baro_altitude == expected


# --- ТЕСТЫ СРАВНЕНИЯ (МАГИЧЕСКИЕ МЕТОДЫ) ---
def test_aeroplane_comparisons():
    low_plane = Aeroplane("LOW", "RU", 0, 0, 1000.0, 0)
    high_plane = Aeroplane("HIGH", "RU", 0, 0, 9000.0, 0)
    equal_plane = Aeroplane("EQUAL", "RU", 0, 0, 1000.0, 0)

    assert low_plane < high_plane  # __lt__
    assert high_plane > low_plane  # __gt__
    assert low_plane == equal_plane  # __eq__
    assert low_plane <= equal_plane  # __le__
    assert high_plane >= low_plane  # __ge__
    assert low_plane != high_plane  # __ne__ (работает через __eq__)


# --- ТЕСТ НА __STR__ ---
def test_aeroplane_str():
    plane = Aeroplane("TEST", "Country", 0, 0, 5000.0, 0)
    expected_str = "Позывной: 'TEST'. Страна: 'Country'. Высота: 5000.0 метров."
    assert str(plane) == expected_str


def test_comparisons_with_invalid_types():
    """Тест сравнения: NotImplemented"""
    plane = Aeroplane("AFL123", "Russia", 0, 0, 10000.0, 800.0)
    invalid_other = "Я просто строка, а не самолет"
    assert (plane == invalid_other) is False
    assert (plane != invalid_other) is True
    with pytest.raises(TypeError):
        _ = plane < invalid_other
    with pytest.raises(TypeError):
        _ = plane > 500
