from typing import Callable, Optional, TypeAlias, Union

from models.message_key import MessageKey
from models.user_connector import UserConnector
from models.utils import Utils

MenuAction: TypeAlias = Optional[Callable[[], "MenuAction"]]
MenuConfig: TypeAlias = dict[str, tuple[Union[MessageKey, str], MenuAction]]


class FlightApp:
    def __init__(self) -> None:
        self.worker = Utils()
        self.connector = UserConnector()

    def run(self) -> None:
        """Запуск программы"""
        print()
        print(self.connector.get_message(MessageKey.GREETINGS))
        current_step: MenuAction = self.menu_main
        while current_step:
            current_step = current_step()
        print()
        print(self.connector.get_message(MessageKey.PROGRAM_END))

    def _show_and_get_choice(self, menu_config: MenuConfig) -> MenuAction:
        """
        Автоматически выводит меню и проверяет ввод.
        """
        print(self.connector.get_message(MessageKey.OPERATIONS_LIST))

        for key, (msg_key, _) in menu_config.items():
            label = self.connector.get_message(msg_key) if isinstance(msg_key, MessageKey) else msg_key
            print(f"{key}. {label}")

        while True:
            choice = input(self.connector.get_message(MessageKey.OPERATION_NUMBER)).strip()
            if choice in menu_config:
                return menu_config[choice][1]
            print("Ошибка: выберите число из списка выше.")

    def menu_main(self) -> MenuAction:
        """Меню: главное"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_MAIN)} ---")
        config: MenuConfig = {
            "1": (MessageKey.WORK_WITH_DATA, self.menu_data_source),
            "2": (MessageKey.WORK_WITH_FILE, self.menu_file_type),
            "0": ("Выход", None),
        }
        return self._show_and_get_choice(config)

    def menu_data_source(self) -> MenuAction:
        """Меню: данные"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_DATA)} ---")
        if not self.worker.last_request_data:
            return self.action_fetch_data()

        config: MenuConfig = {
            "1": (MessageKey.GET_DATA, self.action_fetch_data),
            "2": (MessageKey.WORK_WITH_DATA, self.menu_data_operations),
            "0": ("Назад", self.menu_main),
        }
        return self._show_and_get_choice(config)

    def action_fetch_data(self) -> MenuAction:
        """Метод: обновить текущие данные. Ветка: данные"""
        if not self.worker.last_request_data:
            print(self.connector.get_message(MessageKey.NOT_DATA))
        country = input(self.connector.get_message(MessageKey.COUNTRY))
        self.worker.last_request_data = self.worker.fetch_flight_info(country)

        if self.worker.last_request_data:
            print(self.connector.get_message(MessageKey.DATA_RECEIVED))
            print(self.worker.last_request_data)
            return self.menu_data_source

        print(self.connector.get_message(MessageKey.DATA_RECEIVED_NOT))
        return self.menu_main

    def menu_data_operations(self) -> MenuAction:
        """Меню: операции с данными"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_DATA_OPERATIONS)} ---")
        config: MenuConfig = {
            "1": (MessageKey.TOP_N, self.action_get_top_n),
            "2": (MessageKey.FILTER_COUNTRY, self.action_get_planes_from_country),
            "0": ("Назад", self.menu_data_source),
        }
        return self._show_and_get_choice(config)

    def action_get_top_n(self) -> MenuAction:
        """Метод: топ N"""
        n_str = input(self.connector.get_message(MessageKey.GET_N))
        try:
            n = int(n_str)
            if n <= 0:
                raise ValueError("Число должно быть положительным")
            print(self.worker.get_top_n(n))
        except ValueError:
            print("Ошибка: Пожалуйста, введите целое положительное число.")
        return self.menu_data_operations

    def action_get_planes_from_country(self) -> MenuAction:
        """Метод: страна регистрации"""
        country = input(self.connector.get_message(MessageKey.COUNTRY))
        self.worker.get_planes_from_country(country)
        return self.menu_data_operations

    def menu_file_operations(self) -> MenuAction:
        """Меню: операции с файлом"""
        if not self.worker.file:
            return self.menu_file_type

        print(f"\n--- {self.connector.get_message(MessageKey.MENU_FILE_OPERATIONS)} ---")
        config: MenuConfig = {
            "1": (MessageKey.SAVE_PLANE, self.menu_file_save_plane),
            "2": (MessageKey.GET_PLANE, self.menu_file_get_plane),
            "3": (MessageKey.DELETE_PLANE, self.menu_file_delete_plane),
            "0": ("Назад", self.menu_file_type),
        }
        return self._show_and_get_choice(config)

    def menu_file_save_plane(self) -> MenuAction:
        """Меню: сохранить в файл"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_FILE_SAVE)} ---")
        if not self.worker.last_request_data:
            return self.action_file_fetch_data
        config: MenuConfig = {
            "1": (MessageKey.SAVE_PLANE, self.action_file_save),
            "2": (MessageKey.SAVE_ALL, self.action_file_save_all),
            "0": ("Назад", self.menu_file_operations),
        }
        return self._show_and_get_choice(config)

    def menu_file_get_plane(self) -> MenuAction:
        """Меню: извлечь из файла"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_FILE_GET)} ---")
        config: MenuConfig = {
            "1": (MessageKey.GET_PLANE, self.action_file_get_plane),
            "2": (MessageKey.GET_PLANE_ALL, self.action_file_get_plane_all),
            "0": ("Назад", self.menu_file_operations),
        }
        return self._show_and_get_choice(config)

    def menu_file_delete_plane(self) -> MenuAction:
        """Меню: удалить из файла"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_FILE_DEL)} ---")
        config: MenuConfig = {
            "1": (MessageKey.DELETE_PLANE, self.action_file_delete_plane),
            "2": (MessageKey.DELETE_PLANE_ALL, self.action_file_delete_plane_all),
            "0": ("Назад", self.menu_file_operations),
        }
        return self._show_and_get_choice(config)

    def action_file_fetch_data(self) -> MenuAction:
        """Метод: обновить текущие данные. Ветка: файл"""
        if not self.worker.last_request_data:
            print(self.connector.get_message(MessageKey.NOT_DATA))
        country = input(self.connector.get_message(MessageKey.COUNTRY))
        self.worker.last_request_data = self.worker.fetch_flight_info(country)

        if self.worker.last_request_data:
            print(self.connector.get_message(MessageKey.DATA_RECEIVED))
            print(self.worker.last_request_data)
            return self.menu_file_save_plane

        print(self.connector.get_message(MessageKey.DATA_RECEIVED_NOT))
        return self.menu_main

    def menu_file_type(self) -> MenuAction:
        """Меню: выбор менеджера"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_FILE_TYPE)} ---")
        config: MenuConfig = {
            "1": (MessageKey.FILE_JSON, self.menu_filename),
            "2": (MessageKey.FILE_SQL, self.action_file_sql),
            "0": ("Назад", self.menu_main),
        }
        return self._show_and_get_choice(config)

    def menu_filename(self) -> MenuAction:
        """Меню: выбор имени файла"""
        print(f"\n--- {self.connector.get_message(MessageKey.MENU_FILENAME)} ---")
        config: MenuConfig = {
            "1": (MessageKey.FILENAME_STD, self.action_file_json),
            "2": (MessageKey.FILENAME_USER, self.action_show_file),
        }
        return self._show_and_get_choice(config)

    def action_show_file(self) -> MenuAction:
        """Метод: вывести строку всех файлов в хранилище"""
        files_info = self.worker.get_available_filenames()
        print(files_info)
        return self.action_file_json_filename

    def action_file_json_filename(self) -> MenuAction:
        """Метод: JSON менеджер с названием - актив"""
        filename = input(self.connector.get_message(MessageKey.FILENAME))
        if not filename:
            print("Ошибка: имя файла не может быть пустым.")
            return self.menu_filename
        self.worker.get_file_json_filename(filename)
        print(f"Активный файл: {filename}")
        return self.menu_file_operations

    def action_file_json(self) -> MenuAction:
        """Метод: JSON менеджер - актив"""
        self.worker.get_file("JSON")
        return self.menu_file_operations

    def action_file_sql(self) -> MenuAction:
        """Метод: SQL менеджер - актив. В разработке."""
        print("SQL менеджер находится в разработке.\nПожалуйста, выберите JSON менеджер.")
        return self.menu_file_type

    def action_file_save(self) -> MenuAction:
        """Метод: сохранить самолёт в файл"""
        assert self.worker.file is not None, "Storage must be initialized"
        assert self.worker.last_request_plane is not None, "Aeroplane must be initialized"
        callsing = input(self.connector.get_message(MessageKey.CALLSIGN))
        self.worker.get_plane_by_callsign(callsing)
        self.worker.file.save_one(self.worker.last_request_plane)
        self.worker.last_request_plane = None
        return self.menu_file_operations

    def action_file_save_all(self) -> MenuAction:
        """Метод: сохранить все самолёты в файл"""
        assert self.worker.file is not None, "Storage must be initialized"
        assert self.worker.last_request_data is not None, "AeroplaneData must be initialized"
        self.worker.file.save_all(self.worker.last_request_data)
        return self.menu_file_operations

    def action_file_get_plane(self) -> MenuAction:
        """Метод: прочитать самолёт из файла"""
        assert self.worker.file is not None, "Storage must be initialized"
        callsing = input(self.connector.get_message(MessageKey.CALLSIGN))
        self.worker.last_request_plane = self.worker.file.get_by_callsign(callsing)
        print(self.worker.last_request_plane)
        return self.menu_file_operations

    def action_file_get_plane_all(self) -> MenuAction:
        """Метод: прочитать все самолёты из файла"""
        assert self.worker.file is not None, "Storage must be initialized"
        try:
            data = self.worker.file.get_all()
            if not data:
                print("Файл пуст или данные не найдены.")
                return self.menu_file_operations
            self.worker.last_request_data = data
            print("\nДанные успешно загружены из файла:")
            print(data)
            for i, plane in enumerate(data.aeroplanes, 1):
                print(f"{i}. {plane}")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return self.menu_file_operations
        return self.menu_file_operations

    def action_file_delete_plane(self) -> MenuAction:
        """Метод: удалить самолёт из файла"""
        assert self.worker.file is not None, "Storage must be initialized"
        callsing = input(self.connector.get_message(MessageKey.CALLSIGN))
        self.worker.file.delete_by_callsign(callsing)
        return self.menu_file_operations

    def action_file_delete_plane_all(self) -> MenuAction:
        """Метод: удалить все самолёты из файла"""
        assert self.worker.file is not None, "Storage must be initialized"
        self.worker.file.delete_all()
        print("Все данные из файла успешно удалены.")
        return self.menu_file_operations
