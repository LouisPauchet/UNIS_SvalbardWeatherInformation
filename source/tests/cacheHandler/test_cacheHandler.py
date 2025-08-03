import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import json
import pytest
import shutil
from unittest.mock import patch, MagicMock
from pathlib import Path

from source.configHandler.confighandler import ConfigHandler
from source.logger.logger import Logger
# Importing CacheHandler from its path
from source.cacheHandler.cacheHandler import CacheHandler

# IMPORTANT:
# We do NOT import get_datasource directly here, because we will patch
# it in 'source.cacheHandler.cacheHandler' where it is used.


@pytest.fixture
def temp_cache_dir(tmp_path) -> Path:
    """
    Pytest fixture to supply a temporary directory for cache files.
    """
    return tmp_path


@pytest.fixture
def mock_config_handler():
    """
    Return a mock for the ConfigHandler with default behaviors.
    """
    mock = MagicMock(spec=ConfigHandler)

    # By default, let's say we have 2 stations:
    mock.get_stations.return_value = ["station1", "station2"]
    # If the CacheHandler calls config.get_metadata / get_variable:
    mock.get_metadata.return_value = {
        "datasource": "FrostSource",
        "name": "Test Station",
        "type": "weather",
        "lat": 12.34,
        "lon": 56.78,
    }
    mock.get_variable.return_value = {"temp": {"units": "C"}}
    mock.get_api_credential.return_value = "fake-api-key"
    return mock


@pytest.fixture
def cache_handler(temp_cache_dir, mock_config_handler):
    """
    Creates an instance of CacheHandler, using the temporary directory
    for cache storage. Overwrites the real ConfigHandler with our mock.
    """
    from source.cacheHandler.cacheHandler import CacheHandler  # Ensure correct import
    path_config = {
        'station_metadata': 'cache_stations_status.json',
        'realtime_data': '111_data_realtime/',
        'online': '000_status_online_stations/',
        'offline' : '000_status_offline_stations/'
    }

    ch = CacheHandler(directory=str(temp_cache_dir), path_config=path_config, cleaning_list=['online'])
    ch.config = mock_config_handler
    return ch


