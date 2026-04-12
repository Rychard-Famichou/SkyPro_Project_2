from unittest.mock import MagicMock, patch

import pytest


class TestApiAdapter:

    @patch("models.api_adapter.get")
    def test_get_aeroplanes_success(self, mock_get, api_adapter):
        """Проверка успешного выполнения цепочки запросов."""

        # 1. Настраиваем фейковый ответ от OpenStreetMap
        mock_osm_response = MagicMock()
        mock_osm_response.json.return_value = [{"boundingbox": ["50.0", "51.0", "30.0", "31.0"]}]

        # 2. Настраиваем фейковый ответ от OpenSky
        mock_opensky_response = MagicMock()
        mock_opensky_response.json.return_value = {
            "states": [["3c6541", "DLH123", "Germany", 16171819, 16171820, 7.4, 51.2, 5000, False]]
        }

        # Очередность возвращаемых ответов для каждого вызова get()
        mock_get.side_effect = [mock_osm_response, mock_opensky_response]

        # Выполняем метод
        api_adapter.get_aeroplanes("Germany")

        # ПРОВЕРКИ (Assertions)

        # Проверяем, что было 2 вызова
        assert mock_get.call_count == 2

        # Проверяем параметры первого вызова (OSM)
        first_call_args = mock_get.call_args_list[0]
        assert first_call_args.kwargs["params"]["country"] == "Germany"
        assert "User-Agent" in first_call_args.kwargs["headers"]

        # Проверяем параметры второго вызова (OpenSky)
        second_call_args = mock_get.call_args_list[1]
        expected_params = {"lamin": "50.0", "lamax": "51.0", "lomin": "30.0", "lomax": "31.0"}
        assert second_call_args.kwargs["params"] == expected_params

        # Проверяем итоговый результат в атрибуте класса
        assert api_adapter.aeroplanes["states"][0][1] == "DLH123"

    @patch("models.api_adapter.get")
    def test_get_aeroplanes_empty_geo(self, mock_get, api_adapter):
        """Проверка поведения, если страна не найдена в OSM."""
        mock_osm_response = MagicMock()
        mock_osm_response.json.return_value = []  # Пустой список

        mock_get.return_value = mock_osm_response

        # Ожидаем ошибку IndexError, так как в коде идет обращение data[0]
        with pytest.raises(IndexError):
            api_adapter.get_aeroplanes("NonExistentCountry")
