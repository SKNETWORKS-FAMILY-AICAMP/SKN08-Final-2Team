import requests
from datetime import datetime, timedelta
from urllib.parse import quote
import os

class WeatherServiceImpl:

    def __init__(self):
        self.service_key = os.getenv("KMA_API_KEY")
        self.base_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
        self.nx = 60  # 서울시청 기준 격자 좌표
        self.ny = 127

    def get_base_time(self, now: datetime) -> str:
        """
        현재 시간 기준으로 가장 가까운 정시 (10분 이전까지 보정)
        예: 14:03 → 1300, 14:15 → 1400
        """
        adjusted = now - timedelta(minutes=10)
        return adjusted.strftime("%H") + "00"

    def get_seoul_weather(self) -> dict:
        now = datetime.now()
        base_date = now.strftime("%Y%m%d")
        base_time = self.get_base_time(now)

        params = {
            "serviceKey": self.service_key,
            "numOfRows": 10,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": self.nx,
            "ny": self.ny
        }

        try:
            response = requests.get(self.base_url, params=params)
            print("📡 요청 URL:", response.url)
            print("📄 응답 상태코드:", response.status_code)
            print("📩 응답 미리보기:", response.text[:300])

            data = response.json()

            if "response" not in data or data["response"]["header"]["resultCode"] != "00":
                return {
                    "message": "기상 정보를 불러오는 데 실패했습니다.",
                    "error": data.get("response", {}).get("header", {}).get("resultMsg", "알 수 없음")
                }

            items = data["response"]["body"]["items"]["item"]
            result = {}

            for item in items:
                category = item["category"]
                value = item["obsrValue"]
                if category == "T1H":
                    result["기온"] = f"{value}°C"
                elif category == "REH":
                    result["습도"] = f"{value}%"
                elif category == "RN1":
                    result["강수량"] = f"{value}mm"
                elif category == "WSD":
                    result["풍속"] = f"{value}m/s"

            return result or {"message": "해당 시간대에 기상 정보가 없습니다."}

        except requests.RequestException as req_err:
            return {"message": "기상청 API 요청 실패", "error": str(req_err)}
        except ValueError as val_err:
            return {"message": "응답 JSON 파싱 실패", "error": str(val_err)}
        except Exception as e:
            return {"message": "알 수 없는 에러 발생", "error": str(e)}

    def get_vilage_fcst(self) -> dict:
        """
        오늘 하루 예보 (3시간 간격) 정보 조회
        """
        forecast_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
        now = datetime.now()
        base_date = now.strftime("%Y%m%d")

        # base_time은 0200, 0500, ..., 2300 중 가장 가까운 이전 시각
        hour = now.hour
        base_hour = max([h for h in [2, 5, 8, 11, 14, 17, 20, 23] if h <= hour])
        base_time = f"{base_hour:02d}00"

        params = {
            "serviceKey": self.service_key,
            "numOfRows": 1000,
            "pageNo": 1,
            "dataType": "JSON",
            "base_date": base_date,
            "base_time": base_time,
            "nx": self.nx,
            "ny": self.ny
        }

        try:
            response = requests.get(forecast_url, params=params)
            print("🌤️ 단기예보 요청 URL:", response.url)

            data = response.json()
            if "response" not in data or data["response"]["header"]["resultCode"] != "00":
                return {"message": "단기예보 정보를 불러오는 데 실패했습니다."}

            items = data["response"]["body"]["items"]["item"]
            forecast = {}

            # 시간별로 (예: 0900, 1200 ...) 정리
            for item in items:
                fcst_time = item["fcstTime"]
                category = item["category"]
                value = item["fcstValue"]

                if fcst_time not in forecast:
                    forecast[fcst_time] = {}

                if category in ["T3H", "SKY", "PTY"]:
                    forecast[fcst_time][category] = value

            # 시간별 요약 메시지 구성
            summary = []
            for time_key in sorted(forecast.keys()):
                info = forecast[time_key]
                hour = int(time_key[:2])
                label = f"오전 {hour}시" if hour < 12 else f"오후 {hour - 12}시" if hour > 12 else "정오"

                temp = info.get("T3H", "?")
                sky = info.get("SKY", "0")
                pty = info.get("PTY", "0")

                # 하늘 상태 해석
                sky_map = {"1": "맑음", "3": "구름 많음", "4": "흐림"}
                pty_map = {"0": "", "1": "비", "2": "비/눈", "3": "눈", "4": "소나기"}

                weather_desc = pty_map.get(pty, "") or sky_map.get(sky, "알 수 없음")
                summary.append(f"{label}: {weather_desc}, {temp}°C")

            return {"날씨요약": summary[:5]}  # 최대 5개까지만 출력

        except Exception as e:
            return {"message": "단기예보 요청 실패", "error": str(e)}
