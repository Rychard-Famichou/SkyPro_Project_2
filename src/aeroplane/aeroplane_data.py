from datetime import datetime
from typing import Any

from aeroplane.aeroplane import Aeroplane


class AeroplaneData:
    """Класс СамолётДата:
    хранит данные о самолётах из конкретного запроса
    """

    def __init__(self, country: str) -> None:
        self.aeroplanes: list[Aeroplane] = []
        self.request_country = country
        self.date = datetime.now()

    def __str__(self) -> str:
        return (
            f"Запрос создан.\n"
            f"Страна: {self.request_country}.\n"
            f"Время создания: {self.date.strftime('%d.%m.%Y %H:%M')}.\n"
            f"Количество самолётов: {len(self.aeroplanes)}.\n"
        )

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        self.aeroplanes.append(aeroplane)

    @classmethod
    def from_api_data(cls, country: str, api_response: dict[str, Any]) -> "AeroplaneData":
        """Создаёт объект класса из API"""
        instance = cls(country)
        states = api_response.get("states") or []

        for p in states:
            if p is not None:
                attrs = [p[1], p[2], p[5], p[6], p[7], p[9]]
                plane = Aeroplane(*attrs)
                instance.add_aeroplane(plane)
        return instance

    @classmethod
    def from_file(cls, data: list[dict[str, Any]]) -> "AeroplaneData":
        """Создаёт объект класса из словаря"""
        instance = cls("From file")
        for p in data:
            plane = Aeroplane(**p)
            instance.add_aeroplane(plane)
        return instance
