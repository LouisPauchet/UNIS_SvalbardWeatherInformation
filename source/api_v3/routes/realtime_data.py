from fastapi import APIRouter, HTTPException, Query
from ..models.data import StationDataTimeSerie, DataEntry
from ..models.general import StationID, GPSLocation
from typing import Optional

router = APIRouter()

@router.get("/{station_id}", tags=['Meteorological Data'], response_model=StationDataTimeSerie)
async def realtime_data(
        station_id: str,
        toffset: Optional[int] = Query(
            None,
            description="Optional time offset parameter, can be a positive or negative integer. Negative integer represent past data and positive integer represent forecasted data"
        )
    ) -> StationDataTimeSerie:

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
        raise HTTPException(status_code=500, detail=f"Internal Server Error")    