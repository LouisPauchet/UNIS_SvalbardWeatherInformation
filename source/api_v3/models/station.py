from pydantic import BaseModel

from .general import GPSLocation, StationStatus, StationType, StationID

class StationParameters(StationID):
    """
    A model representing the parameters of a station, inheriting from StationID.

    This class encapsulates various attributes of a station, including its icon,
    geographical location, name, associated project, status, type, and variables.

    Attributes:
        icon (str): The icon associated with the station.
        location (GPSLocation): The geographical location of the station.
        name (str): The name of the station. Defaults to 'No Name'.
        project (str): The project associated with the station. Defaults to 'No Project'.
        status (StationStatus): The status of the station (e.g., online, offline).
        type (StationType): The type of the station (e.g., fixed, mobile).
        variables (list[str]): A list of variables associated with the station.
    """
    icon: str
    location: GPSLocation
    name: str = 'No Name'
    project: str = 'No Project'
    status: StationStatus
    type: StationType
    variables: list[str]