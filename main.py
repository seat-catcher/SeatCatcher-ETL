import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import logging

from requests import Response

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
            start_index: int,
            end_index: int,
            station_code: str = "",
            station_name: str = "",
            line_number: str = ""
    ) -> str:
        logger.debug("[DEBUG] Building the request URL...")

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
            f"{self.auth_key}/{self.request_file_type}/{self.service_name}/"
            f"{start_index}/{end_index}/"
            f"{quote(query_params['station_code'])}/"
            f"{quote(query_params['station_name'])}/"
            f"{quote(query_params['line_number'])}/"
        )

    def get_train_station_info(
            self,
            start_index: int,
            end_index: int,
            station_code: str = "",
            station_name: str = "",
            line_number: str = ""
    ) -> Dict[str, Any]:
        logger.debug("[DEBUG] Fetching train station information...")
        url: str = self.build_url(start_index, end_index, station_code, station_name, line_number)
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
                f"Station Code: {station.STATION_CD}, "
                f"Station Name: {station.STATION_NM}, "
                f"Station Name (ENG): {station.STATION_NM_ENG}, "
                f"Station Name (CHN): {station.STATION_NM_CHN}, "
                f"Station Name (JPN): {station.STATION_NM_JPN}, "
                f"Line Number: {station.LINE_NUM}"
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
    logger.info("[INFO] Script finished.")

