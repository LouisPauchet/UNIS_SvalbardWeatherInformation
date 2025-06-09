from fastapi import APIRouter, HTTPException, Query, Depends
from ..models.station import StationParameters
from ..models.general import StationID, GPSLocation

from ..main import api_v3_get_cache_handler

from typing import Optional
import re

router = APIRouter()

@router.get("/online", tags=["Weather Stations"], response_model=list[StationParameters])
async def online_stations(
          type: Optional[str] = Query(
          'all',
          description="Optional station type. Should be 'fixe', 'mobile' or 'all'."
          ),
          cache_handler = Depends(api_v3_get_cache_handler)
      ) -> list[StationParameters]:
    
    if not type in ['all', 'fixed', 'mobile']:
      raise HTTPException(status_code=400, detail="Station type must be 'fixe', 'mobile' or 'all'.")

    return cache_handler.get_cached_online_stations(type=type)


@router.get("/offline", tags=["Weather Stations"], response_model=list[StationParameters])
async def offline_station(
      type: Optional[str] = Query(
          'all',
          description="Optional station type. Should be 'fixe', 'mobile' or 'all'."
      ),
      cache_handler = Depends(api_v3_get_cache_handler)
      ) -> list[StationParameters]:

    if not type in ['all', 'fixed', 'mobile']:
      raise HTTPException(status_code=400, detail="Station type must be 'fixe', 'mobile' or 'all'.")

    return cache_handler.get_cached_online_stations(type=type, status='offline')

@router.get("/{station_id}", tags=["Weather Stations"],  response_model=StationParameters)
async def station_parameters(station_id: str,
                             cache_handler = Depends(api_v3_get_cache_handler)
                             ) -> StationParameters:
    if not re.match('^[a-zA-Z0-9]+$', station_id):
        raise HTTPException(status_code=400, detail="Station ID must be alphanumeric")

    station_metadata = cache_handler.get_cached_station_metadata(station_id)
    if station_metadata is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return station_metadata