from aeroplane.aeroplane import Aeroplane
from aeroplane.aeroplane_data import AeroplaneData
from api.api_nominatim import NominatimAPI
from api.api_opensky import OpenSkyAPI
from api.base_api import BaseApi
from file.base_file import AeroplaneStorage
from file.file_json import JSONAeroplaneStorage


class Utils:
    def __init__(self) -> None:
        self.last_request_plane: Aeroplane | None = None
        self.last_request_data: AeroplaneData | None = None
        self._geo_service: BaseApi = NominatimAPI()
        self._flight_service: BaseApi = OpenSkyAPI()
        self.file: AeroplaneStorage | None = None

    def fetch_flight_info(self, country_name: str) -> AeroplaneData:
        """Запрашивает данные о самолетах и сохраняет их в объекте."""
        coords = self._geo_service.get_data(country_name)
        flights = self._flight_service.get_data(coords)

        self.last_request_data = AeroplaneData.from_api_data(country_name, flights)
        return self.last_request_data

    def get_top_n(self, n: int) -> str:
        """Получить топ N самолетов по высоте полета из последнего запроса."""
        if not self.last_request_data or not self.last_request_data.aeroplanes:
            return "Нет данных для отображения."

        sorted_planes = sorted(self.last_request_data.aeroplanes, reverse=True)

        top_list = sorted_planes[:n]
        header = f"Топ {len(top_list)} самолетов по высоте над страной '{self.last_request_data.request_country}':"
        lines = [f"{i + 1}. {p}" for i, p in enumerate(top_list)]

        return "\n".join([header] + lines)

    def get_planes_from_country(self, origin_country: str) -> str:
        """Получить список самолетов по стране их регистрации."""
        if not self.last_request_data or not self.last_request_data.aeroplanes:
            return "Нет данных для отображения."

        found = [p for p in self.last_request_data.aeroplanes if p.country.lower() == origin_country.lower()]

        if not found:
            return f"В небе над '{self.last_request_data.request_country}' нет самолетов из '{origin_country}'."

        header = f"Самолеты из '{origin_country}' в небе над '{self.last_request_data.request_country}':"
        return "\n".join([header] + [str(p) for p in found])

    def get_plane_by_callsign(self, callsign: str) -> None:
        """Метод: установить в атрибут самолёт"""
        assert self.last_request_data is not None, "AeroplaneData must be initialized"
        for p in self.last_request_data.aeroplanes:
            if p.callsign == callsign:
                self.last_request_plane = p

    def get_file(self, file: str) -> None:
        """Метод активирует тот обработчик файлов, который выбрал пользователь"""
        if file == "JSON":
            self.file = JSONAeroplaneStorage()

    def get_file_json_filename(self, filename: str) -> None:
        """
        Метод активирует тот обработчик файлов, который выбрал пользователь.
        Использует название файла, заданное пользователем
        """
        self.file = JSONAeroplaneStorage(filename)

    @staticmethod
    def get_available_filenames() -> str:
        """Получает список имен файлов и форматирует их в строку"""
        files = JSONAeroplaneStorage.get_all_saved_files()
        if not files:
            return "Хранилище пока пусто (нет созданных файлов)."

        header = "Доступные файлы в базе:"
        file_list = [f"- {name}" for name in files]
        return "\n".join([header] + file_list)
