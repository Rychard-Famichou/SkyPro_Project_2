import requests

from api.base_api import BaseApi


class NominatimAPI(BaseApi):
    def __init__(self) -> None:
        self.__url = "https://nominatim.openstreetmap.org/search"
        self.__headers = {
            "User-Agent": "SkyPro_Project_App/2.0 (contact: rychard.famichou@gmail.com)",
            "Accept": "application/json",
        }
        super().__init__(self.__url, headers=self.__headers)

    def get_data(self, country: str) -> str:
        """Метод подключения вызывается перед отправкой запроса"""
        if self._check_connection():
            params: dict[str, str | int] = {"country": country, "format": "json", "limit": 1}
            response = requests.get(self.__url, params=params, headers=self.__headers)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data:
                        bbox = data[0].get("boundingbox")
                        return " ".join(bbox) if bbox else ""
                except requests.exceptions.JSONDecodeError:
                    print("Ошибка декодирования JSON. Ответ сервера:", response.text)
            else:
                print(f"Ошибка запроса: {response.status_code}")
        return ""
