from fastapi import APIRouter, HTTPException, Query
from ..models.data import StationDataTimeSerie, DataEntry, StationTimeSeriesRequest
from ..models.general import StationID, GPSLocation

from typing import Optional, List

router = APIRouter()

@router.get("/", tags=['Meteorological Data'], response_model=StationDataTimeSerie)
async def timeseries_data(
    stations: str = Query(..., description="Station ID or list of station IDs"),
    start_time: str = Query(..., description="Start time in ISO-8601 format"),
    end_time: str = Query(..., description="End time in ISO-8601 format"),
    interval: str = Query('1h', description="Resampling interval"),
    variables: Optional[List[str]] = Query([], description="List of variables"),
    format: str = Query('json', description="Output format")
) -> StationDataTimeSerie:
    try:
        # Create a dictionary from the query parameters
        request_data = {
            "stations": stations,
            "start_time": start_time,
            "end_time": end_time,
            "interval": interval,
            "variables": variables,
            "format": format
        }

        # Validate the data using the StationTimeSeriesRequest model
        ts_request = StationTimeSeriesRequest(**request_data)

        # Check if the station ID is valid
        if ts_request.stations != "SN99885":
            raise HTTPException(status_code=404, detail="Station not found")

        # Return the time series data
        return StationDataTimeSerie(
            id=ts_request.stations,
            timeserie=[
                DataEntry(
                    airTemperature=-5.4,
                    timestamp="2025-02-08T17:00:00.000Z",
                    windDirection=205,
                    windSpeed=7.1
                ),
                DataEntry(
                    airTemperature=-5.4,
                    timestamp="2025-02-08T16:00:00.000Z",
                    windDirection=205,
                    windSpeed=8
                )
            ]
        )
    except ValueError as ve:
        raise HTTPException(status_code=422, 
                            detail=[{key: vee[key] for key in ['type', 'msg', 'input', 'loc']} for vee in ve.errors()])
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")