from typing import Any, cast

from models.aeroplane import Aeroplane
from models.api_adapter import ApiAdapter


class AeroplaneApi:
    """
    Класс для создания объектов класса Самолёт из ответа API
    """

    def __init__(self, api: ApiAdapter) -> None:
        """Создаёт объект класса Самолёт для каждого из API"""
        dict_aeroplanes = self.get_dict_aeroplanes(api)
        list_aeroplanes = self.get_list_aeroplanes(dict_aeroplanes)
        aeroplanes = self.get_all_attributes(list_aeroplanes)
        for p in aeroplanes:
            Aeroplane(*p)

    @staticmethod
    def get_all_attributes(aeroplanes: list[list[Any]]) -> list[list[Any]]:
        """Возвращает список самолётов с нужными полями для каждого"""
        return [[p[1], p[2], p[5], p[6], p[7], p[9]] for p in aeroplanes if p is not None]

    @staticmethod
    def get_list_aeroplanes(aeroplanes: dict[str, Any]) -> list[list[Any]]:
        """Возвращает список самолётов"""
        return cast(list[list[Any]], aeroplanes["states"])

    @staticmethod
    def get_dict_aeroplanes(api: ApiAdapter) -> dict[str, Any]:
        """Возвращает словарь ответа API"""
        return api.aeroplanes
