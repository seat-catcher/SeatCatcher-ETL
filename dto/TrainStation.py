from pydantic import BaseModel
from typing import Optional, List, Dict

class TrainStation(BaseModel):
    STATION_CD: str # 역코드
    FR_CODE: str # 외부코드 -> 이거 정렬하면 역 순서 알 수 있음
    STATION_NM: str # 역명
    STATION_NM_ENG: str # 역명(영문)
    STATION_NM_CHN: str # 역명(중문)
    STATION_NM_JPN: str # 역명(일문)
    LINE_NUM: str # 노선번호 (01호선, 02호선, 03호선, 04호선, 05호선, 06호선, 07호선, 08호선, 09호선, 공항철도, ...)

class TrainStationResponse(BaseModel):
    row: List[TrainStation]
