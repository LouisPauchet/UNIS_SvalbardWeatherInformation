from fastapi import APIRouter, HTTPException, Query
from ..models.station import StationParameters
from ..models.general import StationID, GPSLocation

from typing import Optional
import re

router = APIRouter()

@router.get("/online", tags=["Weather Stations"], response_model=list[StationParameters])
async def online_stations(
          type: Optional[str] = Query(
          'all',
          description="Optional station type. Should be 'fixe', 'mobile' or 'all'."
          )
      ) -> list[StationParameters]:
    
    return [{
      "icon": "/static/images/lighthouse.png",
      "id": "SN99885",
      "location": {
        "lat": 78.38166,
        "lon": 14.753
      },
      "name": "Bohemanneset",
      "project": "IWIN Lighthouse",
      "status": "online",
      "type": "fixed",
      "variables": [
        "airTemperature",
        "seaSurfaceTemperature",
        "windSpeed",
        "windDirection",
        "relativeHumidity"
      ]
    }]


@router.get("/offline", tags=["Weather Stations"], response_model=list[StationParameters])
async def offline_station(
      type: Optional[str] = Query(
          'all',
          description="Optional station type. Should be 'fixe', 'mobile' or 'all'."
      )
      ) -> list[StationParameters]:

    return [{
      "icon": "/static/images/lighthouse.png",
      "id": "SN99885",
      "location": {
        "lat": 78.38166,
        "lon": 14.753
      },
      "name": "Bohemanneset",
      "project": "IWIN Lighthouse",
      "status": "online",
      "type": "fixed",
      "variables": [
        "airTemperature",
        "seaSurfaceTemperature",
        "windSpeed",
        "windDirection",
        "relativeHumidity"
      ]
    }]

@router.get("/{station_id}", tags=["Weather Stations"], response_model=StationParameters)
async def station_parameters(station_id: str) -> StationParameters:
    if not re.match('^[a-zA-Z0-9]+$', station_id):
        raise HTTPException(status_code=400, detail="Station ID must be alphanumeric")
    
    if station_id != "SN99885":
        raise HTTPException(status_code=404, detail="Station not found")

    return StationParameters(
        icon="/static/images/lighthouse.png",
        id="SN99885",
        location=GPSLocation(lat=78.38166, lon=14.753),
        name="Bohemanneset",
        project="IWIN Lighthouse",
        status="online",
        type="fixed",
        variables=[
            "airTemperature",
            "seaSurfaceTemperature",
            "windSpeed",
            "windDirection",
            "relativeHumidity"
        ]
    )