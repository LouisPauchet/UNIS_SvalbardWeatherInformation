from pydantic import BaseModel

from .general import GPSLocation, StationStatus, StationType, StationID


class StationParameters(StationID):
      icon: str
      location:GPSLocation
      name: str = 'No Name'
      project: str = 'No Project'   
      status: StationStatus
      type: StationType
      variables: list[str]