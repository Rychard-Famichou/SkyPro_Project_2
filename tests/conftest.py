from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

from aeroplane.aeroplane import Aeroplane
from aeroplane.aeroplane_data import AeroplaneData
from file.file_json import JSONAeroplaneStorage
from models.app import FlightApp
from models.utils import Utils


@pytest.fixture
def filled_utils():
    """Фикстура, которая готовит Utils с данными."""
    utils = Utils()
    apdata = AeroplaneData("Test")
    apdata.add_aeroplane(Aeroplane("TEST1", "Country", 0, 0, 0.0, 0))
    apdata.add_aeroplane(Aeroplane("TEST2", "Country", 0, 0, 10000.0, 0))
    utils.last_request_data = apdata
    return utils


@pytest.fixture
def multi_country_utils():
    """Фикстура с самолетами из разных стран."""
    utils = Utils()
    apdata = AeroplaneData("Iceland")

    apdata.add_aeroplane(Aeroplane("ICE1", "Iceland", 0, 0, 5000, 0))
    apdata.add_aeroplane(Aeroplane("ICE2", "Iceland", 0, 0, 6000, 0))
    apdata.add_aeroplane(Aeroplane("RU1", "Russia", 0, 0, 8000, 0))

    utils.last_request_data = apdata
    return utils


@pytest.fixture
def temp_storage(tmp_path):
    """Фикстура создает хранилище во временной папке."""
    with patch("file.file_json.AEROPLANES_JSON_FILE", tmp_path):
        storage = JSONAeroplaneStorage("test_storage.json")
        yield storage


@pytest.fixture
def file_handler():
    """Создает экземпляр класса для тестов"""
    # Путь может быть любым, так как мы будем его мокать (подменять)
    return JSONAeroplaneStorage("test_file")


@pytest.fixture
def mock_aeroplane_data():
    def _create_mock(planes=None, country="Russia"):
        mock_data = MagicMock()
        mock_data.aeroplanes = planes or ["Самолет TEST"]
        mock_data.request_country = country
        mock_data.date = datetime.now()

        display_text = (
            f"Запрос создан.\n"
            f"Страна: {mock_data.request_country}.\n"
            f"Время создания: {mock_data.date.strftime('%d.%m.%Y %H:%M')}.\n"
            f"Количество самолётов: {len(mock_data.aeroplanes)}.\n"
        )

        mock_data.configure_mock(**{"__str__.return_value": display_text})

        return mock_data

    return _create_mock


@pytest.fixture
def mock_app():
    """Фикстура для создания экземпляра приложения с подмененными зависимостями"""
    app = FlightApp()
    app.worker = MagicMock()
    app.connector = MagicMock()
    app.worker.file = MagicMock()
    app.connector.get_message.return_value = "Mock Message"
    return app
