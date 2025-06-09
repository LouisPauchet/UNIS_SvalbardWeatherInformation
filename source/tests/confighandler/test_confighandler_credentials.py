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
def config_handler():
    """
    Fixture to initialize the ConfigHandler instance.
    """
    return ConfigHandler()

def test_get_api_credential_invalid_datasource(config_handler):
    """Test that an unknown datasource returns None."""
    mock_data = '[{"datasource": "FrostSource", "api_key": "XXXXX"}]'

    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("json.load", return_value=json.loads(mock_data)):
            api_key = config_handler.get_api_credential("UnknownSource")
            assert api_key is None

# def test_get_api_credential_file_not_found(config_handler):
#     """Test that a missing configuration file is handled gracefully."""
#     with patch("builtins.open", side_effect=FileNotFoundError):
#         api_key = config_handler.get_api_credential("FrostSource")
#         assert api_key is None  # Should return None when file is not found
# 
# def test_get_api_credential_malformed_json(config_handler):
#     """Test that a malformed JSON file is handled gracefully."""
#     with patch("builtins.open", mock_open(read_data="INVALID_JSON")):
#         with patch("json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
#             api_key = config_handler.get_api_credential("FrostSource")
#             assert api_key is None  # Should return None if JSON is malformed

# def test_get_api_credential_valid_datasource(config_handler):
#     """Test that a valid datasource returns the correct API key."""
#     mock_data = '[{"datasource": "FrostSource", "api_key": "XXXXX"}]'
# 
#     with patch("builtins.open", mock_open(read_data=mock_data)):
#         with patch("json.load", return_value=json.loads(mock_data)):  # Mock JSON loading
#             api_key = config_handler.get_api_credential("FrostSource")
#             assert api_key == "XXXXX"
