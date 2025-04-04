from pydantic import BaseModel
from typing import List


class RealTimeArrival(BaseModel):
    subwayId: str  # 지하철 노선 ID
    updnLine: str  # 상행
    trainLineNm: str # 목적지 방면 -> 000행(현재역) - 000방면(다음역)
    statnFid: str  # API 호출 기준 이전 역ID
    statnTid: str  # API 호출 기준 다음 역ID
    statnId: str  # API 호출 기준 역ID
    statnNm: str  # 역명
    trnsitCo: str  # 환승 개수
    ordKey: str  # 도착 예정 열차순번 -> 뭔지 모르겠음
    subwayList: str  # 연계 노선 ID? 이것도 뭔지 모름
    statnList: str  # 연계 역 ID


class RealTimeArrivalResponse(BaseModel):
    realtimeArrivalList: List