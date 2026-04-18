from unittest.mock import patch

import pytest

from aeroplane.aeroplane_data import AeroplaneData
from file.file_json import JSONAeroplaneStorage
from models.utils import Utils


@pytest.mark.parametrize(
    "file_manager, expected_class",
    [
        ("JSON", JSONAeroplaneStorage),
    ],
)
def test_get_file(file_manager, expected_class):
    worker = Utils()
    worker.get_file(file_manager)
    assert worker.file is not None
    assert isinstance(worker.file, expected_class)


@pytest.mark.parametrize(
    "input_name, expected_internal",
    [
        ("flights", "flights.json"),
        ("2023_data", "2023_data.json"),
    ],
)
def test_utils_file_activation(input_name, expected_internal):
    """Тест имени файла"""
    worker = Utils()
    worker.get_file_json_filename(input_name)
    assert isinstance(worker.file, JSONAeroplaneStorage)
    assert worker.file.filename == expected_internal


def test_get_available_filenames_empty():
    """Тест случая, когда файлов нет"""
    worker = Utils()
    with patch("models.utils.JSONAeroplaneStorage.get_all_saved_files", return_value=[]):
        result = worker.get_available_filenames()
        assert result == "Хранилище пока пусто (нет созданных файлов)."


def test_get_available_filenames_with_data():
    """Тест случая, когда в папке есть файлы"""
    worker = Utils()
    mock_files = ["planes_2023", "test_flight"]
    with patch("models.utils.JSONAeroplaneStorage.get_all_saved_files", return_value=mock_files):
        result = worker.get_available_filenames()
        assert "Доступные файлы в базе:" in result
        assert "- planes_2023" in result
        assert "- test_flight" in result


def test_get_top_n_clean(filled_utils):
    result = filled_utils.get_top_n(2)
    assert "1. Позывной: 'TEST2'" in result
    assert "2. Позывной: 'TEST1'" in result
    assert "Высота: 10000.0" in result


@pytest.mark.parametrize("data_state", [None, AeroplaneData("test")])
def test_get_top_n_returns_error_message(data_state):
    worker = Utils()
    worker.last_request_data = data_state

    assert worker.get_top_n(10) == "Нет данных для отображения."
    assert worker.get_planes_from_country("Country") == "Нет данных для отображения."


@pytest.mark.parametrize(
    "search_country, expected_fragment, count_expected",
    [
        ("Country", "Самолеты из 'Country'", 2),  # Кейс: Нашёл (регистр совпадает)
        ("COUNTRY", "Самолеты из 'COUNTRY'", 2),  # Кейс: Нашёл (разный регистр)
        ("Mars", "нет самолетов из 'Mars'", 0),  # Кейс: Не нашёл
    ],
)
def test_get_planes_from_country_logic(filled_utils, search_country, expected_fragment, count_expected):
    result = filled_utils.get_planes_from_country(search_country)
    assert expected_fragment in result

    if count_expected > 0:
        assert result.count("Позывной") == count_expected
    else:
        assert "Позывной" not in result


@pytest.mark.parametrize(
    "search_country, expected_count, should_find",
    [
        ("Iceland", 2, True),  # Должен найти 2 самолета
        ("Russia", 1, True),  # Должен найти 1 самолет
        ("USA", 0, False),  # Не должен найти ничего
    ],
)
def test_get_planes_from_country_filtering(multi_country_utils, search_country, expected_count, should_find):
    result = multi_country_utils.get_planes_from_country(search_country)

    if should_find:
        assert f"Самолеты из '{search_country}'" in result
        assert result.count("Позывной") == expected_count

        if search_country == "Russia":
            assert "ICE1" not in result
    else:
        assert f"нет самолетов из '{search_country}'" in result
        assert "Позывной" not in result