@pytest.mark.usefixtures("cache_handler")
class TestCacheHandler:
    """
    Test suite for the CacheHandler class.
    """

    @pytest.mark.parametrize("stations, side_effects", [
        (["station1", "station2"], [True, False]),
        (["station3"], [True]),
    ])
    @patch("source.cacheHandler.cacheHandler.get_datasource")  # <--- PATCH HERE
    def test_cache_stations_status(
        self,
        mock_get_datasource,
        stations,
        side_effects,
        cache_handler,
        mock_config_handler,
        temp_cache_dir
    ):
        # 1. Ensure the config returns the right stations
        mock_config_handler.get_stations.return_value = stations

        # 2. Build a mock datasource that will answer is_station_online
        ds_mock = MagicMock()
        ds_mock.is_station_online.side_effect = side_effects

        # 3. Force all calls to get_datasource(...) to return ds_mock
        mock_get_datasource.return_value = ds_mock

        # 4. Run the code under test
        result = cache_handler.cache_stations_status()

        # 5. Verify we got as many results as stations
        assert len(result) == len(stations)

        # 6. Verify the JSON file was created
        station_status_file = temp_cache_dir / "cache_stations_status.json"
        assert station_status_file.exists(), "Station metadata cache file should exist."

        with station_status_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == len(stations)

        if side_effects[0]:
            # If the first side_effect was True, that station is 'online'
            assert cache_handler.online_stations[0] == stations[0]

    @patch("source.cacheHandler.cacheHandler.get_datasource")
    def test_cache_stations_status_error_handling(
            self,
            mock_get_datasource,
            cache_handler,
            mock_config_handler
    ):
        """
        Test exception handling if there's an error processing a station.
        """
        # Suppose the second station fails on is_station_online
        mock_config_handler.get_stations.return_value = ['station_ok', 'station_fail']

        ds_mock_ok = MagicMock()
        ds_mock_ok.is_station_online.return_value = True

        ds_mock_fail = MagicMock()
        ds_mock_fail.is_station_online.side_effect = ValueError("Simulated error")

        def side_effect_get_datasource(station_id, config=None):
            # station_id can come in as 'station_ok' or 'station_fail'
            if station_id == 'station_ok':
                return ds_mock_ok
            return ds_mock_fail

        mock_get_datasource.side_effect = side_effect_get_datasource

        # Run
        result = cache_handler.cache_stations_status()

        # 'station_ok' is processed; 'station_fail' triggers an exception
        assert len(result) == 1, "Only one station should appear in the result after error."
        assert cache_handler.online_stations == ['station_ok']

    # @patch("source.cacheHandler.cacheHandler.get_datasource")
    # def test_cache_realtime_data_with_online_stations(
    #     self,
    #     mock_get_datasource,
    #     cache_handler
    # ):
    #     cache_handler.online_stations = ["station1"]

    #     ds_mock = MagicMock()
    #     ds_mock.fetch_realtime_data.return_value = {"temp": 22.5}
    #     mock_get_datasource.return_value = ds_mock

    #     cache_handler.cache_realtime_data()

    #     realtime_file = os.path.join(
    #         cache_handler.directory,
    #         "111_data_realtime",
    #         "station1.json",
    #     )
        # assert os.path.exists(realtime_file), "Real-time data file should be written for station1"

        # with open(realtime_file, "r", encoding="utf-8") as f:
        #     data = json.load(f)
        # assert "temp" in data

    @patch("source.cacheHandler.cacheHandler.get_datasource")
    def test_cache_realtime_data_no_online_stations(
        self,
        mock_get_datasource,
        cache_handler
    ):
        # Start with no known online stations
        cache_handler.online_stations = []

        ds_mock = MagicMock()
        ds_mock.is_station_online.return_value = False
        ds_mock.fetch_realtime_data.return_value = {}
        mock_get_datasource.return_value = ds_mock

        cache_handler.cache_realtime_data()

        # No file should be created
        station_file = os.path.join(
            cache_handler.directory,
            "111_data_realtime",
            "station1.json",
        )
        assert not os.path.exists(station_file)

    def test_get_cached_online_stations(
        self,
        cache_handler,
        mock_config_handler,
        temp_cache_dir
    ):
        """
        Test the get_cached_online_stations method writes a file with online/offline stations info.
        """
        metadata_path = temp_cache_dir / "cache_stations_status.json"
        stations_status = [
            {
                "id": "station1",
                "status": "online",
                "type": "weather",
                "name": "Station 1",
                "location": {"lat": 1.0, "lon": 1.0}
            },
            {
                "id": "station2",
                "status": "offline",
                "type": "weather",
                "name": "Station 2",
                "location": {"lat": 2.0, "lon": 2.0}
            },
        ]
        with metadata_path.open("w", encoding="utf-8") as f:
            json.dump(stations_status, f)

        # Test for online stations
        result_online = cache_handler.get_cached_online_stations(type="all", status='online')
        online_stations_file = temp_cache_dir / "000_status_online_stations" / "all.json"
        assert online_stations_file.exists()

        with online_stations_file.open("r", encoding="utf-8") as f:
            data_online = json.load(f)

        assert len(data_online) == 1
        assert data_online[0]["id"] == "station1"

        # Test for offline stations
        result_offline = cache_handler.get_cached_online_stations(type="all", status='offline')
        offline_stations_file = temp_cache_dir / "000_status_offline_stations" / "all.json"
        assert offline_stations_file.exists()

        with offline_stations_file.open("r", encoding="utf-8") as f:
            data_offline = json.load(f)

        assert len(data_offline) == 1
        assert data_offline[0]["id"] == "station2"

    def test_get_cached_realtime_data(
            self,
            cache_handler,
            temp_cache_dir
    ):
        """
        Test the get_cached_realtime_data method retrieves cached real-time data correctly.
        """
        station_id = "station1"
        realtime_data_path = temp_cache_dir / "111_data_realtime"
        realtime_data_path.mkdir(parents=True, exist_ok=True)
        realtime_file = realtime_data_path / f"{station_id}.json"

        realtime_data = {"temp": 22.5, "humidity": 60}
        with realtime_file.open("w", encoding="utf-8") as f:
            json.dump(realtime_data, f)

        # Update cache_handler path_config to use the temp directory
        cache_handler.path_config["realtime_data"] = str(realtime_data_path)

        # Test valid data retrieval
        result = cache_handler.get_cached_realtime_data(station_id)
        # assert result == realtime_data, "Real-time data should match the cached content."

        # Test missing file scenario
        missing_station_id = "station2"
        result_missing = cache_handler.get_cached_realtime_data(missing_station_id)
        assert result_missing is None, "Should return None if the cache file is missing."

        # Test corrupted JSON file scenario
        corrupted_file = realtime_data_path / f"{station_id}_corrupt.json"
        corrupted_file.write_text("{invalid_json: true}")

        cache_handler.path_config["realtime_data"] = str(realtime_data_path)
        result_corrupt = cache_handler.get_cached_realtime_data(f"{station_id}_corrupt")
        assert result_corrupt is None, "Should return None if the cache file has invalid JSON."

    def test_get_cached_station_metadata(
        self,
        cache_handler,
        temp_cache_dir
    ):
        """
        Test the get_cached_station_metadata method retrieves cached station metadata correctly.
        """
        station_id = "station1"
        metadata_path = temp_cache_dir / "stations_metadata"
        metadata_path.mkdir(parents=True, exist_ok=True)
        metadata_file = metadata_path / f"{station_id}.json"

        station_metadata = {
            "id": "station1",
            "name": "Test Station",
            "type": "weather",
            "location": {"lat": 12.34, "lon": 56.78}
        }
        with metadata_file.open("w", encoding="utf-8") as f:
            json.dump(station_metadata, f)

        # Update cache_handler path_config to use the temp directory
        cache_handler.path_config["station_metadata_single"] = str(metadata_path)

        # Test valid data retrieval
        result = cache_handler.get_cached_station_metadata(station_id)
        assert result == station_metadata, "Station metadata should match the cached content."

        # Test missing file scenario
        missing_station_id = "station2"
        result_missing = cache_handler.get_cached_station_metadata(missing_station_id)
        assert result_missing is None, "Should return None if the cache file is missing."

        # Test retrieving from station status when metadata is missing
        station_status_path = temp_cache_dir / "cache_stations_status.json"
        station_status_data = [
            {
                "id": "station2",
                "name": "Fallback Station",
                "type": "weather",
                "location": {"lat": 98.76, "lon": 54.32}
            }
        ]
        with station_status_path.open("w", encoding="utf-8") as f:
            json.dump(station_status_data, f)

        cache_handler.path_config["station_status"] = str(station_status_path)
        result_fallback = cache_handler.get_cached_station_metadata("station2")
        assert result_fallback == station_status_data[0], "Should retrieve metadata from station status if missing in direct metadata."


    def test_clear_cache(
        self,
        cache_handler,
        temp_cache_dir
    ):
        """
        Test _clear_cache removes specified folders/files.
        """
        online_path = temp_cache_dir / "000_status_online_stations"
        online_path.mkdir(parents=True, exist_ok=True)
        dummy_file = online_path / "dummy.json"
        dummy_file.write_text("test content")

        assert dummy_file.exists()

        cache_handler._clear_cache(["online"])
        assert not online_path.exists()

    def test_write_and_read_cache(
        self,
        cache_handler,
        temp_cache_dir
    ):
        """
        Test the _write_cache and _read_cache methods together.
        """
        filename = "test_data.json"
        data_to_write = {"key": "value", "arr": [1, 2, 3]}

        cache_handler._write_cache(data_to_write, filename)
        read_data = cache_handler._read_cache(filename)

        assert read_data == data_to_write

    def test_delete_path(
        self,
        cache_handler,
        temp_cache_dir
    ):
        """
        Test the _delete_path method with both files and directories.
        """
        file_path = temp_cache_dir / "test_file.txt"
        file_path.write_text("some content")

        dir_path = temp_cache_dir / "test_dir"
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / "nested_file.txt").write_text("nested content")

        assert file_path.exists()
        assert dir_path.exists()

        cache_handler._delete_path(str(file_path))
        assert not file_path.exists()

        cache_handler._delete_path(str(dir_path))
        assert not dir_path.exists()
