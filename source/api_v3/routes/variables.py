from fastapi import APIRouter, HTTPException, Depends

from ..models.variables import VariableSettings
from ..main import api_v3_get_cache_handler

from typing import Dict
import re

router = APIRouter()

@router.get("/", tags=['Meteorological Variables'], response_model= list[str])
async def get_variables(cache_handler = Depends(api_v3_get_cache_handler)):
    return list(cache_handler.config.variable_config.keys())


@router.get("/details", tags=['Meteorological Variables'], response_model=Dict[str, VariableSettings])
async def get_variables_details(cache_handler = Depends(api_v3_get_cache_handler)) -> Dict[str, VariableSettings]:
    print(cache_handler.config.variable_config)
    return cache_handler.config.variable_config

@router.get("/{variable_id}", tags=['Meteorological Variables'], response_model=VariableSettings)
async def get_variable_info(variable_id: str, cache_handler=Depends(api_v3_get_cache_handler)) -> VariableSettings:
    # Regular expression to check if variable_id is alphanumeric with underscores
    if not re.match(r'^[a-zA-Z0-9_]+$', variable_id):
        raise HTTPException(status_code=400, detail="Invalid variable ID. It must be alphanumeric and can include underscores.")

    try:
        return cache_handler.config.variable_config[variable_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Variable not found")