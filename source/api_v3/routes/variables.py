from fastapi import APIRouter, HTTPException

from ..models.variables import VariableSettings

router = APIRouter()

@router.get("/", tags=['Meteorological Variables'], response_model= list[str])
async def get_variables():
    return ['a', 'b']


@router.get("/details", tags=['Meteorological Variables'], response_model= list[VariableSettings])
async def get_variables_details() -> list[VariableSettings]:
    return [ VariableSettings(id = 'a')]

@router.get("/{variable_id}", tags=['Meteorological Variables'], response_model= VariableSettings)
async def get_variable_info(variable_id : str) -> VariableSettings:
    return VariableSettings(id = 'a')