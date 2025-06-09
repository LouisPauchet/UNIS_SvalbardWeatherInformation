from pydantic import BaseModel, Field, field_validator
import re
from enum import Enum
from typing import Literal, Union

TimeserieOutputFormat = Literal['json', 'csv', 'netcdf4']


class GPSLocation(BaseModel):
    lat: Union[float, None]
    lon: Union[float, None]

class StationStatus(str, Enum):
    offline = "offline"
    online = "online"
    unknown = "unknown"

class StationType(str, Enum):
    fixed = "fixed"
    modile = "mobile"

class StationID(BaseModel):
    id: str = Field(..., pattern='^[a-zA-Z0-9]+$')

    @field_validator('id')
    def id_must_alphanumeric(cls, v: str) -> str:
        if not re.match('^[a-zA-Z0-9]+$', v):
            raise ValueError('Station ID must be alphanumeric')
        return v
