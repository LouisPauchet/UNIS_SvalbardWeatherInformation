from fastapi import APIRouter, HTTPException, Query
from ..models.data import StationDataTimeSerie, DataEntry
from ..models.general import StationID, GPSLocation
from typing import Optional

# Initialize an APIRouter instance to define routes for this FastAPI application.
router = APIRouter()

@router.get("/{station_id}", tags=['Meteorological Data'], response_model=StationDataTimeSerie)
async def realtime_data(
    station_id: str,
    toffset: Optional[int] = Query(
        None,
        description="Optional time offset parameter, can be a positive or negative integer. Negative integer represents past data and positive integer represents forecasted data."
    )
) -> StationDataTimeSerie:
    """
    Retrieve real-time meteorological data for a specified station.

    This endpoint returns real-time meteorological data for a given station ID.
    An optional time offset parameter can be provided to retrieve past data or forecasted data.

    Args:
        station_id: A string representing the ID of the station for which to retrieve data.
        toffset: An optional integer representing the time offset. Negative values indicate past data,
                 and positive values indicate forecasted data.

    Returns:
        StationDataTimeSerie: An object containing the time series data for the requested station.

    Raises:
        HTTPException: If the station is not found or an internal server error occurs.
    """
    try:
        if station_id != "SN99885":
            raise HTTPException(status_code=404, detail="Station not found")

        return StationDataTimeSerie(
            id="SN99885",
            timeserie=[
                DataEntry(
                    airTemperature=-5.4,
                    timestamp="2025-02-08T17:00:00.000Z",
                    windDirection=205,
                    windSpeed=7.1
                )
            ]
        )
    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail="Internal Server Error")
