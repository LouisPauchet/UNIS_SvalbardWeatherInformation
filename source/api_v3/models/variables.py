from pydantic import BaseModel
from typing import Union

class VariableSettings(BaseModel):
    """
    A model representing the settings for a variable.

    This class encapsulates various attributes of a variable, including its ID, unit,
    minimum and maximum values, name, default status, and an optional icon.

    Attributes:
        id (str): The unique identifier for the variable.
        unit (str): The unit of measurement for the variable. Defaults to '[-]'.
        minValue (Union[int, float]): The minimum value for the variable. Defaults to -100.
        maxValue (Union[int, float]): The maximum value for the variable. Defaults to 100.
        name (str): The name of the variable. Defaults to 'Unknown Variable'.
        default (bool): Indicates whether this variable is the default. Defaults to False.
        icon (str, optional): An optional icon associated with the variable. Defaults to None.
    """
    id: str
    unit: str = '[-]'
    minValue: Union[int, float] = -100
    maxValue: Union[int, float] = 100
    name: str = 'Unknown Variable'
    default: bool = False
    icon: str = None
