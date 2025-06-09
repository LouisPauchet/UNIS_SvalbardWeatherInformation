from fastapi import APIRouter, HTTPException, Query, Depends
from ..models.data import StationDataTimeSerie, DataEntry
from ..models.general import StationID, GPSLocation
from ..main import api_v3_get_cache_handler
from typing import Optional
import re

# Initialize an APIRouter instance to define routes for this FastAPI application.
router = APIRouter()

@router.get("/{station_id}", tags=['Meteorological Data'], response_model=StationDataTimeSerie)
async def realtime_data(
    station_id: str,
    toffset: Optional[int] = Query(
        0,
        description="Optional time offset parameter, can be a positive or negative integer. Negative integer represents past data and positive integer represents forecasted data."
    ),
    cache_handler=Depends(api_v3_get_cache_handler)
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
    if not re.match(r'^[a-zA-Z0-9]+$', station_id):
        raise HTTPException(status_code=400, detail="Invalid station ID. It must be alphanumeric.")

    try:
        if toffset == 'now':
            toffset = 0

        res = cache_handler.get_cached_hourly_data(station_id, toffset)
        if res is not None:
            return res
        else:
            raise HTTPException(status_code=404, detail=f"Data not found for station {station_id}")

    except HTTPException:
        # Re-raise HTTPException to ensure it is not caught by the general exception handler
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")