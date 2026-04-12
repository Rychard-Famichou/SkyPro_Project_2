from models.aeroplane import Aeroplane
from models.aeroplane_api import AeroplaneApi


def test_init(api_two_planes):
    """Тест init"""
    AeroplaneApi(api_two_planes)

    assert len(Aeroplane.planes) == 2
