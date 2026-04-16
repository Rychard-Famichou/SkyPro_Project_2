from typing import Any

import requests

from api.base_api import BaseApi


class OpenSkyAPI(BaseApi):
    def __init__(self) -> None:
        self.__url = "https://opensky-network.org/api/states/all?"
        super().__init__(self.__url)
        self.__aeroplanes: dict[str, Any] = {}

    def get_data(self, geo_coords: str) -> dict[str, Any]:
        """Метод подключения вызывается перед отправкой запроса"""
        if self._check_connection():
            coords = [float(x) for x in geo_coords.split()]
            params = {"lamin": coords[0], "lamax": coords[1], "lomin": coords[2], "lomax": coords[3]}
            response = requests.get(self.__url, params=params)
            self.__aeroplanes = response.json()
            return self.__aeroplanes
        return {"time": 0, "states": []}
