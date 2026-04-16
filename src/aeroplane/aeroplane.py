from functools import total_ordering
from typing import Any


@total_ordering
class Aeroplane:
    """Класс Самолёт: хранит данные о самолёте"""

    __slots__ = ("callsign", "country", "longitude", "latitude", "baro_altitude", "velocity")

    def __init__(
        self, callsign: str, country: str, longitude: float, latitude: float, baro_altitude: float, velocity: float
    ) -> None:
        self.callsign = self.__validate_str(callsign).strip()
        self.country = self.__validate_str(country)
        self.longitude = self.__validate_num(longitude)
        self.latitude = self.__validate_num(latitude)
        self.baro_altitude = self.__validate_num(baro_altitude)
        self.velocity = self.__validate_num(velocity)

    def __validate_str(self, value: Any) -> str:
        if not isinstance(value, str):
            return str(value) if value is not None else "Unknown"
        return value

    def __validate_num(self, value: Any) -> float:
        try:
            return float(value) if value is not None else 0.0
        except (ValueError, TypeError):
            return 0.0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude == other.baro_altitude

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.baro_altitude < other.baro_altitude

    def __str__(self) -> str:
        return f"Позывной: '{self.callsign}'. Страна: '{self.country}'. " f"Высота: {self.baro_altitude} метров."
