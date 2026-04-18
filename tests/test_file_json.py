from unittest.mock import mock_open, patch

import pytest

from aeroplane.aeroplane import Aeroplane
from aeroplane.aeroplane_data import AeroplaneData
from file.file_json import JSONAeroplaneStorage


@pytest.mark.parametrize(
    "input_name, expected_name",
    [
        (None, "aeroplanes.json"),
        ("my_data", "my_data.json"),
        ("archive.json", "archive.json"),
    ],
)
def test_storage_filename_init(tmp_path, input_name, expected_name):
    with patch("file.file_json.AEROPLANES_JSON_FILE", tmp_path):
        storage = JSONAeroplaneStorage(input_name)
        assert storage.filename == expected_name


class TestReadFile:

    @patch("pathlib.Path.exists")
    def test_file_does_not_exist(self, mock_exists, file_handler):
        """1. Файл физически отсутствует на диске"""
        mock_exists.return_value = False

        result = file_handler._read_file()

        assert result == []
        assert isinstance(result, list)

    @patch("pathlib.Path.exists")
    def test_json_decode_error(self, mock_exists, file_handler):
        """2. Файл существует, но внутри невалидный JSON (битый файл)"""
        mock_exists.return_value = True
        invalid_json = "{ 'bad_data': }"  # Неверные кавычки и лишняя запятая

        with patch("builtins.open", mock_open(read_data=invalid_json)):
            result = file_handler._read_file()

        assert result == []

    @patch("pathlib.Path.exists")
    def test_file_not_found_on_open(self, mock_exists, file_handler):
        """3. Race condition: файл исчез сразу после проверки exists()"""
        mock_exists.return_value = True

        with patch("builtins.open", side_effect=FileNotFoundError):
            result = file_handler._read_file()

        assert result == []

    @patch("pathlib.Path.exists")
    def test_successful_read(self, mock_exists, file_handler):
        """4. Успешное чтение валидного JSON"""
        mock_exists.return_value = True
        valid_json = '[{"id": 1, "name": "test"}]'

        with patch("builtins.open", mock_open(read_data=valid_json)):
            result = file_handler._read_file()

        assert result == [{"id": 1, "name": "test"}]


def test_add_one_and_duplicate(temp_storage):
    plane = Aeroplane("TEST01", "Russia", 10.0, 20.0, 5000.0, 120.0)

    temp_storage.save_one(plane)
    data = temp_storage._read_file()
    assert len(data) == 1
    assert data[0]["callsign"] == "TEST01"

    temp_storage.save_one(plane)
    data = temp_storage._read_file()
    assert len(data) == 1


def test_get_by_callsign(temp_storage):
    plane = Aeroplane("FLY777", "France", 45.0, 2.0, 10000.0, 800.0)
    temp_storage.save_one(plane)

    found_plane = temp_storage.get_by_callsign("FLY777")

    assert found_plane is not None
    assert found_plane.callsign == "FLY777"
    assert found_plane.baro_altitude == 10000.0

    assert temp_storage.get_by_callsign("GHOST") is None


def test_save_all_merging(temp_storage):
    temp_storage.save_one(Aeroplane("OLD1", "Country", 0, 0, 0, 0))

    ap_data = AeroplaneData("Batch")
    ap_data.add_aeroplane(Aeroplane("OLD1", "Country", 0, 0, 0, 0))  # Дубликат
    ap_data.add_aeroplane(Aeroplane("NEW2", "Country", 0, 0, 0, 0))  # Новый

    temp_storage.save_all(ap_data)

    all_data = temp_storage._read_file()
    assert len(all_data) == 2
    callsigns = [p["callsign"] for p in all_data]
    assert "OLD1" in callsigns
    assert "NEW2" in callsigns


def test_delete_operations(temp_storage):
    temp_storage.save_one(Aeroplane("DEL1", "C", 0, 0, 0, 0))
    temp_storage.save_one(Aeroplane("KEEP2", "C", 0, 0, 0, 0))

    temp_storage.delete_by_callsign("DEL1")
    assert len(temp_storage._read_file()) == 1

    temp_storage.delete_all()
    assert temp_storage._read_file() == []


def test_delete_by_callsign_not_found(temp_storage, capsys):
    airplane = Aeroplane("EXISTING", "C", 0, 0, 0, 0)
    temp_storage.save_one(airplane)

    data_before = temp_storage._read_file()

    temp_storage.delete_by_callsign("NON_EXISTENT")

    assert temp_storage._read_file() == data_before

    captured = capsys.readouterr()
    assert "Самолет NON_EXISTENT не найден." in captured.out


def test_get_all_saved_files_filtering(tmp_path):
    (tmp_path / "plane1.json").write_text("[]")
    (tmp_path / "plane2.json").write_text("[]")
    (tmp_path / "readme.txt").write_text("not a json")  # Не должен попасть
    (tmp_path / ".DS_Store").write_text("system file")  # Не должен попасть
    (tmp_path / "backup.json.bak").write_text("wrong ext")  # Не должен попасть

    with patch("file.file_json.AEROPLANES_JSON_FILE", tmp_path):
        files = JSONAeroplaneStorage.get_all_saved_files()

    assert len(files) == 2
    assert "plane1" in files
    assert "plane2" in files
    assert "readme" not in files
    assert "plane1.json" not in files  # Проверка, что расширение отрезано


def test_get_all_saved_files_no_directory(tmp_path):
    non_existent_dir = tmp_path / "non_existent_folder"

    with patch("file.file_json.AEROPLANES_JSON_FILE", non_existent_dir):
        files = JSONAeroplaneStorage.get_all_saved_files()

    assert files == []


def test_get_all_logic(temp_storage):
    plane1 = Aeroplane("CALL1", "Country1", 0, 0, 100, 0)
    plane2 = Aeroplane("CALL2", "Country2", 0, 0, 200, 0)
    temp_storage.save_one(plane1)
    temp_storage.save_one(plane2)

    result_data = temp_storage.get_all()

    assert isinstance(result_data, AeroplaneData)
    assert len(result_data.aeroplanes) == 2
    assert result_data.aeroplanes[0].callsign == "CALL1"
    assert result_data.aeroplanes[1].baro_altitude == 200


def test_get_all_empty_storage(temp_storage):
    result_data = temp_storage.get_all()

    assert isinstance(result_data, AeroplaneData)
    assert len(result_data.aeroplanes) == 0
