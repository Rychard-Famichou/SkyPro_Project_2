from unittest.mock import MagicMock, patch

import pytest
import vcr

from models.app import FlightApp

my_vcr = vcr.VCR(
    cassette_library_dir="tests/cassettes",
    filter_headers=[("User-Agent", "REDACTED")],
    record_mode="once",
)


@pytest.fixture
def app():
    return FlightApp()


@my_vcr.use_cassette("integration_flow.yaml")
@patch("builtins.input")
@patch("builtins.print")
def test_full_flow_fetch_data(mock_print, mock_input, app):
    """
    Интеграционный тест:
    1. Главное меню -> 1 (Работа с данными)
    2. action_fetch_data -> ввод "Poland"
    3. Выход (0 -> 0)
    """

    # Имитируем шаги пользователя:
    # "1" - войти в меню данных
    # "Poland" - ввод страны для API
    # "0" - назад в главное меню
    # "0" - выход из программы
    mock_input.side_effect = ["1", "Poland", "0", "0"]

    # Мокаем коннектор, чтобы не зависеть от локализации строк,
    # либо оставляем как есть, если UserConnector работает локально.
    app.connector.get_message = MagicMock(side_effect=lambda x: str(x))

    # ЗАПУСК
    app.run()

    # ПРОВЕРКИ
    # 1. Проверяем, что данные действительно загрузились в worker
    assert app.worker.last_request_data is not None

    # 2. Проверяем, что в консоль вывелось сообщение о получении данных
    # (Мы подменили get_message, поэтому ищем строковое представление ключа)
    mock_print.assert_any_call("MessageKey.DATA_RECEIVED")

    # 3. Проверяем, что программа завершилась корректно
    mock_print.assert_any_call("MessageKey.PROGRAM_END")
