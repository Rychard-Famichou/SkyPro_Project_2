from abc import ABC, abstractmethod
from typing import Any

import requests


class BaseApi(ABC):
    def __init__(self, url: str, headers: dict[str, str] | None = None) -> None:
        if headers is None:
            headers = {}
        self.__base_url = url
        self.__headers = headers

    def __connect(self) -> bool:
        """Приватный метод для проверки статус-кода (по ТЗ)"""
        response = requests.get(self.__base_url, headers=self.__headers, timeout=10)
        if response.status_code == 200:
            return True
        raise ConnectionError(f"Ошибка доступа к {self.__base_url}")

    def _check_connection(self) -> bool:
        """Вспомогательный метод для вызова приватного __connect"""
        return self.__connect()

    @abstractmethod
    def get_data(self, arg: str) -> Any:
        pass
