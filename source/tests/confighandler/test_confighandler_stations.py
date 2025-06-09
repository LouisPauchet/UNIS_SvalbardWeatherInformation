import sys
import os

# Dynamically add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
import json
from unittest.mock import patch, mock_open, MagicMock
from source.configHandler.confighandler import ConfigHandler, StationNotFoundError
from source.logger.logger import Logger


@pytest.fixture
def mock_config_files():
    """
    Fixture to provide mock configuration data.
    """
    fixed_station_data = [
        {"id": "station_001", "type": "fixed", "variables": {"temp": "Temperature"}},
        {"id": "station_002", "type": "fixed", "variables": {"wind": "Wind Speed"}}
    ]

    mobile_station_data = [
        {"id": "station_003", "type": "mobile", "variables": {"humidity": "Humidity"}}
    ]

    return {
        "static/config/fixed_stations.json": json.dumps(fixed_station_data),
        "static/config/mobile_stations.json": json.dumps(mobile_station_data)
    }


@pytest.fixture
def config_handler():
    """
    Fixture to initialize the ConfigHandler instance.
    """
    return ConfigHandler()


@patch("builtins.open")
def test_load_config(mock_open_func, config_handler, mock_config_files):
    """
    Test the `_load_config` method to ensure it loads data from all files.
    """
    # Set the config_files attribute to the desired test files
    config_handler.config_files = [
        "static/config/fixed_stations.json",
        "static/config/mobile_stations.json"
    ]

    # Mock the open calls for each file
    def mock_file_open(file, mode):
        if file in mock_config_files:
            return mock_open(read_data=mock_config_files[file]).return_value
        else:
            raise FileNotFoundError(f"No such file: '{file}'")
    mock_open_func.side_effect = mock_file_open

    configs = config_handler._load_config()

    # Verify the combined data
    assert len(configs) == 3
    assert any(config["id"] == "station_001" for config in configs)
    assert any(config["id"] == "station_003" for config in configs)


@patch.object(ConfigHandler, "_load_config")
def test_get_variable(mock_load_config, config_handler):
    """
    Test `get_variable` for fetching variable mappings for a specific station.
    """
    mock_load_config.return_value = [
        {"id": "station_001", "type": "fixed", "variables": {"temp": "Temperature"}}
    ]

    variables = config_handler.get_variable("station_001")
    assert variables == {"temp": "Temperature"}

    with pytest.raises(StationNotFoundError):
        config_handler.get_variable("station_002")


@patch.object(ConfigHandler, "_load_config")
def test_get_metadata(mock_load_config, config_handler):
    """
    Test `get_metadata` for fetching metadata for a specific station.
    """
    mock_load_config.return_value = [
        {"id": "station_001", "type": "fixed", "variables": {"temp": "Temperature"}}
    ]

    metadata = config_handler.get_metadata("station_001")
    assert metadata == {"id": "station_001", "type": "fixed", "variables": {"temp": "Temperature"}}

    metadata = config_handler.get_metadata("station_002")
    assert metadata is None


@patch.object(ConfigHandler, "_load_config")
def test_get_stations(mock_load_config, config_handler):
    """
    Test `get_stations` for retrieving station IDs by type.
    """
    mock_load_config.return_value = [
        {"id": "station_001", "type": "fixed"},
        {"id": "station_002", "type": "fixed"},
        {"id": "station_003", "type": "mobile"}
    ]

    all_stations = config_handler.get_stations("all")
    assert sorted(all_stations) == ["station_001", "station_002", "station_003"]

    fixed_stations = config_handler.get_stations("fixed")
    assert sorted(fixed_stations) == ["station_001", "station_002"]

    mobile_stations = config_handler.get_stations("mobile")
    assert mobile_stations == ["station_003"]


@patch.object(Logger, "setup_logger", return_value=MagicMock())
@patch("builtins.open", side_effect=FileNotFoundError("Test FileNotFoundError"))
def test_handle_error(mock_open_func, mock_logger, config_handler):
    """
    Test `_handle_error` to ensure it logs errors properly.
    """
    # Replace the logger with the mocked logger
    config_handler.logger = mock_logger

    # Set the config_files attribute to a file that doesn't exist
    config_handler.config_files = ["nonexistent_file.json"]

    # Call _load_config, which should handle the FileNotFoundError and call _handle_error
    try:
        config_handler._load_config()
    except FileNotFoundError:
        pass

    # Check that error was logged
    mock_logger.error.assert_called_once_with("Error occurred: Test FileNotFoundError")



