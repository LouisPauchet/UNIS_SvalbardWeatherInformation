from pydantic import BaseModel, field_validator
import re

from .general import StationID, TimeserieOutputFormat

from typing import Union, List, Literal
from datetime import datetime
from pandas.tseries.frequencies import to_offset


class DataEntry(BaseModel):
    timestamp: str

    class Config:
        extra = 'allow'

class StationDataTimeSerie(StationID):
    timeseries: list[DataEntry]

class StationTimeSeriesRequest(BaseModel):
    stations: Union[str, List[str]]
    start_time: str  # ISO-8601 format
    end_time: str       
    interval: str = '1h'  # Python Resampling Interval
    variables: List[str] = []
    format: TimeserieOutputFormat = 'json'

    @field_validator('stations')
    def validate_stations_alphanumeric(cls, v):
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
        try:
            to_offset(v)
        except ValueError:
            raise ValueError('Interval should a valid DateOffset string')
        return v
    
    @field_validator('variables')
    def validate_variables_alphanumeric(cls, v):
        if v is None:
            return v
        for variable in v:
            if not re.match('^[a-zA-Z0-9]+$', variable):
                raise ValueError('Each variable must be alphanumeric')
        return v