from pydantic import BaseModel, field_validator
import re

from .general import StationID, TimeserieOutputFormat

from typing import Union, List, Literal
from datetime import datetime
from pandas.tseries.frequencies import to_offset

class DataEntry(BaseModel):
    """A data entry with a timestamp and optional additional fields."""
    timestamp: str

    class Config:
        extra = 'allow'

class StationDataTimeSerie(StationID):
    """A time series data associated with a specific station."""
    timeseries: list[DataEntry]

class StationTimeSeriesRequest(BaseModel):
    """
    A request model for querying time series data for specific stations.

    Attributes:
        stations (Union[str, List[str]]): A single station ID or a list of station IDs.
        start_time (str): The start time for the data query in ISO-8601 format.
        end_time (str): The end time for the data query in ISO-8601 format.
        interval (str): The resampling interval for the time series data. Defaults to '1h'.
        variables (List[str]): A list of variables to include in the query. Defaults to an empty list.
        format (TimeserieOutputFormat): The output format for the time series data. Defaults to 'json'.
    """

    stations: Union[str, List[str]]
    start_time: str  # ISO-8601 format
    end_time: str
    interval: str = '1h'  # Python Resampling Interval
    variables: List[str] = []
    format: TimeserieOutputFormat = 'json'

    @field_validator('stations')
    def validate_stations_alphanumeric(cls, v):
        """
        Validates that station IDs are alphanumeric.

        Args:
            v (Union[str, List[str]]): The station ID or list of station IDs to validate.

        Returns:
            Union[str, List[str]]: The validated station ID or list of station IDs.

        Raises:
            ValueError: If any station ID is not alphanumeric.
        """
        if isinstance(v, str):
            if not re.match('^[a-zA-Z0-9]+$', v):
                raise ValueError('Station ID must be alphanumeric')
        elif isinstance(v, list):
            for station in v:
                if not re.match('^[a-zA-Z0-9]+$', station):
                    raise ValueError('Each station ID must be alphanumeric')
        return v

    @field_validator('start_time', 'end_time')
    def validate_iso_format(cls, v):
        """
        Validates that the time strings are in ISO-8601 format.

        Args:
            v (str): The time string to validate.

        Returns:
            str: The validated time string.

        Raises:
            ValueError: If the time string is not in ISO-8601 format.
        """
        try:
            if v.endswith('Z'):
                v = v[:-1] + '+00:00'
            print(v)
            print(datetime.fromisoformat(v))
        except ValueError:
            raise ValueError('Time must be in ISO-8601 format')
        return v

    @field_validator('interval')
    def validate_offset_interval(cls, v):
        """
        Validates that the interval is a valid DateOffset string.

        Args:
            v (str): The interval string to validate.

        Returns:
            str: The validated interval string.

        Raises:
            ValueError: If the interval is not a valid DateOffset string.
        """
        try:
            to_offset(v)
        except ValueError:
            raise ValueError('Interval should a valid DateOffset string')
        return v

    @field_validator('variables')
    def validate_variables_alphanumeric(cls, v):
        """
        Validates that the variables are alphanumeric.

        Args:
            v (List[str]): The list of variables to validate.

        Returns:
            List[str]: The validated list of variables.

        Raises:
            ValueError: If any variable is not alphanumeric.
        """
        if v is None:
            return v
        for variable in v:
            if not re.match('^[a-zA-Z0-9]+$', variable):
                raise ValueError('Each variable must be alphanumeric')
        return v
