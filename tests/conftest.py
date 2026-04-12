import pytest

from models.aeroplane import Aeroplane
from models.api_adapter import ApiAdapter


@pytest.fixture(autouse=True)
def setup_order() -> type[Aeroplane]:
    """Фикстура для очистки полного списка самолётов перед каждым тестом"""
    Aeroplane.planes.clear()
    return Aeroplane


@pytest.fixture
def api_two_planes() -> ApiAdapter:
    """Фикстура для создания объекта класса ApiAdapter"""
    api = ApiAdapter()
    api.aeroplanes = {
        "time": 1775990439,
        "states": [
            [
                "4bb1a5",
                "THY47B  ",
                "Turkey",
                1775990130,
                1775990144,
                -24.8112,
                64.1026,
                10972.8,
                False,
                250.00,
                270.23,
                0,
                None,
                10523.22,
                None,
                False,
                0,
            ],
            [
                "4ac9e6",
                "SAS4788 ",
                "Sweden",
                1775990256,
                1775990256,
                -22.6095,
                63.9891,
                10000.0,
                True,
                50.00,
                180,
                None,
                None,
                None,
                None,
                False,
                0,
            ],
        ],
    }
    return api


@pytest.fixture
def api_two_planes_first() -> ApiAdapter:
    """Фикстура для создания объекта класса ApiAdapter"""
    api = ApiAdapter()
    api.aeroplanes = {
        "time": 1775990439,
        "states": [
            [
                "4bb1a5",
                "THY47B  ",
                "Turkey",
                1775990130,
                1775990144,
                -24.8112,
                64.1026,
                10972.8,
                False,
                250.00,
                270.23,
                0,
                None,
                10523.22,
                None,
                False,
                0,
            ],
            [
                "4ac9e6",
                "SAS4788 ",
                "Sweden",
                1775990256,
                1775990256,
                -22.6095,
                63.9891,
                10000.0,
                True,
                50.00,
                180,
                None,
                None,
                None,
                None,
                False,
                0,
            ],
        ],
    }
    return api


@pytest.fixture
def api_two_planes_second() -> ApiAdapter:
    """Фикстура для создания объекта класса ApiAdapter"""
    api = ApiAdapter()
    api.aeroplanes = {
        "time": 1775990439,
        "states": [
            [
                "4bb1a5",
                "THY47B  ",
                "Turkey",
                1775990130,
                1775990144,
                -24.8112,
                64.1026,
                10000.0,
                False,
                50.00,
                270.23,
                0,
                None,
                10523.22,
                None,
                False,
                0,
            ],
            [
                "4ac9e6",
                "SAS4788 ",
                "Sweden",
                1775990256,
                1775990256,
                -22.6095,
                63.9891,
                10972.8,
                True,
                250.00,
                180,
                None,
                None,
                None,
                None,
                False,
                0,
            ],
        ],
    }
    return api


@pytest.fixture
def api_two_planes_equal() -> ApiAdapter:
    """Фикстура для создания объекта класса ApiAdapter"""
    api = ApiAdapter()
    api.aeroplanes = {
        "time": 1775990439,
        "states": [
            [
                "4bb1a5",
                "THY47B  ",
                "Turkey",
                1775990130,
                1775990144,
                -24.8112,
                64.1026,
                10000.0,
                False,
                250.00,
                270.23,
                0,
                None,
                10523.22,
                None,
                False,
                0,
            ],
            [
                "4ac9e6",
                "SAS4788 ",
                "Sweden",
                1775990256,
                1775990256,
                -22.6095,
                63.9891,
                10000.0,
                True,
                250.00,
                180,
                None,
                None,
                None,
                None,
                False,
                0,
            ],
        ],
    }
    return api


@pytest.fixture
def api_adapter():
    return ApiAdapter()
