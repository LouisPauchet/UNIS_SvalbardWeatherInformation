from fastapi import APIRouter, HTTPException, Query, Depends
from ..models.station import StationParameters
from ..models.general import StationID, GPSLocation

from ..main import api_v3_get_cache_handler

from typing import Optional
import re

# Initialize an APIRouter instance to define routes for this FastAPI application.
router = APIRouter()

@router.get("/online", tags=["Weather Stations"], response_model=list[StationParameters])
async def online_stations(
    type: Optional[str] = Query(
        'all',
        description="Optional station type. Should be 'fixed', 'mobile' or 'all'."
    ),
    cache_handler=Depends(api_v3_get_cache_handler)
) -> list[StationParameters]:
    """
    Retrieve a list of online weather stations based on the specified type.

    This endpoint returns a list of weather stations that are currently online.
    The stations can be filtered by type: 'fixed', 'mobile', or 'all'.

    Args:
        type: An optional string specifying the type of stations to retrieve.
              Defaults to 'all'. Valid values are 'fixed', 'mobile', or 'all'.
        cache_handler: Dependency injection for the cache handler instance.

    Returns:
        A list of StationParameters representing the online weather stations.

    Raises:
        HTTPException: If the station type is invalid.
    """
    if type not in ['all', 'fixed', 'mobile']:
        raise HTTPException(status_code=400, detail="Station type must be 'fixed', 'mobile' or 'all'.")

    return cache_handler.get_cached_online_stations(type=type)

@router.get("/offline", tags=["Weather Stations"], response_model=list[StationParameters])
async def offline_station(
    type: Optional[str] = Query(
        'all',
        description="Optional station type. Should be 'fixed', 'mobile' or 'all'."
    ),
    cache_handler=Depends(api_v3_get_cache_handler)
) -> list[StationParameters]:
    """
    Retrieve a list of offline weather stations based on the specified type.

    This endpoint returns a list of weather stations that are currently offline.
    The stations can be filtered by type: 'fixed', 'mobile', or 'all'.

    Args:
        type: An optional string specifying the type of stations to retrieve.
              Defaults to 'all'. Valid values are 'fixed', 'mobile', or 'all'.
        cache_handler: Dependency injection for the cache handler instance.

    Returns:
        A list of StationParameters representing the offline weather stations.

    Raises:
        HTTPException: If the station type is invalid.
    """
    if type not in ['all', 'fixed', 'mobile']:
        raise HTTPException(status_code=400, detail="Station type must be 'fixed', 'mobile' or 'all'.")

    return cache_handler.get_cached_online_stations(type=type, status='offline')

@router.get("/{station_id}", tags=["Weather Stations"], response_model=StationParameters)
async def station_parameters(
    station_id: str,
    cache_handler=Depends(api_v3_get_cache_handler)
) -> StationParameters:
    """
    Retrieve the metadata for a specific weather station by its ID.

    This endpoint returns the metadata for a weather station identified by its ID.
    The station ID must be alphanumeric.

    Args:
        station_id: A string representing the ID of the weather station.
        cache_handler: Dependency injection for the cache handler instance.

    Returns:
        StationParameters representing the metadata of the specified weather station.

    Raises:
        HTTPException: If the station ID is invalid or the station is not found.
    """
    if not re.match('^[a-zA-Z0-9]+$', station_id):
        raise HTTPException(status_code=400, detail="Station ID must be alphanumeric")

    station_metadata = cache_handler.get_cached_station_metadata(station_id)
    if station_metadata is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return station_metadata