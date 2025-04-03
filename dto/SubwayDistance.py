from pydantic import BaseModel
from typing import Optional, List

class SubwayDistance(BaseModel):
    SBWY_ROUT_LN: str # 노선명 (1, 2, 3, 4, 5, 6, 7, 8, 9)
    SBWY_STNS_NM: str # 역명
    HM: str # 소요시간
    DIST_KM: float # 역간 거리
    ACML_DIST: float # 누적거리

class SubwayDistanceResponse(BaseModel):
    row: List[SubwayDistance]