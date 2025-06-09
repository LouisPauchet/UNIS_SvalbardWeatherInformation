from fastapi import APIRouter, HTTPException
from ..models.data import StationDataTimeSerie, DataEntry
from ..models.general import StationID, GPSLocation

router = APIRouter()

@router.get("/{station_id}", tags=["realtime"], response_model=StationDataTimeSerie)
async def realtime_data(station_id: str) -> StationDataTimeSerie:
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