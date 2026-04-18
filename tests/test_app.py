from unittest.mock import MagicMock, patch


@patch("builtins.input", side_effect=["0"])
@patch("builtins.print")
def test_main_menu_exit(mock_print, mock_input, mock_app):
    """
    Порядок аргументов:
    1. mock_print (от последнего декоратора @patch)
    2. mock_input (от первого декоратора @patch)
    3. mock_app (фикстура из pytest)
    """
    mock_app.connector.get_message.side_effect = lambda key: "Конец программы" if "END" in str(key) else "Mocked Text"
    mock_app.run()
    mock_print.assert_any_call("Конец программы")


@patch("builtins.input", side_effect=["9", "abc", "0"])
@patch("builtins.print")
def test_invalid_input_retry(mock_print, mock_input, mock_app):
    """Тест: ввод неверных команд, затем корректный выход"""
    mock_app.connector.get_message.side_effect = lambda key: str(key)
    mock_app.run()
    error_msg = "Ошибка: выберите число из списка выше."
    error_calls = [call for call in mock_print.mock_calls if error_msg in str(call)]
    assert len(error_calls) >= 2
    assert mock_input.call_count == 3
    mock_print.assert_any_call("MessageKey.PROGRAM_END")


def test_show_and_get_choice_logic(mock_app):
    config = {"1": ("Test", "Result")}
    mock_app.connector.get_message.side_effect = lambda key: "Prompt"

    with patch("builtins.input", side_effect=["9", "1"]):
        result = mock_app._show_and_get_choice(config)
        assert result == "Result"


def test_action_get_top_n_invalid_input(mock_app, monkeypatch, capsys):
    mock_app.connector.get_message.return_value = "Введите N: "
    monkeypatch.setattr("builtins.input", lambda _: "не число")
    mock_app.action_get_top_n()
    captured = capsys.readouterr()
    assert "Ошибка: Пожалуйста, введите целое положительное число." in captured.out


def test_action_get_top_n_negative_number(mock_app, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "-5")
    mock_app.action_get_top_n()
    captured = capsys.readouterr()
    assert "Ошибка: Пожалуйста, введите целое положительное число." in captured.out


class TestFileAction:

    def test_action_show_file(self, mock_app, capsys):
        """Тест вывода файлов"""
        mock_app.worker.get_available_filenames.return_value = "Файлы: 1.json, 2.json"
        next_step = mock_app.action_show_file()
        captured = capsys.readouterr()
        assert "Файлы: 1.json, 2.json" in captured.out
        assert next_step == mock_app.action_file_json_filename

    def test_action_file_json_filename_empty(self, mock_app, capsys):
        """Тест пустое поле ввода filename"""
        with patch("builtins.input", return_value=""):
            next_step = mock_app.action_file_json_filename()
            captured = capsys.readouterr()
            assert "Ошибка: имя файла не может быть пустым." in captured.out
            assert next_step == mock_app.menu_filename

    def test_action_file_save_all_no_data(self, mock_app):
        """Проверка падения, если данные для сохранения отсутствуют"""
        mock_app.worker.last_request_data = None
        import pytest

        with pytest.raises(AssertionError, match="AeroplaneData must be initialized"):
            mock_app.action_file_save_all()

    def test_action_file_save(self, mock_app, monkeypatch):
        """Тест сохранить самолёт"""
        monkeypatch.setattr("builtins.input", lambda _: "AFL123")
        next_step = mock_app.action_file_save()
        mock_app.worker.get_plane_by_callsign.assert_called_with("AFL123")
        mock_app.worker.file.save_one.assert_called()
        assert mock_app.worker.last_request_plane is None
        assert next_step == mock_app.menu_file_operations

    def test_action_file_get_plane_all(self, mock_app, mock_aeroplane_data, capsys):
        """Тест получить все самолёты"""
        mock_data = mock_aeroplane_data(planes=["Самолет TEST"])
        mock_app.worker.file.get_all.return_value = mock_data
        mock_app.action_file_get_plane_all()
        captured = capsys.readouterr()
        assert "Данные успешно загружены из файла" in captured.out
        assert "Запрос создан.\n" in captured.out
        assert "1. Самолет TEST" in captured.out

    def test_action_file_get_plane_all_error(self, mock_app, capsys):
        """Тест получить все самолёты. Ошибка"""
        mock_app.worker.file.get_all.side_effect = Exception("Disk error")
        next_step = mock_app.action_file_get_plane_all()
        captured = capsys.readouterr()
        assert "Ошибка" in captured.out
        assert next_step == mock_app.menu_file_operations

    def test_action_file_delete_plane_all(self, mock_app, capsys):
        """Тест удалить все самолёты"""
        next_step = mock_app.action_file_delete_plane_all()
        mock_app.worker.file.delete_all.assert_called_once()
        captured = capsys.readouterr()
        assert "Все данные из файла успешно удалены." in captured.out
        assert next_step == mock_app.menu_file_operations

    def test_action_file_get_plane_not_found(self, mock_app, capsys, monkeypatch):
        """Тест получить самолёт. Не найден"""
        monkeypatch.setattr("builtins.input", lambda _: "GHOST999")
        mock_app.worker.file.get_by_callsign.return_value = None
        next_step = mock_app.action_file_get_plane()
        captured = capsys.readouterr()
        assert "None" in captured.out
        assert next_step == mock_app.menu_file_operations

    def test_action_file_get_plane_all_empty_list(self, mock_app, mock_aeroplane_data, capsys):
        """Тест получить все самолёты. Пустой список самолётов"""
        mock_data = mock_aeroplane_data()
        mock_data.aeroplanes = []
        new_display_text = (
            f"Запрос создан.\n"
            f"Страна: {mock_data.request_country}.\n"
            f"Время создания: {mock_data.date.strftime('%d.%m.%Y %H:%M')}.\n"
            f"Количество самолётов: 0.\n"
        )
        mock_data.configure_mock(**{"__str__.return_value": new_display_text})
        mock_app.worker.file.get_all.return_value = mock_data
        mock_app.action_file_get_plane_all()
        captured = capsys.readouterr()
        assert "Данные успешно загружены" in captured.out
        assert "Количество самолётов: 0" in captured.out
        assert "1." not in captured.out

    def test_action_file_delete_plane_by_id(self, mock_app, monkeypatch):
        """Тест удалить самолёт"""
        target_callsign = "DLH456"
        monkeypatch.setattr("builtins.input", lambda _: target_callsign)
        mock_app.action_file_delete_plane()
        mock_app.worker.file.delete_by_callsign.assert_called_once_with(target_callsign)

    def test_flow_find_and_save(self, mock_app, monkeypatch):
        mock_plane = MagicMock()
        mock_app.worker.last_request_plane = mock_plane
        monkeypatch.setattr("builtins.input", lambda _: "ANY_CALLSIGN")
        mock_app.action_file_save()
        mock_app.worker.file.save_one.assert_called_with(mock_plane)
        assert mock_app.worker.last_request_plane is None
