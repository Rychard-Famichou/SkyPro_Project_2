from abc import ABC, abstractmethod

from aeroplane.aeroplane import Aeroplane
from aeroplane.aeroplane_data import AeroplaneData


class AeroplaneStorage(ABC):

    @abstractmethod
    def save_one(self, plane: Aeroplane) -> None:
        """Добавить один самолет в существующее хранилище"""
        pass

    @abstractmethod
    def save_all(self, data: AeroplaneData) -> None:
        """Сохранить все самолеты из объекта AeroplaneData в файл/БД"""
        pass

    @abstractmethod
    def get_by_callsign(self, callsign: str) -> Aeroplane | None:
        """Получить данные о самолете по его позывному"""
        pass

    @abstractmethod
    def get_all(self) -> AeroplaneData:
        """Метод получения всех данных из файла"""
        pass

    @abstractmethod
    def delete_by_callsign(self, callsign: str) -> None:
        """Удалить информацию о самолете из хранилища"""
        pass

    @abstractmethod
    def delete_all(self) -> None:
        """Очистить всё хранилище"""
        pass
