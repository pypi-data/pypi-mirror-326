from dataclasses import dataclass
from enum import Enum
from typing import Union, Any, Optional

from .table_types import RegisterFlag
from ..generated import Signal


class PType(Enum):
    STR = "str"
    NUM = "num"


@dataclass
class Param:
    ptype: PType
    val: Union[float, int, str, Any]
    chemstation_key: Union[RegisterFlag, list[RegisterFlag]]


@dataclass
class HPLCMethodParams:
    organic_modifier: int
    flow: float
    pressure: Optional[float] = None #TODO: find this


@dataclass
class TimeTableEntry:
    start_time: float
    organic_modifer: float
    flow: Optional[float] = None


@dataclass
class MethodDetails:
    """An Agilent Chemstation method, TODO is to add MS parameters

    :attribute name: the name of the method, should be the same as the Chemstation method name.
    :attribute timetable: list of entries in the method timetable
    :attribute stop_time: the time the method stops running after the last timetable entry.
    :attribute post_time: the amount of time after the stoptime that the pumps keep running,
        based on settings in the first row of the timetable.
    :attribute params: the organic modifier (pump B) and flow rate displayed for the method (the time 0 settings)
    :attribute dad_wavelengthes:
    """
    name: str
    params: HPLCMethodParams
    timetable: list[TimeTableEntry]
    stop_time: Optional[int] = None
    post_time: Optional[int] = None
    dad_wavelengthes: Optional[list[Signal]] = None
