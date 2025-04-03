import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import logging

from requests import Response

from dto.SubwayDistance import SubwayDistanceResponse
from dto.TrainStation import TrainStationResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()


class StationInfoScraper:
    BASE_URL = "http://openapi.seoul.go.kr:8088"

    def __init__(self):
        logger.debug("[DEBUG] Initializing environment variables...")
        self.request_file_type = "json"
        self.auth_key = os.getenv("SEOUL_OPENAPI_AUTH_KEY")
        self.service_name = "SearchSTNBySubwayLineInfo"

    def build_url(
            self,
            service_name: str,
            start_index: int,
            end_index: int,
            station_code: str = "",
            station_name: str = "",
            line_number: str = "",
    ) -> str:
        logger.debug("[DEBUG] Building the request URL...")

        if service_name == "SearchSTNBySubwayLineInfo":
            query_params: Dict[str, str] = {
                "station_code": station_code,
                "station_name": station_name,
                "line_number": line_number
            }

            for key, value in query_params.items():
                if not value:
                    query_params[key] = " "
                logger.debug(f"[DEBUG] {key}: {value}")

            return (
                f"{self.BASE_URL}/"
                f"{self.auth_key}/{self.request_file_type}/{service_name}/"
                f"{start_index}/{end_index}/"
                f"{quote(query_params['station_code'])}/" # 한글 인코딩
                f"{quote(query_params['station_name'])}/" # 한글 인코딩
                f"{quote(query_params['line_number'])}/" # 한글 인코딩
            )
        elif service_name == "StationDstncReqreTimeHm":
            query_params: Dict[str, str] = {
                "station_name": station_name,
                "line_number": line_number
            }

            for key, value in query_params.items():
                if not value:
                    query_params[key] = " "
                logger.debug(f"[DEBUG] {key}: {value}")

            return (
                f"{self.BASE_URL}/"
                f"{self.auth_key}/{self.request_file_type}/{service_name}/"
                f"{start_index}/{end_index}/"
                f"{quote(query_params['line_number'])}/"  # 한글 인코딩
                f"{quote(query_params['station_name'])}/"  # 한글 인코딩
            )

    def get_train_station_info(
            self,
            start_index: int,
            end_index: int,
            station_code: str = "",
            station_name: str = "",
            line_number: str = ""
    ) -> Dict[str, Any]:
        # https://data.seoul.go.kr/dataList/OA-15442/S/1/datasetView.do
        logger.debug("[DEBUG] Fetching train station information...")
        url: str = self.build_url(
            service_name="SearchSTNBySubwayLineInfo",
            start_index=start_index,
            end_index=end_index,
            station_code=station_code,
            station_name=station_name,
            line_number=line_number
        )
        logger.debug(f"[DEBUG] Request URL: {url}")
        response: Response = requests.get(url)
        return response.json()

    def parse_train_station_info(
            self,
            response: Dict[str, Any]
    ) -> None:
        logger.debug("[DEBUG] Parsing train station information...")
        if not response or response['SearchSTNBySubwayLineInfo']['RESULT']['CODE'] != 'INFO-000':
            logger.error("[ERROR] Failed to fetch data.")
            return

        train_station_data = TrainStationResponse.model_validate({
            "row": response['SearchSTNBySubwayLineInfo']['row']
        })
        for idx, station in enumerate(train_station_data.row):
            logger.info(
                f"[INFO] {idx}th Station Information: "
                f"# 역 코드: {station.STATION_CD}, "
                f"# 역명: {station.STATION_NM}, "
                f"# 역명(영문): {station.STATION_NM_ENG}, "
                f"# 역명(중문): {station.STATION_NM_CHN}, "
                f"# 역명(일문): {station.STATION_NM_JPN}, "
                f"# 노선 번호: {station.LINE_NUM}"
            )

    def get_distance_between_stations(
            self,
            start_index: int,
            end_index: int,
            subway_line_number: str = "",
            subway_station_name: str = ""
    ) -> Dict[str, Any]:
        # https://data.seoul.go.kr/dataList/OA-12034/F/1/datasetView.do
        logger.debug("[DEBUG] Fetching train station information...")
        url: str = self.build_url(
            service_name="StationDstncReqreTimeHm",
            start_index=start_index,
            end_index=end_index,
            station_name=subway_station_name,
            line_number=subway_line_number
        )
        logger.debug(f"[DEBUG] Request URL: {url}")
        response: Response = requests.get(url)
        return response.json()

    def parse_subway_distance_info(
            self,
            response: Dict[str, Any]
    ) -> None:
        logger.debug("[DEBUG] Parsing subway distance information...")
        if not response or response['StationDstncReqreTimeHm']['RESULT']['CODE'] != 'INFO-000':
            logger.error("[ERROR] Failed to fetch data.")
            return

        subway_distance_data = SubwayDistanceResponse.model_validate({
            "row": response['StationDstncReqreTimeHm']['row']
        })
        for idx, station in enumerate(subway_distance_data.row):
            # 기준 역은 이전역이 없으므로 소요시간은 0으로 표시됨
            logger.info(
                f"[INFO] {idx if idx != 0 else "기준역"}th Station Distance Information: "
                f"# 노선 번호: {station.SBWY_ROUT_LN}, "
                f"# 역명: {station.SBWY_STNS_NM}, "
                f"# 이전 역부터 {station.SBWY_STNS_NM}까지 소요 시간: {station.HM}, "
                f"# 역간 거리: {station.DIST_KM}, "
                f"# 축적 거리: {station.ACML_DIST}"
            )


