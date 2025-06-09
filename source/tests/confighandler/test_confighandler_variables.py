import sys
import os

# Dynamically add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import pytest
import tempfile
import json
import os
from unittest.mock import patch, mock_open, MagicMock

from source.configHandler.confighandler import ConfigHandler


def test_load_var_config_with_example_file():
    """
    Test the `_load_var_config` method using an example configuration file.
    """
    # Example configuration data
    example_config_data = {
        "variables": {
            "airTemperature": {
                "unit": "°C",
                "minValue": -40,
                "maxValue": 50,
                "name": "Air Temperature",
                "default": True
            },
            "seaSurfaceTemperature": {
                "unit": "°C",
                "minValue": -2,
                "maxValue": 35,
                "name": "Sea Surface Temperature",
                "default": False
            }
        }
    }

    # Expected data after adding 'id' field
    expected_var_config_data = {
        "airTemperature": {
            "id": "airTemperature",
            "unit": "°C",
            "minValue": -40,
            "maxValue": 50,
            "name": "Air Temperature",
            "default": True
        },
        "seaSurfaceTemperature": {
            "id": "seaSurfaceTemperature",
            "unit": "°C",
            "minValue": -2,
            "maxValue": 35,
            "name": "Sea Surface Temperature",
            "default": False
        }
    }

    # Create a temporary file and write the example configuration data to it
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        json.dump(example_config_data, temp_file)
        temp_file_path = temp_file.name

    try:
        config_handler = ConfigHandler(variable_config_file=temp_file_path)
        config_handler.variables_config_file = temp_file_path
        print('!!!!!!!!!!!\n!!!!!!!!!!!',config_handler.variables_config_file)

        # Call the method
        config_handler._load_var_config()

        # Verify that the variable_config attribute is set correctly
        assert config_handler.variable_config == expected_var_config_data

    finally:
        # Clean up: delete the temporary file
        os.unlink(temp_file_path)


def test_load_var_config_file_not_found(caplog):
    """
    Test the `_load_var_config` method to ensure it handles FileNotFoundError correctly.
    """
    # Mock the open function to raise FileNotFoundError
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        config_handler = ConfigHandler(variable_config_file='Z:\nonnfeihqziohkcnqzphgkj.json')
        # Call the method
        config_handler._load_var_config()

        # Verify that an error was logged
        assert "Error occurred: File not found" in caplog.text

def test_load_var_config_json_decode_error(caplog):
    """
    Test the `_load_var_config` method to ensure it handles JSONDecodeError correctly.
    """
    # Create a temporary file with invalid JSON data
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write("invalid json")
        temp_file_path = temp_file.name

    # Mock the open function to return the temporary file
    config_handler = ConfigHandler(variable_config_file=temp_file_path)
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
            # Call the method with the temporary file path
            config_handler._load_var_config()

            # Verify that an error was logged
            assert "Error occurred: Expecting value" in caplog.text

    os.unlink(temp_file_path)
