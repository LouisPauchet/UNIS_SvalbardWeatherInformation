from pydantic import BaseModel, Field, field_validator
import re
from enum import Enum
from typing import Literal, Union

TimeserieOutputFormat = Literal['json', 'csv', 'netcdf4']

class GPSLocation(BaseModel):
    """A model representing a GPS location with latitude and longitude."""
    lat: Union[float, None]
    lon: Union[float, None]

class StationStatus(str, Enum):
    """
    An enumeration representing the possible statuses of a station.

    Attributes:
        offline (str): The station is offline.
        online (str): The station is online.
        unknown (str): The station status is unknown.
    """
    offline = "offline"
    online = "online"
    unknown = "unknown"

class StationType(str, Enum):
    """
    An enumeration representing the possible types of a station.

    Attributes:
        fixed (str): The station is fixed.
        mobile (str): The station is mobile.
    """
    fixed = "fixed"
    mobile = "mobile"

class StationID(BaseModel):
    """
    A model representing a station ID with validation for alphanumeric characters.

    Attributes:
        id (str): The alphanumeric ID of the station.
    """
    id: str = Field(..., pattern='^[a-zA-Z0-9]+$')

    @field_validator('id')
    def id_must_alphanumeric(cls, v: str) -> str:
        """
        Validates that the station ID is alphanumeric.

        Args:
            v (str): The station ID to validate.

        Returns:
            str: The validated station ID.

        Raises:
            ValueError: If the station ID is not alphanumeric.
        """
        if not re.match('^[a-zA-Z0-9]+$', v):
            raise ValueError('Station ID must be alphanumeric')
        return v