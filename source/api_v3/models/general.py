from pydantic import BaseModel
from enum import Enum

class GPSLocation(BaseModel):
    lat: float
    lon: float

class StationStatus(str, Enum):
    offline = "offline"
    online = "online"

class StationType(str, Enum):
    fixed = "fixed"
    modile = "modile"

class StationID(BaseModel):
    id: str