if __name__ == "__main__":
    #############################################################
    # 01호선 최대 역 개수 : 102개 (1 ~ 102)
    # 02호선 최대 역 개수 : 51개 (1 ~ 51) // 2호선으로 검색 시 인천2호선이 포함됨 -> 서울로만 검색하려면 02호선으로 검색
    # 03호선 최대 역 개수 : 44개 (1 ~ 44)
    # 04호선 최대 역 개수 : 51개 (1 ~ 51)
    # 05호선 최대 역 개수 : 56개 (1 ~ 56)
    # 06호선 최대 역 개수 : 39개 (1 ~ 39)
    # 07호선 최대 역 개수 : 53개 (1 ~ 53)
    # 08호선 최대 역 개수 : 24개 (1 ~ 24)
    # 09호선 최대 역 개수 : 38개 (1 ~ 38)
    # 경의선 최대 역 개수 : 57개 (1 ~ 57)
    # 신분당선 최대 역 개수 : 16개 (1 ~ 16)
    # 공항철도 최대 역 개수 : 14개 (1 ~ 14)
    #############################################################
    logger.info("[INFO] Starting the script...")
    logger.debug("[DEBUG] Initializing the StationInfoScraper...")
    scraper = StationInfoScraper()
    request_result: Dict[str, Any] = scraper.get_train_station_info(start_index=1, end_index=400, line_number="공항철도")
    logger.debug(f"[DEBUG] Result: {request_result}")
    scraper.parse_train_station_info(request_result)

    #############################################################
    # 역간 거리 정보의 경우
    # 1호선은 서울역 기준 -> 청량리 방면에 대한 정보만 제공됨 (대다수가 빠져있어서 활용 불가능할듯)
    # 2호선은 시청역 기준 -> 한양대 방면에 대한 정보만 제공됨 (시계방향 순환 응답)
    # 7호선은 장암역 기준 -> 온수역 방면에 대한 정보만 제공됨 (온수 이후부터는 없음 -> 직접 넣어야할듯)
    #############################################################
    request_result_2: Dict[str, Any] = scraper.get_distance_between_stations(start_index=1, end_index=100, subway_line_number="7", subway_station_name="")
    scraper.parse_subway_distance_info(response=request_result_2)
    logger.info("[INFO] Script finished.")

