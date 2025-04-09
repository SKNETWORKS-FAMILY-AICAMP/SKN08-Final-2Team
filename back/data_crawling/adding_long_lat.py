import pandas as pd
import requests
import re

# Kakao API Key (카카오 REST API 키를 여기에 입력)
KAKAO_API_KEY = '68971ce90d537f18649d2ead5e663b3d'

def clean_address(address):
    """주소에서 불필요한 정보(층, 빌딩명, 범위 등)를 정리"""
    # 1. `층` 관련 정보 정리 (M층, 3층, 2-3층 → 1층)
    address = re.sub(r"\sM층", " 1층", address)  # M층 → 1층
    address = re.sub(r"\s\d+[-,~]?\d*\s?층", " 1층", address)  # "1,2층", "1~3층", "2-3층" → "1층"
    address = re.sub(r"\s*\d+[-,~]?\s*\d*\s*층", " 1층", address)  # "1, 2층" → "1층"
    
    # 2. `호수` 관련 정보 정리 (101~102호 → 101호)
    address = re.sub(r"\s\d+[-,~]?\d*\s?호", " 101호", address)
    
    # 3. `빌딩명` 제거 (빌딩명이 검색을 방해하는 경우가 많음)
    address = re.sub(r"\s\(.+?\)", "", address)  # 괄호로 된 건물명 제거
    address = re.sub(r"\s[가-힣A-Za-z0-9]+빌딩", "", address)  # "호림빌딩", "호서빌딩" 등 제거
    address = re.sub(r"\s[가-힣A-Za-z0-9]+센터", "", address)  # "아트센터", "트레이드센터" 등 제거
    address = re.sub(r"\s[가-힣A-Za-z0-9]+호텔", "", address)  # "호텔오크우드 프리미어" 제거

    return address.strip()

def get_coordinates(address):
    """도로명 주소를 Kakao API로 위도/경도로 변환"""
    cleaned_address = clean_address(address)
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": cleaned_address}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200 and data["documents"]:
        lat = data["documents"][0]["y"]
        lon = data["documents"][0]["x"]
        return lat, lon
    else:
        print(f"주소 변환 실패: {address} → {cleaned_address}")
        return None, None

# ✅ CSV 파일 불러오기
input_csv_file = "강남구_맛집.csv"  # 기존 CSV 파일명
output_csv_file = "강남구_맛집_좌표추가.csv"  # 새로운 CSV 파일명

df = pd.read_csv(input_csv_file)

# ✅ 위도, 경도 컬럼 추가
if "latitude" not in df.columns or "longitude" not in df.columns:
    df["latitude"] = None
    df["longitude"] = None

# ✅ 각 주소에 대해 좌표 변환 실행
for index, row in df.iterrows():
    if pd.isna(row["latitude"]) or pd.isna(row["longitude"]):  # 이미 값이 없는 경우만 실행
        lat, lon = get_coordinates(row["address"])
        df.at[index, "latitude"] = lat
        df.at[index, "longitude"] = lon
        print(f"{row['name']} - {lat}, {lon}")

# ✅ 새 CSV 파일로 저장
df.to_csv(output_csv_file, index=False, encoding="utf-8-sig")
print(f"✅ 변환 완료! {output_csv_file} 파일 저장됨.")
