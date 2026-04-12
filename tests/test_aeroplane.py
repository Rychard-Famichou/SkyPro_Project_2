from models.aeroplane import Aeroplane
from models.aeroplane_api import AeroplaneApi
from models.api_adapter import ApiAdapter


def test_get_baro_altitude_defference_1(api_two_planes_first: ApiAdapter) -> None:
    """Тест разницы высоты: первый самолёт"""
    AeroplaneApi(api_two_planes_first)
    first_plane = Aeroplane.planes[0]
    second_plane = Aeroplane.planes[1]
    defference = first_plane.get_baro_altitude_defference(second_plane)
    assert defference == "THY47B   выше на 972.8"


def test_get_velocity_difference_1(api_two_planes_first: ApiAdapter) -> None:
    """Тест разницы скорости: первый самолёт"""
    AeroplaneApi(api_two_planes_first)
    first_plane = Aeroplane.planes[0]
    second_plane = Aeroplane.planes[1]
    defference = first_plane.get_velocity_difference(second_plane)
    assert defference == "THY47B   быстрее на 200.0"


def test_get_baro_altitude_defference_2(api_two_planes_second: ApiAdapter) -> None:
    """Тест разницы высоты: второй самолёт"""
    AeroplaneApi(api_two_planes_second)
    first_plane = Aeroplane.planes[0]
    second_plane = Aeroplane.planes[1]
    defference = first_plane.get_baro_altitude_defference(second_plane)
    assert defference == "SAS4788  выше на 972.8"


def test_get_velocity_difference_2(api_two_planes_second: ApiAdapter) -> None:
    """Тест разницы скорости: второй самолёт"""
    AeroplaneApi(api_two_planes_second)
    first_plane = Aeroplane.planes[0]
    second_plane = Aeroplane.planes[1]
    defference = first_plane.get_velocity_difference(second_plane)
    assert defference == "SAS4788  быстрее на 200.0"


def test_get_baro_altitude_defference_3(api_two_planes_equal: ApiAdapter) -> None:
    """Тест разницы высоты: второй самолёт"""
    AeroplaneApi(api_two_planes_equal)
    first_plane = Aeroplane.planes[0]
    second_plane = Aeroplane.planes[1]
    defference = first_plane.get_baro_altitude_defference(second_plane)
    assert defference == "THY47B   и SAS4788  летят на одной высоте"


def test_get_velocity_difference_3(api_two_planes_equal: ApiAdapter) -> None:
    """Тест разницы скорости: второй самолёт"""
    AeroplaneApi(api_two_planes_equal)
    first_plane = Aeroplane.planes[0]
    second_plane = Aeroplane.planes[1]
    defference = first_plane.get_velocity_difference(second_plane)
    assert defference == "THY47B   и SAS4788  летят с одинаковой скоростью"
