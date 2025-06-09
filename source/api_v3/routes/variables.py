from fastapi import APIRouter, HTTPException, Depends
from ..models.variables import VariableSettings
from ..main import api_v3_get_cache_handler

from typing import Dict
import re

# Initialize an APIRouter instance to define routes for this FastAPI application.
router = APIRouter()

@router.get("/", tags=['Meteorological Variables'], response_model=list[str])
async def get_variables(cache_handler=Depends(api_v3_get_cache_handler)):
    """
    Retrieve a list of available meteorological variable keys.

    This endpoint returns a list of keys representing the meteorological variables
    available in the cache handler's configuration.

    Args:
        cache_handler: Dependency injection for the cache handler instance.

    Returns:
        A list of strings representing the keys of available meteorological variables.
    """
    return list(cache_handler.config.variable_config.keys())

@router.get("/details", tags=['Meteorological Variables'], response_model=Dict[str, VariableSettings])
async def get_variables_details(cache_handler=Depends(api_v3_get_cache_handler)) -> Dict[str, VariableSettings]:
    """
    Retrieve detailed settings for all meteorological variables.

    This endpoint returns a dictionary containing detailed settings for each meteorological
    variable available in the cache handler's configuration.

    Args:
        cache_handler: Dependency injection for the cache handler instance.

    Returns:
        A dictionary with variable IDs as keys and their corresponding settings as values.
    """
    print(cache_handler.config.variable_config)
    return cache_handler.config.variable_config

@router.get("/{variable_id}", tags=['Meteorological Variables'], response_model=VariableSettings)
async def get_variable_info(variable_id: str, cache_handler=Depends(api_v3_get_cache_handler)) -> VariableSettings:
    """
    Retrieve detailed settings for a specific meteorological variable.

    This endpoint returns detailed settings for a specific meteorological variable identified
    by its ID. The variable ID must be alphanumeric and can include underscores.

    Args:
        variable_id: The ID of the meteorological variable to retrieve.
        cache_handler: Dependency injection for the cache handler instance.

    Returns:
        The settings for the specified meteorological variable.

    Raises:
        HTTPException: If the variable ID is invalid or the variable is not found.
    """
    # Regular expression to check if variable_id is alphanumeric with underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', variable_id):
        raise HTTPException(status_code=400, detail="Invalid variable ID. It must be alphanumeric and can include underscores.")

    try:
        return cache_handler.config.variable_config[variable_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Variable not found")
