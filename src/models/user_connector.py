from models.message_key import MessageKey


class UserConnector:
    MESSAGES: dict[MessageKey, str] = {
        MessageKey.GREETINGS: "Добро пожаловать в программу о самолётах (Beta)",
        MessageKey.OPERATIONS_LIST: "Список доступных операций:",
        MessageKey.GET_DATA: "Получить новые данные",
        MessageKey.WORK_WITH_DATA: "Работа с данными",
        MessageKey.WORK_WITH_FILE: "Работа с файлом",
        MessageKey.TOP_N: "Топ N самолетов по высоте",
        MessageKey.GET_N: "Введите N: ",
        MessageKey.FILTER_COUNTRY: "Фильтр по стране регистрации",
        MessageKey.OPERATION_NUMBER: "Введите номер операции: ",
        MessageKey.NOT_DATA: "Нет данных",
        MessageKey.COUNTRY: "Введите страну: ",
        MessageKey.CALLSIGN: "Введите позывной: ",
        MessageKey.FILENAME: "Введите название файла: ",
        MessageKey.DATA_RECEIVED: "Данные получены",
        MessageKey.DATA_RECEIVED_NOT: "Данные не получены",
        MessageKey.FILE_JSON: "JSON менеджер",
        MessageKey.FILE_SQL: "SQL менеджер",
        MessageKey.FILENAME_STD: "Использовать стандартное имя файла",
        MessageKey.FILENAME_USER: "Задать своё имя файла",
        MessageKey.SAVE_PLANE: "Сохранить данные о самолёте",
        MessageKey.SAVE_ALL: "Сохранить данные о всех самолётах",
        MessageKey.GET_PLANE: "Получить данные о самолёте",
        MessageKey.GET_PLANE_ALL: "Получить данные о всех самолётах",
        MessageKey.DELETE_PLANE: "Удалить данные о самолёте",
        MessageKey.DELETE_PLANE_ALL: "Удалить данные о всех самолётах",
        MessageKey.PROGRAM_END: "Конец программы",
        MessageKey.MENU_MAIN: "Главное меню",
        MessageKey.MENU_DATA: "Меню данных",
        MessageKey.MENU_DATA_OPERATIONS: "Меню операций с данными",
        MessageKey.MENU_FILE_TYPE: "Меню файл-менеджеров",
        MessageKey.MENU_FILE_OPERATIONS: "Меню операций с файлом",
        MessageKey.MENU_FILE_SAVE: "Меню сохранения",
        MessageKey.MENU_FILE_GET: "Меню извлечения",
        MessageKey.MENU_FILE_DEL: "Меню удаления",
        MessageKey.MENU_FILENAME: "Меню названия файла",
    }

    def get_message(self, key: MessageKey, *args: str) -> str:
        message = self.MESSAGES.get(key, "Сообщение не найдено")
        return message.format(*args) if args else message
