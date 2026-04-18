import json
from typing import Any

from aeroplane.aeroplane import Aeroplane
from aeroplane.aeroplane_data import AeroplaneData
from config import AEROPLANES_JSON_FILE
from file.base_file import AeroplaneStorage


class JSONAeroplaneStorage(AeroplaneStorage):
    """Класс для работы с файлами типа JSON"""

    def __init__(self, filename: str | None = None) -> None:
        """Может принимать название файла"""
        if filename is None:
            self.__filename = "aeroplanes.json"
        else:
            if not filename.endswith(".json"):
                filename += ".json"
            self.__filename = filename

        self.__file_path = AEROPLANES_JSON_FILE / self.filename
        self.__file_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def filename(self) -> str:
        """Метод чтения приватного атрибута"""
        return self.__filename

    def _read_file(self) -> list[dict[str, Any]]:
        """Метод чтения файла"""
        if not self.__file_path.exists():
            return []
        try:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, FileNotFoundError, PermissionError, UnicodeDecodeError):
            pass
        return []

    def _write_to_file(self, data: list[dict[str, Any]]) -> None:
        """Метод для записи"""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def save_one(self, plane: Aeroplane) -> None:
        """Метод записи одного самолёта"""
        data = self._read_file()

        if any(p["callsign"] == plane.callsign for p in data):
            print(f"Самолет {plane.callsign} уже существует. Пропуск.")
            return

        plane_dict = {attr: getattr(plane, attr) for attr in plane.__slots__}
        data.append(plane_dict)
        self._write_to_file(data)

    def save_all(self, data_obj: AeroplaneData) -> None:
        """Метод записи всех самолётов"""
        existing_data = self._read_file()
        existing_callsigns = {p["callsign"] for p in existing_data}

        for plane in data_obj.aeroplanes:
            if plane.callsign not in existing_callsigns:
                plane_dict = {attr: getattr(plane, attr) for attr in plane.__slots__}
                existing_data.append(plane_dict)

        self._write_to_file(existing_data)

    def get_by_callsign(self, callsign: str) -> Aeroplane | None:
        """Метод получения записи о самолёте"""
        data = self._read_file()
        plane_data = next((p for p in data if p["callsign"] == callsign), None)
        if plane_data:
            return Aeroplane(**plane_data)
        return None

    def get_all(self) -> AeroplaneData:
        """Метод получения записи о всех самолётах"""
        data = self._read_file()
        planes = AeroplaneData.from_file(data)
        return planes

    def delete_by_callsign(self, callsign: str) -> None:
        """Метод удаления записи о самолёте"""
        data = self._read_file()
        new_data = [p for p in data if p["callsign"] != callsign]

        if len(data) == len(new_data):
            print(f"Самолет {callsign} не найден.")
        else:
            self._write_to_file(new_data)
            print(f"Самолет {callsign} удален.")

    def delete_all(self) -> None:
        """Метод удаления всех записей (очистка файла)"""
        self._write_to_file([])

    @staticmethod
    def get_all_saved_files() -> list[str]:
        """Возвращает список всех json-файлов в директории хранилища"""
        if not AEROPLANES_JSON_FILE.exists():
            return []

        return [f.stem for f in AEROPLANES_JSON_FILE.glob("*.json")]
