import pytest
from unittest.mock import patch
import pandas as pd
import os
import sys
from datetime import datetime, timedelta

# Adjust the system path to include the parent directory of your project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from source.datasource.IWOOSSource import IWOOSSource

# Define a fixture for the IWOOSSource instance
@pytest.fixture
def iwoos_source():
    return IWOOSSource(api_key='your_api_key')

# Test fetching station data
def test_fetch_station_data(iwoos_source):
    station_id = "2025_IWOOS_id4"
    data = iwoos_source.fetch_station_data(station_id)
    assert data == {}, "Should return an empty dict as IWOOS doesn't provide metadata"

# Test fetching real-time data with mock
@patch('pandas.read_csv')
def test_fetch_realtime_data_offline(mock_read_csv, iwoos_source):
    # Setup mock data with datetime objects
    mock_gps_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0)],
        'lat': [60.0],
        'lon': [5.0]
    }).set_index('time')

    mock_wavestat_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0)],
        'pHs0': [1.0],
        'pT02': [2.0],
        'pT24': [3.0]
    }).set_index('time')

    mock_read_csv.side_effect = [mock_gps_data, mock_wavestat_data]

    # Call the method
    station_id = "2025_IWOOS_id4"
    data = iwoos_source.fetch_realtime_data(station_id)

    # Assertions
    assert data is not None, "Should return transformed real-time data"
    assert "timeseries" in data, "Data should contain timeseries"

# Test fetching timeseries data with mock
@patch('pandas.read_csv')
def test_fetch_timeseries_data_offline(mock_read_csv, iwoos_source):
    # Setup mock data with datetime objects
    mock_gps_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0), datetime(2023, 1, 1, 1, 0, 0)],
        'lat': [60.0, 60.1],
        'lon': [5.0, 5.1]
    }).set_index('time')

    mock_wavestat_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0), datetime(2023, 1, 1, 1, 0, 0)],
        'pHs0': [1.0, 1.1],
        'pT02': [2.0, 2.1],
        'pT24': [3.0, 3.1]
    }).set_index('time')

    mock_read_csv.side_effect = [mock_gps_data, mock_wavestat_data]

    # Call the method
    station_id = "2025_IWOOS_id4"
    start_time = "2023-01-01T00:00:00"
    end_time = "2023-01-01T01:00:00"
    data = iwoos_source.fetch_timeseries_data(station_id, start_time, end_time)

    # Assertions
    assert data is not None, "Should return transformed timeseries data"
    assert "timeseries" in data, "Data should contain timeseries"

# Test if station is online with mock
@patch('pandas.read_csv')
def test_is_station_online_offline(mock_read_csv, iwoos_source):
    # Setup mock data with datetime objects
    mock_gps_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0)],
        'lat': [60.0],
        'lon': [5.0]
    }).set_index('time')

    mock_wavestat_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0)],
        'pHs0': [1.0],
        'pT02': [2.0],
        'pT24': [3.0]
    }).set_index('time')

    mock_read_csv.side_effect = [mock_gps_data, mock_wavestat_data]

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert isinstance(is_online, bool), "Should return a boolean indicating if the station is online"


# Test handling of read_csv error for real-time data
@patch('pandas.read_csv')
def test_fetch_realtime_data_read_csv_error(mock_read_csv, iwoos_source):
    # Simulate an IOError when reading CSV
    mock_read_csv.side_effect = IOError("Unable to read CSV file")

    # Call the method
    station_id = "2025_IWOOS_id4"
    data = iwoos_source.fetch_realtime_data(station_id)

    # Assertions
    assert data is None, "Should return None when an error occurs during CSV read"

# Test handling of read_csv error for timeseries data
@patch('pandas.read_csv')
def test_fetch_timeseries_data_read_csv_error(mock_read_csv, iwoos_source):
    # Simulate an IOError when reading CSV
    mock_read_csv.side_effect = IOError("Unable to read CSV file")

    # Call the method
    station_id = "2025_IWOOS_id4"
    start_time = "2023-01-01T00:00:00"
    end_time = "2023-01-01T01:00:00"
    data = iwoos_source.fetch_timeseries_data(station_id, start_time, end_time)

    # Assertions
    assert data is None, "Should return None when an error occurs during CSV read"

# Test handling of read_csv error for station online check
@patch('pandas.read_csv')
def test_is_station_online_read_csv_error(mock_read_csv, iwoos_source):
    # Simulate an IOError when reading CSV
    mock_read_csv.side_effect = IOError("Unable to read CSV file")

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert is_online is False, "Should return False when an error occurs during CSV read"



