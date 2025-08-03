import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
from unittest.mock import patch, MagicMock

# Import the function to be tested
from source.datasource.datasourceFactory import get_datasource
from source.datasource.FrostSource import FrostSource
from source.datasource.IWINFixedSource import IWINFixedSource


@pytest.fixture
def mock_config_handler():
    """
    Fixture to mock the ConfigHandler instance in datasourceFactory.
    """
    # Patch where ConfigHandler is used (i.e., in source.datasource.datasourceFactory).
    with patch("source.datasource.datasourceFactory.ConfigHandler") as MockConfigHandler:
        mock_instance = MagicMock()
        MockConfigHandler.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_logger():
    """
    Fixture to mock Logger.setup_logger in datasourceFactory.
    """
    with patch("source.datasource.datasourceFactory.Logger.setup_logger") as mock_setup_logger:
        mock_logger_instance = MagicMock()
        mock_setup_logger.return_value = mock_logger_instance
        yield mock_logger_instance


def test_get_datasource_frostsource(mock_logger, mock_config_handler):
    """
    Test that get_datasource returns a FrostSource
    when the metadata indicates 'FrostSource'.
    """
    # Arrange
    mock_config_handler.get_metadata.return_value = {"datasource": "FrostSource"}
    mock_config_handler.get_api_credential.return_value = "frost_api_key"

    # Act
    datasource = get_datasource("station_frost")

    # Assert
    assert isinstance(datasource, FrostSource), "Should return FrostSource instance"
    assert datasource.api_key == "frost_api_key", "API key should match the mock credential"

    # Check logger calls
    mock_logger.debug.assert_any_call("Fetching metadata for station_id: station_frost")
    mock_logger.debug.assert_any_call("Datasource identified for station_frost: FrostSource")
    mock_logger.debug.assert_any_call("Fetching API Key for: FrostSource")


def test_get_datasource_iwinfixedsource(mock_logger, mock_config_handler):
    """
    Test that get_datasource returns an IWINFixedSource
    when the metadata indicates 'IWINFixedSource'.
    """
    # Arrange
    mock_config_handler.get_metadata.return_value = {"datasource": "IWINFixedSource"}
    mock_config_handler.get_api_credential.return_value = "iwin_api_key"

    # Act
    datasource = get_datasource("station_iwin")

    # Assert
    assert isinstance(datasource, IWINFixedSource), "Should return IWINFixedSource instance"
    assert datasource.api_key == "iwin_api_key", "API key should match the mock credential"

    # Check logger calls
    mock_logger.debug.assert_any_call("Fetching metadata for station_id: station_iwin")
    mock_logger.debug.assert_any_call("Datasource identified for station_iwin: IWINFixedSource")
    mock_logger.debug.assert_any_call("Fetching API Key for: IWINFixedSource")


def test_get_datasource_unknown_datasource_fallback(mock_logger, mock_config_handler):
    """
    Test that get_datasource falls back to 'FrostSource'
    if the metadata contains an unknown datasource.
    """
    # Arrange
    mock_config_handler.get_metadata.return_value = {"datasource": "UnknownSource", 'type':'fixed'}
    mock_config_handler.get_api_credential.return_value = "fallback_api_key"

    # Act
    datasource = get_datasource("station_unknown")

    # Assert
    # Because "UnknownSource" isn't in DATASOURCE_MAPPING, it should default to FrostSource
    assert isinstance(datasource, FrostSource), "Unknown data source should fall back to FrostSource"
    assert datasource.api_key == "fallback_api_key", "Should use fallback API key"

    # Check logger calls for the warning and fallback notice
    mock_logger.info.assert_any_call(
        "Unknown datasource 'UnknownSource' for station_id station_unknown, defaulting to FrostSource."
    )
    mock_logger.debug.assert_any_call("Datasource identified for station_unknown: FrostSource")
