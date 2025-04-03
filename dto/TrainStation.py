from pydantic import BaseModel
from typing import Optional, List, Dict

class TrainStation(BaseModel):
    STATION_CD: str
    FR_CODE: str
    STATION_NM: str
    STATION_NM_ENG: str
    STATION_NM_CHN: str
    STATION_NM_JPN: str
    LINE_NUM: str

class TrainStationResponse(BaseModel):
    row: List[TrainStation]