# Test fetching timeseries data with return_df option
@patch('pandas.read_csv')
def test_fetch_timeseries_data_return_df(mock_read_csv, iwoos_source):
    # Setup mock data with datetime objects
    mock_gps_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0), datetime(2023, 1, 1, 1, 0, 0)],
        'lat': [60.0, 60.1],
        'lon': [5.0, 5.1]
    }).set_index('time')

    mock_wavestat_data = pd.DataFrame({
        'time': [datetime(2023, 1, 1, 0, 0, 0), datetime(2023, 1, 1, 1, 0, 0)],
        'pHs0': [1.0, 1.1],
        'pT02': [2.0, 2.1],
        'pT24': [3.0, 3.1]
    }).set_index('time')

    mock_read_csv.side_effect = [mock_gps_data, mock_wavestat_data]

    # Call the method with return_df=True
    station_id = "2025_IWOOS_id4"
    start_time = "2023-01-01T00:00:00"
    end_time = "2023-01-01T01:00:00"
    data = iwoos_source.fetch_timeseries_data(station_id, start_time, end_time, return_df=True)

    # Assertions
    assert isinstance(data, pd.DataFrame), "Should return a DataFrame when return_df is True"
    assert not data.empty, "Returned DataFrame should not be empty"

# Test handling of error when fetch_realtime_data returns None
@patch('source.datasource.IWOOSSource.IWOOSSource.fetch_realtime_data')
def test_is_station_online_fetch_error(mock_fetch_realtime_data, iwoos_source):
    # Simulate fetch_realtime_data returning None
    mock_fetch_realtime_data.return_value = None

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert is_online is False, "Should return False when fetch_realtime_data returns None"

# Test handling of missing timeseries in data
@patch('source.datasource.IWOOSSource.IWOOSSource.fetch_realtime_data')
def test_is_station_online_missing_timeseries(mock_fetch_realtime_data, iwoos_source):
    # Simulate fetch_realtime_data returning data without timeseries
    mock_fetch_realtime_data.return_value = {"some_key": "some_value"}

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert is_online is False, "Should return False when timeseries is missing in data"

# Test handling of empty timeseries
@patch('source.datasource.IWOOSSource.IWOOSSource.fetch_realtime_data')
def test_is_station_online_empty_timeseries(mock_fetch_realtime_data, iwoos_source):
    # Simulate fetch_realtime_data returning data with empty timeseries
    mock_fetch_realtime_data.return_value = {"timeseries": []}

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert is_online is False, "Should return False when timeseries is empty"

# Test handling of missing timestamp in timeseries entry
@patch('source.datasource.IWOOSSource.IWOOSSource.fetch_realtime_data')
def test_is_station_online_missing_timestamp(mock_fetch_realtime_data, iwoos_source):
    # Simulate fetch_realtime_data returning data with missing timestamp
    mock_fetch_realtime_data.return_value = {
        "timeseries": [{"location": {"lat": 60.0, "lon": 5.0}}]
    }

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert is_online is False, "Should return False when timestamp is missing in timeseries entry"

# Test handling of invalid timestamp format
@patch('source.datasource.IWOOSSource.IWOOSSource.fetch_realtime_data')
def test_is_station_online_invalid_timestamp(mock_fetch_realtime_data, iwoos_source):
    # Simulate fetch_realtime_data returning data with invalid timestamp format
    mock_fetch_realtime_data.return_value = {
        "timeseries": [{
            "timestamp": "invalid_timestamp_format",
            "location": {"lat": 60.0, "lon": 5.0}
        }]
    }

    # Call the method
    station_id = "2025_IWOOS_id4"
    is_online = iwoos_source.is_station_online(station_id)

    # Assertions
    assert is_online is False, "Should return False when timestamp format is invalid"


# Test station considered online due to recent timestamp
@patch('pandas.read_csv')
def test_is_station_online_recent_timestamp(mock_read_csv, iwoos_source):
    # Setup mock data with a recent timestamp
    recent_time = datetime.utcnow() - timedelta(minutes=10)  # 10 minutes ago
    mock_gps_data = pd.DataFrame({
        'time': [recent_time],
        'lat': [60.0],
        'lon': [5.0]
    }).set_index('time')

    mock_wavestat_data = pd.DataFrame({
        'time': [recent_time],
        'pHs0': [1.0],
        'pT02': [2.0],
        'pT24': [3.0]
    }).set_index('time')

    mock_read_csv.side_effect = [mock_gps_data, mock_wavestat_data]

    # Call the method with a max_inactive_minutes that is greater than the age of the timestamp
    station_id = "2025_IWOOS_id4"
    max_inactive_minutes = 30  # 30 minutes threshold
    is_online = iwoos_source.is_station_online(station_id, max_inactive_minutes)

    # Assertions
    assert is_online is True, "Should return True when the latest timestamp is recent enough"