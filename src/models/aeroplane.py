class Aeroplane:
    planes: list["Aeroplane"] = []

    def __init__(
        self, callsign: str, country: str, longitude: float, latitude: float, baro_altitude: float, velocity: float
    ) -> None:
        """Создаёт объект класса и дополняет в список всех объектов класса"""
        self.callsign = callsign
        self.country = country
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude = baro_altitude
        self.velocity = velocity
        self.planes.append(self)

    def get_baro_altitude_defference(self, other: "Aeroplane") -> str:
        if self.baro_altitude > other.baro_altitude:
            return f"{self.callsign} выше на {round(self.baro_altitude - other.baro_altitude, 1)}"
        elif self.baro_altitude < other.baro_altitude:
            return f"{other.callsign} выше на {round(other.baro_altitude - self.baro_altitude, 1)}"
        else:
            return f"{self.callsign} и {other.callsign} летят на одной высоте"

    def get_velocity_difference(self, other: "Aeroplane") -> str:
        if self.velocity > other.velocity:
            return f"{self.callsign} быстрее на {round(self.velocity - other.velocity, 1)}"
        elif self.velocity < other.velocity:
            return f"{other.callsign} быстрее на {round(other.velocity - self.velocity, 1)}"
        else:
            return f"{self.callsign} и {other.callsign} летят с одинаковой скоростью"
