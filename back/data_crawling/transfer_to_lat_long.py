from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import requests
import re

# Kakao API Key (필요한 경우 여기에 추가)
KAKAO_API_KEY = '' #카카오 rest api key 입력력

def clean_address(address):
    """주소에서 불필요한 정보(층, 빌딩명, 범위 등)를 정리"""
    # 1. `층` 관련 정보 정리 (M층, 3층, 2-3층 → 1층)
    address = re.sub(r"\sM층", " 1층", address)  # M층 → 1층
    #address = re.sub(r"\s\d+[-,~]?\d*\s?층", " 1층", address)  # "1,2층", "1~3층", "2-3층" → "1층"
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
    cleaned_address = clean_address(address)  # 불필요한 정보 정리
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

        # ✅ 빌딩명이 포함된 주소도 다시 시도
        params = {"query": address}  # 원래 주소 다시 검색
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        if response.status_code == 200 and data["documents"]:
            lat = data["documents"][0]["y"]
            lon = data["documents"][0]["x"]
            return lat, lon

    print(f"주소 변환 실패: {address} (빌딩명 제거 후에도 실패)")
    return None, None

url = 'https://map.kakao.com/'
driver = webdriver.Chrome()
driver.get(url)

searchloc = input('찾고 싶은 음식 종류 : ')

search_area = driver.find_element(By.XPATH, '//*[@id="search.keyword.query"]')
search_area.send_keys(searchloc)
driver.find_element(By.XPATH, '//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)
time.sleep(2)

driver.find_element(By.XPATH, '//*[@id="info.main.options"]/li[2]/a').send_keys(Keys.ENTER)
time.sleep(2)

def storeNamePrint(page):
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    store_lists = soup.select('.placelist > .PlaceItem')
    list = []

    for store in store_lists:
        temp = []
        name = store.select('.head_item > .tit_name > .link_name')[0].text
        degree = store.select('.rating > .score > .num')[0].text
        review_element = store.select_one('.review > em[data-id="numberofreview"]')
        review_num = review_element.text if review_element else '0'
        addr = store.select('.info_item > .addr')[0].text.splitlines()[1]  # 도로명주소
        tel = store.select('.info_item > .contact > .phone')[0].text
        
        lat, lon = get_coordinates(addr)
        
        print(name, degree, review_num, addr, tel, lat, lon)

        temp.append(name)
        temp.append(degree)
        temp.append(review_num)
        temp.append(addr)
        temp.append(tel)
        temp.append(lat)
        temp.append(lon)
        
        list.append(temp)
    
    mode = 'w' if page == 1 else 'a'
    with open('중랑구_맛집_좌표.csv', mode, encoding='utf-8-sig', newline='') as f:
        writercsv = csv.writer(f)
        if page == 1:
            writercsv.writerow(['name', 'degree', 'review num', 'address', 'tel', 'latitude', 'longitude'])
        writercsv.writerows(list)

storeNamePrint(1)

try:
    page = 1
    while True:
        for i in range(1, 6):
            try:
                xPath = f'//*[@id="info.search.page.no{i}"]'
                driver.find_element(By.XPATH, xPath).send_keys(Keys.ENTER)
                time.sleep(0.5)
                storeNamePrint(page)
                page += 1
            except:
                print("더 이상 페이지 없음.")
                break
        
        next_btn = driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]')
        if "disabled" in next_btn.get_attribute("class"):
            print("마지막 페이지입니다. 크롤링 종료.")
            break
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(2)

except Exception as e:
    print(f"오류 발생: {e}")
