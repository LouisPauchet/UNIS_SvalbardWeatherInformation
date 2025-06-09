from pydantic import BaseModel
from typing import Union


class VariableSettings(BaseModel):
    id: str
    unit: str = '[-]'
    minValue: Union[int, float] = -100
    maxValue: Union[int, float] = 100
    name: str = 'Unknown Variable'
    default: bool = False
    icon: str = None