from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from pychemstation.utils.tray_types import TenVialColumn


@dataclass
class SequenceDataFiles:
    sequence_name: str
    dir: str
    child_dirs: Optional[list[str]] = None


class SampleType(Enum):
    SAMPLE = 1
    BLANK = 2
    CALIBRATION = 3
    CONTROL = 4

    @classmethod
    def _missing_(cls, value):
        return cls.SAMPLE


class InjectionSource(Enum):
    AS_METHOD = "As Method"
    MANUAL = "Manual"
    MSD = "MSD"
    HIP_ALS = "HipAls"

    @classmethod
    def _missing_(cls, value):
        return cls.HIP_ALS


@dataclass
class SequenceEntry:
    sample_name: str
    vial_location: Union[TenVialColumn, int]
    method: Optional[str] = None
    num_inj: Optional[int] = 1
    inj_vol: Optional[int] = 2
    inj_source: Optional[InjectionSource] = InjectionSource.HIP_ALS
    sample_type: Optional[SampleType] = SampleType.SAMPLE


@dataclass
class SequenceTable:
    name: str
    rows: list[SequenceEntry]
